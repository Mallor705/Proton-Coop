from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ..core.config import Config
from ..core.exceptions import ProtonNotFoundError, RuntimeNotFoundError
from ..core.logger import Logger


class ProtonService:
    """
    A service for locating and managing Proton versions.

    This class provides methods to find specific Proton installations across
    common Steam library paths and to list all available Proton versions.
    It uses caching to speed up repeated lookups.
    """

    def __init__(self, logger: Logger):
        """
        Initializes the ProtonService.

        Args:
            logger (Logger): An instance of the application's logger.
        """
        self.logger = logger
        self._proton_cache: Dict[str, Tuple[Optional[Path], Optional[Path]]] = {}

    @lru_cache(maxsize=1)
    def find_steam_runtime_path(self) -> Path:
        """
        Finds the path to the Steam Linux Runtime 'pressure-vessel' executable.

        It prioritizes the 'Steam Linux Runtime - Soldier' version, which is
        used by modern Proton versions. The result is cached.

        Returns:
            Path: The path to the 'pressure-vessel-wrap' executable.

        Raises:
            RuntimeNotFoundError: If the Steam Linux Runtime cannot be found in
                                  any of the standard Steam library locations.
        """
        self.logger.info("Searching for Steam Linux Runtime...")
        valid_steam_paths = self._get_valid_steam_paths()
        runtime_name = "Steam Linux Runtime - Soldier"
        executable_name = "pressure-vessel-wrap"

        for steam_path in valid_steam_paths:
            runtime_dir = steam_path / "steamapps/common" / runtime_name
            if runtime_dir.is_dir():
                executable_path = runtime_dir / executable_name
                if executable_path.exists():
                    self.logger.info(f"Steam Runtime found at: {executable_path}")
                    return executable_path

                # Also check inside the amd64/ bin directory as a fallback
                fallback_path = runtime_dir / "amd64/bin" / executable_name
                if fallback_path.exists():
                    self.logger.info(f"Steam Runtime found at: {fallback_path}")
                    return fallback_path

        raise RuntimeNotFoundError(f"'{runtime_name}' not found.")

    def find_proton_path(self, version: str) -> Tuple[Path, Path]:
        """
        Finds the executable for a specific Proton version.

        It searches through standard Steam library locations and caches the
        results to accelerate future lookups.

        Args:
            version (str): The Proton version to find (e.g., "GE-Proton8-25",
                           "Experimental").

        Returns:
            Tuple[Path, Path]: A tuple containing the path to the Proton
                               executable and the path to the corresponding
                               Steam root directory.

        Raises:
            ProtonNotFoundError: If the specified Proton version cannot be found.
        """
        if version in self._proton_cache:
            proton_path, steam_root = self._proton_cache[version]
            if proton_path and steam_root:
                self.logger.info(f"Proton '{version}' found in cache: {proton_path}")
                return proton_path, steam_root

        self.logger.info(f"Searching for Proton: {version}...")
        valid_steam_paths = self._get_valid_steam_paths()

        for steam_path in valid_steam_paths:
            proton_path = self._search_proton_in_steam_path(steam_path, version)
            if proton_path and proton_path.exists():
                self.logger.info(f"Proton '{version}' found at: {proton_path}")
                self._proton_cache[version] = (proton_path, steam_path)
                return proton_path, steam_path

        self._proton_cache[version] = (None, None)
        raise ProtonNotFoundError(f"Proton version '{version}' not found.")

    @lru_cache(maxsize=1)
    def _get_valid_steam_paths(self) -> Tuple[Path, ...]:
        """
        Gets a tuple of existing Steam library paths from the config.

        This method is cached to avoid repeated file system checks.

        Returns:
            Tuple[Path, ...]: A tuple of valid, existing Steam path objects.
        """
        valid_paths = [p for p in Config.STEAM_PATHS if p.exists()]
        self.logger.info(f"Found valid Steam paths: {valid_paths}")
        return tuple(valid_paths)

    @lru_cache(maxsize=64)
    def _search_proton_in_steam_path(
        self, steam_path: Path, version: str
    ) -> Optional[Path]:
        """
        Searches for a Proton version within a single Steam library path.

        Args:
            steam_path (Path): The Steam library path to search in.
            version (str): The Proton version string.

        Returns:
            Optional[Path]: The path to the Proton executable if found,
                            otherwise None.
        """
        search_dirs = [
            steam_path / "steamapps/common",
            steam_path / "compatibilitytools.d",
        ]
        version_names = [version, f"Proton {version}", f"GE-Proton{version}"]
        if version == "Experimental":
            version_names.append("Proton - Experimental")

        for search_dir in search_dirs:
            if not search_dir.exists():
                continue
            for name in version_names:
                proton_script = search_dir / name / "proton"
                if proton_script.exists():
                    return proton_script
        return None

    def list_installed_proton_versions(self) -> List[str]:
        """
        Scans all Steam libraries and returns a list of installed Proton versions.

        Returns:
            List[str]: A sorted list of the names of all found Proton versions,
                       with "None" as the first option.
        """
        self.logger.info("Discovering installed Proton versions...")
        installed_versions = set()
        valid_steam_paths = self._get_valid_steam_paths()

        for steam_path in valid_steam_paths:
            search_dirs = [
                steam_path / "steamapps/common",
                steam_path / "compatibilitytools.d",
            ]
            for search_dir in search_dirs:
                if search_dir.exists():
                    for item in search_dir.iterdir():
                        if item.is_dir() and "proton" in item.name.lower():
                            if (item / "proton").exists():
                                installed_versions.add(item.name)

        sorted_versions = sorted(list(installed_versions))
        self.logger.info(f"Found Proton versions: {sorted_versions}")
        return ["None"] + sorted_versions
