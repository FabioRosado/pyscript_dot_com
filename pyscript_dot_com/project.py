import json
from typing import Any

from pyscript import window

from pyscript_dot_com.base import BaseDataStore
from pyscript_dot_com.const import PSDC_DOMAIN
from pyscript_dot_com.requests import request


class Datastore(BaseDataStore):
    def __init__(self):
        # This is used as a basic cache
        self._data = {}

    def get(self, key: str):
        """Get a value from datastore."""
        return self._data.get(key)

    def set(self, key: str, value: Any):
        """Set a value in datastore."""
        # if isinstance(value, dict):
        #     value = json.dumps(value)
        # elif isinstance(value, set):
        #     value = json.dumps(list(value))
        self._data[key] = value
        return value

    def delete(self, key: str):
        """Delete a value from datastore."""
        del self._data[key]

    def items(self):
        """Get all items in datastore."""
        # In this case we should always hit the DB and
        # return the latest data, plus updating `self._data`
        return list(self._data.items())

    def values(self):
        """Get all values in datastore."""
        # Here we should probably hit the DB so we always have the latest data?
        return list(self._data.values())

    def keys(self):
        """Get all keys in datastore."""
        # Here we should probably hit the DB so we always have the latest data?
        return list(self._data.keys())

    def contains(self, key: str):
        """Check if a key exists in the datastore."""
        return key in self.keys()

    def setdefault(self, key: str, default=None):
        """Implement setdefault method."""
        if key in self.keys():
            return self.get(key)
        self.set(key, default)
        return default

    def pop(self, key, default=None):
        """Pop the specified item from the data store."""
        if key in self:
            result = self[key]
            # Since we are already getting the key we can probably
            # just remove it from the db
            del self[key]
            return result
        raise KeyError(key)

    def update(self, *args, **kwargs):
        """For each key/value pair in the iterable."""
        new_items = {}
        for arg in args:
            if isinstance(arg, dict):
                new_items.update(arg)
        new_items.update(kwargs)
        for key, value in new_items.items():
            self[key] = value

    def copy(self):
        """Return a shallow copy of the data store."""
        result = {}
        for key in self.keys():
            value = self[key]
            result[key] = value
        return result


datastore = Datastore()
