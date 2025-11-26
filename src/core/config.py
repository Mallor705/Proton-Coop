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

    CONFIG_DIR: Path = Path.home() / f".config/{APP_NAME}"
    LOG_DIR: Path = Path.home() / f".cache/{APP_NAME}/logs"

    @staticmethod
    def get_profile_path() -> Path:
        """Returns the path to the default profile JSON file."""
        return Config.CONFIG_DIR / "profile.json"

    @staticmethod
    def get_steam_home_path(instance_num: int) -> Path:
        """Returns the isolated Steam home path for a given instance."""
        return Config.CONFIG_DIR / f"steam_home_{instance_num}"

    @staticmethod
    def migrate_legacy_paths() -> None:
        """
        Migrates legacy 'multi-scope' configuration paths to the new
        'multiscope' structure.
        """
        legacy_config_dir = Path.home() / ".config/multi-scope"
        legacy_cache_dir = Path.home() / ".cache/multi-scope"

        if legacy_config_dir.exists() and not Config.CONFIG_DIR.exists():
            try:
                shutil.move(str(legacy_config_dir), str(Config.CONFIG_DIR))
                print(f"Info: Migrated config from '{legacy_config_dir}' to '{Config.CONFIG_DIR}'.")
            except OSError as e:
                print(f"Error migrating config directory: {e}", file=sys.stderr)

        if legacy_cache_dir.exists() and not Config.LOG_DIR.parent.exists():
            try:
                shutil.move(str(legacy_cache_dir), str(Config.LOG_DIR.parent))
                print(f"Info: Migrated cache from '{legacy_cache_dir}' to '{Config.LOG_DIR.parent}'.")
            except OSError as e:
                print(f"Error migrating cache directory: {e}", file=sys.stderr)
