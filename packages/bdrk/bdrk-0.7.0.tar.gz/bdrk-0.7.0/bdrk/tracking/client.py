import io
import logging
import os
import threading
from datetime import datetime
from pathlib import Path
from tempfile import SpooledTemporaryFile
from typing import IO, List, Mapping, Optional
from zipfile import ZIP_DEFLATED, ZipFile

import requests

from bdrk.backend.v1 import (
    ApiClient,
    ApiException,
    Configuration,
    ModelApi,
    PipelineApi,
    ProjectApi,
)
from bdrk.backend.v1.models.add_upstream_model_request_schema import AddUpstreamModelRequestSchema
from bdrk.backend.v1.models.create_model_artefact_schema import CreateModelArtefactSchema
from bdrk.backend.v1.models.metric_point_schema import MetricPointSchema
from bdrk.backend.v1.models.model_artefact_schema import ModelArtefactSchema
from bdrk.backend.v1.models.pipeline_run_parameters_schema import PipelineRunParametersSchema
from bdrk.backend.v1.models.project_schema import ProjectSchema
from bdrk.backend.v1.models.start_training_run_schema import StartTrainingRunSchema
from bdrk.backend.v1.models.training_pipeline_run_schema import TrainingPipelineRunSchema
from bdrk.backend.v1.models.training_pipeline_schema import TrainingPipelineSchema
from bdrk.backend.v1.models.training_run_and_steps_schema import TrainingRunAndStepsSchema
from bdrk.backend.v1.models.training_run_step_schema import TrainingRunStepSchema
from bdrk.backend.v1.models.update_pipeline_run_metric_schema import UpdatePipelineRunMetricSchema
from bdrk.backend.v1.models.update_pipeline_run_status_schema import UpdatePipelineRunStatusSchema
from bdrk.utils.decorators import bedrock_env_skipped
from bdrk.utils.exceptions import DataMismatchError, MultipleRunContextError, NoRunContextError
from bdrk.utils.vars import Constants
from spanlib.infrastructure.kubernetes.env_var import API_DOMAIN
from spanlib.types import PipelineRunStatus

from .training_pipeline import RunContext

_logger = logging.getLogger(Constants.MAIN_LOG)


