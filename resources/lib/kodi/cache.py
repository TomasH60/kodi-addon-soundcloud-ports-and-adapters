"""Cache wrapper - kept for backward compatibility, but should use ICache port."""
from resources.lib.ports.cache import ICache


class Cache(ICache):
    """Cache wrapper that implements ICache port."""
    
    def __init__(self, cache: ICache):
        """Initialize with an ICache implementation."""
        self._cache = cache

    def get(self, filename: str, age: int = 60):
        """
        Get a cached file.
        :param filename: Cache key
        :param age: Maximum age in minutes
        :return: Cached content or None if not found/expired
        """
        return self._cache.get(filename, age)

    def add(self, filename: str, data: str):
        """
        Add data to cache.
        :param filename: Cache key
        :param data: Data to cache
        :return: Filepath on success, None on failure
        """
        return self._cache.add(filename, data)
