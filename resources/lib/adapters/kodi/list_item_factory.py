"""KODI list item factory - creates XBMC list items."""
import xbmcgui
from typing import Tuple, Optional, Any
from resources.lib.ports.list_item_factory import IListItemFactory


class KodiListItemFactory(IListItemFactory):
    """KODI implementation of list item factory."""
    
    def create_list_item(self, label: str, label2: Optional[str] = None) -> Any:
        """Create a list item with the given labels."""
        return xbmcgui.ListItem(label=label, label2=label2)
    
    def create_playable_item(self, url: str, label: str, thumb: Optional[str] = None,
                            info: Optional[dict] = None, properties: Optional[dict] = None) -> Tuple[str, Any, bool]:
        """Create a playable list item."""
        listitem = xbmcgui.ListItem(label=label)
        
        if thumb:
            listitem.setArt({"thumb": thumb})
        
        if info:
            listitem.setInfo("music", info)
        
        if properties:
            for key, value in properties.items():
                listitem.setProperty(key, value)
        
        listitem.setProperty("isPlayable", "true")
        
        return url, listitem, False
    
    def create_folder_item(self, url: str, label: str, label2: Optional[str] = None,
                          thumb: Optional[str] = None, info: Optional[dict] = None) -> Tuple[str, Any, bool]:
        """Create a folder list item."""
        listitem = xbmcgui.ListItem(label=label, label2=label2)
        
        if thumb:
            listitem.setArt({"thumb": thumb})
        
        if info:
            listitem.setInfo("video", info)
        
        listitem.setIsFolder(True)
        listitem.setProperty("isPlayable", "false")
        
        return url, listitem, True
    
    def set_item_property(self, listitem: Any, property_name: str, value: str) -> None:
        """Set a property on a list item."""
        listitem.setProperty(property_name, value)
    
    def get_item_property(self, listitem: Any, property_name: str) -> str:
        """Get a property from a list item."""
        return listitem.getProperty(property_name)
    
    def set_item_path(self, listitem: Any, path: str) -> None:
        """Set the path/URL of a list item."""
        listitem.setPath(path)

