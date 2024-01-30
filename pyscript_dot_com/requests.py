import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Optional

import requests


async def async_request(
    url: str,
    method: str = "GET",
    mode: str = "cors",
    body: Optional[str] = None,
    headers: Optional[dict[str, str]] = None,
    cookies: Optional[dict[str, str]] = None,
    include_cookies: bool = False,
    **fetch_kwargs: Any,
):
    """
    Async request function to make requests to the web.

    Parameters:
        url: str = URL to make request to
        method: str = {"GET", "POST", "PUT", "DELETE"} from `JavaScript` global fetch())
        body: str = body to pass to the request.
        headers: dict[str, str] = headers to be passed to the request.
        fetch_kwargs: Any = any other keyword arguments to pass to `pyfetch` (will be passed to `fetch`)
    Return:
        response: pyodide.http.FetchResponse = use with .status or await.json(), etc.

    """

    kwargs = {
        "method": method,
        "mode": mode,
    }
    if body and method not in ["GET", "HEAD"]:
        kwargs["data"] = json.dumps(body)
    if headers:
        kwargs["headers"] = json.dumps(headers)
    if include_cookies:
        kwargs["credentials"] = "include"
        kwargs["cookies"] = json.dumps(cookies)

    result = requests.request(url=url, **kwargs)

    return result.json()


def request(
    url: str,
    method: str = "GET",
    mode: str = "cors",
    body: Optional[str] = None,
    headers: Optional[dict[str, str]] = None,
    cookies: Optional[dict[str, str]] = None,
    block_thread: bool = False,
    **fetch_kwargs: Any,
):
    """Call underlying async request function and return result.

    This function is meant to run in a synchronous context, so we will
    make sure that it doesn't block the thread by running it in a threadsafe manner.

    This means that calling this function will not block the main thread, which means
    that you may get the result of the request after the rest of the synchronous code
    has finished executing. If you want to wait for the result, set `block_thread` to
    True.


    Parameters:
        url: str = URL to make request to
        method: str = {"GET", "POST", "PUT", "DELETE"} from `JavaScript` global
            fetch())
        body: str = body to pass to the request.
        headers: dict[str, str] = headers to be passed to the request.
        fetch_kwargs: Any = any other keyword arguments to pass to `pyfetch`
            (will be passed to `fetch`)
    Return:
        response: dictionary response from the request.

    """
    loop = asyncio.get_event_loop()

    if block_thread:
        response = loop.run_until_complete(
            async_request(
                url,
                method=method,
                mode=mode,
                body=body,
                headers=headers,
                cookies=cookies,
                **fetch_kwargs,
            )
        )
        return response

    # This makes sure that we don't block the thread, by using
    # futures and callbacks.
    future = asyncio.Future()
    async_task = asyncio.ensure_future(
        async_request(
            url,
            method=method,
            mode=mode,
            body=body,
            headers=headers,
            cookies=cookies,
            **fetch_kwargs,
        ),
        loop=loop,
    )
    async_task.add_done_callback(lambda f: future.set_result(f.result()))
    return_value = loop.run_until_complete(future)

    return return_value
