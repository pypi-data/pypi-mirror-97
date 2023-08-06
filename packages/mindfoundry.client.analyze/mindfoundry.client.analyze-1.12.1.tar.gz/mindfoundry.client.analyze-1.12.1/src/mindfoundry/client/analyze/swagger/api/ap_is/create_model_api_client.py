from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.create_deployed_api_client_request import CreateDeployedApiClientRequest
from ...models.deployed_api_client_create_response import (
    DeployedApiClientCreateResponse,
)
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    model_api_id: int,
    json_body: CreateDeployedApiClientRequest,

) -> Dict[str, Any]:
    url = "{}/v1/modelApis/{modelApiId}/clients".format(
        client.base_url,modelApiId=model_api_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    json_json_body = json_body.to_dict()



    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[
    DeployedApiClientCreateResponse,
    None,
    None
]]:
    if response.status_code == 201:
        response_201 = DeployedApiClientCreateResponse.from_dict(response.json())



        return response_201
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[
    DeployedApiClientCreateResponse,
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
    model_api_id: int,
    json_body: CreateDeployedApiClientRequest,

) -> Response[Union[
    DeployedApiClientCreateResponse,
    None,
    None
]]:
    kwargs = _get_kwargs(
        client=client,
model_api_id=model_api_id,
json_body=json_body,

    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    *,
    client: Client,
    model_api_id: int,
    json_body: CreateDeployedApiClientRequest,

) -> Optional[Union[
    DeployedApiClientCreateResponse,
    None,
    None
]]:
    """ Create a new client to access and use a given published model api and returns its new credentials (client id and secret) """

    return sync_detailed(
        client=client,
model_api_id=model_api_id,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    model_api_id: int,
    json_body: CreateDeployedApiClientRequest,

) -> Response[Union[
    DeployedApiClientCreateResponse,
    None,
    None
]]:
    kwargs = _get_kwargs(
        client=client,
model_api_id=model_api_id,
json_body=json_body,

    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    *,
    client: Client,
    model_api_id: int,
    json_body: CreateDeployedApiClientRequest,

) -> Optional[Union[
    DeployedApiClientCreateResponse,
    None,
    None
]]:
    """ Create a new client to access and use a given published model api and returns its new credentials (client id and secret) """

    return (await asyncio_detailed(
        client=client,
model_api_id=model_api_id,
json_body=json_body,

    )).parsed
