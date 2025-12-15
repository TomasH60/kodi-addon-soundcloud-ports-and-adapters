from resources.lib.models.list_item import ListItem


class Playlist(ListItem):
    """Domain model for a playlist."""
    thumb = ""
    info = {}
    is_album = False
    
    def get_description(self, likes_label: str) -> str:
        """Get the description text for the playlist."""
        return "{}\n{} {}\n\n{}".format(
            self.info.get("artist"),
            self.info.get("likes"),
            likes_label,
            self.info.get("description") or ""
        )
