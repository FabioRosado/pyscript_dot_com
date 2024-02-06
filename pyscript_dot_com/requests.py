import asyncio
from typing import Optional

import requests

# TODO:
# - Support Micropython
# - Support sync/async


def request(
    url: str,
    method: str = "GET",
    body: Optional[dict[str, str]] = None,
    headers: Optional[dict[str, str]] = None,
    cookies: Optional[dict[str, str]] = None,
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
        cookies: Optional[dict[str, str]] = Cookies to be passed to the request.
    Return:
        response: dictionary response from the request.

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

    result = requests.request(url=url, verify=True, **kwargs)

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
