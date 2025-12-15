"""Platform adapter port - abstracts KODI platform operations."""
from abc import ABC, abstractmethod
from typing import Optional, Tuple, Any


class IPlatformAdapter(ABC):
    """Interface for platform-specific operations (KODI, testing, etc.)."""
    
    @abstractmethod
    def log(self, message: str, level: int) -> None:
        """Log a message at the specified level."""
        pass
    
    @abstractmethod
    def get_language_iso_639_1(self) -> str:
        """Get the current language code in ISO 639-1 format."""
        pass
    
    @abstractmethod
    def get_addon_id(self) -> str:
        """Get the addon ID."""
        pass
    
    @abstractmethod
    def get_addon_base_url(self) -> str:
        """Get the base URL for the addon (plugin://addon.id)."""
        pass
    
    @abstractmethod
    def get_addon_profile_path(self) -> str:
        """Get the addon profile directory path."""
        pass
    
    @abstractmethod
    def get_localized_string(self, string_id: int) -> str:
        """Get a localized string by ID."""
        pass
    
    @abstractmethod
    def open_settings(self) -> None:
        """Open the addon settings dialog."""
        pass
    
    @abstractmethod
    def set_content(self, handle: int, content_type: str) -> None:
        """Set the content type for the plugin directory."""
        pass
    
    @abstractmethod
    def add_directory_items(self, handle: int, items: list) -> None:
        """Add directory items to the plugin."""
        pass
    
    @abstractmethod
    def end_of_directory(self, handle: int) -> None:
        """Signal that directory listing is complete."""
        pass
    
    @abstractmethod
    def set_resolved_url(self, handle: int, succeeded: bool, listitem: Any) -> None:
        """Resolve a media URL."""
        pass
    
    @abstractmethod
    def execute_builtin(self, command: str) -> None:
        """Execute a KODI builtin command."""
        pass
    
    @abstractmethod
    def create_music_playlist(self) -> Any:
        """Create a music playlist object."""
        pass
    
    @abstractmethod
    def show_ok_dialog(self, heading: str, message: str) -> None:
        """Show an OK dialog."""
        pass
    
    @abstractmethod
    def input_dialog(self, heading: str) -> Optional[str]:
        """Show an input dialog and return the entered text."""
        pass

