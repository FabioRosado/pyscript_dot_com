from unittest import mock

import pytest

from tests.simple_server import start_server, stop_server


@pytest.fixture(scope="session")
def running_server():
    server_info = start_server()
    yield server_info
    stop_server(server_info)


@pytest.fixture()
def url(running_server):
    with mock.patch("pyscript_dot_com.utils.document") as mocked_document:
        mocked_document.URL = f"{running_server['address']}/project-slug/version/"

        yield mocked_document
