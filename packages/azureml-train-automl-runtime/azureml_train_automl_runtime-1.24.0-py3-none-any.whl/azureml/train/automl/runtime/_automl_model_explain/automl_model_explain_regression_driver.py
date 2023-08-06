# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from azureml.automl.runtime.shared.datasets import DatasetBase
from azureml.core import Run
from azureml.train.automl.runtime._automl_model_explain.automl_model_explain_driver import AutoMLModelExplainDriver


class AutoMLModelExplainRegressionDriver(AutoMLModelExplainDriver):
    def __init__(self, automl_child_run: Run, dataset: DatasetBase,
                 max_cores_per_iteration: int):
        """
        Class for model explain configuration for AutoML regression models.

        :param automl_child_run: The automated ML child run.
        :type automl_child_run: azureml.core.Run
        :param dataset: Containing X, y and other transformed data info.
        :type dataset: DatasetBase
        :param max_cores_per_iteration: Number of cores configuration used for AutoML models.
        :type max_cores_per_iteration: int
        """
        super().__init__(automl_child_run=automl_child_run, dataset=dataset,
                         max_cores_per_iteration=max_cores_per_iteration)
