import sys
from pathlib import Path

class Config:
    """Global Linux-Coop configurations, including directories, commands, and Steam paths."""

    @staticmethod
    def _get_script_dir():
        """Get the script directory, handling PyInstaller frozen executable."""
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # PyInstaller bundle
            return Path(sys._MEIPASS)
        else:
            # Normal Python execution
            return Path(__file__).parent.parent.parent

    SCRIPT_DIR = _get_script_dir()
    PROFILE_DIR = Path.home() / ".config/linux-coop/profiles"
    LOG_DIR = Path.home() / ".cache/linux-coop/logs"
    PREFIX_BASE_DIR = Path.home() / "Games/linux-coop/prefixes/"

    STEAM_PATHS = [
        Path.home() / ".steam/root",
        Path.home() / ".local/share/Steam",
        Path.home() / ".steam/steam",
        Path.home() / ".steam/debian-installation",
        Path.home() / ".steam/steam/root",
        Path.home() / ".steam/steam/steamapps",
        Path.home() / ".local/share/Steam/steamapps",
        Path.home() / ".local/share/Steam/steamapps/common",
    ]

    REQUIRED_COMMANDS = ["bwrap"]  # gamescope is now optional, checked per-profile
    OPTIONAL_COMMANDS = ["gamescope"]

    # Timeout configurations (in seconds)
    PROCESS_START_TIMEOUT = 30
    PROCESS_TERMINATE_TIMEOUT = 10
    SUBPROCESS_TIMEOUT = 15
    FILE_IO_TIMEOUT = 5

    @staticmethod
    def migrate_legacy_paths() -> None:
        """
        Comprehensive migration for legacy paths. Renames prefix directories and profile
        .json files from using spaces to hyphens.
        """
        # 1. Migrate Prefix Directories
        if Config.PREFIX_BASE_DIR.exists() and Config.PREFIX_BASE_DIR.is_dir():
            for path in Config.PREFIX_BASE_DIR.iterdir():
                if path.is_dir() and " " in path.name:
                    new_name = path.name.replace(" ", "-")
                    new_path = path.parent / new_name
                    if new_path.exists():
                        print(f"Warning: Cannot migrate prefix '{path.name}' because '{new_name}' already exists. Skipping.", file=sys.stderr)
                        continue
                    try:
                        path.rename(new_path)
                        print(f"Info: Migrated prefix directory '{path.name}' to '{new_name}'.")
                    except OSError as e:
                        print(f"Error: Could not migrate prefix directory '{path.name}'. Error: {e}", file=sys.stderr)

        # 2. Migrate Profile Filenames
        if Config.PROFILE_DIR.exists() and Config.PROFILE_DIR.is_dir():
            for path in Config.PROFILE_DIR.glob('*.json'):
                if " " in path.stem:
                    new_name = f"{path.stem.replace(' ', '-')}.json"
                    new_path = path.parent / new_name
                    if new_path.exists():
                        print(f"Warning: Cannot migrate profile '{path.name}' because '{new_name}' already exists. Skipping.", file=sys.stderr)
                        continue
                    try:
                        path.rename(new_path)
                        print(f"Info: Migrated profile file '{path.name}' to '{new_name}'.")
                    except OSError as e:
                        print(f"Error: Could not migrate profile file '{path.name}'. Error: {e}", file=sys.stderr)

    @staticmethod
    def get_prefix_base_dir(game_name: str) -> Path:
        """
        Returns the base prefix directory for a specific game, replacing spaces with hyphens.
        """
        safe_game_name = game_name.replace(" ", "-")
        return Config.PREFIX_BASE_DIR / safe_game_name
