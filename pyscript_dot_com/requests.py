from typing import Optional

import requests
import urllib3

# from pyodide.http import pyfetch

# TODO:
# - Support Micropython

# TODO: Confirm if we can use the same logic here
# async def async_request(
#     url: str,
#     method: str = "GET",
#     body: Optional[dict[str, str]] = None,
#     headers: Optional[dict[str, str]] = None,
#     cookies: Optional[dict[str, str]] = None,
#     **kwargs,
# ):
#     """Call underlying async request function and return result.

#     This function is meant to run in a synchronous context, so we will
#     make sure that it doesn't block the thread by running it in a threadsafe manner.

#     This means that calling this function will not block the main thread, which means
#     that you may get the result of the request after the rest of the synchronous code
#     has finished executing. If you want to wait for the result, set `block_thread` to
#     True.


#     Parameters:
#         url: str = URL to make request to
#         method: str = {"GET", "POST", "PUT", "DELETE"} from `JavaScript` global
#             fetch())
#         body: str = body to pass to the request.
#         headers: dict[str, str] = headers to be passed to the request.
#         cookies: Optional[dict[str, str]] = Cookies to be passed to the request.
#     Return:
#         response: dictionary response from the request.

#     """

#     if not kwargs:
#         kwargs = {}

#     kwargs["method"] = method

#     _headers = {
#         "User-Agent": "PyScript.com",
#         "Accept": "*/*",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Connection": "keep-alive",
#     }

#     if body and method not in ["GET", "HEAD"]:
#         _headers["Accept-Encoding"] = "application/json"
#         kwargs["body"] = body
#     if headers:
#         _headers.update(headers)
#     if cookies:
#         kwargs["cookies"] = cookies

#     result = pyfetch(url=url, headers=_headers, verify=True, **kwargs)

#     # Not going to raise an exception here otherwise
#     # we need to handle it in the callback and is a
#     # bit of a pain, let's just return a dict with the
#     # status code and status text so that we can handle
#     # bad responses in the logic that handles the request
#     if not result.ok:
#         return {
#             "error": True,
#             "status": result.status_code,
#             "statusText": result.reason,
#         }

#     try:
#         return await result.json()
#     except Exception:
#         return result.text


def request(
    url: str,
    method: str = "GET",
    body: Optional[dict[str, str]] = None,
    headers: Optional[dict[str, str]] = None,
    cookies: Optional[dict[str, str]] = None,
    **kwargs,
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

    # Disable InsecureRequestWarning from urllib3 - since the preview is running in
    # an iframe, we can't verify the SSL cert since it's running in a different domain
    # we then disable the warnings and explicitly pass `verify=True`
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    if not kwargs:
        kwargs = {}

    kwargs["method"] = method

    _headers = {
        "User-Agent": "PyScript.com",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    if body and method not in ["GET", "HEAD"]:
        _headers["Accept-Encoding"] = "application/json"
        kwargs["json"] = body
    if headers:
        _headers.update(headers)
    if cookies:
        kwargs["cookies"] = cookies

    result = requests.request(url=url, headers=_headers, verify=True, **kwargs)

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

    try:
        return result.json()
    except Exception:
        return result.text
