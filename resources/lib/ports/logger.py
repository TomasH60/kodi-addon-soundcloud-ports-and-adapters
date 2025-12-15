"""Logger port - abstracts logging operations."""
from abc import ABC, abstractmethod


class ILogger(ABC):
    """Interface for logging operations."""
    
    @abstractmethod
    def debug(self, message: str) -> None:
        """Log a debug message."""
        pass
    
    @abstractmethod
    def info(self, message: str) -> None:
        """Log an info message."""
        pass
    
    @abstractmethod
    def warning(self, message: str) -> None:
        """Log a warning message."""
        pass
    
    @abstractmethod
    def error(self, message: str) -> None:
        """Log an error message."""
        pass

