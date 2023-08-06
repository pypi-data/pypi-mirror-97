from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.create_test_request import CreateTestRequest
from ...models.test_response import TestResponse
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: CreateTestRequest,

) -> Dict[str, Any]:
    url = "{}/v1/tests".format(
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
    TestResponse,
    None,
    None
]]:
    if response.status_code == 201:
        response_201 = TestResponse.from_dict(response.json())



        return response_201
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[
    TestResponse,
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
    json_body: CreateTestRequest,

) -> Response[Union[
    TestResponse,
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
    json_body: CreateTestRequest,

) -> Optional[Union[
    TestResponse,
    None,
    None
]]:
    """ Create a new test using the model identified by the modelId and the data set identified by the dataSetId """

    return sync_detailed(
        client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    json_body: CreateTestRequest,

) -> Response[Union[
    TestResponse,
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
    json_body: CreateTestRequest,

) -> Optional[Union[
    TestResponse,
    None,
    None
]]:
    """ Create a new test using the model identified by the modelId and the data set identified by the dataSetId """

    return (await asyncio_detailed(
        client=client,
json_body=json_body,

    )).parsed
