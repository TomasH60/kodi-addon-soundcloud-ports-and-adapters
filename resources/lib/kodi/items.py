from resources.lib.kodi.utils import format_bold
from resources.routes import *
from resources.lib.ports.platform import IPlatformAdapter
from resources.lib.ports.list_item_factory import IListItemFactory
from resources.lib.domain.model_mapper import ModelMapper
from resources.lib.kodi.search_history import SearchHistory

import urllib.parse


class Items:
    def __init__(self, platform: IPlatformAdapter, factory: IListItemFactory, 
                 mapper: ModelMapper, search_history: SearchHistory):
        self._platform = platform
        self._factory = factory
        self._mapper = mapper
        self.search_history = search_history
        self._addon_base = platform.get_addon_base_url()

    def root(self):
        items = []

        # Search
        list_item = self._factory.create_list_item(
            label=self._platform.get_localized_string(30101)
        )
        url = self._addon_base + PATH_SEARCH
        items.append((url, list_item, True))

        # Charts
        list_item = self._factory.create_list_item(
            label=self._platform.get_localized_string(30102)
        )
        url = self._addon_base + PATH_CHARTS
        items.append((url, list_item, True))

        # Discover
        list_item = self._factory.create_list_item(
            label=self._platform.get_localized_string(30103)
        )
        url = self._addon_base + PATH_DISCOVER
        items.append((url, list_item, True))

        # Settings
        list_item = self._factory.create_list_item(
            label=self._platform.get_localized_string(30108)
        )
        url = self._addon_base + "/?action=settings"
        items.append((url, list_item, False))

        # Sign in TODO
        # list_item = self._factory.create_list_item(
        #     label=self._platform.get_localized_string(30109)
        # )
        # url = self._addon_base + "/action=signin"
        # items.append((url, list_item, False))

        return items

    def search(self):
        items = []

        # New search
        list_item = self._factory.create_list_item(
            label=format_bold(self._platform.get_localized_string(30201))
        )
        url = self._addon_base + PATH_SEARCH + "?action=new"
        items.append((url, list_item, True))

        # Search history
        history = self.search_history.get()
        for k in sorted(list(history), reverse=True):
            query = history[k].get("query")
            list_item = self._factory.create_list_item(label=query)
            # Note: Context menu items would need to be added via factory if needed
            # For now, we'll skip this as it's a platform-specific feature
            url = self._addon_base + PATH_SEARCH + "?" + urllib.parse.urlencode({
                "query": history[k].get("query")
            })
            items.append((url, list_item, True))

        return items

    def search_sub(self, query):
        items = []

        # People
        list_item = self._factory.create_list_item(
            label=format_bold(self._platform.get_localized_string(30211))
        )
        url = self._addon_base + PATH_SEARCH + "?" + urllib.parse.urlencode({
            "action": "people",
            "query": query
        })
        items.append((url, list_item, True))

        # Albums
        list_item = self._factory.create_list_item(
            label=format_bold(self._platform.get_localized_string(30212))
        )
        url = self._addon_base + PATH_SEARCH + "?" + urllib.parse.urlencode({
            "action": "albums",
            "query": query
        })
        items.append((url, list_item, True))

        # Playlists
        list_item = self._factory.create_list_item(
            label=format_bold(self._platform.get_localized_string(30213))
        )
        url = self._addon_base + PATH_SEARCH + "?" + urllib.parse.urlencode({
            "action": "playlists",
            "query": query
        })
        items.append((url, list_item, True))

        return items

    def user(self, id):
        items = []

        # Albums
        list_item = self._factory.create_list_item(
            label=format_bold(self._platform.get_localized_string(30212))
        )
        url = self._addon_base + "/?" + urllib.parse.urlencode({
            "action": "call",
            "call": f"/users/{id}/albums"
        })
        items.append((url, list_item, True))

        # Playlists
        list_item = self._factory.create_list_item(
            label=format_bold(self._platform.get_localized_string(30213))
        )
        url = self._addon_base + "/?" + urllib.parse.urlencode({
            "action": "call",
            "call": f"/users/{id}/playlists_without_albums"
        })
        items.append((url, list_item, True))

        # Spotlight
        list_item = self._factory.create_list_item(
            label=format_bold(self._platform.get_localized_string(30214))
        )
        url = self._addon_base + "/?" + urllib.parse.urlencode({
            "action": "call",
            "call": f"/users/{id}/spotlight"
        })
        items.append((url, list_item, True))

        return items

    def charts(self):
        items = []

        # Top 50
        # TODO Not working anymore, replace with new GraphQL API
        # list_item = self._factory.create_list_item(
        #     label=format_bold(self._platform.get_localized_string(30301))
        # )
        # url = self._addon_base + PATH_CHARTS + "?" + urllib.parse.urlencode({
        #     "action": "top"
        # })
        # items.append((url, list_item, True))

        # Trending
        list_item = self._factory.create_list_item(
            label=format_bold(self._platform.get_localized_string(30302))
        )
        url = self._addon_base + PATH_CHARTS + "?" + urllib.parse.urlencode({
            "action": "trending"
        })
        items.append((url, list_item, True))

        return items

    def from_collection(self, collection):
        items = []

        for item in collection.items:
            items.append(self._mapper.to_list_item(item))

        if collection.next_href:
            next_item = self._factory.create_list_item(
                label=self._platform.get_localized_string(30901)
            )
            url = self._addon_base + "/?" + urllib.parse.urlencode({
                "action": "call",
                "call": collection.next_href
            })
            items.append((url, next_item, True))

        return items
