# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
import os
import sys
import tempfile
from multiprocessing import current_process
from pathlib import Path
from subprocess import PIPE, Popen
from typing import Any, Dict, List, Union

import pandas as pd
from azureml.automl.core.shared import log_server
from azureml.core import Run
from pandas.core.frame import DataFrame

from .train_helper import Arguments, MetadataFileHandler

# Clearing this environment variable avoids periodic calls from
# dprep log uploading to Run.get_context() and cause RH throttling
# when running at scale. It looks like this logging path repeatedly uploads timespan
# tracing data to the PRS step itself from each worker.
os.environ['AZUREML_OTEL_EXPORT_RH'] = ''

# Batch / flush metrics in the many models scenario
os.environ["AZUREML_METRICS_POLLING_INTERVAL"] = '30'

# Once the metrics service has uploaded & queued metrics for processing, we don't
# need to wait for those metrics to be ingested on flush.
os.environ['AZUREML_FLUSH_INGEST_WAIT'] = ''

# This is needed since CE and requirements.txt dont match due to known constraint.
os.environ['DISABLE_ENV_MISMATCH'] = 'True'

# This is the requested pipeline batch size.
PIPELINE_FETCH_MAX_BATCH_SIZE = 15


class ManyModelsTrain:
    """
    This class is used for training one or more AutoML runs.
    """

    def __init__(self,
                 current_step_run: Run,
                 automl_settings: Dict[str, Any],
                 process_count_per_node: int,
                 retrain_failed_models: bool):
        """
        This class is used for training one or more AutoML runs.
        :param current_step_run: Current step run object, parent of AutoML run.
        :param automl_settings: AutoML settings dictionary.
        :process_count_per_node: Process count per node.
        :retrain_failed_models: Retrain failed models flag.
        """

        self.current_step_run = current_step_run
        self.automl_settings = automl_settings
        self.metadata_file_handler = MetadataFileHandler(tempfile.mkdtemp())

        self.timestamp_column = self.automl_settings.get('time_column_name', None)  # type: str
        self.grain_column_names = self.automl_settings.get('grain_column_names', [])  # type: List[str]
        self.partition_column_names = self.automl_settings.get('partition_column_names', [])  # type: List[str]
        self.max_horizon = self.automl_settings.get('max_horizon', 0)  # type: int
        self.target_column = self.automl_settings.get('label_column_name', None)  # type: str
        self.automl_settings['many_models'] = True
        self.automl_settings['many_models_process_count_per_node'] = process_count_per_node
        self.automl_settings['pipeline_fetch_max_batch_size'] = self.automl_settings.get(
            'pipeline_fetch_max_batch_size', PIPELINE_FETCH_MAX_BATCH_SIZE)

        print("max_horizon: {}".format(self.max_horizon))
        print("target_column: {}".format(self.target_column))
        print("timestamp_column: {}".format(self.timestamp_column))
        print("partition_column_names: {}".format(self.partition_column_names))
        print("grain_column_names: {}".format(self.grain_column_names))
        print("retrain_failed_models: {}".format(retrain_failed_models))

        output_folder = os.path.join(os.environ.get("AZ_BATCHAI_INPUT_AZUREML", ""), "temp/output")
        working_dir = os.environ.get("AZ_BATCHAI_OUTPUT_logs", "")
        ip_addr = os.environ.get("AZ_BATCHAI_WORKER_IP", "")
        log_dir = os.path.join(working_dir, "user", ip_addr, current_process().name)
        t_log_dir = Path(log_dir)
        t_log_dir.mkdir(parents=True, exist_ok=True)

        # Try stopping logging server in the parent minibatch process.
        # Otherwise, the logging server will progressively consume more and more CPU, leading to
        # CPU starvation on the box. TODO: diagnose why this happens and fix
        try:
            if hasattr(log_server, "server") and log_server.server is not None:
                log_server.server.stop()
        except Exception as e:
            print("Stopping the AutoML logging server in the entry script parent process failed with exception: {}"
                  .format(e))

        debug_log = self.automl_settings.get('debug_log', None)
        if debug_log is not None:
            self.automl_settings['debug_log'] = os.path.join(log_dir, debug_log)
            self.automl_settings['path'] = tempfile.mkdtemp()
            print("{}.AutoML debug log:{}".format(__file__, automl_settings['debug_log']))

        # Write metadata files to disk, so they can be consumed by subprocesses that run AutoML
        arguments = Arguments(process_count_per_node, retrain_failed_models)
        self.metadata_file_handler.write_args_to_disk(arguments)
        self.metadata_file_handler.write_automl_settings_to_disk(self.automl_settings)

        print("{}.output_folder:{}".format(__file__, output_folder))
        self.metadata_file_handler.write_run_dto_to_disk(current_step_run._client.run_dto)
        print("init()")

    def run(self, input_data: Union[DataFrame, str]) -> DataFrame:
        """
        Train one or more partitions of data

        :param input_data: Input dataframe or file.
        """

        print("Entering run()")
        os.makedirs('./outputs', exist_ok=True)
        resultList = []  # type:  List[Any]
        input_data_files = input_data

        # ****************************
        # Handle tabular dataset input:
        # Writing to file would take(input_data.to_csv(tabular_input_file, index=False) few seconds,
        #    but it is better than sending dataframe across procecss which may involve  marshalling/unmarshalling
        # *****************************
        if isinstance(input_data, DataFrame):
            group_columns_dict = {}
            for column_name in self.partition_column_names:
                group_columns_dict.update(
                    {column_name: str(input_data.iat[0, input_data.columns.get_loc(column_name)])})
            model_string = '_'.join(str(v)
                                    for k, v in sorted(group_columns_dict.items()))
            print("Training using tabular dataset.")

            tabular_input_file = "train_tabular_input_{}.csv".format(model_string)
            input_data.to_csv(tabular_input_file, index=False)
            print("Finished writing pandas dataframe to : {}".format(tabular_input_file))
            input_data_files = [tabular_input_file]

        for input_data_file in input_data_files:
            print("Launch subprocess to run AutoML on the data")
            env = os.environ.copy()
            # Aggressively buffer I/O from the subprocess
            env['PYTHONUNBUFFERED'] = '0'
            subprocess = Popen([
                sys.executable,
                os.path.join(os.path.dirname(os.path.realpath(__file__)), 'train_model.py'),
                input_data_file,
                self.metadata_file_handler.data_dir], env=env, stdout=PIPE, stderr=PIPE)
            if hasattr(subprocess, "stdout") and subprocess.stdout is not None:
                for line in subprocess.stdout:
                    print(line.decode().rstrip())
            subprocess.wait()
            print("Subprocess completed with exit code: {}".format(subprocess.returncode))
            if hasattr(subprocess, "stderr") and subprocess.stderr is not None:
                subprocess_stderr = subprocess.stderr.read().decode().rstrip()
            if subprocess_stderr:
                print("stderr from subprocess:\n{}\n".format(subprocess_stderr))
            if subprocess.returncode != 0:
                raise Exception("AutoML training subprocess exited unsuccessfully with error code: {}\n"
                                "stderr from subprocess: \n{}\n".format(subprocess.returncode, subprocess_stderr))
            logs = self.metadata_file_handler.load_logs()
            resultList.append(logs)
            self.metadata_file_handler.delete_logs_file_if_exists()
        print("Constructing DataFrame from results")
        result = pd.DataFrame(data=resultList)
        print("Ending run()\n")
        return result

    def read_from_json(self, snapshot_dir):
        """
        Read automl settings from snapshot directory.

        :param snapshot_dir: Snapshot directory.
        """
        with open(str(snapshot_dir) + "/automl_settings.json") as json_file:
            return json.load(json_file)
