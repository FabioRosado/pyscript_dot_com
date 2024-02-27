import contextlib
import json
from typing import Any

from pyscript import window

from pyscript_dot_com.base import BaseDataStore
from pyscript_dot_com.requests import request
from pyscript_dot_com.utils import get_base_url


class Datastore(BaseDataStore):
    def __init__(self):
        # This is used as a basic cache
        self._data = {}
        self.api_base = get_base_url()

    def get(self, key: str):
        """Get a value from datastore."""
        result = request(f"{self.api_base}/datastore/{key}")

        return self._handle_response(result, key)

    def set(self, key: str, value: Any):
        """Set a value in datastore."""
        if isinstance(value, dict):
            value = json.dumps(value)
        elif isinstance(value, set):
            value = json.dumps(list(value))
        else:
            # Should we always convert to string?
            value = str(value)

        result = request(
            f"{self.api_base}/datastore",
            method="POST",
            body={"key": key, "value": value},
        )
        return self._handle_response(result, key)

    def delete(self, key: str):
        """Delete a value from datastore."""
        request(f"{self.api_base}/datastore/{key}", method="DELETE")
        # We can't be sure that the key is in self._data so let's
        # just suppress the error
        with contextlib.suppress(KeyError):
            del self._data[key]

    def items(self):
        """Get all items in datastore."""
        # In this case we should always hit the DB and
        # return the latest data, plus updating `self._data`
        result = request(f"{self.api_base}/datastore")
        if self._is_api_error(result):
            return []
        self._data = result
        return list(self._data.items())

    def values(self):
        """Get all values in datastore."""
        # Call .items first to make sure we get everything
        # in the remote server
        self.items()
        return list(self._data.values())

    def keys(self):
        """Get all keys in datastore."""
        # Call .items first to make sure we get everything
        # in the remote server
        self.items()
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
        result = None
        if key in self:
            result = self[key]
            # Since we are already getting the key we can probably
            # just remove it from the db
            del self[key]
            return result
        else:
            # If the key is not in cache, get it!
            result = self.get(key)
            self.delete(key)

        if result is None and default is not None:
            return default

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
        """Return a shallow copy of the data store.

        This is a shallow copy, so the data is not duplicated
        in the remote server and will only be available in the
        local instance.

        """
        result = {}
        for key in self.keys():
            value = self[key]
            result[key] = value
        return result

    def paginate_items(self, count: int = 10):
        """Paginate items in datastore."""
        result = request(f"{self.api_base}/datastore", params={"count": count})
        if self._is_api_error(result):
            return []
        self._data = result
        return list(self._data.items())

    def _is_api_error(self, response):
        """Check if the response from the API is an error."""
        return not isinstance(response, dict) or response.get("error")

    def _handle_response(self, response, key):
        """Handle the response from the API.

        Helper function to remove duplication
        """
        if self._is_api_error(response):
            return None

        if self._is_api_error(response):
            return None

        _value = response.get(key)

        # _value may be a list such as "['one', 'two']" which
        # will cause it to fail. We will try to convert it
        try:
            value = json.loads(_value.strip('"').replace("'", '"'))
        except Exception:
            value = _value

        self._data[key] = value
        return value


datastore = Datastore()
