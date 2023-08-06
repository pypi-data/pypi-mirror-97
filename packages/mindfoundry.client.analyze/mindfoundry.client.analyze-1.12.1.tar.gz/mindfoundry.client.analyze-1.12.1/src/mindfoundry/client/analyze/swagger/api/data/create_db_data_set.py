from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.create_db_data_set_request import CreateDbDataSetRequest
from ...models.future import Future
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: CreateDbDataSetRequest,

) -> Dict[str, Any]:
    url = "{}/v1/dataSets/db".format(
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
    None
]]:
    if response.status_code == 201:
        response_201 = Future.from_dict(response.json())



        return response_201
    if response.status_code == 401:
        response_401 = None

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[
    Future,
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
    json_body: CreateDbDataSetRequest,

) -> Response[Union[
    Future,
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
    json_body: CreateDbDataSetRequest,

) -> Optional[Union[
    Future,
    None
]]:
    """ Your data will start being imported immediately. The response will contain a `futureId` which you can use with the `/futures` endpoint to check the progress of your import. Upon completion the future will give you information about the resulting data set. """

    return sync_detailed(
        client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    json_body: CreateDbDataSetRequest,

) -> Response[Union[
    Future,
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
    json_body: CreateDbDataSetRequest,

) -> Optional[Union[
    Future,
    None
]]:
    """ Your data will start being imported immediately. The response will contain a `futureId` which you can use with the `/futures` endpoint to check the progress of your import. Upon completion the future will give you information about the resulting data set. """

    return (await asyncio_detailed(
        client=client,
json_body=json_body,

    )).parsed
