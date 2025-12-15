"""KODI cache adapter - implements ICache."""
import time
from resources.lib.ports.cache import ICache
from resources.lib.ports.filesystem import IFileSystem


class KodiCacheAdapter(ICache):
    """KODI implementation of cache adapter."""
    
    def __init__(self, settings, filesystem: IFileSystem):
        self._settings = settings
        self._filesystem = filesystem
    
    def get(self, filename: str, age: int = 60):
        """
        Get a cached file.
        :param filename: Cache key
        :param age: Maximum age in minutes
        :return: Cached content or None if not found/expired
        """
        file = self._filesystem.read(filename)
        
        if file:
            mtime = self._filesystem.get_mtime(filename)
            if (int(time.time()) - age * 60) > mtime:
                return None
        
        return file
    
    def add(self, filename: str, data: str):
        """
        Add data to cache.
        :param filename: Cache key
        :param data: Data to cache
        :return: Filepath on success, None on failure
        """
        return self._filesystem.write(filename, data)

