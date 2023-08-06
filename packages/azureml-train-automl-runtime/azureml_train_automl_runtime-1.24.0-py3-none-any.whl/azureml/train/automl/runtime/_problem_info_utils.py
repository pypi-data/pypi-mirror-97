# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Methods related to setting problem info on local & remote azure orchestrated runs."""
import json
import logging
from typing import Optional, Union

import numpy as np
import pandas as pd
import scipy.sparse
from azureml.core import Run

from azureml.automl.core.shared import logging_utilities
from azureml.automl.runtime import data_transformation
from azureml.automl.runtime import feature_skus_utilities
from azureml.automl.runtime.data_context import RawDataContext, TransformedDataContext
from azureml.automl.runtime.shared import runtime_logging_utilities
from azureml.automl.runtime.shared.cache_store import CacheStore
from azureml.automl.runtime.shared.types import DataInputType, DataSingleColumnInputType
from azureml.automl.runtime.streaming_data_context import StreamingTransformedDataContext
from azureml.train.automl import _constants_azureml
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings


logger = logging.getLogger(__name__)


def _subsampling_recommended(num_samples, num_features):
    """
    Recommend whether subsampling should be on or off based on shape of X.

    :param num_samples: Number of samples after preprocessing.
    :type num_samples: int
    :param num_features: Number of features after preprocessing.
    :type num_features: int
    :return: Flag indicate whether subsampling is recommended for given shape of X.
    :rtype: bool
    """
    # Ideally this number should be on service side.
    # However this number is proportional to the iteration overhead.
    # Which makes this specific number SDK specific.
    # For nativeclient or miroclient, this number will be different due to smaller overhead.
    # We will leave this here for now until we have a way of incorporating
    # hardware and network numbers in our model
    return num_samples * num_features > 300000000


def set_problem_info(
    X: DataInputType,
    y: DataSingleColumnInputType,
    automl_settings: AzureAutoMLSettings,
    current_run: Run,
    cache_store: CacheStore,
    transformed_data_context: Optional[Union[TransformedDataContext,
                                             StreamingTransformedDataContext]] = None,
    is_adb_run: bool = False
) -> None:
    """
    Set statistics about user data.

    :param X: The training features to use when fitting pipelines during AutoML experiment.
    :type X: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
    :param y: Training labels to use when fitting pipelines during AutoML experiment.
    :type y: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
    :param automl_settings: The AutoML settings to use.
    :type automl_settings: AzureAutoMLSettings
    :param current_run: The AutoMLRun to set the info for.
    :type current_run: azureml.core.run.Run
    :param transformed_data_context: Containing X, y and other transformed data info.
    :type transformed_data_context: TransformedDataContext or StreamingTransformedDataContext
    :param is_adb_run: flag whether this is a Azure Databricks run or not.
    :type is_adb_run: bool
    :return: None
    """
    with logging_utilities.log_activity(logger, activity_name='set_problem_info'):
        run_id = current_run.id
        streaming = automl_settings.enable_streaming
        logger.info("Logging dataset information for {}".format(run_id))
        runtime_logging_utilities.log_data_info(data_name="X", data=X,
                                                run_id=run_id, streaming=streaming)
        runtime_logging_utilities.log_data_info(data_name="y", data=y,
                                                run_id=run_id, streaming=streaming)

        subsampling = automl_settings.enable_subsampling
        if subsampling is None:
            subsampling = _subsampling_recommended(X.shape[0], X.shape[1])

        problem_info_dict = {
            "dataset_num_categorical": 0,
            "is_sparse": scipy.sparse.issparse(X),
            "subsampling": subsampling
        }

        if automl_settings.enable_streaming:
            # Note: when using incremental learning, we are not calculating
            # some problem info properties that Miro may use for recommendation. It's uncertain at
            # this point whether these properties are needed
            problem_info_dict["dataset_features"] = X.head(1).shape[1]

            # If subsampling, set the number of dataset samples.
            # Note: when not subsampling, avoid this, because invoking Dataflow.shape
            # triggers Dataflow profile computation, which is expensive on large data
            if subsampling:
                problem_info_dict["dataset_samples"] = X.shape[0]
        else:
            problem_info_dict["dataset_classes"] = len(np.unique(y))
            problem_info_dict["dataset_features"] = X.shape[1]
            problem_info_dict["dataset_samples"] = X.shape[0]
            if isinstance(transformed_data_context, TransformedDataContext):
                problem_info_dict['single_frequency_class_detected'] = \
                    transformed_data_context._check_if_y_label_has_single_occurrence_class()
        problem_info_str = json.dumps(problem_info_dict)

        # This is required since token may expire
        if is_adb_run:
            current_run = Run.get_context()

        current_run.add_properties({
            _constants_azureml.Properties.PROBLEM_INFO: problem_info_str,
            'feature_skus': feature_skus_utilities.serialize_skus(
                feature_skus_utilities.get_feature_skus_from_settings(automl_settings)
            )
        })
