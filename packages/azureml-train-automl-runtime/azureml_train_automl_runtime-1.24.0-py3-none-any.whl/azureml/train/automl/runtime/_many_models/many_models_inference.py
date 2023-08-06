# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import List, Optional, Union
import datetime
import hashlib
import logging
from logging import Logger
import os

import pandas as pd
from azureml.core import Run
from azureml.core.model import Model
from pandas.core.frame import DataFrame
import joblib


class ManyModelsInference:
    """This class is used for doing batch inference."""

    def __init__(self,
                 current_step_run: Run,
                 partition_column_names: List[str],
                 target_column_name: Optional[str],
                 time_column_name: Optional[str],
                 train_run_id: Optional[str],
                 logger: Optional[Logger] = None):
        """
        This class is used for doing batch inference.

        :param current_step_run: Current step run object, parent of AutoML run.
        :param partition_column_names: Partition column names.
        :param target_column_name: The target column name. Needs to be passed only if inference data contains target.
        :param time_column_name: The time column name, op
        :param train_run_id: The training pipeline run id.
        :param logger: The logger object
        """
        self.current_step_run = current_step_run
        self.partition_column_names = partition_column_names
        self.target_column_name = target_column_name
        self.time_column_name = time_column_name
        self.train_run_id = train_run_id
        self.logger = logger or logging.getLogger(__name__)
        print("partition_column_names: {}".format(self.partition_column_names))
        print("target_column_name: {}".format(self.target_column_name))
        print("time_column_name: {}".format(self.time_column_name))
        print("train_run_id: {}".format(self.train_run_id))

    def run(self, input_data: Union[str, DataFrame]) -> DataFrame:
        """
        Perform batch inference on specified partition(s) of data

        :param input_data: Input dataframe or file.
        """
        print("InputData type: {}".format(type(input_data)))
        # 1.0 Set up Logging
        self.logger.info('Making predictions')
        os.makedirs('./outputs', exist_ok=True)

        all_predictions = pd.DataFrame()
        date1 = datetime.datetime.now()
        self.logger.info('starting ' + str(date1))

        # Input is tabular dataset
        if isinstance(input_data, DataFrame):
            data = input_data
            data = self._do_inference(data)
            all_predictions = all_predictions.append(data)
        else:
            # Input is file dataset
            # 2.0 Iterate through input data
            for idx, file_path in enumerate(input_data):
                file_name, file_extension = os.path.splitext(
                    os.path.basename(file_path))
                self.logger.info(file_path)
                if file_extension.lower() == ".parquet":
                    data = pd.read_parquet(file_path)
                else:
                    data = pd.read_csv(file_path)
                data = self._do_inference(data)
                all_predictions = all_predictions.append(data)

        # 5.0 Log the run
        date2 = datetime.datetime.now()
        self.logger.info('ending ' + str(date2))

        print(all_predictions.head())
        return all_predictions

    def _do_inference(self, data: DataFrame) -> DataFrame:
        """
        Perform inference on the dataframe

        :param data: Input dataframe to make predictions on
        """
        # 2.0 make predictions on the given data

        tags_dict = {}
        for column_name in self.partition_column_names:
            tags_dict.update(
                {column_name: str(data.iat[0, data.columns.get_loc(column_name)])})

        print(tags_dict)

        model_string = '_'.join(str(v) for k, v in sorted(
            tags_dict.items()) if k in self.partition_column_names)
        self.logger.info("model string to encode " + model_string)
        print("model string to encode " + model_string)
        sha = hashlib.sha256()
        sha.update(model_string.encode())
        model_name = 'automl_' + sha.hexdigest()
        print(model_name)
        ws = self.current_step_run.experiment.workspace

        model_tags = []
        if self.train_run_id:
            model_tags.append(['RunId', self.train_run_id])

        self.logger.info('query the model ' + model_name)
        model_list = Model.list(ws, name=model_name,
                                tags=model_tags, latest=True)

        if not model_list:
            print("Could not find model")
            return
        print('Got {} models'.format(len(model_list)))

        # 4.0 Un-pickle model and make predictions
        model_path = model_list[0].download(exist_ok=True)
        model = joblib.load(model_path)
        model_name = model_list[0].name
        print('Unpickled the model ' + model_name)

        X_test = data.copy()
        if self.target_column_name is not None:
            X_test.pop(self.target_column_name)

        print("prediction data head")
        print(X_test.head())
        y_predictions, X_trans = model.forecast(
            X_test, ignore_data_errors=True)
        print('Made predictions ' + model_name)

        # Insert predictions to test set
        predicted_column_name = 'Predictions'
        data[predicted_column_name] = y_predictions
        print(data.head())
        print('Inserted predictions ' + model_name)

        return data
