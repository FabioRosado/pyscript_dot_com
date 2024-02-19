import pytest

from pyscript_dot_com import local


def test_local_setdefault():
    with pytest.raises(NotImplementedError):
        local.datastore.setdefault("test", "test_value")

    # response = local.datastore.get("test")

    # assert response == "test_value"

    # local.datastore.delete("test")
    # response = local.datastore.get("test")
    # assert response == None


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
    with pytest.raises(NotImplementedError):
        response = local.datastore.items()

        expected_value = {"test": "test_value"}
        assert response == expected_value.items()


def test_loal_set_dict():
    local.datastore.set("test", {"test": "test_value"})
    response = local.datastore.get("test")

    assert response == {"test": "test_value"}

    local.datastore.delete("test")
    response = local.datastore.get("test")
    assert response == None


def test_local_update_dict():
    local.datastore.set("test", {"test": "test_value"})
    local.datastore.set("test", {"test": "new_value"})
    response = local.datastore.get("test")

    assert response == {"test": "new_value"}

    local.datastore.delete("test")
    response = local.datastore.get("test")
    assert response == None
