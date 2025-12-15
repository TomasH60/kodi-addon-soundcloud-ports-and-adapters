"""VFS wrapper - kept for backward compatibility, but should use IFileSystem port."""
import json
from resources.lib.ports.filesystem import IFileSystem


class VFS:
    """VFS wrapper that provides additional JSON helpers on top of IFileSystem."""
    
    def __init__(self, filesystem: IFileSystem):
        """Initialize with an IFileSystem implementation."""
        self._filesystem = filesystem

    def read(self, filename: str):
        """Read a file and return its contents."""
        return self._filesystem.read(filename)

    def write(self, filename: str, content: str):
        """Write content to a file."""
        return self._filesystem.write(filename, content)

    def delete(self, filename: str) -> bool:
        """Delete a file."""
        return self._filesystem.delete(filename)

    def destroy(self) -> None:
        """Delete the entire file system root and all contents."""
        self._filesystem.destroy()

    def get_mtime(self, filename: str) -> int:
        """Returns last modification time (timestamp)."""
        return self._filesystem.get_mtime(filename)

    def get_json_as_obj(self, filename: str, default=None):
        """Read a JSON file and return as object."""
        string = self.read(filename)
        if string:
            return json.loads(string)
        else:
            return default if default else {}

    def save_obj_to_json(self, filename: str, obj) -> bool:
        """Save an object as JSON file."""
        string = json.dumps(obj)
        result = self.write(filename, string)
        return result is not None
