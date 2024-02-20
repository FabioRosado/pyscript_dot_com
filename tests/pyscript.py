"""We dont do anything here - this is just to make tests work."""


class document:
    """Mocked document class."""

    URL = "http://localhost:5000"


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
        return ",".join(self.storage.keys())

    def object_values(self):
        """Get values from local storage."""
        return ",".join(self.storage.values())

    def object_items(self):
        """Get items from local storage."""
        items = []
        for key, value in self.storage.items():
            items.append(f"{key},{value}")

        return ",".join(items)


class window:
    """Mocked window class."""

    localStorage = localStorage()
    document = document
