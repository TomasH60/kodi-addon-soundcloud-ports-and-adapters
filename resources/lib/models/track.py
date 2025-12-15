from resources.lib.models.list_item import ListItem


class Track(ListItem):
    """Domain model for a track."""
    blocked = False
    preview = False
    thumb = ""
    media = ""
    info = {}
