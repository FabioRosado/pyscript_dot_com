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


class window:
    """Mocked window class."""

    localStorage = localStorage()
    document = document
