import asyncio
from typing import Any, Optional

import requests


async def async_request(
    url: str,
    method: str = "GET",
    body: Optional[dict[str, str]] = None,
    headers: Optional[dict[str, str]] = None,
    cookies: Optional[dict[str, str]] = None,
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
    }
    if body and method not in ["GET", "HEAD"]:
        kwargs["json"] = body
    if headers:
        kwargs["headers"] = headers
    if cookies:
        kwargs["cookies"] = cookies

    result = requests.request(url=url, **kwargs)

    # Not going to raise an exception here otherwise
    # we need to handle it in the callback and is a
    # bit of a pain, let's just return a dict with the
    # status code and status text so that we can handle
    # bad responses in the logic that handles the request
    if not result.ok:
        return {
            "error": True,
            "status": result.status_code,
            "statusText": result.reason,
        }

    if result.headers.get("Content-Type") == "application/json":
        return result.json()

    return result.text


def request(
    url: str,
    method: str = "GET",
    body: Optional[dict[str, str]] = None,
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
                body=body,
                headers=headers,
                cookies=cookies,
                **fetch_kwargs,
            )
        )

    else:
        # This makes sure that we don't block the thread, by using
        # futures and callbacks.
        future = asyncio.Future()
        async_task = asyncio.ensure_future(
            async_request(
                url,
                method=method,
                body=body,
                headers=headers,
                cookies=cookies,
                **fetch_kwargs,
            ),
            loop=loop,
        )
        async_task.add_done_callback(lambda f: future.set_result(f.result()))
        response = loop.run_until_complete(future)

    return response
