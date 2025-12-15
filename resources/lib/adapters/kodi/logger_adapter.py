"""KODI logger adapter - implements ILogger."""
import xbmc
from resources.lib.ports.logger import ILogger


class KodiLoggerAdapter(ILogger):
    """KODI implementation of logger adapter."""
    
    def __init__(self, addon_id: str = "plugin.audio.soundcloud"):
        self._addon_id = addon_id
    
    def debug(self, message: str) -> None:
        """Log a debug message."""
        xbmc.log(f"{self._addon_id}: {message}", xbmc.LOGDEBUG)
    
    def info(self, message: str) -> None:
        """Log an info message."""
        xbmc.log(f"{self._addon_id}: {message}", xbmc.LOGINFO)
    
    def warning(self, message: str) -> None:
        """Log a warning message."""
        xbmc.log(f"{self._addon_id}: {message}", xbmc.LOGWARNING)
    
    def error(self, message: str) -> None:
        """Log an error message."""
        xbmc.log(f"{self._addon_id}: {message}", xbmc.LOGERROR)

