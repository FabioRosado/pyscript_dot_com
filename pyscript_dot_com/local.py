import json
from typing import Any

from pyscript import window

from pyscript_dot_com.base import BaseDataStore


class Datastore(BaseDataStore):
    def __init__(self):
        self.storage = window.localStorage

    def get(self, key: str):
        """Get a value from datastore."""
        item = self.storage.getItem(key)
        if item:
            try:
                return json.loads(item)
            except json.JSONDecodeError:
                return item

    def set(self, key: str, value: Any):
        """Set a value in datastore."""
        if isinstance(value, dict):
            value = json.dumps(value)
        elif isinstance(value, set):
            value = json.dumps(list(value))
        self.storage.setItem(key, value)

    def delete(self, key: str):
        """Delete a value from datastore."""
        self.storage.removeItem(key)

    def items(self):
        """Get all items in datastore."""
        items = []
        for key in self.keys():
            items.append((key, self.get(key)))

        return items

    def values(self):
        """Get all values in datastore."""
        values = self.storage.object_values()
        if values:
            return values.split(",")
        return []

    def keys(self):
        """Get all keys in datastore."""
        keys = self.storage.object_keys()
        if keys:
            return keys.split(",")
        return []

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
            self.storage.removeItem(key)
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
