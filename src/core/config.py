import sys
from pathlib import Path
import shutil

class Config:
    """
    Global MultiScope configurations.
    """
    APP_NAME = "multiscope"

    @staticmethod
    def _get_script_dir() -> Path:
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            return Path(sys._MEIPASS)
        else:
            return Path(__file__).parent.parent.parent

    SCRIPT_DIR: Path = _get_script_dir()
    APP_DIR: Path = Path(__file__).parent.parent.parent

    LOCAL_DIR: Path = Path.home() / f".local/share/{APP_NAME}"
    CONFIG_DIR: Path = Path.home() / f".config/{APP_NAME}"
    LOG_DIR: Path = Path.home() / f".cache/{APP_NAME}/logs"

    @staticmethod
    def get_profile_path() -> Path:
        """Returns the path to the default profile JSON file."""
        return Config.CONFIG_DIR / "profile.json"

    @staticmethod
    def get_steam_home_path(instance_num: int) -> Path:
        """Returns the isolated Steam home path for a given instance."""
        return Config.LOCAL_DIR / f"steam_home_{instance_num}"
