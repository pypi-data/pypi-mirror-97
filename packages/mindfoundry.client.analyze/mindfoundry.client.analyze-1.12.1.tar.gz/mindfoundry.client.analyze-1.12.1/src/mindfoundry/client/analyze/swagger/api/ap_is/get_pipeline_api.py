from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.deployed_pipeline_api_response import DeployedPipelineApiResponse
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    pipeline_api_id: int,

) -> Dict[str, Any]:
    url = "{}/v1/pipelineApis/{pipelineApiId}".format(
        client.base_url,pipelineApiId=pipeline_api_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[
    DeployedPipelineApiResponse,
    None,
    None,
    None
]]:
    if response.status_code == 200:
        response_200 = DeployedPipelineApiResponse.from_dict(response.json())



        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 403:
        response_403 = None

        return response_403
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[
    DeployedPipelineApiResponse,
    None,
    None,
    None
]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    pipeline_api_id: int,

) -> Response[Union[
    DeployedPipelineApiResponse,
    None,
    None,
    None
]]:
    kwargs = _get_kwargs(
        client=client,
pipeline_api_id=pipeline_api_id,

    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    *,
    client: Client,
    pipeline_api_id: int,

) -> Optional[Union[
    DeployedPipelineApiResponse,
    None,
    None,
    None
]]:
    """ Gets general information about the published data prep pipeline api """

    return sync_detailed(
        client=client,
pipeline_api_id=pipeline_api_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    pipeline_api_id: int,

) -> Response[Union[
    DeployedPipelineApiResponse,
    None,
    None,
    None
]]:
    kwargs = _get_kwargs(
        client=client,
pipeline_api_id=pipeline_api_id,

    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    *,
    client: Client,
    pipeline_api_id: int,

) -> Optional[Union[
    DeployedPipelineApiResponse,
    None,
    None,
    None
]]:
    """ Gets general information about the published data prep pipeline api """

    return (await asyncio_detailed(
        client=client,
pipeline_api_id=pipeline_api_id,

    )).parsed
