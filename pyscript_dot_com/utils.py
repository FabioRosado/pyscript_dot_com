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


def get_project_slug_and_user_from_url() -> tuple[str, str]:
    """Return the project slug and user from the URL."""
    url = get_page_url()

    # URL should be in the format of:
    # https://<user>.pyscriptapps.com/<project_slug>/version/<version>
    parts = url.split("https://")[1].split(".pyscriptapps.com/")
    user = parts[0]
    project_slug = parts[1].split("/")[0]

    return project_slug, user