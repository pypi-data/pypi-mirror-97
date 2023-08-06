# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging
from typing import Any, Dict, Optional

from azureml.automl.runtime import fit_pipeline as fit_pipeline_helper
from azureml.automl.runtime.automl_pipeline import AutoMLPipeline
from azureml.automl.runtime.automl_run_context import AutoMLAbstractRunContext
from azureml.automl.runtime.fit_output import FitOutput
from azureml.automl.runtime.onnx_convert import OnnxConverter
from azureml.automl.runtime.shared.datasets import DatasetBase
from azureml.core import Run
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings

logger = logging.getLogger(__name__)


class TrainingIterationPhase:
    """Iteration that outputs a fully trained ML model."""

    @staticmethod
    def run(
        automl_parent_run: Run,
        automl_run_context: AutoMLAbstractRunContext,
        automl_settings: AzureAutoMLSettings,
        dataset: DatasetBase,
        onnx_cvt: Optional[OnnxConverter],
        pipeline_id: str,
        pipeline_spec: str,
        training_percent: float,
        elapsed_time: Optional[int] = None
    ) -> FitOutput:
        """Run the training iteration."""
        logger.info('Beginning the training iteration for run {}.'.format(automl_run_context.run_id))

        automl_pipeline = AutoMLPipeline(automl_run_context, pipeline_spec, pipeline_id, training_percent / 100)

        # Dataset will have a valid value for # of CV splits if we were to do auto CV.
        # Set the value of n_cross_validations in AutoML settings if that were the case
        if automl_settings.n_cross_validations is None and dataset.get_num_auto_cv_splits() is not None:
            n_cv = dataset.get_num_auto_cv_splits()
            logger.info("Number of cross-validations in dataset is {}.".format(n_cv))
            automl_settings.n_cross_validations = None if n_cv == 0 else n_cv

        fit_output = fit_pipeline_helper.fit_pipeline(
            automl_pipeline=automl_pipeline,
            automl_settings=automl_settings,
            automl_run_context=automl_run_context,
            dataset=dataset,
            onnx_cvt=onnx_cvt,
            elapsed_time=elapsed_time)

        if not fit_output.errors:
            primary_metric = fit_output.primary_metric
            score = fit_output.score
            duration = fit_output.actual_time
            logger.info('Child run completed with {}={} after {} seconds.'.format(primary_metric, score, duration))

        return fit_output
