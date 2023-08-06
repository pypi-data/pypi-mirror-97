from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.delete_data_prep_steps_request import DeleteDataPrepStepsRequest
from ...models.future import Future
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    id: int,
    json_body: DeleteDataPrepStepsRequest,

) -> Dict[str, Any]:
    url = "{}/v1/dataSets/{id}/dataPrepSteps".format(
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
    Future,
    None,
    None,
    None
]]:
    if response.status_code == 200:
        response_200 = Future.from_dict(response.json())



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
    id: int,
    json_body: DeleteDataPrepStepsRequest,

) -> Response[Union[
    Future,
    None,
    None,
    None
]]:
    kwargs = _get_kwargs(
        client=client,
id=id,
json_body=json_body,

    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    *,
    client: Client,
    id: int,
    json_body: DeleteDataPrepStepsRequest,

) -> Optional[Union[
    Future,
    None,
    None,
    None
]]:
    """ Deletes the specified data prep steps from the dataset. This may take some time as later steps need to be reapplied so a future is returned. """

    return sync_detailed(
        client=client,
id=id,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    id: int,
    json_body: DeleteDataPrepStepsRequest,

) -> Response[Union[
    Future,
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
        response = await _client.delete(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    *,
    client: Client,
    id: int,
    json_body: DeleteDataPrepStepsRequest,

) -> Optional[Union[
    Future,
    None,
    None,
    None
]]:
    """ Deletes the specified data prep steps from the dataset. This may take some time as later steps need to be reapplied so a future is returned. """

    return (await asyncio_detailed(
        client=client,
id=id,
json_body=json_body,

    )).parsed
