from unittest import mock

from pyscript_dot_com.requests import request


def test_request_happy_path(monkeypatch):

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
