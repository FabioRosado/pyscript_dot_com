class BaseDataStore:
    def __init__(self): ...

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __delitem__(self, key):
        self.delete(key)

    def __iter__(self):
        return iter(self._items())

    def __len__(self): ...

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

    def _items(self):
        """Get all items in datastore."""
        # This is empty so we can override it in the subclasses
        ...
