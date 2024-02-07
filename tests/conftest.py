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
def project():
    with mock.patch("pyscript_dot_com.storage.request") as mocked_request:
        expected_project_id = "cd0350f0"
        mocked_request.return_value = {
            "id": expected_project_id,
            "user_id": "7a3ff64c",
            "username": "",
            "type": "app",
            "name": "Broken Snow",
            "slug": "broken-snow",
            "description": "",
            "icon": "./pyscript-logo.png",
            "created_at": "2024-02-05T16:05:03.063892Z",
            "updated_at": "2024-02-05T16:05:03.063892Z",
            "latest": {},
            "default_version": "latest",
            "tags": [],
            "auth_required": False,
            "auth_users_allowed": [],
        }
        yield mocked_request
