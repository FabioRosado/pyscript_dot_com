import pytest

from pyscript_dot_com import project


@pytest.fixture()
def cleanup():
    yield
    keys = project.datastore.keys()
    for key in keys:
        project.datastore.delete(key)


def test_project_setdefault(fake_project_api, cleanup):
    project.datastore.setdefault("test", "test_value")
    value = project.datastore.get("test")

    assert value == "test_value"

    project.datastore.delete("test")
    value = project.datastore.get("test")
    assert value is None


def test_project_set_get_delete(fake_project_api, cleanup):

    project.datastore.set("test", "test_value")
    value = project.datastore.get("test")

    assert value == "test_value"

    project.datastore.delete("test")
    value = project.datastore.get("test")
    assert value is None


def test_project_get_not_there(fake_project_api, cleanup):
    response = project.datastore.get("test")
    assert response == None


def test_project_delete(fake_project_api, cleanup):
    project.datastore.set("test", "test_value")
    value = project.datastore.get("test")

    assert value == "test_value"

    del project.datastore["test"]
    value = project.datastore.get("test")
    assert value == None


def test_project_items(fake_project_api, cleanup):
    project.datastore.set("test", "test_value")
    items = project.datastore.items()

    expected_value = [("test", "test_value")]
    assert items == expected_value


def test_project_paginate_items(fake_project_api, cleanup):
    project.datastore.set("test", "test_value")
    response = project.datastore.paginate_items()

    assert response == [("test", "test_value")]

    project.datastore.delete("test")
    response = project.datastore.paginate_items(count=0)
    assert response == []


def test_project_set_as_dict(fake_project_api, cleanup):
    project.datastore["test"] = "test_value"
    value = project.datastore.get("test")

    assert value == "test_value"

    project.datastore.delete("test")
    value = project.datastore.get("test")
    assert value is None


def test_project_update_as_dict(fake_project_api, cleanup):
    project.datastore["test"] = "test_value"
    project.datastore["test"] = "new_test_value"
    response = project.datastore.get("test")

    assert response == "new_test_value"

    project.datastore.delete("test")
    response = project.datastore.get("test")
    assert response == None


def test_project_iter(fake_project_api, cleanup):
    project.datastore.set("test", "test_value")
    project.datastore.set("test2", "test_value2")

    for key, value in project.datastore:
        assert key in ["test", "test2"]
        assert value in ["test_value", "test_value2"]

    response = list(iter(project.datastore))
    assert response == [("test", "test_value"), ("test2", "test_value2")]

    project.datastore.delete("test")
    project.datastore.delete("test2")
    response = list(iter(project.datastore))
    assert response == []


def test_project_contains(fake_project_api, cleanup):
    project.datastore.set("test", "test_value")
    key_exists = project.datastore.contains("test")

    assert key_exists == True

    project.datastore.delete("test")
    key_exists = "test" in project.datastore
    assert key_exists == False


def test_project_copy(fake_project_api, cleanup):
    project.datastore["test"] = "test_value"
    copied_dict = project.datastore.copy()
    assert copied_dict == {"test": "test_value"}


def test_project_pop(fake_project_api, cleanup):
    project.datastore.set("test", "test_value")
    poped_value = project.datastore.pop("test")

    assert poped_value == "test_value"

    value = project.datastore.pop("test")
    assert value is None


def test_project_values(fake_project_api, cleanup):
    project.datastore.set("test", "test_value")
    values = project.datastore.values()

    assert values == ["test_value"]

    project.datastore.delete("test")
    response = project.datastore.values()
    assert list(response) == []


def test_project_keys(fake_project_api, cleanup):
    project.datastore.set("test", "test_value")
    keys = project.datastore.keys()

    assert keys == ["test"]

    project.datastore.delete("test")
    keys = project.datastore.keys()
    assert keys == []


def test_project_length(fake_project_api, cleanup):
    project.datastore.set("test", "test_value")
    length = len(project.datastore)

    assert length == 1

    project.datastore.delete("test")
    length = len(project.datastore)
    assert length == 0
