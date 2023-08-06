import io
from typing import IO
from zipfile import ZipFile

import requests
from bdrk.backend.v1 import ApiClient, ModelApi
from spanlib.common.exceptions import IOError


def download_stream(src: IO[bytes], dst: IO[bytes], buffer_size=8192) -> None:
    try:
        while True:
            buf = src.read(buffer_size)
            if not buf:
                break
            dst.write(buf)
    except Exception as e:
        raise IOError("Failed to copy stream to file") from e


def unzip_file_to_dir(src: IO[bytes], dir: str) -> None:
    try:
        with ZipFile(src) as zf:
            zf.extractall(path=dir)
    except Exception as e:
        raise IOError(f"Failed to unzip to {dir}") from e


def get_artefact_stream(api_client: ApiClient, model_id: str, artefact_id: str, project_id: str) -> IO[bytes]:
    """
    Get download stream of the given model artefact

    :param ApiClient api_client: API client instance
    :param str model_id: Model collection public ID
    :param str model_artefact_id: Model artefact or version ID, which is an UUID
    """
    try:
        model_api = ModelApi(api_client)
        download = model_api.get_artefact_download_url(
            model_id=model_id, artefact_id=artefact_id, project_id=project_id
        )
    except Exception as e:
        raise IOError(f"Failed to get download url for model_id={model_id}") from e

    try:
        url = download.url
        rsp = requests.get(url, stream=True)
        rsp.raise_for_status()
    except Exception as e:
        raise IOError(f"Failed to download from {url}") from e

    return io.BytesIO(rsp.content)


def download_and_unzip_artefact(
    api_client: ApiClient, model_id: str, artefact_id: str, project_id: str, output_dir: str
) -> None:
    """
    Download and unzip the model artefact of the given model collection

    :param ApiClient api_client: API client instance
    :param str model_id: Model collection public ID
    :param str model_artefact_id: Model artefact or version ID, which is an UUID
    :param str output_dir: Path that downloaded artefacts will be unzipped to
    """
    stream = get_artefact_stream(
        api_client=api_client, model_id=model_id, artefact_id=artefact_id, project_id=project_id
    )
    unzip_file_to_dir(src=stream, dir=output_dir)
