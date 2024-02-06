from pyscript import document


def get_page_url() -> str:
    """Return the URL of the current page."""
    return document.URL


def get_page_cookies() -> dict[str, str]:
    """Return the cookies from the browser."""
    document_cookies = document.cookie.split(";")
    cookies_dict = {}

    for cookie in document_cookies:
        if "=" in cookie:
            # We are assuming we will always have a cookie here
            name, value = cookie.split("=")
            cookies_dict[name.strip()] = value

    return cookies_dict
