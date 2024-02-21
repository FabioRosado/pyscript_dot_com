"""We dont do anything here - this is just to make tests work."""


class document:
    """Mocked document class."""

    URL = "http://localhost:5000"


# Very basic way to mock pyodide ffi
class object_keys:
    def __init__(self, storage):
        self.storage = storage

    def to_py(self):
        return list(self.storage.keys())


class object_values:
    def __init__(self, storage):
        self.storage = storage

    def to_py(self):
        return list(self.storage.values())


class object_entries(object_keys):
    def __init__(self, storage):
        self.storage = storage

    def to_py(self):
        return list(self.storage.items())


class localStorage:
    """Mocked localStorage class."""

    storage = {}

    def setItem(self, key, value):
        """Set item in local storage."""
        self.storage[key] = value

    def getItem(self, key):
        """Get item from local storage."""
        return self.storage.get(key)

    def removeItem(self, key):
        """Remove item from local storage."""
        self.storage.pop(key, None)

    def clear(self):
        """Clear local storage."""
        self.storage = {}

    def object_keys(self):
        """Get keys from local storage."""
        return object_keys(self.storage)
        # return ",".join(self.storage.keys())

    def object_values(self):
        """Get values from local storage."""
        return object_values(self.storage)

    def object_entries(self):
        """Get items from local storage."""
        return object_entries(self.storage)


class window:
    """Mocked window class."""

    localStorage = localStorage()
    document = document
