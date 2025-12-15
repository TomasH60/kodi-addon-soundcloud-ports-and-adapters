"""KODI platform adapter - implements IPlatformAdapter using XBMC."""
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
from resources.lib.ports.platform import IPlatformAdapter


class KodiPlatformAdapter(IPlatformAdapter):
    """KODI implementation of platform adapter."""
    
    def __init__(self):
        self._addon = xbmcaddon.Addon()
        self._addon_id = self._addon.getAddonInfo("id")
        self._addon_base = "plugin://" + self._addon_id
    
    def log(self, message: str, level: int) -> None:
        """Log a message at the specified level."""
        xbmc.log(message, level)
    
    def get_language(self, format: int) -> str:
        """Get the current language code."""
        return xbmc.getLanguage(format)
    
    def get_language_iso_639_1(self) -> str:
        """Get the current language code in ISO 639-1 format."""
        return xbmc.getLanguage(xbmc.ISO_639_1)
    
    def get_addon_id(self) -> str:
        """Get the addon ID."""
        return self._addon_id
    
    def get_addon_base_url(self) -> str:
        """Get the base URL for the addon."""
        return self._addon_base
    
    def get_addon_profile_path(self) -> str:
        """Get the addon profile directory path."""
        import xbmcvfs
        return xbmcvfs.translatePath(self._addon.getAddonInfo("profile"))
    
    def get_localized_string(self, string_id: int) -> str:
        """Get a localized string by ID."""
        return self._addon.getLocalizedString(string_id)
    
    def open_settings(self) -> None:
        """Open the addon settings dialog."""
        self._addon.openSettings()
    
    def set_content(self, handle: int, content_type: str) -> None:
        """Set the content type for the plugin directory."""
        xbmcplugin.setContent(handle, content_type)
    
    def add_directory_items(self, handle: int, items: list) -> None:
        """Add directory items to the plugin."""
        xbmcplugin.addDirectoryItems(handle, items, len(items))
    
    def end_of_directory(self, handle: int) -> None:
        """Signal that directory listing is complete."""
        xbmcplugin.endOfDirectory(handle)
    
    def set_resolved_url(self, handle: int, succeeded: bool, listitem) -> None:
        """Resolve a media URL."""
        xbmcplugin.setResolvedUrl(handle, succeeded, listitem)
    
    def execute_builtin(self, command: str) -> None:
        """Execute a KODI builtin command."""
        xbmc.executebuiltin(command)
    
    def create_playlist(self, playlist_type: int):
        """Create a playlist object."""
        return xbmc.PlayList(playlist_type)
    
    def create_music_playlist(self):
        """Create a music playlist object."""
        return xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
    
    def show_ok_dialog(self, heading: str, message: str) -> None:
        """Show an OK dialog."""
        dialog = xbmcgui.Dialog()
        dialog.ok(heading, message)
    
    def input_dialog(self, heading: str):
        """Show an input dialog and return the entered text."""
        dialog = xbmcgui.Dialog()
        return dialog.input(heading)

