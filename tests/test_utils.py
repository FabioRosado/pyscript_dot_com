from pyscript_dot_com.utils import get_page_cookies


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
