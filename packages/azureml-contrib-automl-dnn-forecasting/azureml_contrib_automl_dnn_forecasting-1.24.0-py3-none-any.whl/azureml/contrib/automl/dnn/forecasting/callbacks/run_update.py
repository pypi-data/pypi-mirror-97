# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Callbacks which computes and uploads metric to run."""
import json
import logging
import os
from typing import Union

import azureml.dataprep as dprep
import pandas as pd
import pkg_resources
from azureml.automl.core import inference, package_utilities
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.systemusage_telemetry import SystemResourceUsageTelemetryFactory
from azureml.core.run import Run
from azureml.train.automl._constants_azureml import MLFlowSettings
from azureml.train.automl.runtime._azureautomlruncontext import AzureAutoMLRunContext
from forecast.callbacks import Callback

from azureml.automl.runtime.data_transformation import _get_data_snapshot
from ..constants import ForecastConstant
from ..metrics.metrics import compute_metric, get_target_values, save_metric
from ..wrapper.forecast_wrapper import DNNForecastWrapper, DNNParams

logger = logging.getLogger(__name__)


class RunUpdateCallback(Callback):
    """Wraps AutoML metric computation and upload in a callback."""

    def __init__(self,
                 model_wrapper: DNNForecastWrapper,
                 run_context: Run,
                 X_valid: Union[pd.DataFrame, dprep.Dataflow],
                 y_valid: Union[pd.DataFrame, dprep.Dataflow],
                 params: DNNParams,
                 logger: logging.Logger = None):
        """Initialize callback to compute and upload metric to the run context.

        :param model_wrapper: DNNForecastWrapper Model that is being trained
        :param run_context:AutoML run context to be used for uploading model/metrices
        :param X_valid: X validation data used for computing metrices
        :param y_valid: y validation data used for computing metrices
        :param params: DNNParams
        :param logger: Logger
        """
        super().__init__()
        self.model_wrapper = model_wrapper
        self.run_context = run_context
        self.X_valid = X_valid
        self.y_valid = y_valid
        self.ds_valid = None
        self.params = params
        self.logger = logger
        self._scores = None
        self._samples = None

        self.telemetry_logger = SystemResourceUsageTelemetryFactory.get_system_usage_telemetry(interval=10)
        self.automl_run_context = AzureAutoMLRunContext(self.run_context)
        # Add properties required for automl UI.
        run_properties_for_ui = {"runTemplate": "automl_child",
                                 "run_preprocessor": "",
                                 "run_algorithm": self.model_wrapper.name,
                                 ForecastConstant.primary_metric: params.get_value(ForecastConstant.primary_metric)}
        self.run_context.add_properties(run_properties_for_ui)

        self.report_interval = params.get_value(ForecastConstant.report_interval)
        self.num_epochs = params.get_value(ForecastConstant.num_epochs)
        self.num_epochs_done = 0

    def on_train_epoch_end(self, epoch, loss, metrics) -> None:
        """On each train epoch end set to compute metric and upload.

        :param epoch: Current epoch number
        :param loss: current loss
        :param metrics: metrics already computed
        """
        # TODO move this to different Telemetry callback
        self.telemetry_logger.send_usage_telemetry_log(
            prefix_message="[RunId:{}][After DNN Train epoch {} completed]".format(
                self.automl_run_context.run_id, epoch
            )
        )
        if self._is_validation_data_available():
            if self.ds_valid is None:
                self.ds_valid = self.model_wrapper._get_timeseries(self.X_valid, self.y_valid)
            # else:
            # validation data is already transformed and cached, so no need to transform it again
            # self.ds_valid.transform = None
            y_pred = self.model_wrapper._predict(self.ds_valid)
            horizon = self.model_wrapper.params.get_value(ForecastConstant.Horizon)
            assert horizon == y_pred.shape[-1], "h={0} y={1}".format(horizon, y_pred.shape)
            y_test = get_target_values(self.model_wrapper, self.ds_valid)

            scores = compute_metric(y_pred=y_pred, y_true_forecast=y_test, horizon=horizon,
                                    scalar_only=True, logger=self.logger)
            self.logger.info("Scores: '{0}'".format(scores))
            save_metric(self.run_context, scores)

        if epoch == self.num_epochs - 1:  # epochs start at 0
            if self._is_validation_data_available():
                self.upload_properties_tabular_metrics(y_pred=y_pred, y_test=y_test)
            self.upload_model()

    def _is_validation_data_available(self):
        return self.ds_valid is not None or (self.X_valid is not None and self.y_valid is not None)

    def _get_primary_metric_score(self, scores) -> float:
        score = float('nan')
        primary_metric = self.params.get_value(ForecastConstant.primary_metric)
        if primary_metric in scores:
            score = scores[primary_metric]
        else:
            self.logger.warning("Primary metric '{0}' is missing from the scores".format(primary_metric))
        return score

    def upload_properties_tabular_metrics(self, y_pred, y_test, ) -> None:
        """On train end set to upload tabular metrics.

        :param y_pred: predicted target values
        :param y_test: actual target values
        """
        # upload tabular metrics
        horizon = self.model_wrapper.params.get_value(ForecastConstant.Horizon)
        scores = compute_metric(y_pred=y_pred, y_true_forecast=y_test, horizon=horizon, scalar_only=False)
        save_metric(self.run_context, scores)

        # Add the score that is mandatory for the ui to show the run in UI
        score = self._get_primary_metric_score(scores)
        self.run_context.add_properties({"score": float(score)})

    def upload_model(self) -> None:
        """Upload dnn model to run context."""
        model_id = self._get_model_id(self.run_context.id)
        self._save_model_for_automl_inference(model_id, self.model_wrapper)

    def _get_sample_data_json(self, logger: logging.Logger):
        # create input data json from the first row of sample data
        # this input_data is used by the swagger to infer the input data for aci inference.
        sample_str = "None"
        try:
            if self._samples is None:
                if self.X_valid is not None:
                    if isinstance(self.X_valid, pd.DataFrame):
                        self._samples = self.X_valid[-1:].copy()
                    else:
                        self._samples = self.X_valid.take(1).to_pandas_dataframe(extended_types=True)
                else:
                    self._samples = self.model_wrapper._data_for_inference[-1:].copy()
                    if ForecastConstant.automl_constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN in self._samples:
                        self._samples.pop(ForecastConstant.automl_constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN)

            sample_str = _get_data_snapshot(self._samples, is_forecasting=True)
        except Exception as e:
            logger.warning("Failed to create score inference file.")
            logging_utilities.log_traceback(e, logger, is_critical=False)

        return sample_str

    def _get_inference_file_content(self, logger: logging.Logger):
        # generate sample data for scoring file, by looking at first row fom sample data
        input_json = self._get_sample_data_json(logger)
        return self._get_scoring_file(input_json)

    # this code has to be refactored in automl sdk where it can take the model and context and save
    # all inferencing related data
    def _save_model_for_automl_inference(self, model_id: str,
                                         model: DNNForecastWrapper):
        """Save model and runproperties needed for inference.

        :param model_id: the unique id for identifying the model with in the workspace.
        :param model: model to save in artifact.
        :return:
        """
        all_dependencies = package_utilities._all_dependencies()
        strs_to_save = {}

        # save versions to artifacts
        strs_to_save[ForecastConstant.automl_constants.DEPENDENCIES_PATH] = json.dumps(all_dependencies, indent=4)

        # save conda environment file into artifacts
        try:
            strs_to_save[ForecastConstant.automl_constants.CONDA_ENV_FILE_PATH] = self._create_conda_env_file_content()
        except Exception as e:
            self.logger.warning("Failed to create conda environment file.")
            logging_utilities.log_traceback(e, logger, is_critical=False)

        # save scoring file into artifacts
        try:
            scoring_file_str = self._get_inference_file_content(logger)
            strs_to_save[ForecastConstant.automl_constants.SCORING_FILE_PATH] = scoring_file_str
        except Exception as e:
            self.logger.warning("Failed to create score inference file.")
            logging_utilities.log_traceback(e, logger, is_critical=False)

        # Upload files to artifact store
        models_to_upload = {ForecastConstant.MODEL_PATH: model}

        try:
            # This code makes 3 network calls, we may want to optimize it away and consume save_mlflow some other way
            automl_settings = self.run_context.parent.parent.get_properties().get('AMLSettingsJsonString', "{}")
            save_as_mlflow = json.loads(automl_settings).get("save_mlflow", False)
        except Exception:
            logger.warning("Could not load AutoMLSettings from parent run.")
            save_as_mlflow = False
        self.automl_run_context.batch_save_artifacts(
            os.getcwd(),
            strs_to_save,
            models_to_upload,
            save_as_mlflow=save_as_mlflow)

        # save artifact ids as properties
        properties_to_add = {
            inference.AutoMLInferenceArtifactIDs.CondaEnvDataLocation:
                self.automl_run_context._get_artifact_id(ForecastConstant.automl_constants.CONDA_ENV_FILE_PATH),
            inference.AutoMLInferenceArtifactIDs.ModelDataLocation:
                self.automl_run_context._get_artifact_id(ForecastConstant.MODEL_PATH)
        }

        properties_to_add.update({
            inference.AutoMLInferenceArtifactIDs.ScoringDataLocation:
                self.automl_run_context._get_artifact_id(ForecastConstant.automl_constants.SCORING_FILE_PATH),
            inference.AutoMLInferenceArtifactIDs.ModelName: model_id
        })

        # automl code saves the graph json for the pipeline. Todo add code to save the model graph.

        self.automl_run_context._run.add_properties(properties_to_add)

    def _get_model_id(self, runid: str):
        """Generate a model name from runid.

        :param runid:  runid string of the hyperdrive child run.
        :return: the id produced by taking run number and last 12 chars from hyperdrive runid.
        """
        name = 'DNN'
        parent_num_part = ''
        child_num = ''
        if runid:
            parts = runid.split("_")
            if len(parts) > 0:
                child_num = parts[-1]
            if len(parts) > 1:
                parent_num_part = parts[-2][-12:]

        return name + parent_num_part + child_num

    def _get_scoring_file(self, input_sample_str: str = "pd.DataFrame()") -> str:
        """
        Return scoring file to be used at the inference time.

        If there are any changes to the scoring file, the version of the scoring file should
        be updated in the vendor.

        :return: Scoring python file as a string
        """
        scoring_file_path = pkg_resources.resource_filename(
            inference.inference.PACKAGE_NAME, os.path.join('inference', 'score_forecasting_dnn.txt'))

        inference_data_type = inference.inference.PandasParameterType

        with open(scoring_file_path, 'r') as scoring_file_ptr:
            content = scoring_file_ptr.read()
            content = content.replace('<<ParameterType>>', inference_data_type)
            content = content.replace('<<input_sample>>', input_sample_str)
            content = content.replace('<<model_filename>>', ForecastConstant.MODEL_FILENAME)

        return content

    def _create_conda_env_file_content(self):
        """
        Return conda/pip dependencies for the current AutoML run.

        If there are any changes to the conda environment file, the version of the conda environment
        file should be updated in the vendor.

        :return: Conda dependencies as string
        """
        from azureml.core.conda_dependencies import CondaDependencies
        sdk_dependencies = package_utilities._all_dependencies()
        pip_package_list_with_version = []
        automl_forecast_dnn_package = ['azureml-contrib-automl-dnn-forecasting']
        for pip_package in inference.AutoMLPipPackagesList + automl_forecast_dnn_package:
            if 'azureml' in pip_package:
                if pip_package in sdk_dependencies:
                    pip_package_list_with_version.append(pip_package + "==" + sdk_dependencies[pip_package])
            else:
                pip_package_list_with_version.append(pip_package)
        AutoMLCondaPackagesList = inference.AutoMLCondaPackagesList
        AutoMLCondaPackagesList.append("pytorch>=1.2")

        myenv = CondaDependencies.create(conda_packages=AutoMLCondaPackagesList,
                                         pip_packages=pip_package_list_with_version,
                                         python_version='3.7',
                                         pin_sdk_version=False)
        myenv.add_channel("pytorch")
        return myenv.serialize_to_string()
