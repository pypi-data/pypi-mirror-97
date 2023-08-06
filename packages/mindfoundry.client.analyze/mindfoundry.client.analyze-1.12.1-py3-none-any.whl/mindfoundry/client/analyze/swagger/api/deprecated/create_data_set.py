from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.create_data_set_request import CreateDataSetRequest
from ...models.future import Future
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    multipart_data: CreateDataSetRequest,

) -> Dict[str, Any]:
    url = "{}/v1/dataSets".format(
        client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "files": multipart_data.to_dict(),
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
    multipart_data: CreateDataSetRequest,

) -> Response[Union[
    Future,
    None
]]:
    kwargs = _get_kwargs(
        client=client,
multipart_data=multipart_data,

    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    *,
    client: Client,
    multipart_data: CreateDataSetRequest,

) -> Optional[Union[
    Future,
    None
]]:
    """ Your data will start being imported immediately. The response will contain a `futureId` which you can use with the `/futures` endpoint to check the progress of your import. Upon completion the future will give you information about the resulting data set. """

    return sync_detailed(
        client=client,
multipart_data=multipart_data,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    multipart_data: CreateDataSetRequest,

) -> Response[Union[
    Future,
    None
]]:
    kwargs = _get_kwargs(
        client=client,
multipart_data=multipart_data,

    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    *,
    client: Client,
    multipart_data: CreateDataSetRequest,

) -> Optional[Union[
    Future,
    None
]]:
    """ Your data will start being imported immediately. The response will contain a `futureId` which you can use with the `/futures` endpoint to check the progress of your import. Upon completion the future will give you information about the resulting data set. """

    return (await asyncio_detailed(
        client=client,
multipart_data=multipart_data,

    )).parsed
