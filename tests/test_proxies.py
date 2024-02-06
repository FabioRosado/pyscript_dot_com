from pyscript_dot_com import proxy


def test_proxy_happy_path(url):
    """Test that we can call a proxy.

    The test server already has an endpoint that uses the right path,
    we are simply checking if we get what we expect back from it.
    """

    assert proxy("test", "GET") == {
        "message": "You called the 'test' proxy with a 'GET' method!"
    }
