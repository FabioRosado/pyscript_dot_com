from typing import Optional
from urllib.parse import urlparse

from pyscript_dot_com.requests import request
from pyscript_dot_com.utils import get_page_url


def proxy(name, method: str = "GET", account: Optional[str] = None):
    """Call a PyScript.com proxy by name.

    By default the look up for the proxy name is from the account of the
    app using this function. If you wish to use a proxy from a different
    account, you can use the `account` parameter instead.

    """
    if account:
        # TODO: Probably should grab the url from the page?
        proxy_url = f"https://{account}.pyscriptapps.com/my/api-proxies/{name}"
    else:
        # TODO: For the love of everything, please
        # refactor this dumpster fire!
        page_url = get_page_url()

        # TODO: We need to support micropython here
        parsed_url = urlparse(page_url)

        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        proxy_url = f"{base_url}/my/api-proxies/{name}"

    response = request(proxy_url, method=method)

    return response
