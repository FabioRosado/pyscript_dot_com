import pytest

from tests.simple_server import start_server, stop_server


@pytest.fixture(scope="session")
def running_server():
    server_info = start_server()
    yield server_info
    stop_server(server_info)
