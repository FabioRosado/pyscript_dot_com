import pytest

from pyscript_dot_com import local


def test_local_setdefault():
    local.datastore.setdefault("test", "test_value")

    response = local.datastore.get("test")

    assert response == "test_value"

    local.datastore.delete("test")
    response = local.datastore.get("test")
    assert response == None


def test_local_set():
    local.datastore.set("test", "test_value")
    response = local.datastore.get("test")

    assert response == "test_value"

    local.datastore.delete("test")
    response = local.datastore.get("test")
    assert response == None


def test_local_get():
    local.datastore.set("test", "test_value")
    response = local.datastore.get("test")

    assert response == "test_value"

    local.datastore.delete("test")
    response = local.datastore.get("test")
    assert response == None


def test_local_get_not_there():
    response = local.datastore.get("test")
    assert response == None


def test_local_delete():
    local.datastore.set("test", "test_value")
    response = local.datastore.get("test")

    assert response == "test_value"

    del local.datastore["test"]
    response = local.datastore.get("test")
    assert response == None


def test_local_items():
    local.datastore.set("test", "test_value")
    items = local.datastore.items()
    assert items == [("test", "test_value")]


def test_loal_set_dict():
    local.datastore.set("test", {"test": "test_value"})
    response = local.datastore.get("test")

    assert response == {"test": "test_value"}

    local.datastore.delete("test")
    response = local.datastore.get("test")
    assert response == None


def test_local_set_set_value():
    local.datastore.set("test", {1, 2, 3})

    test = local.datastore.get("test")
    assert test == [1, 2, 3]


def test_local_update_dict():
    local.datastore.set("test", {"test": "test_value"})
    local.datastore.set("test", {"test": "new_value"})
    response = local.datastore.get("test")

    assert response == {"test": "new_value"}

    local.datastore.delete("test")
    response = local.datastore.get("test")
    assert response == None


def test_local_contains():
    local.datastore.set("test", "test_value")
    key_exists = local.datastore.contains("test")

    assert key_exists == True

    local.datastore.delete("test")
    key_exists = "test" in local.datastore
    assert key_exists == False


def test_local_copy():
    local.datastore["test"] = "test_value"
    copied_dict = local.datastore.copy()
    assert copied_dict == {"test": "test_value"}


def test_local_pop():
    local.datastore.set("test", "test_value")
    poped_value = local.datastore.pop("test")

    assert poped_value == "test_value"
    with pytest.raises(KeyError):
        local.datastore.pop("test")


def test_local_values():
    local.datastore.set("test", "test_value")
    values = local.datastore.values()

    assert values == ["test_value"]

    local.datastore.delete("test")
    response = local.datastore.values()
    assert list(response) == []


def test_local_keys():
    local.datastore.set("test", "test_value")
    keys = local.datastore.keys()

    assert keys == ["test"]

    local.datastore.delete("test")
    keys = local.datastore.keys()
    assert keys == []


def test_local_length():
    local.datastore.set("test", "test_value")
    length = len(local.datastore)

    assert length == 1

    local.datastore.delete("test")
    length = len(local.datastore)
    assert length == 0


def test_project_paginate_items(fake_project_api):
    local.datastore.set("test", "test_value")
    response = local.datastore.paginate_items()

    assert response == [("test", "test_value")]

    local.datastore.delete("test")
    response = local.datastore.paginate_items(count=0)
    assert response == []
