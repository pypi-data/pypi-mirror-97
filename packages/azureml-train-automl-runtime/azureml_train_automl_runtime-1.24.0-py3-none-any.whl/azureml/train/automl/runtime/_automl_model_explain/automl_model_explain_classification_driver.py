# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from azureml.automl.runtime.shared.datasets import DatasetBase
from azureml.core import Run
from azureml.train.automl.runtime._automl_model_explain.automl_model_explain_driver import AutoMLModelExplainDriver
from azureml.train.automl.runtime.automl_explain_utilities import _get_unique_classes


class AutoMLModelExplainClassificationDriver(AutoMLModelExplainDriver):
    def __init__(self, automl_child_run: Run, dataset: DatasetBase,
                 max_cores_per_iteration: int):
        """
        Class for model explain configuration for AutoML classification models.

        :param automl_child_run: The automated ML child run.
        :type automl_child_run: azureml.core.Run
        :param dataset: Containing X, y and other transformed data info.
        :type dataset: DatasetBase
        :param max_cores_per_iteration: Number of cores configuration used for AutoML models.
        :type max_cores_per_iteration: int
        """
        super().__init__(automl_child_run=automl_child_run, dataset=dataset,
                         max_cores_per_iteration=max_cores_per_iteration)

    def setup_class_labels(self) -> None:
        """Return the unique classes in y or obtain classes from inverse transform using y_transformer."""
        self._automl_explain_config_obj._classes = _get_unique_classes(
            y=self._automl_explain_config_obj._y,
            automl_estimator=self._automl_explain_config_obj._automl_estimator,
            y_transformer=self._dataset.get_y_transformer())
