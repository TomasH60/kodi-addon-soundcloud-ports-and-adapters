"""KODI settings adapter - implements ISettings."""
import xbmcaddon
from resources.lib.ports.settings import ISettings


class KodiSettingsAdapter(ISettings):
    """KODI implementation of settings adapter."""
    
    AUDIO_FORMATS = {
        "0": {
            "mime_type": "audio/ogg; codecs=\"opus\"",
            "protocol": "hls",
        },
        "1": {
            "mime_type": "audio/mpeg",
            "protocol": "hls",
        },
        "2": {
            "mime_type": "audio/mpeg",
            "protocol": "progressive",
        }
    }
    
    APIV2_LOCALE = {
        "auto": "0",
        "disabled": "1"
    }
    
    def __init__(self):
        self._addon = xbmcaddon.Addon()
    
    def get(self, setting_id: str) -> str:
        """Get a setting value by ID."""
        return self._addon.getSetting(setting_id)
    
    def set(self, setting_id: str, value: str) -> None:
        """Set a setting value."""
        self._addon.setSetting(setting_id, value)

