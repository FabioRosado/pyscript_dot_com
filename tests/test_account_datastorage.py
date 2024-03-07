import pytest

from pyscript_dot_com import account


@pytest.fixture()
def cleanup():
    yield
    keys = account.datastore.keys()
    for key in keys:
        account.datastore.delete(key)


def test_account_setdefault(fake_account_api, cleanup):
    account.datastore.setdefault("test", "test_value")
    value = account.datastore.get("test")

    assert value == "test_value"

    account.datastore.delete("test")
    value = account.datastore.get("test")
    assert value is None


def test_account_set_get_delete(fake_account_api, cleanup):

    account.datastore.set("test", "test_value")
    value = account.datastore.get("test")

    assert value == "test_value"

    account.datastore.delete("test")
    value = account.datastore.get("test")
    assert value is None


def test_account_get_not_there(fake_account_api, cleanup):
    response = account.datastore.get("test")
    assert response == None


def test_account_delete(fake_account_api, cleanup):
    account.datastore.set("test", "test_value")
    value = account.datastore.get("test")

    assert value == "test_value"

    del account.datastore["test"]
    value = account.datastore.get("test")
    assert value == None


def test_account_items(fake_account_api, cleanup):
    account.datastore.set("test", "test_value")
    items = account.datastore.items()

    expected_value = [("test", "test_value")]
    assert items == expected_value


def test_account_paginate_items(fake_account_api, cleanup):
    account.datastore.set("test", "test_value")
    response = account.datastore.paginate_items()

    assert response == [("test", "test_value")]

    account.datastore.delete("test")
    response = account.datastore.paginate_items(count=0)
    assert response == []


def test_account_set_as_dict(fake_account_api, cleanup):
    account.datastore["test"] = "test_value"
    value = account.datastore.get("test")

    assert value == "test_value"

    account.datastore.delete("test")
    value = account.datastore.get("test")
    assert value is None


def test_account_update_as_dict(fake_account_api, cleanup):
    account.datastore["test"] = "test_value"
    account.datastore["test"] = "new_test_value"
    response = account.datastore.get("test")

    assert response == "new_test_value"

    account.datastore.delete("test")
    response = account.datastore.get("test")
    assert response == None


def test_account_contains(fake_account_api, cleanup):
    account.datastore.set("test", "test_value")
    key_exists = account.datastore.contains("test")

    assert key_exists == True

    account.datastore.delete("test")
    key_exists = "test" in account.datastore
    assert key_exists == False


def test_account_copy(fake_account_api, cleanup):
    account.datastore["test"] = "test_value"
    copied_dict = account.datastore.copy()
    assert copied_dict == {"test": "test_value"}


def test_account_pop(fake_account_api, cleanup):
    account.datastore.set("test", "test_value")
    poped_value = account.datastore.pop("test")

    assert poped_value == "test_value"

    value = account.datastore.pop("test")
    assert value is None


def test_account_values(fake_account_api, cleanup):
    account.datastore.set("test", "test_value")
    values = account.datastore.values()

    assert values == ["test_value"]

    account.datastore.delete("test")
    response = account.datastore.values()
    assert list(response) == []


def test_account_keys(fake_account_api, cleanup):
    account.datastore.set("test", "test_value")
    keys = account.datastore.keys()

    assert keys == ["test"]

    account.datastore.delete("test")
    keys = account.datastore.keys()
    assert keys == []


def test_account_length(fake_account_api, cleanup):
    account.datastore.set("test", "test_value")
    length = len(account.datastore)

    assert length == 1

    account.datastore.delete("test")
    length = len(account.datastore)
    assert length == 0


def test_account_iter(fake_account_api, cleanup):
    account.datastore.set("test", "test_value")
    account.datastore.set("test2", "test_value2")

    for key, value in account.datastore:
        assert key in ["test", "test2"]
        assert value in ["test_value", "test_value2"]

    response = list(iter(account.datastore))
    assert response == [("test", "test_value"), ("test2", "test_value2")]

    account.datastore.delete("test")
    account.datastore.delete("test2")
    response = list(iter(account.datastore))
    assert response == []
