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
            proton_path: The path to the Proton executable script.
            steam_root: The path to the Steam root directory.
        """
        self.logger = logger
        self.proton_path = proton_path
        self.steam_root = steam_root
        self.proton_root_dir = self.proton_path.parent
        self.proton_bin_path = self.proton_root_dir / "dist/bin"

    def _get_custom_env(self, prefix_path: Path) -> Dict[str, str]:
        """
        Prepares a custom environment for running Wine/Proton commands.
        This modifies the PATH to ensure the correct Proton version is used.
        """
        env = os.environ.copy()
        env["PATH"] = f"{self.proton_bin_path}:{env.get('PATH', '')}"
        env["WINEPREFIX"] = str(prefix_path / "pfx")
        env["WINE"] = str(self.proton_bin_path / "wine")
        env["WINESERVER"] = str(self.proton_bin_path / "wineserver")
        env["STEAM_COMPAT_CLIENT_INSTALL_PATH"] = str(self.steam_root)
        env["DXVK_ASYNC"] = "1"
        env["DXVK_LOG_LEVEL"] = "info"
        return env

    def _find_dll_paths(self, lib_name: str) -> Optional[Dict[str, Path]]:
        """
        Dynamically finds the library paths for a given library name (e.g., 'dxvk').
        It searches within the Proton installation directory for common structures.
        """
        self.logger.info(f"Searching for '{lib_name}' library in '{self.proton_root_dir}'...")

        # First, try the standard Valve Proton structure
        std_x64_path = self.proton_root_dir / f"dist/lib64/wine/{lib_name}"
        std_x86_path = self.proton_root_dir / f"dist/lib/wine/{lib_name}"

        if std_x64_path.exists() and std_x86_path.exists():
            self.logger.info(f"Found '{lib_name}' using standard Proton 'dist' structure.")
            return {"x64": std_x64_path, "x86": std_x86_path}

        # If not found, try a broader search for GE-Proton and other custom versions
        self.logger.warning(f"Standard paths not found for '{lib_name}'. Trying broader search for custom Proton versions...")

        found_base_dirs = list(self.proton_root_dir.rglob(lib_name))

        for base_dir in found_base_dirs:
            if not base_dir.is_dir():
                continue

            x64_dir = base_dir / 'x64' if (base_dir / 'x64').exists() else base_dir / 'lib64'
            x86_dir = base_dir / 'x86' if (base_dir / 'x86').exists() else base_dir / 'lib'

            if x64_dir.exists() and x86_dir.exists():
                self.logger.info(f"Found '{lib_name}' paths in custom structure: {base_dir}")
                return {"x64": x64_dir, "x86": x86_dir}

        self.logger.error(f"Failed to find any valid directory structure for '{lib_name}' in {self.proton_root_dir}.")
        return None

    def apply_dxvk_vkd3d(self, prefix_path: Path):
        """
        Applies DXVK/VKD3D to the given Wine prefix.
        """
        self.logger.info(f"Applying DXVK/VKD3D to prefix: {prefix_path}")

        system32_path = prefix_path / "pfx/system32"
        syswow64_path = prefix_path / "pfx/syswow64"

        dll_sources = {
            "dxvk": self._find_dll_paths("dxvk"),
            "vkd3d-proton": self._find_dll_paths("vkd3d-proton"),
        }

        for lib_name, paths in dll_sources.items():
            if not paths:
                self.logger.warning(f"Skipping '{lib_name}' as its paths were not found.")
                continue

            for arch, src_path in paths.items():
                dest_path = syswow64_path if arch == "x86" else system32_path
                if not src_path.exists():
                    self.logger.warning(f"Source path for {lib_name} ({arch}) not found: {src_path}")
                    continue

                self.logger.info(f"Copying DLLs for {lib_name} ({arch}) from {src_path} to {dest_path}")
                for dll in src_path.glob("*.dll"):
                    self.logger.info(f"Copying {dll.name} to {dest_path}")
                    shutil.copy(dll, dest_path)

        reg_commands = {
            'HKEY_CURRENT_USER\\Software\\Wine\\DllOverrides': [
                ('d3d10', 'native,builtin'), ('d3d10_1', 'native,builtin'),
                ('d3d10core', 'native,builtin'), ('d3d11', 'native,builtin'),
                ('d3d9', 'native,builtin'), ('dxgi', 'native,builtin'),
                ('d3d12', 'native,builtin'), ('d3d12core', 'native,builtin'),
            ]
        }

        custom_env = self._get_custom_env(prefix_path)

        for key, values in reg_commands.items():
            for value_name, value_data in values:
                try:
                    subprocess.run(
                        ["wine", "reg", "add", key, "/v", value_name, "/d", value_data, "/f"],
                        env=custom_env,
                        check=True,
                        capture_output=True,
                        text=True,
                        errors='replace',
                    )
                    self.logger.info(f"Successfully set registry key: {key}\\{value_name} = {value_data}")
                except subprocess.CalledProcessError as e:
                    self.logger.error(f"Failed to set registry key: {key}\\{value_name}")
                    self.logger.error(f"Stderr: {e.stderr}")
                    self.logger.error(f"Stdout: {e.stdout}")

    def apply_winetricks(self, prefix_path: Path, verbs: List[str]):
        """
        Applies Winetricks verbs to the given Wine prefix.
        """
        if not verbs:
            return

        self.logger.info(f"Applying Winetricks verbs: {verbs}")

        winetricks_path = shutil.which("winetricks")
        if not winetricks_path:
            self.logger.error("Winetricks is not installed or not in PATH.")
            return

        custom_env = self._get_custom_env(prefix_path)

        try:
            subprocess.run(
                [winetricks_path, *verbs],
                env=custom_env,
                check=True,
                capture_output=True,
                text=True,
                errors='replace',
            )
            self.logger.info(f"Successfully applied Winetricks verbs: {verbs}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to apply Winetricks verbs: {verbs}")
            self.logger.error(f"Stderr: {e.stderr}")
            self.logger.error(f"Stdout: {e.stdout}")