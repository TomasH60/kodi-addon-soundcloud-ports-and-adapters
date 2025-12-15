"""Settings port - abstracts settings operations."""
from abc import ABC, abstractmethod


class ISettings(ABC):
    """Interface for settings operations."""
    
    @abstractmethod
    def get(self, setting_id: str) -> str:
        """Get a setting value by ID."""
        pass
    
    @abstractmethod
    def set(self, setting_id: str, value: str) -> None:
        """Set a setting value."""
        pass

