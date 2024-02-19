import json
from typing import Union

from pyscript import window

from pyscript_dot_com.base import BaseDataStore


class Datastore(BaseDataStore):
    def get(self, key: str):
        """Get a value from datastore."""
        item = window.localStorage.getItem(key)
        if item:
            try:
                return json.loads(item)
            except json.JSONDecodeError:
                return item

    def set(self, key: str, value: Union[str, dict]):
        """Set a value in datastore."""
        # TODO: What to do with lists/sets/etc?
        if isinstance(value, dict):
            value = json.dumps(value)
        window.localStorage.setItem(key, value)

    def delete(self, key: str):
        """Delete a value from datastore."""
        window.localStorage.removeItem(key)

    def items(self):
        """Get all items in datastore."""
        # TODO: Maybe the key in broser storage should be pre-defined?
        raise NotImplementedError("This method is not yet implemented.")

    def setdefault(self, key: str, default=None):
        """Implement setdefault method."""
        # If key exists, return its value; otherwise, set the default value and return it
        raise NotImplementedError("This method is not yet implemented.")


datastore = Datastore()
