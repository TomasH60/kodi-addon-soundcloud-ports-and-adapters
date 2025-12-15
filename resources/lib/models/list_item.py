class ListItem:
    """Base domain model for list items."""
    id = 0
    label = ""
    label2 = None

    def __init__(self, id, label):
        self.id = id
        self.label = label
