import pytest

from pyscript_dot_com import project


def test_project_setdefault():
    project.datastore.setdefault("test", "test_value")
    response = project.datastore.get("test")

    assert response == "test_value"

    project.datastore.delete("test")
    response = project.datastore.get("test")
    assert response == None


def test_project_set(project):
    project.datastore.set("test", "test_value")
    response = project.datastore.get("test")

    assert response == "test_value"

    project.datastore.delete("test")
    response = project.datastore.get("test")
    assert response == None


def test_project_get():
    project.datastore.set("test", "test_value")
    response = project.datastore.get("test")

    assert response == "test_value"

    project.datastore.delete("test")
    response = project.datastore.get("test")
    assert response == None


def test_project_delete():
    project.datastore.set("test", "test_value")
    response = project.datastore.get("test")

    assert response == "test_value"

    del project.datastore["test"]
    response = project.datastore.get("test")
    assert response == None


def test_project_items():
    project.datastore.set("test", "test_value")
    response = project.datastore.items()

    expected_value = {"test": "test_value"}
    assert response == expected_value.items()


@pytest.mark.xfail(
    reason="We expect this to fail until we implement the paginate_items method"
)
def test_project_paginate_items():
    project.datastore.set("test", "test_value")
    response = project.datastore.paginate_items()

    assert response == [("test", "test_value")]

    project.datastore.delete("test")
    response = project.datastore.paginate_items(count=0)
    assert response == []


def test_project_set_as_dict():
    project.datastore["test"] = "test_value"
    response = project.datastore.get("test")

    assert response == "test_value"

    project.datastore.delete("test")
    response = project.datastore.get("test")
    assert response == None


def test_project_update_as_dict():
    project.datastore["test"] = "test_value"
    project.datastore["test"] = "new_test_value"
    response = project.datastore.get("test")

    assert response == "new_test_value"

    project.datastore.delete("test")
    response = project.datastore.get("test")
    assert response == None


def test_project_iter():
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
