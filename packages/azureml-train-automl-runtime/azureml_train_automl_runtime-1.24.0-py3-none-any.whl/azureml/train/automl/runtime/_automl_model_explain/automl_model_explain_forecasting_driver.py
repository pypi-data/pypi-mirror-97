# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from azureml.automl.runtime.shared.datasets import DatasetBase
from azureml.core import Run
from azureml.train.automl.runtime._automl_model_explain.automl_model_explain_driver import AutoMLModelExplainDriver
from azureml.train.automl.runtime.automl_explain_utilities import _should_set_reset_index


class AutoMLModelExplainForecastingDriver(AutoMLModelExplainDriver):
    def __init__(self, automl_child_run: Run, dataset: DatasetBase,
                 max_cores_per_iteration: int):
        """
        Class for model explain configuration for AutoML forecasting models.

        :param automl_child_run: The automated ML child run.
        :type automl_child_run: azureml.core.Run
        :param dataset: Containing X, y and other transformed data info.
        :type dataset: DatasetBase
        :param max_cores_per_iteration: Number of cores configuration used for AutoML models.
        :type max_cores_per_iteration: int
        """
        super().__init__(automl_child_run=automl_child_run, dataset=dataset,
                         max_cores_per_iteration=max_cores_per_iteration)

        # Disable raw data upload for explanations of forecasting models
        # This is because the codepath for forecasting data cleaning is not aligned
        # with those of classification and regression.
        # Refactoring data cleaning will be required to enable raw forecasting explanations.
        self._should_upload_raw_eval_dataset = False

    def setup_surrogate_model_and_params(self, should_reset_index: bool = False) -> None:
        super().setup_surrogate_model_and_params(
            should_reset_index=_should_set_reset_index(automl_run=self._automl_child_run))