class BedrockClient(object):
    def __init__(
        self, access_token: str, project_id: str,
    ):
        # Generate backends
        configuration = Configuration()
        configuration.host = os.environ.get(API_DOMAIN, Constants.DEFAULT_API_DOMAIN)
        configuration.api_key[Constants.HEADER_ACCESS_TOKEN] = access_token
        api_client = ApiClient(configuration)

        # Immutable variables, which should not be changed after the creation.
        self._access_token = access_token
        self._project_id = project_id
        self._project_api = ProjectApi(api_client)
        self._pipeline_api = PipelineApi(api_client)
        self._model_api = ModelApi(api_client)

        # Lock object for locking editable variables.
        self._lock = threading.Lock()

        # Following are editable variables. These variables need to be locked before editing.
        # A run context will contain related info .i.e current run_id, pipeline_id
        self._run_context = None

    @property
    def run_context(self):
        if not self._run_context:
            raise NoRunContextError
        return self._run_context

    def init_run_context(self, run_context: RunContext):
        """Register the current run context
        Args:
            run_context (RunContext): the current run_context
        """
        with self._lock:
            if self._run_context:
                raise MultipleRunContextError
            self._run_context = run_context

    def exit_run_context(self):
        """Exit the current run context
        """
        self._run_context = None

    @bedrock_env_skipped
    def create_project_if_not_exist(self, project_id: str):
        """Check if project does not exist, then create it

        Args:
            project_id (str): project id
        """
        try:
            response = self._project_api.get_project(project_id=project_id)
            _logger.debug(f"Project found: {response}")
        except ApiException as exc:
            if exc.status == 404:
                # Project not found, create a new one
                response = self._project_api.create_project(
                    project_schema=ProjectSchema(
                        public_id=project_id, description="Auto created by bdrk client library"
                    )
                )
                _logger.debug(f"Project created: {response}")
            else:
                raise exc

    @bedrock_env_skipped
    def get_or_create_training_pipeline(
        self, pipeline_id: str, model_id: Optional[str]
    ) -> TrainingPipelineSchema:
        """Get a training pipeline detail. In case of 404, create a new pipeline.

        Args:
            pipeline_id (str): pipeline_id
            model_id (Optional[str]): model_id to be set if pipeline does not exist

        Returns:
            TrainingPipelineSchema: Training pipeline object
        """
        try:
            response = self._pipeline_api.get_training_pipeline_by_id(
                project_id=self._project_id, pipeline_id=pipeline_id,
            )
            # model_id is given but does not match the existing pipeline
            if model_id and response.model_id != model_id:
                raise DataMismatchError(
                    resp_details=(
                        f"model_id {model_id} should match pipeline.model_id {response.model_id}"
                    )
                )
            _logger.debug(f"Pipeline found: {response}")
            return response
        except ApiException as exc:
            if exc.status == 404:
                response = self._pipeline_api.create_training_pipeline(
                    project_id=self._project_id,
                    training_pipeline_schema=TrainingPipelineSchema(
                        model_id=model_id or pipeline_id, pipeline_id=pipeline_id
                    ),
                )
                _logger.warn(f"New pipeline created: {pipeline_id}")
                _logger.debug(f"Pipeline created: {response}")
                return response
            else:
                raise exc

    @bedrock_env_skipped
    def create_training_run(
        self, environment_id: str, pipeline_id: str
    ) -> TrainingRunAndStepsSchema:
        """Create a training pipeline if it does not exist, then start a run

        Args:
            environment_id (str): environment to store the artefact
            pipeline_id (str): pipeline id

        Returns:
            TrainingRunAndStepsSchema: Run and step details
        """
        response = self._pipeline_api.start_run(
            project_id=self._project_id,
            start_training_run_schema=StartTrainingRunSchema(
                environment_id=environment_id,
                pipeline_id=pipeline_id,
                timestamp=datetime.utcnow(),
            ),
        )
        _logger.debug(f"Run created: {response}")
        return response

    @bedrock_env_skipped
    def add_upstream_model(
        self, pipeline_id: str, run_id: int, step_name: str, model_id: str, version: int
    ):
        """To add an upstream model to the run step

        Args:
            pipeline_id (str): pipeline id
            run_id (int): run id
            step_name (str): step name
            model_id (str): model id
            version (int): model version id

        Returns:
            TrainingRunStepSchema: Run and step details
        """
        response = self._pipeline_api.add_upstream_model(
            project_id=self._project_id,
            pipeline_id=pipeline_id,
            run_id=run_id,
            step_name=step_name,
            add_upstream_model_request_schema=[
                AddUpstreamModelRequestSchema(model_id=model_id, model_version_id=version)
            ],
        )
        _logger.debug(f"Upstream model added to: {response}")
        return response

    @bedrock_env_skipped
    def update_training_run_status(
        self, pipeline_id: str, run_id: int, status: PipelineRunStatus,
    ) -> TrainingRunAndStepsSchema:
        """To update a training run status

        Args:
            pipeline_id (str): pipeline id
            run_id (int): run id
            status (PipelineRunStatus): the new run status

        Returns:
            TrainingRunAndStepsSchema: Run and step details
        """
        response = self._pipeline_api.update_run_steps_status(
            project_id=self._project_id,
            pipeline_id=pipeline_id,
            run_id=run_id,
            update_pipeline_run_status_schema=UpdatePipelineRunStatusSchema(
                status=status, timestamp=datetime.utcnow(),
            ),
        )
        _logger.debug(f"Run updated: {response}")
        return response

    def update_training_run_params(
        self, pipeline_id: str, run_id: int, parameters: Mapping[str, str]
    ) -> TrainingPipelineRunSchema:
        """To update a training run parameters.
        This should be run inside a run context

        Args:
            pipeline_id (str): pipeline id
            run_id (int): run id
            parameters (Mapping[str, str]): new params to be updated.
                This will override the old values in cases of duplicated keys
        """
        response = self._pipeline_api.update_run_params(
            project_id=self._project_id,
            pipeline_id=pipeline_id,
            run_id=run_id,
            # Need to convert keys and values to string.
            pipeline_run_parameters_schema=PipelineRunParametersSchema(
                script_parameters={str(k): str(v) for k, v in parameters.items()}
            ),
        )
        _logger.debug(f"Run params updated: {response}")
        return response

    @bedrock_env_skipped
    def create_model_version(
        self, model_id: str, pipeline_id: str, run_id: int
    ) -> ModelArtefactSchema:
        """Create a new model version for the targeting run

        Args:
            model_id (str): model id
            pipeline_id (str): pipeline id
            run_id (int): targeting run id
        """
        response = self._model_api.create_model_version(
            project_id=self._project_id,
            model_id=model_id,
            create_model_artefact_schema=CreateModelArtefactSchema(
                pipeline_id=pipeline_id, pipeline_run_id=run_id,
            ),
        )
        _logger.debug(f"Model version created: {response}")
        return response

    @bedrock_env_skipped
    def zip_and_upload_artefact(self, pipeline_id: str, run_id: int, step_name: str, path: str):
        """Zips and uploads a trained model. This should be called inside a run context.

        Args:
            pipeline_id (str): pipeline id
            run_id (int): run id
            step_name (str): step name
            path (str): path to a model file or a directory.
        """
        fpath = Path(path)
        if not fpath.exists():
            raise ValueError(f"Specified path does not exist: {path}")

        # Implementation adapted from zipfile.main
        def add_to_zip(zf, fpath, zpath):
            if fpath.is_file():
                zf.write(filename=fpath, arcname=zpath, compress_type=ZIP_DEFLATED)
            elif fpath.is_dir():
                if zpath.name:
                    zf.write(filename=fpath, arcname=zpath)
                for nm in sorted(fpath.iterdir()):
                    add_to_zip(zf, fpath.joinpath(nm), zpath.joinpath(nm))
            # else: ignore

        # Cache files bigger than 100MB to disk
        SIZE_100_MB = 100 * 1024 * 1024
        with SpooledTemporaryFile(max_size=SIZE_100_MB) as tmp:
            with ZipFile(file=tmp, mode="w") as archive:
                # Treat files as single file directories
                zpath = Path(fpath.name) if fpath.is_file() else Path("")
                add_to_zip(zf=archive, fpath=fpath, zpath=zpath)

            upload = self._pipeline_api.get_step_artefact_upload_url(
                pipeline_id=pipeline_id,
                run_id=run_id,
                step_name=step_name,
                project_id=self._project_id,
            )

            # stream the file to gcs
            tmp.seek(0)
            resp = requests.put(upload.url, headers=upload.headers, data=tmp, stream=True)
            resp.raise_for_status()
            # TODO: upload archive.filelist

            self._pipeline_api.update_step_artefact_uploaded(
                pipeline_id=pipeline_id,
                run_id=run_id,
                step_name=step_name,
                project_id=self._project_id,
            )

    @bedrock_env_skipped
    def download_and_unzip_artefact(self, model_id: str, version: int, path: str):
        """Zips and uploads a trained model. This should be called inside a run context.
        Args:
            model_id (str): model id
            version (int): model version number
            path (str): Destination path where artefacts are downloaded to. If unspecified, will
            download to the current working directory
        """

        def unzip_file_to_dir(src: IO[bytes], path: str) -> None:
            try:
                with ZipFile(src) as zf:
                    zf.extractall(path=path)
            except Exception as e:
                raise IOError(f"Failed to unzip to {path}") from e

        fpath = Path(path)
        if not fpath.exists():
            raise ValueError(f"Specified path does not exist: {path}")

        try:
            download = self._model_api.get_model_version_download_url(
                model_id=model_id, model_version_id=version, project_id=self._project_id
            )
        except Exception as e:
            raise IOError(
                f"Failed to get download url for model_id:{model_id} version:{version}"
            ) from e

        try:
            rsp = requests.get(download.url, stream=True)
            rsp.raise_for_status()
        except Exception as e:
            raise IOError(f"Failed to download from {download.url}") from e
        unzip_file_to_dir(src=io.BytesIO(rsp.content), path=path)

    @bedrock_env_skipped
    def log_training_run_step_metrics(
        self,
        pipeline_id: str,
        run_id: int,
        step_name: str,
        metrics: Mapping[str, List[MetricPointSchema]],
    ) -> TrainingRunStepSchema:
        """Log training run step metrics

        Args:
            pipeline_id (str): pipeline id
            run_id (int): run id
            step_name (str): step name
            metrics (Mapping[str, List[MetricPointSchema]]): metrics to be logged

        Returns:
            TrainingRunStepSchema: the updated step with new metrics
        """
        response = self._pipeline_api.log_step_metrics(
            project_id=self._project_id,
            pipeline_id=pipeline_id,
            run_id=run_id,
            step_name=step_name,
            update_pipeline_run_metric_schema=UpdatePipelineRunMetricSchema(metrics=metrics),
        )
        _logger.debug(f"Metrics logged: {response}")
        return response
