"""List item factory port - abstracts UI item creation."""
from abc import ABC, abstractmethod
from typing import Tuple, Any, Optional


class IListItemFactory(ABC):
    """Interface for creating platform-specific list items."""
    
    @abstractmethod
    def create_list_item(self, label: str, label2: Optional[str] = None) -> Any:
        """Create a list item with the given labels."""
        pass
    
    @abstractmethod
    def create_playable_item(self, url: str, label: str, thumb: Optional[str] = None, 
                            info: Optional[dict] = None, properties: Optional[dict] = None) -> Tuple[str, Any, bool]:
        """
        Create a playable list item.
        :return: Tuple of (url, listitem, is_folder)
        """
        pass
    
    @abstractmethod
    def create_folder_item(self, url: str, label: str, label2: Optional[str] = None,
                          thumb: Optional[str] = None, info: Optional[dict] = None) -> Tuple[str, Any, bool]:
        """
        Create a folder list item.
        :return: Tuple of (url, listitem, is_folder)
        """
        pass
    
    @abstractmethod
    def set_item_property(self, listitem: Any, property_name: str, value: str) -> None:
        """Set a property on a list item."""
        pass
    
    @abstractmethod
    def get_item_property(self, listitem: Any, property_name: str) -> str:
        """Get a property from a list item."""
        pass
    
    @abstractmethod
    def set_item_path(self, listitem: Any, path: str) -> None:
        """Set the path/URL of a list item."""
        pass

