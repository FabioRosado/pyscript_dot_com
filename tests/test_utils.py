from pyscript_dot_com.utils import (
    get_base_url,
    get_page_cookies,
    get_page_url,
    get_project_slug_and_user_from_url,
)


def test_get_page_cookies_no_cookies(document):
    document.cookie = ""

    cookies = get_page_cookies()

    assert cookies == {}


def test_get_page_cookies_one_cookie(document):
    document.cookie = "name=value"

    cookies = get_page_cookies()

    assert cookies == {"name": "value"}


def test_get_page_cookies_two_cookies(document):
    document.cookie = "name1=value1; name2=value2"

    cookies = get_page_cookies()

    assert cookies == {"name1": "value1", "name2": "value2"}


def test_get_page_url(document):
    document.URL = "https://example.com"

    url = get_page_url()

    assert url == "https://example.com"


def test_get_project_slug_and_user_from_url(document):
    document.URL = "https://user.pyscriptapps.com/project_slug/version/1"

    project_slug, user = get_project_slug_and_user_from_url()

    assert project_slug == "project_slug"
    assert user == "user"


def test_get_base_url(document):
    document.URL = "https://user.pyscriptapps.com/project_slug/version/"

    base_url = get_base_url()

    assert base_url == "https://user.pyscriptapps.com/project_slug"

    document.URL = "https://user.pyscriptapps.com/project_slug/version/1"

    base_url = get_base_url()

    assert base_url == "https://user.pyscriptapps.com/project_slug"
