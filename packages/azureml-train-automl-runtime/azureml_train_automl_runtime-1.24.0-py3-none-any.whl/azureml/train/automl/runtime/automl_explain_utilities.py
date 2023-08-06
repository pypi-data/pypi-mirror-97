# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Contains utilities used after training for explaining automated ML models in Azure Machine Learning.

For more information, see:

* [Interpretability: model explanations in automated machine
    learning](https://docs.microsoft.com/azure/machine-learning/how-to-machine-learning-interpretability-automl)

* [ONNX and Azure Machine Learning: Create and accelerate
    ML models](https://docs.microsoft.com/azure/machine-learning/concept-onnx)
"""
from typing import List, Optional, Any, Tuple, Union, cast, Dict

import json
import logging

import pandas as pd
import numpy as np
import scipy
from azureml._common._error_definition import AzureMLError
from azureml._common._error_definition.user_error import ArgumentBlankOrEmpty
from azureml.automl.core.shared._diagnostics.automl_error_definitions import DatasetsFeatureCountMismatch, \
    FeatureUnsupportedForIncompatibleArguments, InvalidArgumentWithSupportedValues
from azureml.automl.core.shared._diagnostics.validation import Validation
from azureml.dataprep.api.dataflow import Dataflow
from nimbusml import Pipeline as NimbusMLPipeline
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.model_selection import train_test_split

import azureml.automl.runtime._ml_engine as ml_engine
from azureml.automl.runtime.onnx_convert import OnnxConverter
from azureml.automl.runtime.onnx_convert import OnnxInferenceHelper
from azureml.automl.runtime.onnx_convert import OnnxFeaturizerHelper
from azureml.automl.runtime.onnx_convert import OnnxInferenceFromFeaturesHelper
from azureml.automl.runtime import dataprep_utilities
from azureml.automl.runtime.featurization.streaming import StreamingFeaturizationTransformer
from azureml.data import TabularDataset
from azureml.core import Run
from azureml.automl.core.shared import constants
from azureml.automl.core.shared.exceptions import OnnxConvertException, ValidationException
from azureml.automl.runtime.shared.types import DataInputType, DataSingleColumnInputType
from azureml.automl.runtime.cpu_utilities import _get_num_physical_cpu_cores_model_explanations
from azureml.automl.runtime.streaming_pipeline_wrapper import StreamingPipelineWrapper
from azureml.automl.runtime.training_utilities import _upgrade_sparse_matrix_type
from azureml.automl.core.shared.constants import Transformers
from azureml.train.automl.exceptions import ConfigException

logger = logging.getLogger(__name__)

ModelExpDebugPkgList = ['azureml-train-automl-runtime',
                        'azureml-interpret',
                        'interpret-community',
                        'interpret-core']
DefaultWeightRawFeatureToEngineeredFeatureMap = 1.0
ModelExplanationRunId = 'model_explain_run_id'
ModelExplanationBestRunChildId = 'model_explain_best_run_child_id'
EngineeredExpFolderName = 'engineered_exp_folder_name'
RawExpFolderName = 'raw_exp_folder_name'
NumberofBestRunRetries = 4
MaxExplainedFeaturesToUpload = 100
MaximumEvaluationSamples = 5000
SparseNumFeaturesThreshold = 1000
LinearSurrogateModelParam = 'sparse_data'
LGBMSurrogateModelParam = 'n_jobs'
ExplainableModelArgsStr = 'explainable_model_args'
AugmentDataStr = 'augment_data'


class SurrogateModelTypes:
    """Defines surrogate models used in automated ML to explain models."""

    LightGBM = "LightGBM"
    LinearModel = "LinearModel"


class StreamingPipelineExplainabilityWrapper:
    """A wrapper for streaming pipelines that implements APIs expected by Azure model explainability library.

    :param pipeline: A streaming pipeline.
    :param task: The machine learning task.
    :type task: str
    """

    def __init__(self, pipeline: Any, task: str):
        """
        Initialize the StreamingPipelineExplainabilityWrapper object.

        :param pipeline: A streaming pipeline.
        :param task: The machine learning task.
        :type task: str
        """
        self._pipeline = pipeline
        self.classes_ = None

        if task == constants.Tasks.CLASSIFICATION:
            # All NimbusML pipelines (including regression) have a 'predict_proba' method, (even though
            # the 'predict_proba' raises an error for regression pipelines).
            # Azure model explainability library expects 'predict_proba' method only on classification pipelines,
            # and can error if a regression pipeline object has a predict_proba attribute.
            self.predict_proba = self._pipeline.predict_proba
            self.classes_ = self._pipeline.classes_ if hasattr(self._pipeline, 'classes_') else None

            self._projection_column_name_in_predict_df = 'PredictedLabel'
        else:
            self._projection_column_name_in_predict_df = 'Score'

    def predict(self, *args, **kwargs):
        """Make predictions for target values."""
        result = self._pipeline.predict(*args, **kwargs)
        if isinstance(result, pd.DataFrame):
            # The 'predict' method on Nimbus pipelines returns a pandas DataFrame with predictions,
            # but Azure model explainability library expects a numpy array (like the sklearn predict API).
            result = result[self._projection_column_name_in_predict_df].values
        return result


class ONNXEstimatorInferceHelperExplainabilityWrapper:
    """A wrapper base class for automated ML ONNX pipelines that implements standard predict() and predict_proba().

    :param onnx_estimator_helper: An automated ML ONNX inference helper object. This is specifically an estimator
        inference helper, which only uses the estimator part of the ONNX model, and can only take the
        transformed features as input (with same schema of the output of the featurizer ONNX model).
    :type onnx_estimator_helper: azureml.automl.runtime.onnx_convert.OnnxInferenceFromFeaturesHelper
    """

    def __init__(self, onnx_estimator_helper: OnnxInferenceFromFeaturesHelper):
        """
        Initialize the ONNXEstimatorInferceHelperExplainabilityWrapper object.

        :param onnx_estimator_helper: An automated ML ONNX inference helper object. This is specifically an estimator
            inference helper, which only uses the estimator part of the ONNX model, and can only take the
            transformed features as input (with same schema of the output of the featurizer ONNX model).
        :type onnx_estimator_helper: azureml.automl.runtime.onnx_convert.OnnxInferenceFromFeaturesHelper
        """
        self._onnx_estimator_helper = onnx_estimator_helper

    def predict(self, X: DataInputType) -> DataSingleColumnInputType:
        """Make predictions for target values using the automated ML ONNX helper model.

        :param X: The target values.
        :type X: typing.Union[numpy.ndarray, pandas.DataFrame, scipy.sparse.csr_matrix, azureml.dataprep.Dataflow]
        """
        predict, _ = self._onnx_estimator_helper.predict(X=X, with_prob=False)
        return predict


class ONNXEstimatorClassificationInferceHelperExplainabilityWrapper(ONNXEstimatorInferceHelperExplainabilityWrapper):
    """
    A wrapper class for automated ML ONNX classification pipelines.

    This class implements standard predict() and predict_proba() functions.

    :param onnx_estimator_helper: An automated ML ONNX inference helper object.
    :type onnx_estimator_helper: azureml.automl.runtime.onnx_convert.OnnxInferenceFromFeaturesHelper
    """

    def __init__(self, onnx_estimator_helper: OnnxInferenceFromFeaturesHelper):
        """
        Initialize the ONNXEstimatorClassificationInferceHelperExplainabilityWrapper object.

        :param onnx_estimator_helper: An automated ML ONNX inference helper object.
        :type onnx_estimator_helper: azureml.automl.runtime.onnx_convert.OnnxInferenceFromFeaturesHelper
        """
        super().__init__(onnx_estimator_helper)

    def predict_proba(self, X: DataInputType) -> DataSingleColumnInputType:
        """Return prediction probabilities for target values using the automated ML ONNX helper model.

        :param X: The target values.
        :type X: typing.Union[numpy.ndarray, pandas.DataFrame, scipy.sparse.csr_matrix, azureml.dataprep.Dataflow]
        """
        predict, predict_proba = self._onnx_estimator_helper.predict(X=X)
        return predict_proba


class ONNXEstimatorRegressionInferceHelperExplainabilityWrapper(ONNXEstimatorInferceHelperExplainabilityWrapper):
    """A wrapper class for automated ML ONNX regression pipelines that implement standard predict() function.

    :param onnx_estimator_helper: An automated ML ONNX inference helper object.
    :type onnx_estimator_helper: azureml.automl.runtime.onnx_convert.OnnxInferenceFromFeaturesHelper
    """

    def __init__(self, onnx_estimator_helper: OnnxInferenceFromFeaturesHelper):
        """
        Initialize the ONNXEstimatorRegressionInferceHelperExplainabilityWrapper object.

        :param onnx_estimator_helper: An automated ML ONNX inference helper object.
        :type onnx_estimator_helper: azureml.automl.runtime.onnx_convert.OnnxInferenceFromFeaturesHelper
        """
        super().__init__(onnx_estimator_helper)


class AutoMLExplainerSetupClass:
    """
    Represents a placeholder class for interfacing with the Azure Machine Learning explain package.

    Use the ``automl_setup_model_explanations`` function in this module to return an
    AutoMLExplainerSetupClass.

    :param X_transform: The featurized training features used for fitting pipelines during an automated ML experiment.
    :type X_transform: typing.Union[pandas.DataFrame, numpy.ndarray, scipy.sparse.csr_matrix]
    :param X_test_raw: The raw test features used evaluating an automated ML trained pipeline.
    :type X_test_raw: typing.Union[pandas.DataFrame, numpy.ndarray, scipy.sparse.csr_matrix]
    :param X_test_transform: The featurized test features for evaluating an automated ML estimator.
    :type X_test_transform: typing.Union[pandas.DataFrame, numpy.ndarray, scipy.sparse.csr_matrix]
    :param pipeline: The entire fitted automated ML model.
    :type pipeline: sklearn.pipeline
    :param estimator: The automated ML estimator, including the model specific preprocessor and learner.
    :type estimator: sklearn.pipeline
    :param featurizer: The automated ML featurizer which does transformations from raw features to engineered features.
    :type featurizer: sklearn.pipeline
    :param engineered_feature_names: The list of names for the features generated by the automated ML featurizers.
    :type engineered_feature_names: list[str]
    :param raw_feature_names: The list of names for the raw features to be explained.
    :type raw_feature_names: list[str]
    :param feature_map: The mapping of indicating which raw features generated which engineered features, expressed
                        as a numpy array or scipy sparse matrix.
    :type feature_map: typing.Union[numpy.ndarray, scipy.sparse.csr_matrix]
    :param classes: The list of classes discovered in the labeled column, for classification problems.
    :type classes: list
    """

    def __init__(self, X_transform: Optional[DataInputType] = None,
                 X_test_raw: Optional[DataInputType] = None,
                 X_test_transform: Optional[DataInputType] = None,
                 pipeline: Optional[Union[Pipeline, StreamingPipelineExplainabilityWrapper]] = None,
                 estimator: Optional[Union[Pipeline, StreamingPipelineExplainabilityWrapper]] = None,
                 featurizer: Optional[Union[Pipeline, StreamingFeaturizationTransformer]] = None,
                 engineered_feature_names: Optional[List[str]] = None,
                 raw_feature_names: Optional[List[str]] = None,
                 feature_map: Optional[DataInputType] = None,
                 classes: Optional[List[Any]] = None,
                 surrogate_model: Optional[Any] = None,
                 surrogate_model_params: Optional[Dict[str, Any]] = None):
        """
        Initialize the automated ML explainer setup class.

        :param X_transform: The featurized training features used for fitting pipelines during an automated ML
            experiment.
        :type X_transform: typing.Union[pandas.DataFrame, numpy.ndarray, scipy.sparse.csr_matrix]
        :param X_test_raw: The raw test features used evaluating an automated ML trained pipeline.
        :type X_test_raw: typing.Union[pandas.DataFrame, numpy.ndarray, scipy.sparse.csr_matrix]
        :param X_test_transform: The featurized test features for evaluating an automated ML estimator.
        :type X_test_transform: typing.Union[pandas.DataFrame, numpy.ndarray, scipy.sparse.csr_matrix]
        :param pipeline: The entire fitted automated ML model.
        :type pipeline: sklearn.pipeline
        :param estimator: The automated ML estimator, including the model specific preprocessor and learner.
        :type estimator: sklearn.pipeline
        :param featurizer: The automated ML featurizer which does transformations from raw features to engineered
            features.
        :type featurizer: sklearn.pipeline
        :param engineered_feature_names: The list of names for the features generated by the automated ML featurizers.
        :type engineered_feature_names: list[str]
        :param raw_feature_names: The list of names for the raw features to be explained.
        :type raw_feature_names: list[str]
        :param feature_map: The mapping of indicating which raw features generated which engineered features, expressed
                            as a numpy array or scipy sparse matrix.
        :type feature_map: typing.Union[numpy.ndarray, scipy.sparse.csr_matrix]
        :param classes: The list of classes discovered in the labeled column, for classification problems.
        :type classes: list
        :type surrogate_model: The surrogate model parameters for explaining the automated ML model using MimicWrapper.
        :type surrogate_model_params: The surrogate model parameters for explaining the automated ML model using
                                      MimicWrapper.
        :type surrogate_model_params: Dict
        """
        self._X_transform = X_transform
        self._y = None  # type: Optional[DataSingleColumnInputType]
        self._y_test_raw = None  # type: Optional[DataSingleColumnInputType]
        self._X_test_transform = X_test_transform
        self._X_test_raw = X_test_raw
        self._automl_pipeline = pipeline
        self._automl_estimator = estimator
        self._automl_featurizer = featurizer
        self._engineered_feature_names = engineered_feature_names
        self._raw_feature_names = raw_feature_names
        self._feature_map = feature_map
        self._classes = classes
        self._surrogate_model = surrogate_model
        self._surrogate_model_params = surrogate_model_params
        self._top_k = MaxExplainedFeaturesToUpload

    @property
    def X_transform(self) -> DataInputType:
        """
        Return the featurized training features used for fitting pipelines during automated ML experiment.

        :return: The featurized training features used for fitting pipelines during automated ML experiment.
        :type: DataInputType
        """
        return self._X_transform

    @property
    def X_test_transform(self) -> DataInputType:
        """
        Return the featurized test features for evaluating an automated ML estimator.

        :return: The featurized test features for evaluating an automated ML estimator.
        :type: DataInputType
        """
        return self._X_test_transform

    @property
    def X_test_raw(self) -> DataInputType:
        """
        Return the raw test features used evaluating an automated ML trained pipeline.

        :return: The raw test features used evaluating an automated ML trained pipeline.
        :type: DataInputType
        """
        return self._X_test_raw

    @property
    def automl_pipeline(self) -> Union[Pipeline, StreamingPipelineWrapper]:
        """
        Return the entire fitted automated ML model.

        :return: The entire fitted automated ML model.
        :type: typing.Union[sklearn.pipeline.Pipeline]
            azureml.automl.runtime.streaming_pipeline_wrapper.StreamingPipelineWrapper)
        """
        return self._automl_pipeline

    @property
    def automl_estimator(self) -> Union[Pipeline, StreamingPipelineWrapper]:
        """
        Return the automated ML estimator, including the model specific preprocessor and learner.

        :return: The automated ML estimator, including the model specific preprocessor and learner.
        :type: typing.Union[sklearn.pipeline.Pipeline]
            azureml.automl.runtime.streaming_pipeline_wrapper.StreamingPipelineWrapper)
        """
        return self._automl_estimator

    @property
    def automl_featurizer(self) -> Union[Pipeline, StreamingFeaturizationTransformer]:
        """
        Return the automated ML featurizer which does transformations from raw features to engineered features.

        :return: The automated ML featurizer which does transformations from raw features to engineered features.
        :type: typing.Union[sklearn.pipeline.Pipeline,
            azureml.automl.runtime.streaming_pipeline_wrapper.StreamingPipelineWrapper]
        """
        return self._automl_featurizer

    @property
    def engineered_feature_names(self) -> Optional[List[str]]:
        """
        Return the list of names for the features generated by the automated ML featurizers.

        :return: The list of names for the features generated by the automated ML featurizers.
        :type: List[str]
        """
        return self._engineered_feature_names

    @property
    def raw_feature_names(self) -> Optional[List[str]]:
        """
        Return the list of names for the raw features to be explained.

        :return: The list of names for the raw features to be explained.
        :type: List[str]
        """
        return self._raw_feature_names

    @property
    def feature_map(self) -> DataInputType:
        """
        Return the mapping of which raw features generated which engineered features.

        :return: The mapping of which raw features generated which engineered features.
        :type: DataInputType
        """
        return self._feature_map

    @property
    def classes(self) -> Optional[List[Any]]:
        """
        Return the list of classes discovered in the labeled column in case of classification problem.

        :return: The list of classes discovered in the labeled column in case of classification problem.
        :type: list
        """
        return self._classes

    @property
    def surrogate_model(self) -> Any:
        """
        Return the surrogate model for explaining the automated ML model using MimicWrapper.

        :return: The surrogate model for explaining the automated ML model using MimicWrapper.
        """
        return self._surrogate_model

    @property
    def surrogate_model_params(self) -> Optional[Dict[str, Any]]:
        """
        Return the surrogate model parameters for explaining the automated ML model using MimicWrapper.

        :return: The surrogate model parameters for explaining the automated ML model using MimicWrapper.
        :type: Dict
        """
        return self._surrogate_model_params

    def __str__(self) -> str:
        """
        Return the string representation on the automated ML explainer setup class.

        :return: The string representation on the automated ML explainer setup class.
        :type: str
        """
        print_str = "The setup class is: \n"
        if self.X_transform is not None:
            print_str += "\tx_train_transform = {}\n".format(self.X_transform.shape)
        if self.X_test_raw is not None:
            print_str += "\tX_test_raw = {}\n".format(self.X_test_raw.shape)
        if self.X_test_transform is not None:
            print_str += "\tX_test_transform = {}\n".format(self.X_test_transform.shape)
        return print_str


def _get_featurizer(
        fitted_model: Union[Pipeline, StreamingPipelineWrapper]
) -> Union[Pipeline, StreamingFeaturizationTransformer]:
    """Return the featurizer in the automated ML model."""
    pipeline_transformer = None
    for name, transformer in fitted_model.steps[:-1]:
        if (transformer is not None) and \
                (name == Transformers.X_TRANSFORMER or name == Transformers.TIMESERIES_TRANSFORMER):
            pipeline_transformer = transformer
    return pipeline_transformer


def _get_pipeline(
        fitted_model: Union[Pipeline, StreamingPipelineWrapper],
        task: str,
        streaming: bool
) -> Union[Pipeline, StreamingPipelineExplainabilityWrapper]:
    """Return pipeline to be used as input to AzureML explainability library."""
    if streaming:
        return StreamingPipelineExplainabilityWrapper(fitted_model, task)
    return fitted_model


def _get_estimator(
        a_pipeline: Union[Pipeline, StreamingPipelineWrapper],
        task: str,
        streaming: bool) -> Union[Pipeline, StreamingPipelineExplainabilityWrapper]:
    """
    Return the estimator in the automated ML model.

    The estimator pipeline includes the model preprocessors and the learner.
    """
    if streaming:
        return _get_estimator_streaming(a_pipeline, task)
    return _get_estimator_non_streaming(a_pipeline)


def _get_estimator_non_streaming(a_pipeline: Pipeline) -> Pipeline:
    """Return the estimator in the automated ML model."""
    excluded_transfomers = set([Transformers.X_TRANSFORMER, Transformers.TIMESERIES_TRANSFORMER])
    modified_steps = [step[1] for step in a_pipeline.steps
                      if step[0] not in excluded_transfomers]
    if len(modified_steps) != len(a_pipeline.steps):
        return make_pipeline(*[s for s in modified_steps])
    else:
        return a_pipeline


def _get_estimator_streaming(
        pipeline: StreamingPipelineWrapper,
        task: str) -> StreamingPipelineExplainabilityWrapper:
    """Return the estimator in the automated ML model."""
    predictor_pipeline = NimbusMLPipeline()
    predictor_pipeline.load_model(pipeline._pipeline.predictor_model)
    return StreamingPipelineExplainabilityWrapper(predictor_pipeline, task)


def _get_feature_map(
        fitted_model: Union[Pipeline, StreamingPipelineWrapper], raw_feature_names_list: Optional[List[str]] = None,
        number_of_raw_features: Optional[int] = None) -> DataInputType:
    """Generate a feature map capturing which engineered feature came from which raw feature."""
    if raw_feature_names_list is None:
        # Using combined names below since that will be become the 'target' of the raised exception, indicating to the
        # user that both params are Blank/Empty
        Validation.validate_value(number_of_raw_features, name="number_of_raw_features/raw_feature_names_list")

    if number_of_raw_features is not None:
        feature_map = np.eye(number_of_raw_features, number_of_raw_features)
        return feature_map

    transformer = _get_featurizer(fitted_model)
    if transformer is None:
        feature_map = np.eye(len(cast(List[str], raw_feature_names_list)),
                             len(cast(List[str], raw_feature_names_list)))
        return feature_map

    # Get the JSON representation of the enigneered feature names
    engineered_feature_json_str_list = transformer.get_json_strs_for_engineered_feature_names()

    # Initialize an empty feature map
    feature_map = np.zeros(shape=(len(cast(List[str], raw_feature_names_list)),
                                  len(engineered_feature_json_str_list)))

    # Create a dictionary mapping from raw feature names to indexes
    raw_feature_name_to_index_dict = \
        {cast(List[str], raw_feature_names_list)[index]: index for index in range(
            0, len(cast(List[str], raw_feature_names_list)))}

    # Iterate over all the engineered features
    for engineered_feature_index, engineered_feature_json_str in enumerate(engineered_feature_json_str_list):
        engineered_feature_json = json.loads(engineered_feature_json_str)
        transformer = engineered_feature_json['Transformations']['Transformer1']
        raw_feature_names = [n for n in transformer["Input"]]
        for raw_feature_name in raw_feature_names:
            if raw_feature_name_to_index_dict.get(raw_feature_name) is not None:
                feature_map[raw_feature_name_to_index_dict.get(raw_feature_name), engineered_feature_index] = \
                    DefaultWeightRawFeatureToEngineeredFeatureMap

    return feature_map


def _get_engineered_feature_names(
        fitted_model: Union[Pipeline, StreamingPipelineWrapper]
) -> Optional[List[str]]:
    """Get the engineered feature names from the automated ML pipeline."""
    engineered_feature_names = None  # type: Optional[List[str]]
    for name, transformer in fitted_model.steps[:-1]:
        if (transformer is not None) and \
                (name == Transformers.X_TRANSFORMER or name == Transformers.TIMESERIES_TRANSFORMER):
            engineered_feature_names = transformer.get_engineered_feature_names()

    return engineered_feature_names


def _convert_to_pandas_or_numpy(
        X: Optional[Union[DataInputType, TabularDataset]] = None,
        y: Optional[Union[DataSingleColumnInputType, TabularDataset]] = None,
        X_test: Optional[Union[DataInputType, TabularDataset]] = None) -> Tuple[Optional[DataInputType],
                                                                                Optional[DataInputType],
                                                                                Optional[DataSingleColumnInputType]]:
    """Convert different azureml data objects to pandas/numpy structures."""
    X_extracted = None
    X_test_extracted = None
    y_numpy = None
    comparer_obj, name = None, ""
    if X is not None:
        comparer_obj, name = X, "X"
    elif X_test is not None:
        comparer_obj, name = X_test, "X_test"
    elif y is not None:
        comparer_obj, name = y, "y"
    else:
        # All of the inputs are None
        raise ValidationException._with_error(
            AzureMLError.create(ArgumentBlankOrEmpty, argument_name="X/y/X_test", target="X/y/X_test")
        )

    Validation.validate_type(comparer_obj, name,
                             (pd.DataFrame, np.ndarray, scipy.sparse.spmatrix, TabularDataset, Dataflow))

    if isinstance(comparer_obj, pd.DataFrame) or isinstance(comparer_obj, np.ndarray) or \
            scipy.sparse.issparse(comparer_obj):
        X_extracted = X
        X_test_extracted = X_test
        y_numpy = y

    if isinstance(comparer_obj, TabularDataset):
        if X is not None:
            X_extracted = X._dataflow.to_pandas_dataframe(extended_types=False)
        if X_test is not None:
            X_test_extracted = X_test._dataflow.to_pandas_dataframe(extended_types=False)
        if y is not None:
            y_numpy = y._dataflow.to_pandas_dataframe(extended_types=False).values

    # This code path should be safe to remove, since we've deprecated Dataflow as input type from AutoMLConfig
    # Validate streaming use cases before doing so.
    if dataprep_utilities.is_dataflow(comparer_obj):
        if X is not None:
            X_extracted = dataprep_utilities.materialize_dataflow(X)

        if y is not None:
            y_numpy = dataprep_utilities.materialize_dataflow(y, as_numpy=True)

        if X_test is not None:
            X_test_extracted = dataprep_utilities.materialize_dataflow(X_test)

    return X_extracted, X_test_extracted, y_numpy


def _get_transformed_data(
        fitted_model: Union[Pipeline, StreamingPipelineWrapper],
        X: Optional[Union[DataInputType]] = None,
        y: Optional[Union[DataSingleColumnInputType]] = None,
        X_test: Optional[Union[DataInputType]] = None,
        featurizer: Optional[Union[Pipeline, StreamingFeaturizationTransformer]] = None,
        streaming: Optional[bool] = False) -> Tuple[Optional[DataInputType], Optional[DataInputType]]:
    """
    Transform the train or test data whichever provided.

    Currently this supports only classification/regression/forecasting.
    """
    if streaming:
        return _get_transformed_data_streaming(
            fitted_model, cast(StreamingFeaturizationTransformer, featurizer), X, X_test)
    return _get_transformed_data_non_streaming(fitted_model, featurizer, X, y, X_test)


def _get_transformed_data_non_streaming(
        fitted_model: Optional[Pipeline], featurizer: Optional[Any],
        X: Optional[Union[DataInputType]] = None,
        y: Optional[Union[DataSingleColumnInputType]] = None,
        X_test: Optional[Union[DataInputType]] = None
) -> Tuple[Optional[DataInputType], Optional[DataInputType]]:
    """Transform the train or test data whichever provided."""
    X_transform = X
    X_test_transform = X_test
    y_numpy = y
    if X_transform is not None and X_test_transform is not None:
        x_transform_shape = X_transform.shape[1]
        x_test_transform_shape = X_test_transform.shape[1]
        if x_transform_shape != x_test_transform_shape:
            raise ConfigException._with_error(
                AzureMLError.create(
                    DatasetsFeatureCountMismatch, target="train/test data",
                    first_dataset_name="X", first_dataset_shape=x_transform_shape,
                    second_dataset_name="X_test", second_dataset_shape=x_test_transform_shape
                )
            )

    if fitted_model is None:
        # We need to have at least one way to featurize the data
        Validation.validate_value(featurizer, "fitted_model/featurizer")

    if fitted_model is not None:
        for name, transformer in fitted_model.steps[:-1]:
            if (transformer is not None) and \
                    (name == Transformers.X_TRANSFORMER or name == Transformers.TIMESERIES_TRANSFORMER):
                if name == Transformers.TIMESERIES_TRANSFORMER:
                    if y_numpy is not None:
                        X_transform = transformer.transform(X_transform, y_numpy)
                        X_transform.pop(constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN)
                        if X_test is not None:
                            X_test_transform = transformer.transform(X_test_transform)
                    else:
                        raise ConfigException._with_error(
                            AzureMLError.create(
                                ArgumentBlankOrEmpty, target="y/target column", argument_name="y/target column"
                            )
                        )
                else:
                    if X_transform is not None:
                        X_transform = transformer.transform(X_transform)
                    if X_test is not None:
                        X_test_transform = transformer.transform(X_test_transform)
    elif featurizer is not None:
        X_transform = featurizer.featurize(X_transform)
        X_test_transform = featurizer.featurize(X_test_transform)

    X_transform = _upgrade_sparse_matrix_type(X_transform)
    X_test_transform = _upgrade_sparse_matrix_type(X_test_transform)
    return X_transform, X_test_transform


def _get_transformed_data_streaming(
        fitted_model: StreamingPipelineWrapper,
        featurizer: StreamingFeaturizationTransformer,
        X: Optional[Union[DataInputType]],
        X_test: Optional[Union[DataInputType]],
) -> Tuple[DataInputType, DataInputType]:
    """Transform the train or test data whichever provided."""
    if featurizer is None:
        return X, X_test
    if X is None:
        transformed_X = None
    else:
        transformed_X = featurizer.transform(X, as_csr=True)
    if X_test is None:
        transformed_X_test = None
    else:
        transformed_X_test = featurizer.transform(X_test, as_csr=True)
    return transformed_X, transformed_X_test


def _get_unique_classes(y: DataSingleColumnInputType,
                        automl_estimator: Optional[Union[Pipeline, StreamingPipelineExplainabilityWrapper]] = None,
                        y_transformer: Optional[Any] = None) -> Optional[List[Any]]:
    """Return the unique classes in y or obtain classes from inverse transform using y_transformer."""
    infer_trained_labels = True
    if automl_estimator is not None:
        try:
            if (hasattr(automl_estimator, 'classes_') and
                    automl_estimator.classes_ is not None):
                class_labels = automl_estimator.classes_
                infer_trained_labels = False
                logger.info("Got class labels from the AutoML estimator")
        except Exception:
            pass

    if infer_trained_labels is True:
        class_labels = np.unique(y)
        logger.info("Inferring trained class labels from target")

    # For classification problems, inverse transform the class labels
    if y_transformer is not None:
        class_labels = y_transformer.inverse_transform(class_labels)

    logger.info("The number of unique classes in training data are {0}".format(
                len(class_labels)))

    res = class_labels.tolist()  # type: Optional[List[Any]]
    return res


def _get_raw_feature_names(X: DataInputType) -> Optional[List[str]]:
    """Extract the raw feature names from the raw data if available."""
    if isinstance(X, pd.DataFrame):
        return list(X.columns)
    else:
        return None


def _convert_to_onnx_models(fitted_model: Pipeline,
                            X: Union[DataInputType]) -> Tuple[OnnxInferenceHelper,
                                                              OnnxFeaturizerHelper,
                                                              OnnxInferenceFromFeaturesHelper]:
    """
    Convert an automated ML Python pipeline into ONNX-based inference models.

    Return ONNX-based inference models for featurizer, estimator, and the pipeline.
    """
    onnx_metadata = OnnxConverter.get_onnx_metadata(X)

    # Convert to ONNX models
    onnx_mdl, fea_onnx_mdl, est_onnx_mdl, onnx_res, err = ml_engine.convert_to_onnx(
        trained_model=fitted_model, metadata_dict=onnx_metadata,
        enable_split_onnx_models=True,
        model_name='test with transformer')

    if err is not None:
        raise OnnxConvertException.create_without_pii("Unable to convert AutoML python models to ONNX models")

    if len(onnx_res) == 0 or onnx_mdl is None or fea_onnx_mdl is None or est_onnx_mdl is None:
        raise OnnxConvertException.create_without_pii("ONNX conversion of AutoML python model failed.")

    # Convert ONNX model to Inference Helper object
    mdl_bytes = onnx_mdl.SerializeToString()
    onnx_mdl_inference = OnnxInferenceHelper(mdl_bytes, onnx_res)

    # Convert featurizer ONNX model to Inference Helper object
    mdl_bytes = fea_onnx_mdl.SerializeToString()
    fea_onnx_mdl_inference = OnnxFeaturizerHelper(mdl_bytes, onnx_res)

    # Convert estimator ONNX model to Inference Helper object
    mdl_bytes = est_onnx_mdl.SerializeToString()
    est_onnx_mdl_inference = OnnxInferenceFromFeaturesHelper(mdl_bytes, onnx_res)

    # Return the converted ONNX model, ONNX featurizer and ONNX estimator
    return onnx_mdl_inference, fea_onnx_mdl_inference, est_onnx_mdl_inference


def automl_setup_model_explanations(fitted_model: Union[Pipeline, StreamingPipelineWrapper], task: str,
                                    X: Optional[Union[DataInputType, TabularDataset]] = None,
                                    X_test: Optional[Union[DataInputType, TabularDataset]] = None,
                                    y: Optional[Union[DataSingleColumnInputType, TabularDataset]] = None,
                                    features: Optional[List[str]] = None,
                                    **kwargs: Any) -> AutoMLExplainerSetupClass:
    """
    Set up the featurized data for explaining an automated ML model.

    After setting up explanations, you can use the :class:`azureml.interpret.mimic_wrapper.MimicWrapper`
    class to compute and visualize feature importance. For more information, see
    `Interpretability: model explanations in automated machine
    learning <https://docs.microsoft.com/azure/machine-learning/how-to-machine-learning-interpretability-automl>`_.

    :param fitted_model: The fitted automated ML model.
    :type: typing.Union[sklearn.pipeline.Pipeline,
        azureml.automl.runtime.streaming_pipeline_wrapper.StreamingPipelineWrapper]
    :param task: The task type, 'classification', 'regression', or 'forecasting' depending on what kind of ML problem
        is being solved.
    :type task: typing.Union[str, azureml.train.automl.constants.Tasks]
    :param X: The training features used when fitting pipelines during an automated ML experiment.
    :type X: typing.Union[pandas.DataFrame, numpy.ndarray, azureml.dataprep.Dataflow, azureml.core.Dataset,
        azureml.data.TabularDataset]
    :param y: Training labels to use when fitting pipelines during automated ML experiment.
    :type y: typing.Union[pandas.DataFrame, numpy.ndarray, azureml.dataprep.Dataflow, azureml.core.Dataset,
        azureml.data.TabularDataset]
    :param X_test: Test data using which the model will be explained.
    :type X_test: typing.Union[pandas.DataFrame, numpy.ndarray, azureml.dataprep.Dataflow, azureml.core.Dataset,
        azureml.data.TabularDataset]
    :param features: A list of raw feature names.
    :type features: list[str]
    :param kwargs:
    :type kwargs: dict
    :return: The model's explanation setup class.
    :rtype: azureml.train.automl.runtime.automl_explain_utilities.AutoMLExplainerSetupClass
    """
    should_convert_models_to_onnx = kwargs.get('onnx_compatibility', False)
    if task != constants.Tasks.CLASSIFICATION and task != constants.Tasks.REGRESSION and \
            task != constants.Subtasks.FORECASTING:
        raise ValidationException._with_error(
            AzureMLError.create(
                InvalidArgumentWithSupportedValues, target="task", arguments="task ({})".format(task),
                supported_values=", ".join(
                    [constants.Tasks.CLASSIFICATION, constants.Tasks.REGRESSION, constants.Subtasks.FORECASTING]
                )
            )
        )

    # determine whether or not the pipeline is streaming
    if isinstance(fitted_model, StreamingPipelineWrapper):
        streaming = True
    else:
        streaming = False

    if should_convert_models_to_onnx:
        if task == constants.Subtasks.FORECASTING:
            raise ConfigException._with_error(
                AzureMLError.create(
                    FeatureUnsupportedForIncompatibleArguments, target="onnx_compatibility",
                    feature_name='ONNX Conversion',
                    arguments="task ({})".format(constants.Subtasks.FORECASTING))
            )
        if streaming:
            raise ConfigException._with_error(
                AzureMLError.create(
                    FeatureUnsupportedForIncompatibleArguments, target="onnx_compatibility",
                    feature_name='ONNX Conversion',
                    arguments="fitted_model (of type {})".format(type(fitted_model)))
            )

    print("Current status: Setting up data for AutoML explanations")
    # Convert to pythonic structures if needed
    X_pythonic, X_test_pythonic, y_pythonic = _convert_to_pandas_or_numpy(X=X, y=y, X_test=X_test)
    if should_convert_models_to_onnx:
        print("Current status: Setting up the AutoML ONNX featurizer")
        print("Current status: Setting up the AutoML ONNX estimator")
        onnx_pipeline, onnx_featurizer, onnx_estimator = _convert_to_onnx_models(fitted_model, X_pythonic)
        pipeline = onnx_pipeline  # type: Any
        featurizer = onnx_featurizer
        if task == constants.Tasks.REGRESSION:
            estimator = ONNXEstimatorRegressionInferceHelperExplainabilityWrapper(onnx_estimator)  # type: Any
        else:
            estimator = ONNXEstimatorClassificationInferceHelperExplainabilityWrapper(onnx_estimator)
    else:
        print("Current status: Setting up the AutoML featurizer")
        featurizer = _get_featurizer(fitted_model)
        print("Current status: Setting up the AutoML estimator")
        estimator = _get_estimator(fitted_model, task, streaming)
        pipeline = _get_pipeline(fitted_model, task, streaming)

    if features is None:
        if X is not None:
            raw_feature_names = _get_raw_feature_names(X_pythonic)
        elif X_test is not None:
            raw_feature_names = _get_raw_feature_names(X_test_pythonic)
        else:
            raw_feature_names = None
    else:
        raw_feature_names = features
    print("Current status: Setting up the AutoML featurization for explanations")
    # Sample down x_test if it is large
    sampled_X_test_raw = None
    if X_test_pythonic is not None:
        if X_test_pythonic.shape[0] > MaximumEvaluationSamples:
            print("Current status: Downsampling of evaluation samples from {0} to {1} samples".format(
                X_test_pythonic.shape[0], MaximumEvaluationSamples))
            sampled_X_test_raw, _ = train_test_split(X_test_pythonic, train_size=MaximumEvaluationSamples)
        else:
            print("Current status: Using {} evaluation samples".format(X_test_pythonic.shape[0]))
            sampled_X_test_raw = X_test_pythonic
    if should_convert_models_to_onnx:
        X_transform, X_test_transform = _get_transformed_data(
            None, X=X_pythonic, y=y_pythonic, X_test=sampled_X_test_raw, featurizer=featurizer, streaming=streaming)
    else:
        X_transform, X_test_transform = _get_transformed_data(
            fitted_model, X=X_pythonic, y=y_pythonic, X_test=sampled_X_test_raw,
            featurizer=featurizer, streaming=streaming)

    engineered_feature_names = _get_engineered_feature_names(fitted_model)
    engineered_feature_names = features if engineered_feature_names is None else engineered_feature_names

    print("Current status: Generating a feature map for raw feature importance")
    feature_map = _get_feature_map(fitted_model, raw_feature_names)
    if task == constants.Tasks.CLASSIFICATION and y_pythonic is not None:
        print("Current status: Finding all classes from the dataset")
        classes = _get_unique_classes(y=y_pythonic)  # type: Optional[List[Any]]
    else:
        classes = None

    surrogate_model, surrogate_model_params = _automl_pick_surrogate_model_and_set_params(
        explainer_test_data=X_test_transform,
        num_cpu_cores=_get_num_physical_cpu_cores_model_explanations(),
        should_reset_index=_should_set_reset_index(fitted_model=fitted_model))
    print("Current status: Choosing the surrogate model as {0} for the AutoML model".format(
        _get_user_friendly_surrogate_model_name(surrogate_model)))

    print("Current status: Data for AutoML explanations successfully setup")
    return AutoMLExplainerSetupClass(X_transform=X_transform, X_test_raw=sampled_X_test_raw,
                                     X_test_transform=X_test_transform, pipeline=pipeline,
                                     estimator=estimator, featurizer=featurizer,
                                     engineered_feature_names=engineered_feature_names,
                                     raw_feature_names=raw_feature_names,
                                     feature_map=feature_map, classes=classes,
                                     surrogate_model=surrogate_model,
                                     surrogate_model_params=surrogate_model_params)


def _get_user_friendly_surrogate_model_name(surrogate_model: Any) -> Optional[str]:
    from interpret_community.mimic.models.lightgbm_model import LGBMExplainableModel
    from interpret_community.mimic.models.linear_model import LinearExplainableModel
    if surrogate_model == LGBMExplainableModel or isinstance(surrogate_model, LGBMExplainableModel):
        return SurrogateModelTypes.LightGBM
    elif surrogate_model == LinearExplainableModel or isinstance(surrogate_model, LinearExplainableModel):
        return SurrogateModelTypes.LinearModel
    else:
        return None


def automl_check_model_if_explainable(run: Any, need_refresh_run: bool = True) -> bool:
    """
    Check to see if an automated ML child run is explainable.

    :param run: The automated ML child run.
    :type run: azureml.core.run.Run
    :param need_refresh_run: If the run needs to be refreshed.
    :type need_refresh_run: bool
    :return: 'True' if the model can be explained and 'False' otherwise.
    :type: bool
    """
    from azureml.automl.core.model_explanation import ModelExpSupportStr
    if need_refresh_run:
        automl_run_properties = run.get_properties()
    else:
        automl_run_properties = run.properties
    model_exp_support_property = automl_run_properties.get(ModelExpSupportStr)
    if model_exp_support_property is not None:
        return cast(bool, model_exp_support_property == 'True')
    else:
        return False


def _should_set_reset_index(automl_run: Optional[Run] = None,
                            fitted_model: Optional[Union[Pipeline, StreamingPipelineWrapper]] = None) -> bool:
    """
    Check if index needs to be reset while explaining automated ML model.

    :param automl_run: The run to store information.
    :type automl_run: azureml.core.run.Run
    :param fitted_model: The fitted automated ML model.
    :type: typing.Union[sklearn.pipeline.Pipeline,
        azureml.automl.runtime.streaming_pipeline_wrapper.StreamingPipelineWrapper]
    :return: True if reset index needs to be set and False otherwise.
    :rtype: bool
    """
    if automl_run is not None:
        run_algorithm = automl_run.properties.get('run_algorithm')
        if run_algorithm is not None and (constants.SupportedModels.Forecasting.AutoArima in run_algorithm or
                                          'ProphetModel' in run_algorithm):
            return True
        elif automl_run.tags.get('ensembled_algorithms') is not None:
            tmp = (constants.SupportedModels.Forecasting.AutoArima in automl_run.tags.get('ensembled_algorithms') or
                   'ProphetModel' in automl_run.tags.get('ensembled_algorithms'))
            return tmp
    elif fitted_model is not None:
        tmp = (constants.SupportedModels.Forecasting.AutoArima in fitted_model.named_steps or
               'ProphetModel' in fitted_model.named_steps)
        return tmp
    return False


def _automl_pick_surrogate_model_and_set_params(explainer_test_data: DataInputType,
                                                num_cpu_cores: int,
                                                should_reset_index: Optional[bool] = False) -> Tuple[Any,
                                                                                                     Dict[str, Any]]:
    """
    Choose surrogate model class and its parameters.

    :param explainer_test_data: The featurized version of validation data.
    :type explainer_test_data: DataInputType
    :param num_cpu_cores: Number of CPU cores for LightGBM surrogate model.
    :type num_cpu_cores: int
    :param should_reset_index: If we should reset index.
    :type should_reset_index: bool
    :return: Surrogate model class, surrogate model parameters
    """
    from interpret_community.mimic.models.lightgbm_model import LGBMExplainableModel
    from interpret_community.mimic.models.linear_model import LinearExplainableModel
    from interpret_community.common.constants import MimicSerializationConstants
    from interpret_community.common.constants import ResetIndex
    surrogate_model_params = {AugmentDataStr: False}  # type: Dict[str, Any]
    surrogate_model = LGBMExplainableModel
    if scipy.sparse.issparse(explainer_test_data) and explainer_test_data.shape[1] > SparseNumFeaturesThreshold:
        logger.info("Using linear surrogate model due to sparse data")
        surrogate_model = LinearExplainableModel
        surrogate_model_params[ExplainableModelArgsStr] = {LinearSurrogateModelParam: True}
    else:
        logger.info("The number of core being set for explainable model is: " + str(num_cpu_cores))
        # Set the number of cores for LightGBM model
        surrogate_model_params[ExplainableModelArgsStr] = {LGBMSurrogateModelParam: num_cpu_cores}

    if should_reset_index is True:
        surrogate_model_params[MimicSerializationConstants.RESET_INDEX] = ResetIndex.ResetTeacher
    return surrogate_model, surrogate_model_params
