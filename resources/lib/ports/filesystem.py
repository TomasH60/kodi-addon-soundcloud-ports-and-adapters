"""File system port - abstracts file operations."""
from abc import ABC, abstractmethod
from typing import Optional, Any


class IFileSystem(ABC):
    """Interface for file system operations."""
    
    @abstractmethod
    def read(self, filename: str) -> Optional[str]:
        """Read a file and return its contents."""
        pass
    
    @abstractmethod
    def write(self, filename: str, content: str) -> Optional[str]:
        """Write content to a file. Returns filepath on success, None on failure."""
        pass
    
    @abstractmethod
    def delete(self, filename: str) -> bool:
        """Delete a file."""
        pass
    
    @abstractmethod
    def exists(self, path: str) -> bool:
        """Check if a file or directory exists."""
        pass
    
    @abstractmethod
    def get_mtime(self, filename: str) -> int:
        """Get the last modification time of a file (timestamp)."""
        pass
    
    @abstractmethod
    def destroy(self) -> None:
        """Delete the entire file system root and all contents."""
        pass

