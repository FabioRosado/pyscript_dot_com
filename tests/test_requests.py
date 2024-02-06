from pyscript_dot_com import request


def test_get_request_bad_response(running_server):
    expected_response = {
        "error": True,
        "status": 500,
        "statusText": "Internal Server Error",
    }

    response = request(f"{running_server['address']}/exception")
    assert response == expected_response



def test_end_to_end_get_request(running_server):
    """Test that we can make a request to a running server."""
    expected_response = {"message": "Hello, this is the server response!"}
    response = request(f"{running_server['address']}/some_endpoint")

    # This is the default response from the server
    assert response == expected_response

def test_request_gets_cookies_correctly(running_server):
    """Test that the request function gets cookies correctly."""
    cookies = {"cookie": "my-cookie"}
    response = request(f"{running_server['address']}/test-cookies", cookies=cookies)

    # The server will return the passed in cookies on this path
    assert response == cookies



def test_request_gets_headers_correctly(running_server):
    """Test that the request function gets the headers correctly."""
    headers = {"X-Test": "test"}
    response = request(f"{running_server['address']}/test-headers", headers=headers)

    # The server returns the headers on this path
    assert response and response.get("X-Test") == "test"


def test_end_to_end_post_request(running_server):
    """Test that we can make a request to a running server."""

    data = {"test": "testing"}

    response = request(
        f"{running_server['address']}/some_endpoint",
        method="POST",
        body=data,
    )

    # This is the default response from the server
    assert response == data
