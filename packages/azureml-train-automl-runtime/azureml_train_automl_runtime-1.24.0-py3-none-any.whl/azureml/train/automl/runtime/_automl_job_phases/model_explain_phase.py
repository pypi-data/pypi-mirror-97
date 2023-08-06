# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging
from typing import Optional

from azureml.automl.core._run import RunType
from azureml.automl.core.automl_base_settings import AutoMLBaseSettings
from azureml.automl.core.console_interface import ConsoleInterface
from azureml.automl.runtime.shared.datasets import DatasetBase
from azureml.core import Run
from azureml.train.automl._azure_experiment_observer import ExperimentObserver
from azureml.train.automl.runtime._automl_model_explain import (_explain_run, _automl_perform_best_run_explain_model)
from azureml.train.automl.runtime.run import AutoMLRun

logger = logging.getLogger(__name__)


class ModelExplainPhase:
    """AutoML job phase that explains the model."""

    @staticmethod
    def explain_run(child_run: RunType,
                    dataset: DatasetBase,
                    automl_settings: AutoMLBaseSettings,
                    experiment_observer: Optional[ExperimentObserver] = None) -> None:
        """
        Execute the model explain run.

        :param child_run: The explain run
        :param parent_dataset: ClientDatasets which contains the post setup/featurization training data.
        :param automl_settings: AzureAutoMLSettings for the parent run.
        :return:
        """
        _explain_run(child_run, dataset, automl_settings, experiment_observer)

    @staticmethod
    def explain_best_run(parent_run: AutoMLRun,
                         dataset: DatasetBase,
                         automl_settings: AutoMLBaseSettings,
                         compute_target: Optional[str] = None,
                         current_run: Optional[Run] = None,
                         experiment_observer: Optional[ExperimentObserver] = None,
                         console_interface: Optional[ConsoleInterface] = None) -> None:
        """
        Explain the best model in the training stage and store the explanation in that child run.

        :param parent_run: The automated ML parent run.
        :type parent_run: azureml.train.automl.run.AutoMLRun
        :param dataset: Containing X, y and other transformed data info.
        :type dataset: DatasetBase
        :param automl_settings: Automated ML run settings.
        :type automl_settings: AutoMLBaseSettings
        :param compute_target: Local/ADB/Remote
        :type compute_target: str
        :param current_run: Current run for computing model explanations.
        :param current_run: azureml.core.Run
        :param experiment_observer: The experiment observer.
        :type experiment_observer: azureml.train.automl._azure_experiment_observer.AzureExperimentObserver
        :param console_interface: The console interface to write the status of model explanation run.
        :type console_interface: azureml.automl.core.console_interface.ConsoleInterface
        :return: None
        """
        _automl_perform_best_run_explain_model(parent_run,
                                               dataset,
                                               automl_settings,
                                               compute_target,
                                               current_run,
                                               experiment_observer,
                                               console_interface)
