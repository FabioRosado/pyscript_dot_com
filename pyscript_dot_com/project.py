from pyscript_dot_com.base import BaseDataStore
from pyscript_dot_com.requests import request


class Datastore(BaseDataStore):
    """Datastore class for projects."""

    def __init__(self):
        self._data = {}

    def get(self, key):
        """Get a value from datastore."""
        # This is empty so we can override it in the subclasses
        return self._data.get(key)

    def set(self, key, value):
        """Set a value in datastore."""
        # This is empty so we can override it in the subclasses
        self._data[key] = value

    def delete(self, key):
        """Delete a value from datastore."""
        # This is empty so we can override it in the subclasses
        del self._data[key]

    def items(self):
        """Get all items in datastore."""
        # This is empty so we can override it in the subclasses
        return self._data.items()

    def setdefault(self, key, default=None):
        """Implement setdefault method."""
        # If key exists, return its value; otherwise, set the default value and return it
        return self._data.setdefault(key, default)


datastore = Datastore()
