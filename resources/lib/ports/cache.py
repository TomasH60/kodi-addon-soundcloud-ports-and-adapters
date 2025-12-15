"""Cache port - abstracts caching operations."""
from abc import ABC, abstractmethod
from typing import Optional


class ICache(ABC):
    """Interface for caching operations."""
    
    @abstractmethod
    def get(self, filename: str, age: int = 60) -> Optional[str]:
        """
        Get a cached file.
        :param filename: Cache key
        :param age: Maximum age in minutes
        :return: Cached content or None if not found/expired
        """
        pass
    
    @abstractmethod
    def add(self, filename: str, data: str) -> Optional[str]:
        """
        Add data to cache.
        :param filename: Cache key
        :param data: Data to cache
        :return: Filepath on success, None on failure
        """
        pass

