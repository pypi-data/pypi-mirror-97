from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.deployed_model_api_response import DeployedModelApiResponse
from ...models.edit_deployed_model_api_request import EditDeployedModelApiRequest
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    model_api_id: int,
    json_body: EditDeployedModelApiRequest,

) -> Dict[str, Any]:
    url = "{}/v1/modelApis/{modelApiId}".format(
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
    DeployedModelApiResponse,
    None,
    None,
    None
]]:
    if response.status_code == 200:
        response_200 = DeployedModelApiResponse.from_dict(response.json())



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
    DeployedModelApiResponse,
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
    model_api_id: int,
    json_body: EditDeployedModelApiRequest,

) -> Response[Union[
    DeployedModelApiResponse,
    None,
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
    json_body: EditDeployedModelApiRequest,

) -> Optional[Union[
    DeployedModelApiResponse,
    None,
    None,
    None
]]:
    """ Edits the specified published model """

    return sync_detailed(
        client=client,
model_api_id=model_api_id,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    model_api_id: int,
    json_body: EditDeployedModelApiRequest,

) -> Response[Union[
    DeployedModelApiResponse,
    None,
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
    json_body: EditDeployedModelApiRequest,

) -> Optional[Union[
    DeployedModelApiResponse,
    None,
    None,
    None
]]:
    """ Edits the specified published model """

    return (await asyncio_detailed(
        client=client,
model_api_id=model_api_id,
json_body=json_body,

    )).parsed
