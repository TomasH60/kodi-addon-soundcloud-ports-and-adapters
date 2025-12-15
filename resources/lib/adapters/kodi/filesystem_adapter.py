"""KODI file system adapter - implements IFileSystem using xbmcvfs."""
import os
import xbmcvfs
from resources.lib.ports.filesystem import IFileSystem


class KodiFileSystemAdapter(IFileSystem):
    """KODI implementation of file system adapter."""
    
    def __init__(self, root_path: str):
        self._root_path = root_path
        if not xbmcvfs.exists(self._root_path):
            xbmcvfs.mkdir(self._root_path)
    
    def read(self, filename: str):
        """Read a file and return its contents."""
        filepath = os.path.join(self._root_path, filename)
        if xbmcvfs.exists(filepath):
            with xbmcvfs.File(filepath) as file:
                return file.read()
        return None
    
    def write(self, filename: str, content: str):
        """Write content to a file."""
        filepath = os.path.join(self._root_path, filename)
        with xbmcvfs.File(filepath, "w") as file:
            return filepath if file.write(content) else None
    
    def delete(self, filename: str) -> bool:
        """Delete a file."""
        filepath = os.path.join(self._root_path, filename)
        return xbmcvfs.delete(filepath)
    
    def exists(self, path: str) -> bool:
        """Check if a file or directory exists."""
        return xbmcvfs.exists(path)
    
    def get_mtime(self, filename: str) -> int:
        """Get the last modification time of a file."""
        filepath = os.path.join(self._root_path, filename)
        stat = xbmcvfs.Stat(filepath)
        return stat.st_mtime()
    
    def destroy(self) -> None:
        """Delete the entire file system root and all contents."""
        self._remove_dir(self._root_path)
    
    def _remove_dir(self, path: str) -> None:
        """Recursively remove a directory."""
        dir_list, file_list = xbmcvfs.listdir(path)
        
        for file in file_list:
            xbmcvfs.delete(os.path.join(path, file))
        
        for directory in dir_list:
            self._remove_dir(os.path.join(path, directory))
        
        xbmcvfs.rmdir(path)

