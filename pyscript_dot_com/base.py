class BaseDataStore:
    def __init__(self, **kwargs):
        self._data = {}
        if kwargs:
            self.update(kwargs)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __delitem__(self, key):
        self.delete(key)

    def __iter__(self):
        return iter(self.items())

    def __len__(self):
        return len(self.keys())

    def __contains__(self, key):
        """Checks if a key is in the datastore."""
        return self.contains(key)

    def get(self, key):
        """Get a value from datastore."""
        # This is empty so we can override it in the subclasses
        ...

    def set(self, key, value):
        """Set a value in datastore."""
        # This is empty so we can override it in the subclasses
        ...

    def delete(self, key):
        """Delete a value from datastore."""
        # This is empty so we can override it in the subclasses
        ...

    def paginate_items(self, count: int = 10):
        """Paginate items in datastore."""
        # This is empty so we can override it in the subclasses
        ...

    def contains(self, key):
        """Check if a key exists in datastore."""
        # This is empty so we can override it in the subclasses
        ...

    def items(self):
        """Get all items in datastore."""
        ...

    def keys(self):
        """Get all keys in datastore."""
        ...

    def values(self):
        """Get all values in datastore."""
        ...

    def pop(self, key, default=None):
        """Pop a value from datastore."""
        # This is empty so we can override it in the subclasses
        ...

    def update(self, *args, **kwargs):
        """Update datastore with new values."""
        ...
