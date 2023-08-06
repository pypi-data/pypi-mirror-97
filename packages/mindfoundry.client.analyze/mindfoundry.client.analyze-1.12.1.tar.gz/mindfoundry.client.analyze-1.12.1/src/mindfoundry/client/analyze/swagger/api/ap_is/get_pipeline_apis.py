from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.deployed_pipeline_api_list_response import (
    DeployedPipelineApiListResponse,
)
from ...types import Response


def _get_kwargs(
    *,
    client: Client,

) -> Dict[str, Any]:
    url = "{}/v1/pipelineApis".format(
        client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[
    DeployedPipelineApiListResponse,
    None
]]:
    if response.status_code == 200:
        response_200 = DeployedPipelineApiListResponse.from_dict(response.json())



        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[
    DeployedPipelineApiListResponse,
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

) -> Response[Union[
    DeployedPipelineApiListResponse,
    None
]]:
    kwargs = _get_kwargs(
        client=client,

    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    *,
    client: Client,

) -> Optional[Union[
    DeployedPipelineApiListResponse,
    None
]]:
    """ Returns a list of all published data prep pipeline apis in the current project """

    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,

) -> Response[Union[
    DeployedPipelineApiListResponse,
    None
]]:
    kwargs = _get_kwargs(
        client=client,

    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    *,
    client: Client,

) -> Optional[Union[
    DeployedPipelineApiListResponse,
    None
]]:
    """ Returns a list of all published data prep pipeline apis in the current project """

    return (await asyncio_detailed(
        client=client,

    )).parsed
