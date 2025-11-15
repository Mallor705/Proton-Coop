import re
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

    @lru_cache(maxsize=8)
    def find_steam_runtime_path(self, proton_version: str) -> Path:
        """
        Finds the correct Steam Linux Runtime for a given Proton version.

        It determines whether to use 'sniper' (for Proton 8.0+) or 'soldier'
        (for older versions) and locates the appropriate wrapper script
        ('run-in-sniper' or 'run-in-soldier'). The result is cached.

        Args:
            proton_version (str): The name of the Proton version.

        Returns:
            Path: The path to the runtime wrapper executable.

        Raises:
            RuntimeNotFoundError: If the appropriate Steam Linux Runtime cannot be found.
        """
        major_version = 0
        match = re.search(r"(\d+)", proton_version)
        if match:
            major_version = int(match.group(1))

        if "experimental" in proton_version.lower() or major_version >= 8:
            runtime_name = "sniper"
            runtime_display_name = "Steam Linux Runtime 3.0 (sniper)"
            executable_name = "run-in-sniper"
        else:
            runtime_name = "soldier"
            runtime_display_name = "Steam Linux Runtime 2.0 (soldier)"
            executable_name = "run-in-soldier"

        self.logger.info(
            f"Searching for {runtime_display_name} for Proton '{proton_version}'..."
        )

        valid_steam_paths = self._get_valid_steam_paths()

        for steam_path in valid_steam_paths:
            common_dir = steam_path / "steamapps/common"
            if not common_dir.is_dir():
                continue

            for item in common_dir.iterdir():
                item_name_lower = item.name.lower()
                if (
                    item.is_dir()
                    and "runtime" in item_name_lower
                    and runtime_name in item_name_lower
                ):
                    self.logger.info(f"Found potential runtime directory: {item.name}")
                    executable_path = item / executable_name
                    if executable_path.exists():
                        self.logger.info(f"Steam Runtime found at: {executable_path}")
                        return executable_path

        raise RuntimeNotFoundError(f"{runtime_display_name} not found.")

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
