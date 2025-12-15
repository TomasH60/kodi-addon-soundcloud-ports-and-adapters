"""Main plugin entry point - composition root for ports-and-adapters architecture."""
import os
import sys
import urllib.parse

# Import adapters
from resources.lib.adapters.kodi.platform_adapter import KodiPlatformAdapter
from resources.lib.adapters.kodi.filesystem_adapter import KodiFileSystemAdapter
from resources.lib.adapters.kodi.cache_adapter import KodiCacheAdapter
from resources.lib.adapters.kodi.settings_adapter import KodiSettingsAdapter
from resources.lib.adapters.kodi.list_item_factory import KodiListItemFactory
from resources.lib.adapters.kodi.logger_adapter import KodiLoggerAdapter

# Import domain/use cases
from resources.lib.soundcloud.api_v2 import ApiV2
from resources.lib.kodi.items import Items
from resources.lib.kodi.search_history import SearchHistory
from resources.lib.domain.model_mapper import ModelMapper

# Import routes
from resources.routes import *

# Import XBMC only for plugin handle and args (minimal usage at composition root)
import xbmcplugin

# Initialize adapters (composition root)
platform = KodiPlatformAdapter()
logger = KodiLoggerAdapter(platform.get_addon_id())
settings_adapter = KodiSettingsAdapter()
vfs_adapter = KodiFileSystemAdapter(platform.get_addon_profile_path())
vfs_cache_adapter = KodiFileSystemAdapter(os.path.join(platform.get_addon_profile_path(), "cache"))
cache_adapter = KodiCacheAdapter(settings_adapter, vfs_cache_adapter)
factory = KodiListItemFactory()

# Wrap adapters for backward compatibility (if needed)
from resources.lib.kodi.settings import Settings
from resources.lib.kodi.vfs import VFS
from resources.lib.kodi.cache import Cache
settings = Settings(settings_adapter)
vfs = VFS(vfs_adapter)
vfs_cache = VFS(vfs_cache_adapter)
cache = Cache(cache_adapter)

# Initialize domain services
api = ApiV2(settings, platform.get_language_iso_639_1(), cache, logger)
search_history = SearchHistory(settings, vfs)

# Initialize mapper with localized strings
mapper = ModelMapper(
    factory=factory,
    addon_base=platform.get_addon_base_url(),
    blocked_label=platform.get_localized_string(30902),
    preview_label=platform.get_localized_string(30903),
    followers_label=platform.get_localized_string(30904),
    likes_label=platform.get_localized_string(30905)
)

# Initialize UI layer
listItems = Items(platform, factory, mapper, search_history)


