"""Mapper to convert domain models to platform-specific list items."""
import urllib.parse
from resources.lib.ports.list_item_factory import IListItemFactory
from resources.lib.models.track import Track
from resources.lib.models.user import User
from resources.lib.models.playlist import Playlist
from resources.lib.models.selection import Selection
from resources.lib.models.list_item import ListItem
from resources.routes import PATH_USER, PATH_DISCOVER


class ModelMapper:
    """Maps domain models to platform-specific list items."""
    
    def __init__(self, factory: IListItemFactory, addon_base: str, 
                 blocked_label: str, preview_label: str, 
                 followers_label: str, likes_label: str):
        self._factory = factory
        self._addon_base = addon_base
        self._blocked_label = blocked_label
        self._preview_label = preview_label
        self._followers_label = followers_label
        self._likes_label = likes_label
    
    def to_list_item(self, item: ListItem):
        """Convert a domain model to a platform-specific list item."""
        if isinstance(item, Track):
            return self._track_to_list_item(item)
        elif isinstance(item, User):
            return self._user_to_list_item(item)
        elif isinstance(item, Playlist):
            return self._playlist_to_list_item(item)
        elif isinstance(item, Selection):
            return self._selection_to_list_item(item)
        else:
            # Fallback for base ListItem
            url, listitem, is_folder = self._factory.create_folder_item(
                self._addon_base, item.label
            )
            return url, listitem, is_folder
    
    def _track_to_list_item(self, track: Track):
        """Convert a Track to a list item."""
        list_item_label = track.label
        if track.blocked:
            list_item_label = f"[{self._blocked_label}] {list_item_label}"
        if track.preview:
            list_item_label = f"[{self._preview_label}] {list_item_label}"
        
        url = self._addon_base + "/play/?" + urllib.parse.urlencode({
            "media_url": track.media
        })
        
        info = {
            "artist": track.info.get("artist"),
            "duration": track.info.get("duration"),
            "genre": track.info.get("genre"),
            "title": track.label,
            "playcount": track.info.get("playback_count"),
            "comment": track.info.get("description")
        }
        
        # Add year if date is available
        date = track.info.get("date")
        if date and len(date) >= 4:
            info["year"] = date[:4]
        
        properties = {
            "mediaUrl": track.media
        }
        
        return self._factory.create_playable_item(
            url, list_item_label, thumb=track.thumb, 
            info=info, properties=properties
        )
    
    def _user_to_list_item(self, user: User):
        """Convert a User to a list item."""
        url = self._addon_base + PATH_USER + "?" + urllib.parse.urlencode({
            "id": user.id,
            "call": f"/users/{user.id}/tracks"
        })
        
        info = {
            "plot": user.get_description(self._followers_label)
        }
        
        return self._factory.create_folder_item(
            url, user.label, label2=user.label2,
            thumb=user.thumb, info=info
        )
    
    def _playlist_to_list_item(self, playlist: Playlist):
        """Convert a Playlist to a list item."""
        url = self._addon_base + "/?" + urllib.parse.urlencode({
            "action": "call",
            "call": f"/playlists/{playlist.id}"
        })
        
        info = {
            "plot": playlist.get_description(self._likes_label)
        }
        
        return self._factory.create_folder_item(
            url, playlist.label, label2=playlist.label2,
            thumb=playlist.thumb, info=info
        )
    
    def _selection_to_list_item(self, selection: Selection):
        """Convert a Selection to a list item."""
        url = self._addon_base + PATH_DISCOVER + "?" + urllib.parse.urlencode({
            "selection": selection.id
        })
        
        info = {
            "title": selection.info.get("description")
        }
        
        url_item, listitem, _ = self._factory.create_folder_item(
            url, selection.label, label2=selection.label2
        )
        listitem.setInfo("music", info)
        
        return url_item, listitem, True

