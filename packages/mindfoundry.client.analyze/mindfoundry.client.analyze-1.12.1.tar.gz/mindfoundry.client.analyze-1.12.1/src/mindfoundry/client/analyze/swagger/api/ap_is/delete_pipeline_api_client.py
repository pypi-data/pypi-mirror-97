from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    pipeline_api_id: int,
    client_id: str,

) -> Dict[str, Any]:
    url = "{}/v1/pipelineApis/{pipelineApiId}/clients/{clientId}".format(
        client.base_url,pipelineApiId=pipeline_api_id,clientId=client_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[
    None,
    None,
    None
]]:
    if response.status_code == 204:
        response_204 = None

        return response_204
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[
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
    client_id: str,

) -> Response[Union[
    None,
    None,
    None
]]:
    kwargs = _get_kwargs(
        client=client,
pipeline_api_id=pipeline_api_id,
client_id=client_id,

    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    *,
    client: Client,
    pipeline_api_id: int,
    client_id: str,

) -> Optional[Union[
    None,
    None,
    None
]]:
    """ Delete a data prep pipeline api client """

    return sync_detailed(
        client=client,
pipeline_api_id=pipeline_api_id,
client_id=client_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    pipeline_api_id: int,
    client_id: str,

) -> Response[Union[
    None,
    None,
    None
]]:
    kwargs = _get_kwargs(
        client=client,
pipeline_api_id=pipeline_api_id,
client_id=client_id,

    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    *,
    client: Client,
    pipeline_api_id: int,
    client_id: str,

) -> Optional[Union[
    None,
    None,
    None
]]:
    """ Delete a data prep pipeline api client """

    return (await asyncio_detailed(
        client=client,
pipeline_api_id=pipeline_api_id,
client_id=client_id,

    )).parsed
