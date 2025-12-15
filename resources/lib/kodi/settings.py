"""Settings wrapper - kept for backward compatibility, but should use ISettings port."""
from resources.lib.ports.settings import ISettings


class Settings(ISettings):
    """Settings wrapper that implements ISettings port."""
    
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

    def __init__(self, settings: ISettings):
        """Initialize with an ISettings implementation."""
        self._settings = settings

    def get(self, setting_id: str) -> str:
        """Get a setting value by ID."""
        return self._settings.get(setting_id)

    def set(self, setting_id: str, value: str) -> None:
        """Set a setting value."""
        self._settings.set(setting_id, value)
