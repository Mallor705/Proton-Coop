from pathlib import Path
from typing import Tuple, Optional, Dict, List
from functools import lru_cache
from ..core.config import Config
from ..core.exceptions import ProtonNotFoundError
from ..core.logger import Logger
from enum import Enum

class SteamRuntimeType(Enum):
    """Types of Steam Runtime"""
    PRESSURE_VESSEL = "pressure_vessel"
    LEGACY = "legacy"
    NONE = "none"

class ProtonService:
    """Service responsible for locating and validating Proton and Steam directories."""
    def __init__(self, logger: Logger):
        """Initializes the Proton service with a logger."""
        self.logger = logger
        self._steam_path_cache: Dict[str, Optional[Path]] = {}
        self._proton_cache: Dict[str, Tuple[Optional[Path], Optional[Path]]] = {}
    
    def find_proton_path(self, version: str) -> Tuple[Path, Path]:
        """Searches for the Proton executable and the Steam root directory for the given version."""
        # Check cache first
        if version in self._proton_cache:
            cached_result = self._proton_cache[version]
            if cached_result[0] is not None and cached_result[1] is not None:
                self.logger.info(f"Proton found in cache: {cached_result[0]}")
                return cached_result[0], cached_result[1]
        
        self.logger.info(f"Searching for Proton: {version}")
        
        # Get valid Steam paths (cached)
        valid_steam_paths = self._get_valid_steam_paths()
        
        for steam_path in valid_steam_paths:
            proton_path = self._search_proton_in_steam(steam_path, version)
            
            if proton_path and proton_path.exists():
                self.logger.info(f"Proton found: {proton_path}")
                # Cache the result
                self._proton_cache[version] = (proton_path, steam_path)
                return proton_path, steam_path
        
        # Cache negative result
        self._proton_cache[version] = (None, None)
        raise ProtonNotFoundError(f"Proton '{version}' not found")
    
    @lru_cache(maxsize=32)
    def _get_valid_steam_paths(self) -> Tuple[Path, ...]:
        """Caches Steam paths that exist on the system."""
        valid_paths = []
        for steam_path in Config.STEAM_PATHS:
            cache_key = str(steam_path)
            if cache_key not in self._steam_path_cache:
                self._steam_path_cache[cache_key] = steam_path if steam_path.exists() else None
            
            if self._steam_path_cache[cache_key]:
                valid_paths.append(self._steam_path_cache[cache_key])
        
        return tuple(valid_paths)

    @lru_cache(maxsize=64)
    def _search_proton_in_steam(self, steam_path: Path, version: str) -> Optional[Path]:
        """Searches for Proton in Steam directories with cache."""
        search_dirs = [
            steam_path / "steamapps/common",
            steam_path / "compatibilitytools.d"
        ]
        
        for search_dir in search_dirs:
            if not search_dir.exists():
                continue
                
            # Try different naming conventions
            proton_candidates = []
            if version == "Experimental":
                proton_candidates = [search_dir / "Proton - Experimental"]
            else:
                proton_candidates = [
                    search_dir / f"Proton {version}",
                    search_dir / version
                ]
            
            for proton_dir in proton_candidates:
                proton_script = proton_dir / "proton"
                if proton_script.exists():
                    return proton_script
        
        return None

    def find_steam_runtime(self, steam_root: Path) -> Tuple[Optional[Path], SteamRuntimeType]:
        """Finds the Steam Runtime (Pressure Vessel or legacy runtime) for running Proton.
        
        Returns a tuple of (path, runtime_type) where path is the runtime script and
        runtime_type indicates whether it's Pressure Vessel or legacy runtime.
        
        Priority order:
        1. Pressure Vessel (modern, preferred for Proton 5.13+)
        2. Steam Runtime v2 (soldier/sniper)
        3. Legacy Steam Runtime v1 (scout)
        """
        self.logger.info("Searching for Steam Runtime...")
        
        # Try Pressure Vessel first (modern approach used by Steam client)
        pressure_vessel_paths = [
            (steam_root / "steamapps/common/SteamLinuxRuntime_soldier/pressure-vessel/bin/pressure-vessel-wrap", SteamRuntimeType.PRESSURE_VESSEL),
            (steam_root / "steamapps/common/SteamLinuxRuntime_sniper/pressure-vessel/bin/pressure-vessel-wrap", SteamRuntimeType.PRESSURE_VESSEL),
        ]
        
        for pv_path, runtime_type in pressure_vessel_paths:
            if pv_path.exists():
                self.logger.info(f"Found Pressure Vessel Steam Runtime at: {pv_path}")
                return pv_path, runtime_type
        
        # Fallback: Look for legacy steam-runtime script
        legacy_runtime_paths = [
            steam_root / "ubuntu12_32/steam-runtime/run.sh",
            steam_root / "ubuntu12_64/steam-runtime/run.sh",
        ]
        
        for legacy_path in legacy_runtime_paths:
            if legacy_path.exists():
                self.logger.info(f"Found legacy Steam Runtime at: {legacy_path}")
                return legacy_path, SteamRuntimeType.LEGACY
        
        # Final fallback: Look for any steam-runtime script
        runtime_search_paths = [
            steam_root / "ubuntu12_32/steam-runtime",
            steam_root / "ubuntu12_64/steam-runtime",
            steam_root / "steam-runtime",
        ]
        
        for runtime_dir in runtime_search_paths:
            if runtime_dir.exists():
                run_script = runtime_dir / "run.sh"
                if run_script.exists():
                    self.logger.info(f"Found legacy Steam Runtime at: {run_script}")
                    return run_script, SteamRuntimeType.LEGACY
        
        self.logger.warning("Steam Runtime not found! Games may not work correctly.")
        return None, SteamRuntimeType.NONE

    def list_installed_proton_versions(self) -> List[str]:
        """Lists all installed Proton versions found in Steam directories."""
        self.logger.info("Listing installed Proton versions.")
        installed_versions = set()
        
        valid_steam_paths = self._get_valid_steam_paths()
        
        for steam_path in valid_steam_paths:
            search_dirs = [
                steam_path / "steamapps/common",
                steam_path / "compatibilitytools.d"
            ]
            
            for search_dir in search_dirs:
                if search_dir.exists():
                    for item in search_dir.iterdir():
                        if item.is_dir() and ("Proton" in item.name or "GE-Proton" in item.name or "Wine" in item.name):
                            # Basic check for a 'proton' executable within the directory
                            if (item / "proton").exists():
                                installed_versions.add(item.name)
        
        sorted_versions = sorted(list(installed_versions))
        self.logger.info(f"Found Proton versions: {sorted_versions}")
        return sorted_versions