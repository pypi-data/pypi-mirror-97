import logging
import os
from contextlib import AbstractContextManager
from datetime import datetime
from typing import List, Mapping, Optional

import bdrk
from bdrk.backend.v1.exceptions import ApiException
from bdrk.backend.v1.models.metric_point_schema import MetricPointSchema
from bdrk.utils.exceptions import BedrockClientNotFound
from bdrk.utils.utils import check_param
from bdrk.utils.vars import Constants
from spanlib.infrastructure.kubernetes.env_var import (
    BEDROCK_ENVIRONMENT_ID,
    BEDROCK_PIPELINE_ID,
    BEDROCK_PIPELINE_RUN_ID,
)
from spanlib.types import PipelineRunStatus

from .client_old import BedrockApi

_logger = logging.getLogger(Constants.MAIN_LOG)


class RunContext(AbstractContextManager):
    def __init__(
        self, pipeline_id: str, environment_id: str, model_id: Optional[str] = None,
    ):
        """Initialize the run context, register the necessary variables
        """
        self.pipeline_id = pipeline_id
        self.environment_id = environment_id
        self.model_id = model_id
        self.run_id = None
        # Only single step pipeline is currently supported, the default name is `train`
        self.step_name = "train"

    def __enter__(self):
        """Enter the run context, register it with the bedrock_client
        """
        if bdrk.bedrock_client is None:
            raise BedrockClientNotFound
        # First, need to register the run context to block other runs
        bdrk.bedrock_client.init_run_context(self)
        try:
            # Try to get/create pipeline and
            pipeline = bdrk.bedrock_client.get_or_create_training_pipeline(
                pipeline_id=self.pipeline_id, model_id=self.model_id,
            )

            # Start the run. This is no-op in case of orchestrated run
            run = bdrk.bedrock_client.create_training_run(
                pipeline_id=self.pipeline_id, environment_id=self.environment_id,
            )

            # Update run_id and model_id
            if pipeline and run:
                self.model_id = pipeline.model_id
                self.run_id = run.run.entity_number
                # Only single step pipeline is currently supported
                self.step_name = run.steps[0].name
            else:
                if BEDROCK_PIPELINE_RUN_ID not in os.environ:
                    raise ValueError(f"{BEDROCK_PIPELINE_RUN_ID} must be supported in env vars")
                self.run_id = os.environ[BEDROCK_PIPELINE_RUN_ID]
            _logger.info(f"Run started: {self.pipeline_id}-run{self.run_id}")
        except Exception as e:
            # Clean up the run context if the run cannot start
            bdrk.bedrock_client.exit_run_context()
            raise e
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the run context, unregister it with the bedrock_client
        """
        try:
            if exc_type is None:
                # Succeeded, creating model version
                status = PipelineRunStatus.SUCCEEDED

                # Try creating a model version.
                # This will fail if the model artefact has not been logged.
                try:
                    model_version = bdrk.bedrock_client.create_model_version(
                        model_id=self.model_id, pipeline_id=self.pipeline_id, run_id=self.run_id
                    )
                    if model_version:
                        _logger.info(
                            f"Model version created: "
                            f"{self.model_id}-v{model_version.model_version_id}"
                        )
                except ApiException as exc:
                    _logger.warn(f"Skipping: Cannot create model version -- {exc.body}")
                    _logger.debug("Model version creation failed", exc)

            elif exc_type == KeyboardInterrupt:
                status = PipelineRunStatus.STOPPED
            else:
                status = PipelineRunStatus.FAILED

            bdrk.bedrock_client.update_training_run_status(
                pipeline_id=self.pipeline_id, run_id=self.run_id, status=status,
            )
            _logger.info(f"Run {status}: {self.pipeline_id}-run{self.run_id}")
        finally:
            # Always exit the context
            bdrk.bedrock_client.exit_run_context()

        _logger.info("Run exitted")
        return True if exc_type is None else False


def start_run(
    pipeline_id: Optional[str] = None,
    environment_id: Optional[str] = None,
    model_id: Optional[str] = None,
) -> RunContext:
    """Start a run. This will return a RunContext that's to be used in a `with` statement.
    Without a `with` statement, the run_context will not start.

    Args:
        pipeline_id (Optional[str], optional): pipeline_id. Defaults to None and data
            is read from the environment variables.
        environment_id (Optional[str], optional): [description]. Defaults to None and data
            is read from the environment variables
        model_id (Optional[str], optional): [description]. Defaults to None.
    Returns:
        RunContext: the run context
    """
    pip_id = check_param(
        param_name="pipeline_id", param_var=pipeline_id, env_name=BEDROCK_PIPELINE_ID
    )
    env_id = check_param(
        param_name="environment_id", param_var=environment_id, env_name=BEDROCK_ENVIRONMENT_ID
    )
    return RunContext(pipeline_id=pip_id, model_id=model_id, environment_id=env_id)


def log_params(params: Mapping[str, str]):
    """To log training run parameters. This should be run inside a run context.

    Args:
        parameters (Mapping[str, str]): new params to be logged.
            This will override the old values in cases of duplicated keys
    """
    if bdrk.bedrock_client is None:
        raise BedrockClientNotFound
    run = bdrk.bedrock_client.update_training_run_params(
        pipeline_id=bdrk.bedrock_client.run_context.pipeline_id,
        run_id=bdrk.bedrock_client.run_context.run_id,
        parameters=params,
    )
    _logger.info(f"Params updated: {run.script_parameters}")


def log_model(path: str):
    """To log a trained model. This should be called inside a run context.

    Args:
        path (str): path to a model file or a directory.
    """
    if bdrk.bedrock_client is None:
        raise BedrockClientNotFound

    bdrk.bedrock_client.zip_and_upload_artefact(
        pipeline_id=bdrk.bedrock_client.run_context.pipeline_id,
        run_id=bdrk.bedrock_client.run_context.run_id,
        step_name=bdrk.bedrock_client.run_context.step_name,
        path=path,
    )
    _logger.info(f"Model logged: {path}")


def log_metrics(metrics: Mapping[str, float], x: Optional[float] = 0):
    """Log multiple training run metrics. This should be called inside a run context.

    Args:
        metrics (Mapping[str, float]): Dictionary mapping metric keys to values
        x (Optional[float], optional): x-axis value. Defaults to 0.
    """
    if bdrk.bedrock_client is None:
        raise BedrockClientNotFound

    timestamp = datetime.utcnow()
    formatted_metrics = {
        k: [MetricPointSchema(x=x, value=v, timestamp=timestamp)] for k, v in metrics.items()
    }
    bdrk.bedrock_client.log_training_run_step_metrics(
        pipeline_id=bdrk.bedrock_client.run_context.pipeline_id,
        run_id=bdrk.bedrock_client.run_context.run_id,
        step_name=bdrk.bedrock_client.run_context.step_name,
        metrics=formatted_metrics,
    )
    _logger.info(f"New metrics logged: with x={x}, metrics={metrics}")


def log_metric(key: str, value: float, x: Optional[float] = 0):
    """Log a single training run metric

    Args:
        key (str): metric key
        value (float): metric value
        x (Optional[float], optional): x-axis value. Defaults to 0.
    """
    log_metrics(metrics={key: value}, x=x)


def log_binary_classifier_metrics(actual: List[int], probability: List[float]):
    """Log binary classifier metrics using a series of predicted probabilities and actual values.
    Calculate the confusion matrix at various discrimination thresholds and log to a special
    metric key, "binary_classifier_chart"

    :param List[int] actual: Actual values; must be 0 or 1.
    :param List[float] probability: Predicted probabilities produced by model,
        must be between 0 and 1.
    """

    if bdrk.bedrock_client is None:
        raise BedrockClientNotFound
    if not all(map(lambda v: v in [0, 1], actual)):
        _logger.warn(f"log_binary_classifier_metrics: actual values must be 0 or 1: {actual}")
        return

    if not all(map(lambda v: 0.0 <= v <= 1.0, probability)):
        _logger.warn(
            f"log_binary_classifier_metrics: "
            f"probability values must be between 0 and 1: {probability}"
        )
        return

    if not len(actual) == len(probability):
        _logger.warn(
            f"log_chart_data: mismatch in length of actual ({len(actual)}) "
            f"vs probability ({len(probability)}) values"
        )
        return

    timestamp = datetime.utcnow()
    metrics: Mapping[str, List[MetricPointSchema]] = {
        f"bdrk.binary_classifier_chart.{key}": [] for key in ["tn", "fp", "fn", "tp"]
    }

    thresholds = (round(x * 0.05, 2) for x in range(0, 20))  # 0 to 1 in 0.05 increments
    for threshold in thresholds:
        prediction = [int(p > threshold) for p in probability]
        tn, fp, fn, tp = BedrockApi._compute_tn_fp_fn_tp(actual, prediction)
        for key, val in [("tn", tn), ("fp", fp), ("fn", fn), ("tp", tp)]:
            metrics[f"bdrk.binary_classifier_chart.{key}"].append(
                MetricPointSchema(x=threshold, value=val, timestamp=timestamp)
            )

    bdrk.bedrock_client.log_training_run_step_metrics(
        pipeline_id=bdrk.bedrock_client.run_context.pipeline_id,
        run_id=bdrk.bedrock_client.run_context.run_id,
        step_name=bdrk.bedrock_client.run_context.step_name,
        metrics=metrics,
    )
    _logger.info("Confusion matrix logged")


def download_model(model_id: str, version: int, path: str = "", log_dependency: bool = True):
    """Downloads artefacts for a Model Version.

    Args:
        model_id (str): model id.
        version (int): model version number.
        path (str): Destination path where artefacts are downloaded to. If unspecified, will
            download to the current working directory.
        log_dependency (bool): Whether to log the downloaded Model Version as an upstream
        dependency of the current run. Defaults to True.
    """
    if bdrk.bedrock_client is None:
        raise BedrockClientNotFound

    bdrk.bedrock_client.download_and_unzip_artefact(model_id=model_id, version=version, path=path)
    if log_dependency:
        bdrk.bedrock_client.add_upstream_model(
            pipeline_id=bdrk.bedrock_client.run_context.pipeline_id,
            run_id=bdrk.bedrock_client.run_context.run_id,
            step_name=bdrk.bedrock_client.run_context.step_name,
            model_id=model_id,
            version=version,
        )
    _logger.info(f"Model {model_id}-v{version} downloaded: {path or os.getcwd()}")
