from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.future import Future
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    future_id: str,

) -> Dict[str, Any]:
    url = "{}/v1/futures/{futureId}".format(
        client.base_url,futureId=future_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[
    Future,
    None
]]:
    if response.status_code == 200:
        response_200 = Future.from_dict(response.json())



        return response_200
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
    future_id: str,

) -> Response[Union[
    Future,
    None
]]:
    kwargs = _get_kwargs(
        client=client,
future_id=future_id,

    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    *,
    client: Client,
    future_id: str,

) -> Optional[Union[
    Future,
    None
]]:
    """  """

    return sync_detailed(
        client=client,
future_id=future_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    future_id: str,

) -> Response[Union[
    Future,
    None
]]:
    kwargs = _get_kwargs(
        client=client,
future_id=future_id,

    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    *,
    client: Client,
    future_id: str,

) -> Optional[Union[
    Future,
    None
]]:
    """  """

    return (await asyncio_detailed(
        client=client,
future_id=future_id,

    )).parsed
