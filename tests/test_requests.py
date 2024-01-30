from unittest import mock

# from pyscript_dot_com.requests import request
from pyscript_dot_com import request


def test_request_happy_path():

    with mock.patch("requests.request") as mocked_request:

        mocked_request.return_value.ok = True
        mocked_request.return_value.status = 200
        mocked_request.return_value.statusText = "OK"
        mocked_request.return_value.json = mock.MagicMock(return_value={"foo": "bar"})

        response = request("https://example.com")

        assert response == {"foo": "bar"}

        # Make sure that block_thread set to True still returns the response

        response = request("https://example.com", block_thread=True)
        assert response == {"foo": "bar"}


def test_request_headers():

    with mock.patch("requests.request") as mocked_request:

        mocked_request.return_value.ok = True
        mocked_request.return_value.status = 200
        mocked_request.return_value.statusText = "OK"
        mocked_request.return_value.json = mock.MagicMock(return_value={"foo": "bar"})

        response = request("https://example.com", headers={"X-Test": "test"})

        assert response == {"foo": "bar"}
        assert mocked_request.call_args.kwargs["headers"] == {"X-Test": "test"}
        assert mocked_request.call_args.kwargs["method"] == "GET"


def test_request_post_request():

    with mock.patch("requests.request") as mocked_request:

        mocked_request.return_value.ok = True
        mocked_request.return_value.status = 200
        mocked_request.return_value.statusText = "OK"
        mocked_request.return_value.json = mock.MagicMock(return_value={"foo": "bar"})

        response = request(
            "https://example.com", method="POST", body={"test": "testing"}
        )

        assert response == {"foo": "bar"}
        assert mocked_request.call_args.kwargs["json"] == {"test": "testing"}
        assert mocked_request.call_args.kwargs["method"] == "POST"


def test_request_post_request_with_cookies():

    with mock.patch("requests.request") as mocked_request:

        mocked_request.return_value.ok = True
        mocked_request.return_value.status = 200
        mocked_request.return_value.statusText = "OK"
        mocked_request.return_value.json = mock.MagicMock(return_value={"foo": "bar"})

        response = request(
            "https://example.com",
            method="POST",
            body={"test": "testing"},
            cookies={"cookie": "my-cookie"},
        )

        assert response == {"foo": "bar"}
        assert mocked_request.call_args.kwargs["json"] == {"test": "testing"}
        assert mocked_request.call_args.kwargs["method"] == "POST"
        assert mocked_request.call_args.kwargs["cookies"] == {"cookie": "my-cookie"}
