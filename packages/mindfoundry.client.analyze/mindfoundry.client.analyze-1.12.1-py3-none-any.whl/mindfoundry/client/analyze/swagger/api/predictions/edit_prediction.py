from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.edit_prediction_request import EditPredictionRequest
from ...models.prediction_response import PredictionResponse
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    id: int,
    json_body: EditPredictionRequest,

) -> Dict[str, Any]:
    url = "{}/v1/predictions/{id}".format(
        client.base_url,id=id)

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
    PredictionResponse,
    None,
    None,
    None
]]:
    if response.status_code == 200:
        response_200 = PredictionResponse.from_dict(response.json())



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
    PredictionResponse,
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
    id: int,
    json_body: EditPredictionRequest,

) -> Response[Union[
    PredictionResponse,
    None,
    None,
    None
]]:
    kwargs = _get_kwargs(
        client=client,
id=id,
json_body=json_body,

    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    *,
    client: Client,
    id: int,
    json_body: EditPredictionRequest,

) -> Optional[Union[
    PredictionResponse,
    None,
    None,
    None
]]:
    """ Edit the name and description of the specified prediction """

    return sync_detailed(
        client=client,
id=id,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    id: int,
    json_body: EditPredictionRequest,

) -> Response[Union[
    PredictionResponse,
    None,
    None,
    None
]]:
    kwargs = _get_kwargs(
        client=client,
id=id,
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
    id: int,
    json_body: EditPredictionRequest,

) -> Optional[Union[
    PredictionResponse,
    None,
    None,
    None
]]:
    """ Edit the name and description of the specified prediction """

    return (await asyncio_detailed(
        client=client,
id=id,
json_body=json_body,

    )).parsed
