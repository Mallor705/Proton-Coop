import shutil
from pathlib import Path
from typing import Optional, List, Dict
from ..core.logger import Logger
from ..core.exceptions import DependencyError


class UmuService:
    """Service responsible for managing umu-launcher integration."""
    
    def __init__(self, logger: Logger):
        """Initializes the UMU service with a logger."""
        self.logger = logger
        self._umu_available: Optional[bool] = None
        
    def is_umu_available(self) -> bool:
        """Checks if umu-run is available on the system."""
        if self._umu_available is None:
            self._umu_available = shutil.which('umu-run') is not None
            if self._umu_available:
                self.logger.info("umu-run found on system")
            else:
                self.logger.warning("umu-run not found on system")
        return self._umu_available
    
    def validate_umu_dependency(self) -> None:
        """Validates if umu-run is available, raises error if not."""
        if not self.is_umu_available():
            raise DependencyError(
                "umu-run is not installed. Please install umu-launcher to use this feature. "
                "See: https://github.com/Open-Wine-Components/umu-launcher"
            )
        self.logger.info("UMU dependency validated successfully")
    
    def prepare_umu_environment(
        self,
        base_env: dict,
        wineprefix: Path,
        umu_id: Optional[str] = None,
        umu_store: Optional[str] = None,
        umu_proton_path: Optional[str] = None
    ) -> dict:
        """Prepares environment variables for umu-run execution.
        
        Args:
            base_env: Base environment variables to extend
            wineprefix: Path to the Wine prefix directory
            umu_id: Game ID from umu-database (defaults to umu-default)
            umu_store: Store identifier (egs, gog, steam, etc.)
            umu_proton_path: Path to specific Proton version or "GE-Proton" for latest
            
        Returns:
            Updated environment dictionary
        """
        env = base_env.copy()
        
        # Set WINEPREFIX for umu
        env['WINEPREFIX'] = str(wineprefix)
        self.logger.info(f"UMU: Setting WINEPREFIX to {wineprefix}")
        
        # Set GAMEID (defaults to umu-default if not provided)
        if umu_id:
            env['GAMEID'] = umu_id
            self.logger.info(f"UMU: Setting GAMEID to {umu_id}")
        else:
            env['GAMEID'] = 'umu-default'
            self.logger.info("UMU: Using default GAMEID (umu-default)")
        
        # Set STORE if provided
        if umu_store:
            env['STORE'] = umu_store
            self.logger.info(f"UMU: Setting STORE to {umu_store}")
        else:
            env['STORE'] = 'none'
            self.logger.info("UMU: Using default STORE (none)")
        
        # Set PROTONPATH if provided
        if umu_proton_path:
            env['PROTONPATH'] = umu_proton_path
            self.logger.info(f"UMU: Setting PROTONPATH to {umu_proton_path}")
        else:
            # Use UMU-Proton (default)
            self.logger.info("UMU: Using default UMU-Proton")
        
        return env
    
    def build_umu_command(
        self,
        exe_path: Path,
        game_args: Optional[str] = None
    ) -> List[str]:
        """Builds the umu-run command.
        
        Args:
            exe_path: Path to the game executable
            game_args: Additional game arguments
            
        Returns:
            List of command arguments
        """
        cmd = ['umu-run', str(exe_path)]
        
        if game_args:
            cmd.extend(game_args.split())
        
        self.logger.info(f"UMU command: {' '.join(cmd)}")
        return cmd
    
    def get_umu_info(self) -> Dict[str, str]:
        """Returns information about the umu installation."""
        info = {
            'available': str(self.is_umu_available()),
            'command': 'umu-run'
        }
        
        if self.is_umu_available():
            umu_path = shutil.which('umu-run')
            if umu_path:
                info['path'] = umu_path
        
        return info
