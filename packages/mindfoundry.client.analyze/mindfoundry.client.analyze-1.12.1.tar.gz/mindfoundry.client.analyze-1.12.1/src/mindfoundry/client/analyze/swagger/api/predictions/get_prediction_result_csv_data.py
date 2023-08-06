from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    id: int,
    separator: Union[Unset, str] = UNSET,
    quote_char: Union[Unset, str] = UNSET,
    escape_char: Union[Unset, str] = UNSET,

) -> Dict[str, Any]:
    url = "{}/v1/predictions/{id}/data/csv".format(
        client.base_url,id=id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    params: Dict[str, Any] = {
        "separator": separator,
        "quoteChar": quote_char,
        "escapeChar": escape_char,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[
    None,
    None,
    None,
    None
]]:
    if response.status_code == 200:
        response_200 = None

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
    None,
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
    separator: Union[Unset, str] = UNSET,
    quote_char: Union[Unset, str] = UNSET,
    escape_char: Union[Unset, str] = UNSET,

) -> Response[Union[
    None,
    None,
    None,
    None
]]:
    kwargs = _get_kwargs(
        client=client,
id=id,
separator=separator,
quote_char=quote_char,
escape_char=escape_char,

    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    *,
    client: Client,
    id: int,
    separator: Union[Unset, str] = UNSET,
    quote_char: Union[Unset, str] = UNSET,
    escape_char: Union[Unset, str] = UNSET,

) -> Optional[Union[
    None,
    None,
    None,
    None
]]:
    """ Get the prediction result as a csv file """

    return sync_detailed(
        client=client,
id=id,
separator=separator,
quote_char=quote_char,
escape_char=escape_char,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    id: int,
    separator: Union[Unset, str] = UNSET,
    quote_char: Union[Unset, str] = UNSET,
    escape_char: Union[Unset, str] = UNSET,

) -> Response[Union[
    None,
    None,
    None,
    None
]]:
    kwargs = _get_kwargs(
        client=client,
id=id,
separator=separator,
quote_char=quote_char,
escape_char=escape_char,

    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    *,
    client: Client,
    id: int,
    separator: Union[Unset, str] = UNSET,
    quote_char: Union[Unset, str] = UNSET,
    escape_char: Union[Unset, str] = UNSET,

) -> Optional[Union[
    None,
    None,
    None,
    None
]]:
    """ Get the prediction result as a csv file """

    return (await asyncio_detailed(
        client=client,
id=id,
separator=separator,
quote_char=quote_char,
escape_char=escape_char,

    )).parsed
