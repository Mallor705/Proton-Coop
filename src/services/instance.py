import os
import shlex
import copy
import shutil
import signal
import subprocess
import time
from pathlib import Path
from typing import List, Optional

import psutil

from ..core.config import Config
from ..core.exceptions import DependencyError
from ..core.logger import Logger
from ..models.profile import Profile, PlayerInstanceConfig


class InstanceService:
    """Service responsible for managing Steam instances."""

    def __init__(self, logger: Logger):
        """Initializes the instance service."""
        self.logger = logger
        self.pids: dict[int, int] = {}
        self.processes: dict[int, subprocess.Popen] = {}
        self.cpu_count = psutil.cpu_count(logical=True)
        self.termination_in_progress = False

    def _get_cpu_affinity_for_instance(self, instance_num: int, total_instances: int) -> List[int]:
        """
        Calculates which CPU cores should be assigned to a specific instance.
        Divides available cores evenly among instances.

        Args:
            instance_num: The instance number (1-based)
            total_instances: Total number of instances being launched

        Returns:
            List of CPU core indices for this instance
        """
        if not self.cpu_count or total_instances == 0:
            return []

        cores_per_instance = self.cpu_count // total_instances
        if cores_per_instance == 0:
            cores_per_instance = 1

        start_core = (instance_num - 1) * cores_per_instance
        end_core = start_core + cores_per_instance

        # Last instance gets any remaining cores
        if instance_num == total_instances:
            end_core = self.cpu_count

        cpu_list = list(range(start_core, end_core))
        self.logger.info(f"Instance {instance_num}: Assigned CPU cores {cpu_list}")
        return cpu_list

    def launch_steam(self, profile: Profile) -> None:
        """A wrapper for launch_steam_instances that can be called from the GUI."""
        self.launch_steam_instances(profile)

    def validate_dependencies(self, use_gamescope: bool = True) -> None:
        """Validates if all necessary commands are available on the system."""
        self.logger.info("Validating dependencies...")
        required_commands = ["bwrap", "steam"]
        if use_gamescope:
            required_commands.insert(0, "gamescope")
        for cmd in required_commands:
            if not shutil.which(cmd):
                raise DependencyError(f"Required command '{cmd}' not found")
        self.logger.info("Dependencies validated successfully")

    def launch_steam_instances(self, profile: Profile) -> None:
        """Launches all Steam instances according to the provided profile."""
        self.validate_dependencies(use_gamescope=profile.use_gamescope)

        Config.LOG_DIR.mkdir(parents=True, exist_ok=True)

        num_instances = profile.effective_num_players()
        if num_instances == 0:
            self.logger.info("No instances to launch.")
            return

        self.logger.info(f"Launching {num_instances} instance(s) of Steam...")

        for i in range(num_instances):
            instance_num = (profile.selected_players[i] if profile.selected_players else i + 1)
            self.launch_instance(profile, instance_num)
            time.sleep(5) # Stagger launches

        self.logger.info(f"All {num_instances} instances launched")
        self.logger.info(f"PIDs: {self.pids}")

    def _launch_single_instance(self, profile: Profile, instance_num: int) -> None:
        """Launches a single steam instance."""
        self.logger.info(f"Preparing instance {instance_num}...")

        home_path = Config.get_steam_home_path(instance_num)
        home_path.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Instance {instance_num}: Using isolated home path '{home_path}'")

        # Prepare minimal home structure - Steam will auto-install on first run
        self._prepare_steam_home(home_path)

        instance_idx = instance_num - 1
        device_info = self._validate_input_devices(profile, instance_idx, instance_num)

        env = self._prepare_environment(profile, device_info, instance_num)
        total_instances = profile.effective_num_players()
        cmd = self._build_command(profile, device_info, instance_num, home_path, total_instances)

        log_file = Config.LOG_DIR / f"steam_instance_{instance_num}.log"
        self.logger.info(f"Launching instance {instance_num} (Log: {log_file})")

        try:
            # Use 'script' command to capture all terminal output from nested processes
            # (gamescope -> bwrap -> steam). This is more reliable than stdout redirection
            # because it captures output from a pseudo-terminal.
            cmd_str = shlex.join(cmd)
            script_cmd = ["script", "-q", "-e", "-c", cmd_str, str(log_file)]

            process = subprocess.Popen(
                script_cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=env,
                cwd=Path.home(),  # Launch from the user's real home directory
                preexec_fn=os.setpgrp,
            )
            self.pids[instance_num] = process.pid
            self.processes[instance_num] = process
            self.logger.info(f"Instance {instance_num} started with PID: {process.pid}")
        except Exception as e:
            self.logger.error(f"Failed to launch instance {instance_num}: {e}")

    def launch_instance(
        self,
        profile: Profile,
        instance_num: int,
        use_gamescope_override: Optional[bool] = None,
    ) -> None:
        """Launches a single Steam instance."""
        active_profile = profile
        if use_gamescope_override is not None:
            active_profile = copy.deepcopy(profile)
            active_profile.use_gamescope = use_gamescope_override

        self.validate_dependencies(use_gamescope=active_profile.use_gamescope)
        Config.LOG_DIR.mkdir(parents=True, exist_ok=True)
        self._launch_single_instance(active_profile, instance_num)

    def terminate_instance(self, instance_num: int) -> None:
        """Terminates a single Steam instance."""
        if instance_num not in self.processes:
            self.logger.warning(
                f"Attempted to terminate non-existent instance {instance_num}"
            )
            return

        process = self.processes[instance_num]
        if process.poll() is None:
            try:
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                self.logger.info(
                    f"Sent SIGKILL to process group of PID {process.pid} for instance {instance_num}"
                )
            except ProcessLookupError:
                self.logger.info(
                    f"Process group for PID {process.pid} not found for instance {instance_num}."
                )
            except Exception as e:
                self.logger.error(
                    f"Failed to kill process group for PID {process.pid} for instance {instance_num}: {e}"
                )
        process.wait()
        del self.processes[instance_num]
        del self.pids[instance_num]

    def _prepare_steam_home(self, home_path: Path) -> None:
        """
        Prepares the isolated Steam data directory for an instance.
        This directory will be mounted over the default ~/.local/share/Steam.
        """
        self.logger.info(f"Preparing instance data directory at {home_path}...")

        # Create mount points for sharing host's game and tool files
        (home_path / "steamapps" / "common").mkdir(parents=True, exist_ok=True)
        (home_path / "compatibilitytools.d").mkdir(parents=True, exist_ok=True)

        # Copy .acf files from host Steam to instance to share game libraries.
        # This makes Steam think the games are installed in this instance.
        host_steamapps = Path.home() / ".local/share/Steam/steamapps"
        dest_steamapps = home_path / "steamapps"
        for acf_file in host_steamapps.glob("*.acf"):
            dest_file = dest_steamapps / acf_file.name
            if not dest_file.exists():
                shutil.copy(acf_file, dest_file)

        self.logger.info(f"Instance data directory {home_path} is ready.")

    def _prepare_environment(self, profile: Profile, device_info: dict, instance_num: int) -> dict:
        """Prepares a minimal environment for the Steam instance."""
        env = os.environ.copy()
        env.pop("PYTHONHOME", None)
        env.pop("PYTHONPATH", None)

        # Enable this if you experience system crashes and graphical glitches.
        # env["ENABLE_GAMESCOPE_WSI"] = "1"
        # env["LD_PRELOAD"] = ""
        # Handle joystick assignment
        if device_info.get("joystick_path_str_for_instance"):
            env["SDL_JOYSTICK_DEVICE"] = device_info["joystick_path_str_for_instance"]
            self.logger.info(f"Instance {instance_num}: Setting SDL_JOYSTICK_DEVICE to '{device_info['joystick_path_str_for_instance']}'.")

        # Handle audio device assignment
        if device_info.get("audio_device_id_for_instance"):
            env["PULSE_SINK"] = device_info["audio_device_id_for_instance"]
            self.logger.info(f"Instance {instance_num}: Setting PULSE_SINK to '{device_info['audio_device_id_for_instance']}'.")

        # Custom ENV variables are set via bwrap --setenv to target Steam directly.

        self.logger.info(f"Instance {instance_num}: Final environment prepared.")
        return env

    def _build_command(self, profile: Profile, device_info: dict, instance_num: int, home_path: Path, total_instances: int = 2) -> List[str]:
        """
        Builds the final command array in the correct order:
        [taskset] -> [gamescope] -> [bwrap] -> [steam]  (when gamescope is enabled)
        [taskset] -> [bwrap] -> [steam]                  (when gamescope is disabled)
        """
        instance_idx = instance_num - 1

        # 1. Build the innermost steam command
        steam_cmd = self._build_base_steam_command(instance_num, profile.use_gamescope)

        # 2. Build the bwrap command, which will wrap the steam command
        bwrap_cmd = self._build_bwrap_command(profile, instance_idx, device_info, instance_num, home_path)

        # 3. Prepend bwrap to the steam command
        final_cmd = bwrap_cmd + steam_cmd

        # 4. Build the Gamescope command and prepend it (if enabled)
        if profile.use_gamescope:
            should_add_grab_flags = device_info.get("should_add_grab_flags", False)
            gamescope_cmd = self._build_gamescope_command(profile, should_add_grab_flags, instance_num)

            # Add the '--' separator before the command Gamescope will run
            final_cmd = gamescope_cmd + ["--"] + final_cmd
            self.logger.info(f"Instance {instance_num}: Launching with Gamescope")
        else:
            self.logger.info(f"Instance {instance_num}: Launching without Gamescope (bwrap only)")

        # 5. Build taskset command to limit CPU cores for this instance
        cpu_list = self._get_cpu_affinity_for_instance(instance_num, total_instances)
        if cpu_list:
            cpu_mask = ",".join(str(c) for c in cpu_list)
            taskset_cmd = ["taskset", "-c", cpu_mask]
            final_cmd = taskset_cmd + final_cmd
            self.logger.info(f"Instance {instance_num}: Using taskset with cores: {cpu_mask}")

        self.logger.info(f"Instance {instance_num}: Full command: {shlex.join(final_cmd)}")
        return final_cmd

    def _validate_input_devices(self, profile: Profile, instance_idx: int, instance_num: int) -> dict:
        """Validates input devices and returns information about them."""
        # Get specific player config
        player_config = (
            profile.player_configs[instance_idx]
            if profile.player_configs and 0 <= instance_idx < len(profile.player_configs)
            else PlayerInstanceConfig() # Default empty config
        )

        def _validate_device(path_str: Optional[str], device_type: str) -> Optional[str]:
            if not path_str or not path_str.strip():
                return None
            path_obj = Path(path_str)
            if path_obj.exists() and path_obj.is_char_device():
                 self.logger.info(f"Instance {instance_num}: {device_type} device '{path_str}' assigned.")
                 return str(path_obj.resolve())
            self.logger.warning(
                f"Instance {instance_num}: {device_type} device '{path_str}' not found or not a char device."
            )
            return None

        mouse_path = _validate_device(player_config.MOUSE_EVENT_PATH, "Mouse")
        keyboard_path = _validate_device(player_config.KEYBOARD_EVENT_PATH, "Keyboard")
        joystick_path = _validate_device(player_config.PHYSICAL_DEVICE_ID, "Joystick")

        audio_id = player_config.AUDIO_DEVICE_ID
        if audio_id and audio_id.strip():
            self.logger.info(f"Instance {instance_num}: Audio device ID '{audio_id}' assigned.")

        return {
            "mouse_path_str_for_instance": mouse_path,
            "keyboard_path_str_for_instance": keyboard_path,
            "joystick_path_str_for_instance": joystick_path,
            "audio_device_id_for_instance": audio_id if audio_id and audio_id.strip() else None,
            "should_add_grab_flags": bool(mouse_path and keyboard_path),
        }

    def _build_gamescope_command(self, profile: Profile, should_add_grab_flags: bool, instance_num: int) -> List[str]:
        """Builds the Gamescope command."""
        width, height = profile.get_instance_dimensions(instance_num)
        if not width or not height:
            self.logger.error(f"Instance {instance_num}: Invalid dimensions. Aborting launch.")
            return []

        cmd = [
            "gamescope",
            "-e", # Enable Steam integration
            "-W", str(width),
            "-H", str(height),
            "-w", str(width),
            "-h", str(height),
            # "--xwayland-count", "1",
            # "--mangoapp",
        ]

        # Always set an unfocused FPS limit to a very high value
        cmd.extend(["-o", "999"])
        self.logger.info(f"Instance {instance_num}: Setting unfocused FPS limit to 999.")

        # Always set a focused FPS limit to a very high value
        cmd.extend(["-r", "999"])
        self.logger.info(f"Instance {instance_num}: Setting focused FPS limit to 999.")

        if not profile.is_splitscreen_mode:
            cmd.extend(["-f", "--adaptive-sync"])
        else:
            cmd.append("-b") # Borderless

        if should_add_grab_flags:
            self.logger.info(f"Instance {instance_num}: Using dedicated mouse/keyboard. Grabbing input.")
            cmd.extend(["--grab", "--force-grab-cursor"])

        return cmd

    def _build_base_steam_command(self, instance_num: int, use_gamescope: bool = True) -> List[str]:
        """Builds the base steam command."""
        if use_gamescope:
            self.logger.info(f"Instance {instance_num}: Using Steam command with Gamescope flags.")
            return ["steam", "-gamepadui"]
        else:
            self.logger.info(f"Instance {instance_num}: Using plain Steam command.")
            return ["steam"]

    def _build_bwrap_command(self, profile: Profile, instance_idx: int, device_info: dict, instance_num: int, home_path: Path) -> List[str]:
        """
        Builds the bwrap command for sandboxing.
        The instance runs as the host user, but its Steam data directory
        (typically ~/.local/share/Steam) is redirected to an isolated path.
        This preserves user data isolation while allowing seamless integration
        with the host user's desktop environment (D-Bus, etc.).
        """
        user_home = Path.home()
        steam_data_dir = user_home / ".local/share/Steam"

        cmd = [
            "bwrap",
            "--dev-bind", "/", "/",
            "--proc", "/proc",
            "--dev", "/dev",
            "--bind", "/tmp", "/tmp",
            "--share-net",
            "--die-with-parent",
        ]

        # 1. Mount the isolated instance data over the real Steam data directory.
        #    This is the core of the isolation strategy.
        cmd.extend(["--bind", str(home_path), str(steam_data_dir)])

        # 2. Mount the shared subdirectories from the real Steam installation
        #    into the now-redirected (sandboxed) Steam data directory.
        #    This allows all instances to share game files and tools.
        cmd.extend(["--bind", str(steam_data_dir / "steamapps" / "common"), str(steam_data_dir / "steamapps" / "common")])

        # Mount host compatibility tools directory to share compatibility tools
        host_compat_dir = steam_data_dir / "compatibilitytools.d"
        ignore = {"LegacyRuntime"}
        if host_compat_dir.exists():
            for folder in host_compat_dir.iterdir():
                if folder.is_dir() and folder.name not in ignore:
                    target_path = steam_data_dir / "compatibilitytools.d" / folder.name
                    cmd.extend(["--bind", str(folder), str(target_path)])

        # Set environment variables required for Steam within the sandbox
        cmd.extend(["--setenv", "LD_PRELOAD", "", "--setenv", "ENABLE_GAMESCOPE_WSI", "1"])

        # Ensure custom ENV variables from the profile reach Steam
        try:
            extra_env = profile.get_env_for_instance(instance_idx) if hasattr(profile, "get_env_for_instance") else {}
            for k, v in (extra_env or {}).items():
                if v is None:
                    v = ""
                cmd.extend(["--setenv", str(k), str(v)])
            if extra_env:
                self.logger.info(f"Instance {instance_num}: Added {len(extra_env)} --setenv entries to bwrap.")
        except Exception as e:
            self.logger.error(f"Instance {instance_num}: Failed to add custom --setenv entries: {e}")

        return cmd

    def terminate_all(self) -> None:
        """Terminates all managed steam instances."""
        if self.termination_in_progress:
            return
        try:
            self.termination_in_progress = True
            self.logger.info("Starting termination of all instances...")

            for instance_num in list(self.processes.keys()):
                self.terminate_instance(instance_num)

            self.logger.info("Instance termination complete.")
            self.pids.clear()
            self.processes.clear()
        finally:
            self.termination_in_progress = False
