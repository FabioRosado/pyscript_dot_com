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

    def __len__(self): ...

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
        return self._data.items()

    def keys(self):
        """Get all keys in datastore."""
        return self._data.keys()

    def values(self):
        """Get all values in datastore."""
        return self._data.values()

    def pop(self, key, default=None):
        """Pop a value from datastore."""
        # This is empty so we can override it in the subclasses
        ...


class DataStore:
    """
    A simple key/value data store.

    Wraps a JavaScript `Storage` object for browser based data storage. Looks
    and feels mostly like a Python `dict` but has the same characteristics
    as a JavaScript `localStorage` object.

    For more information see:

    <https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API>
    """

    def __init__(self, **kwargs):
        """
        The underlying `Storage` object is an instance of `Window.localStorage`
        (it persists between browser opening/closing). Any `**kwargs` are added
        to the dictionary. All keys are silently prepended with the value of
        self.namespace.
        """
        self.namespace = "invent"
        self.store = window.localStorage
        if kwargs:
            self.update(kwargs)

    def clear(self):
        """
        Removes all items from the data store.
        """
        return self.store.clear()

    def copy(self):
        """
        Returns a Python `dict` copy of the data store.
        """
        return {k: v for k, v in self.items()}

    def get(self, key, default=None):
        """
        Return the value of the item with the specified key.
        """
        if key in self:
            return self[key]
        return default

    def items(self):
        """
        Yield over the key/value pairs in the data store.
        """
        for key in self.keys():
            value = self[key]
            yield (key, value)

    def keys(self):
        """
        Returns a list of keys stored by the user.
        """
        result = []
        namespace_slice = len(self.namespace)
        for i in range(0, self.store.length):
            key = self.store.key(i)
            if key.startswith(self.namespace):
                real_key = key[namespace_slice:]
                result.append(real_key)
        return result

    def pop(self, key, default=None):
        """
        Pop the specified item from the data store and return the associated
        value.
        """
        if key in self:
            result = self[key]
            del self[key]
        else:
            result = default
        return result

    def popitem(self):
        """
        Makes no sense given the underlying JavaScript Storage object's
        behaviour. Raises a `NotImplementedError`.
        """
        raise NotImplementedError()

    def setdefault(self, key, value=None):
        """
        Returns the value of the item with the specified key.

        If the key does not exist, insert the key, with the specified value.

        Default value is `None`.
        """
        if key in self:
            return self[key]
        self[key] = value
        return value

    def update(self, *args, **kwargs):
        """
        For each key/value pair in the iterable, insert them into the
        data store.
        """
        new_items = {}
        for arg in args:
            if isinstance(arg, dict):
                new_items.update(arg)
        new_items.update(kwargs)
        for key, value in new_items.items():
            self[key] = value

    def values(self):
        """
        Return a list of the values stored in the data store.
        """
        result = []
        for key in self.keys():
            result.append(self[key])
        return result

    def _namespace_key(self, key):
        """
        Convenience method to create a properly namespaced key.
        """
        return f"{self.namespace}{key}"

    def __len__(self):
        """
        The number of items in the data store.
        """
        return len(self.keys())

    def __getitem__(self, key):
        """
        Get and JSON deserialize the item stored against the given key.
        """
        if key in self:
            return json.loads(self.store.getItem(self._namespace_key(key)))
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        """
        Set the value (as a JSON string) against the given key.

        The underlying JavaScript Storage only stored values as strings.

        Publishes a message whose type is the item's key, along with the new
        value, to the "store-data" channel.
        """
        result = self.store.setItem(self._namespace_key(key), json.dumps(value))
        publish(
            Message(subject=key, value=value),
            to_channel="store-data",
        )
        return result

    def __delitem__(self, key):
        """
        Delete the item stored against the given key.

        Publishes a message whose type is the item's the key, to the
        "delete-data" channel.
        """
        if key in self:
            result = self.store.removeItem(self._namespace_key(key))
            publish(Message(subject=key), to_channel="delete-data")
            return result
        else:
            raise KeyError(key)

    def __iter__(self):
        """
        Return an iterator over the keys.
        """
        return (key for key in self.keys())

    def __contains__(self, key):
        """
        Checks if a key is in the datastore.
        """
        return key in self.keys()
