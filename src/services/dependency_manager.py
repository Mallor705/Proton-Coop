import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Optional

from ..core.config import Config
from ..core.logger import Logger


class DependencyManager:
    """Manages the installation of dependencies like DXVK, VKD3D, and Winetricks."""

    def __init__(self, logger: Logger, proton_path: Path, steam_root: Path):
        """
        Initializes the DependencyManager.

        Args:
            logger: The logger instance.
            proton_path: The path to the Proton executable.
            steam_root: The path to the Steam root directory.
        """
        self.logger = logger
        self.proton_path = proton_path
        self.steam_root = steam_root
        self.wine_path = self.proton_path.parent / "dist/bin/wine"
        self.wineserver_path = self.proton_path.parent / "dist/bin/wineserver"
        self.proton_dist_path = self.proton_path.parent / "dist"

    def apply_dxvk_vkd3d(self, prefix_path: Path):
        """
        Applies DXVK/VKD3D to the given Wine prefix.

        Args:
            prefix_path: The path to the Wine prefix.
        """
        self.logger.info(f"Applying DXVK/VKD3D to prefix: {prefix_path}")

        system32_path = prefix_path / "pfx/system32"
        syswow64_path = prefix_path / "pfx/syswow64"

        dll_map = {
            "dxvk": {
                "x64": self.proton_dist_path / "lib64/wine/dxvk",
                "x86": self.proton_dist_path / "lib/wine/dxvk",
            },
            "vkd3d": {
                "x64": self.proton_dist_path / "lib64/wine/vkd3d-proton",
                "x86": self.proton_dist_path / "lib/wine/vkd3d-proton",
            },
        }

        for lib, paths in dll_map.items():
            for arch, src_path in paths.items():
                dest_path = syswow64_path if arch == "x86" else system32_path
                if not src_path.exists():
                    self.logger.warning(f"Source path for {lib} ({arch}) not found: {src_path}")
                    continue

                for dll in src_path.glob("*.dll"):
                    self.logger.info(f"Copying {dll.name} to {dest_path}")
                    shutil.copy(dll, dest_path)

        # Apply registry changes
        reg_commands = {
            'HKEY_CURRENT_USER\\Software\\Wine\\DllOverrides': [
                ('d3d10', 'native,builtin'),
                ('d3d10_1', 'native,builtin'),
                ('d3d10core', 'native,builtin'),
                ('d3d11', 'native,builtin'),
                ('d3d9', 'native,builtin'),
                ('dxgi', 'native,builtin'),
                ('d3d12', 'native,builtin'),
                ('d3d12core', 'native,builtin'),
            ]
        }

        for key, values in reg_commands.items():
            for value_name, value_data in values:
                try:
                    subprocess.run(
                        [
                            str(self.wine_path),
                            "reg",
                            "add",
                            key,
                            "/v",
                            value_name,
                            "/d",
                            value_data,
                            "/f",
                        ],
                        env={"WINEPREFIX": str(prefix_path / "pfx")},
                        check=True,
                        capture_output=True,
                        text=True,
                    )
                    self.logger.info(f"Successfully set registry key: {key}\\{value_name} = {value_data}")
                except subprocess.CalledProcessError as e:
                    self.logger.error(f"Failed to set registry key: {key}\\{value_name}")
                    self.logger.error(f"Stderr: {e.stderr}")
                    self.logger.error(f"Stdout: {e.stdout}")

    def apply_winetricks(self, prefix_path: Path, verbs: List[str]):
        """
        Applies Winetricks verbs to the given Wine prefix.

        Args:
            prefix_path: The path to the Wine prefix.
            verbs: A list of Winetricks verbs to apply.
        """
        if not verbs:
            return

        self.logger.info(f"Applying Winetricks verbs: {verbs}")

        winetricks_path = shutil.which("winetricks")
        if not winetricks_path:
            self.logger.error("Winetricks is not installed or not in PATH.")
            return

        env = {
            **self.get_base_env(),
            "WINE": str(self.wine_path),
            "WINESERVER": str(self.wineserver_path),
            "WINEPREFIX": str(prefix_path / "pfx"),
        }

        try:
            subprocess.run(
                [winetricks_path, *verbs],
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            self.logger.info(f"Successfully applied Winetricks verbs: {verbs}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to apply Winetricks verbs: {verbs}")
            self.logger.error(f"Stderr: {e.stderr}")
            self.logger.error(f"Stdout: {e.stdout}")

    def get_base_env(self) -> Dict[str, str]:
        """
        Returns a base set of environment variables for running Wine/Proton commands.

        Returns:
            A dictionary of environment variables.
        """
        env = os.environ.copy()
        env["STEAM_COMPAT_CLIENT_INSTALL_PATH"] = str(self.steam_root)
        env["DXVK_ASYNC"] = "1"
        env["DXVK_LOG_LEVEL"] = "info"
        return env