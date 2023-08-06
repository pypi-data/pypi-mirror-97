from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.create_deployed_model_api_request import CreateDeployedModelApiRequest
from ...models.future import Future
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: CreateDeployedModelApiRequest,

) -> Dict[str, Any]:
    url = "{}/v1/modelApis".format(
        client.base_url)

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
    Future,
    None,
    None,
    None
]]:
    if response.status_code == 201:
        response_201 = Future.from_dict(response.json())



        return response_201
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
    Future,
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
    json_body: CreateDeployedModelApiRequest,

) -> Response[Union[
    Future,
    None,
    None,
    None
]]:
    kwargs = _get_kwargs(
        client=client,
json_body=json_body,

    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    *,
    client: Client,
    json_body: CreateDeployedModelApiRequest,

) -> Optional[Union[
    Future,
    None,
    None,
    None
]]:
    """ Deploy a model API for the specified model. The response will contain a `futureId` which you can use with the `/futures` endpoint to check the progress of the deployment. Upon completion the future will give you information about the resulting deployment. """

    return sync_detailed(
        client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    json_body: CreateDeployedModelApiRequest,

) -> Response[Union[
    Future,
    None,
    None,
    None
]]:
    kwargs = _get_kwargs(
        client=client,
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
    json_body: CreateDeployedModelApiRequest,

) -> Optional[Union[
    Future,
    None,
    None,
    None
]]:
    """ Deploy a model API for the specified model. The response will contain a `futureId` which you can use with the `/futures` endpoint to check the progress of the deployment. Upon completion the future will give you information about the resulting deployment. """

    return (await asyncio_detailed(
        client=client,
json_body=json_body,

    )).parsed