def run():
    """Main plugin entry point."""
    url = urllib.parse.urlparse(sys.argv[0])
    path = url.path
    handle = int(sys.argv[1])
    args = urllib.parse.parse_qs(sys.argv[2][1:])
    platform.set_content(handle, "songs")

    if path == PATH_ROOT:
        action = args.get("action", None)
        if action is None:
            items = listItems.root()
            platform.add_directory_items(handle, items)
            platform.end_of_directory(handle)
        elif "call" in action:
            collection = listItems.from_collection(api.call(args.get("call")[0]))
            platform.add_directory_items(handle, collection)
            platform.end_of_directory(handle)
        elif "settings" in action:
            platform.open_settings()
        else:
            logger.error("Invalid root action")

    elif path == PATH_CHARTS:
        action = args.get("action", [None])[0]
        genre = args.get("genre", ["soundcloud:genres:all-music"])[0]
        if action is None:
            items = listItems.charts()
            platform.add_directory_items(handle, items)
            platform.end_of_directory(handle)
        else:
            api_result = api.charts({"kind": action, "genre": genre, "limit": 50})
            collection = listItems.from_collection(api_result)
            platform.add_directory_items(handle, collection)
            platform.end_of_directory(handle)

    elif path == PATH_DISCOVER:
        selection = args.get("selection", [None])[0]
        collection = listItems.from_collection(api.discover(selection))
        platform.add_directory_items(handle, collection)
        platform.end_of_directory(handle)

    elif path == PATH_PLAY:
        # Public params
        track_id = args.get("track_id", [None])[0]
        playlist_id = args.get("playlist_id", [None])[0]
        url_param = args.get("url", [None])[0]

        # Public legacy params (@deprecated)
        audio_id_legacy = args.get("audio_id", [None])[0]
        track_id = audio_id_legacy if audio_id_legacy else track_id

        # Private params
        media_url = args.get("media_url", [None])[0]

        if media_url:
            resolved_url = api.resolve_media_url(media_url)
            listitem = factory.create_list_item(label="")
            factory.set_item_path(listitem, resolved_url)
            platform.set_resolved_url(handle, succeeded=True, listitem=listitem)
        elif track_id:
            collection = listItems.from_collection(api.resolve_id(track_id))
            playlist = platform.create_music_playlist()
            resolve_list_item(handle, collection[0][1], api, factory, platform)
            playlist.add(url=collection[0][0], listitem=collection[0][1])
        elif playlist_id:
            call = f"/playlists/{playlist_id}"
            collection = listItems.from_collection(api.call(call))
            playlist = platform.create_music_playlist()
            for item in collection:
                resolve_list_item(handle, item[1], api, factory, platform)
                playlist.add(url=item[0], listitem=item[1])
        elif url_param:
            collection = listItems.from_collection(api.resolve_url(url_param))
            playlist = platform.create_music_playlist()
            for item in collection:
                resolve_list_item(handle, item[1], api, factory, platform)
                playlist.add(url=item[0], listitem=item[1])
        else:
            logger.error("Invalid play param")

    elif path == PATH_SEARCH:
        action = args.get("action", None)
        query = args.get("query", [""])[0]

        if action and "remove" in action:
            search_history.remove(query)
            platform.execute_builtin("Container.Refresh")
        elif action and "clear" in action:
            search_history.clear()
            platform.execute_builtin("Container.Refresh")

        if query:
            if action is None:
                search(handle, query, listItems, api, platform)
            elif "people" in action:
                platform.set_content(handle, "artists")
                collection = listItems.from_collection(api.search(query, "users"))
                platform.add_directory_items(handle, collection)
                platform.end_of_directory(handle)
            elif "albums" in action:
                platform.set_content(handle, "albums")
                collection = listItems.from_collection(api.search(query, "albums"))
                platform.add_directory_items(handle, collection)
                platform.end_of_directory(handle)
            elif "playlists" in action:
                platform.set_content(handle, "albums")
                collection = listItems.from_collection(
                    api.search(query, "playlists_without_albums")
                )
                platform.add_directory_items(handle, collection)
                platform.end_of_directory(handle)
            else:
                logger.error("Invalid search action")
        else:
            if action is None:
                items = listItems.search()
                platform.add_directory_items(handle, items)
                platform.end_of_directory(handle)
            elif "new" in action:
                query = platform.input_dialog(platform.get_localized_string(30101))
                if query:
                    search_history.add(query)
                    search(handle, query, listItems, api, platform)
            else:
                logger.error("Invalid search action")

    # Legacy search query used by Chorus2 (@deprecated)
    elif path == PATH_SEARCH_LEGACY:
        query = args.get("q", [""])[0]
        collection = listItems.from_collection(api.search(query))
        platform.add_directory_items(handle, collection)
        platform.end_of_directory(handle)

    elif path == PATH_USER:
        user_id = args.get("id")[0]
        default_action = args.get("call")[0]
        if user_id:
            items = listItems.user(user_id)
            collection = listItems.from_collection(api.call(default_action))
            platform.add_directory_items(handle, items)
            platform.add_directory_items(handle, collection)
            platform.end_of_directory(handle)
        else:
            logger.error("Invalid user action")

    elif path == PATH_SETTINGS_CACHE_CLEAR:
        vfs_cache.destroy()
        platform.show_ok_dialog("SoundCloud", platform.get_localized_string(30501))

    else:
        logger.error("Path not found")


def resolve_list_item(handle, list_item, api, factory, platform):
    """Resolve a list item's media URL."""
    media_url = factory.get_item_property(list_item, "mediaUrl")
    resolved_url = api.resolve_media_url(media_url)
    factory.set_item_path(list_item, resolved_url)
    platform.set_resolved_url(handle, succeeded=True, listitem=list_item)


def search(handle, query, listItems, api, platform):
    """Handle search functionality."""
    search_options = listItems.search_sub(query)
    collection = listItems.from_collection(api.search(query))
    platform.add_directory_items(handle, search_options)
    platform.add_directory_items(handle, collection)
    platform.end_of_directory(handle)
