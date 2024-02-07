from unittest import mock

import pytest

from tests.simple_server import start_server, stop_server


@pytest.fixture(scope="session")
def running_server():
    server_info = start_server()
    yield server_info
    stop_server(server_info)


@pytest.fixture()
def url(document, running_server):
    document.URL = f"{running_server['address']}/project-slug/version/"
    yield document


@pytest.fixture()
def document():
    with mock.patch("pyscript_dot_com.utils.document") as mocked_document:

        mocked_document.URL = "https://user.pyscriptapps.com/project_slug/version/1"
        mocked_document.cookie = "session=1234"
        yield mocked_document


@pytest.fixture()
def project(document, running_server):
    with mock.patch(
        "pyscript_dot_com.storage.PSDC_DOMAIN", new=running_server["address"]
    ) as mocked_domain:
        yield mocked_domain
