import io
from unittest import mock

import pytest

from pyscript_dot_com import storage


def test__get_project_by_slug(project):
    expected_project_id = "cd0350f0"
    project_id = storage._get_project_by_slug()

    assert project_id == expected_project_id


def test_save_file_to_project(project):
    file = io.BytesIO(b"test")
    name = "test.txt"

    response = storage.save_file_to_project(file, name)

    assert response == True


def test_save_file_to_project_no_name(project):
    file = io.BytesIO(b"test")
    file.name = "test.txt"

    response = storage.save_file_to_project(file)

    assert response == True


def test_save_file_to_project_error(project):
    with mock.patch("pyscript_dot_com.storage.request") as mocked_request, mock.patch(
        "pyscript_dot_com.storage._get_project_by_slug"
    ) as mocked_get_project_by_slug:
        mocked_get_project_by_slug.return_value = "cd0350f0"
        mocked_request.return_value = {
            "error": "Something went wrong"
        }  # This is a fake response

        file = io.BytesIO(b"test")
        file.name = "test.txt"

        with pytest.raises(Exception) as excinfo:
            storage.save_file_to_project(file)
        assert str(excinfo.value) == "Something went wrong"


def test_state_set_get_and_delete_browser(document, project):
    key = "test"
    value = "test_value"

    storage.state().set(key, value, use_browser_storage=True)
    response = storage.state().get(key, use_browser_storage=True)

    assert response == value

    storage.state().delete(key, use_browser_storage=True)
    response = storage.state().get(key, use_browser_storage=True)
    assert response == {}


def test_state_get_api(document, project):
    with pytest.raises(NotImplementedError):
        storage.state().get("key", use_browser_storage=False)


def test_state_get_invalid_key(document, project):
    with pytest.raises(ValueError):
        storage.state().get(1, use_browser_storage=False)


def test_state_set_api(document, project):
    with pytest.raises(NotImplementedError):
        storage.state().set("key", {}, use_browser_storage=False)


def test_state_delete_api(document, project):
    with pytest.raises(NotImplementedError):
        storage.state().delete("key", use_browser_storage=False)


def test_state_delete_invalid_key(document, project):
    with pytest.raises(ValueError):
        storage.state().delete(1, use_browser_storage=False)


def test_state_set_invalid_state(document, project):
    with pytest.raises(ValueError):
        storage.state().set(1, "key", use_browser_storage=False)


def test_state_set_invalid_key(document, project):
    with pytest.raises(ValueError):
        storage.state().set({}, 1, use_browser_storage=False)


def test_store_get_api(document, project):
    with pytest.raises(NotImplementedError):
        storage.store().get("key", use_browser_storage=False)


def test_store_set_get_and_delete_browser(document, project):
    key = "test"
    value = {"test": "test_value"}

    storage.state().set(key, value, use_browser_storage=True)
    response = storage.state().get(key, use_browser_storage=True)

    assert response == value

    storage.state().delete(key, use_browser_storage=True)
    response = storage.state().get(key, use_browser_storage=True)
    assert response == {}


def test_store_set_api(document, project):
    with pytest.raises(NotImplementedError):
        storage.store().set("", "key", use_browser_storage=False)


def test_store_set_invalid_payload(document, project):
    with pytest.raises(ValueError):
        storage.store().set(1, "key", use_browser_storage=False)


def test_store_set_invalid_key(document, project):
    with pytest.raises(ValueError):
        storage.store().set("", 1, use_browser_storage=False)


def test_store_delete_api(document, project):
    with pytest.raises(NotImplementedError):
        storage.store().delete("key", use_browser_storage=False)


def test_store_delete_invalid_key(document, project):
    with pytest.raises(ValueError):
        storage.store().delete(1, use_browser_storage=False)
