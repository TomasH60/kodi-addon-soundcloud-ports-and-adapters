from resources.lib.models.list_item import ListItem


class User(ListItem):
    """Domain model for a user."""
    thumb = ""
    info = {}
    
    def get_description(self, followers_label: str) -> str:
        """Get the description text for the user."""
        return "{}\n{} {}\n\n{}".format(
            self.label2 if self.label2 != "" else self.label,
            self.info.get("followers"),
            followers_label,
            self.info.get("description") or ""
        )
