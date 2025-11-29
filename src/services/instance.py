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

        # Get paths for isolated Steam directories
        steam_data_path = Config.get_steam_home_path(instance_num)
        steam_root_path = Config.get_steam_root_path(instance_num)

        # Create the directories if they don't exist
        steam_data_path.mkdir(parents=True, exist_ok=True)
        steam_root_path.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Instance {instance_num}: Using isolated Steam data path '{steam_data_path}'")
        self.logger.info(f"Instance {instance_num}: Using isolated Steam root path '{steam_root_path}'")


        # Prepare minimal data structure for the instance
        self._prepare_steam_home(steam_data_path, steam_root_path)

        instance_idx = instance_num - 1
        device_info = self._validate_input_devices(profile, instance_idx, instance_num)

        env = self._prepare_environment(profile, device_info, instance_num)
        total_instances = profile.effective_num_players()
        cmd = self._build_command(profile, device_info, instance_num, steam_data_path, steam_root_path, total_instances)

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

    def _prepare_steam_home(self, steam_data_path: Path, steam_root_path: Path) -> None:
        """
        Prepares the isolated Steam directories for an instance by creating
        the necessary upper and work directories for the overlayfs mounts.
        """
        self.logger.info(f"Preparing overlay directories for instance...")

        # Prepare for ~/.local/share/Steam overlay
        (steam_data_path / "upper").mkdir(parents=True, exist_ok=True)
        (steam_data_path / "work").mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Overlay directories for Steam data created at '{steam_data_path}'")

        # Prepare for ~/.steam overlay
        (steam_root_path / "upper").mkdir(parents=True, exist_ok=True)
        (steam_root_path / "work").mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Overlay directories for Steam root created at '{steam_root_path}'")

        self.logger.info("Instance directories are ready for overlay mounts.")

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

    def _build_command(self, profile: Profile, device_info: dict, instance_num: int, steam_data_path: Path, steam_root_path: Path, total_instances: int = 2) -> List[str]:
        """
        Builds the final command array in the correct order:
        [taskset] -> [gamescope] -> [bwrap] -> [steam]  (when gamescope is enabled)
        [taskset] -> [bwrap] -> [steam]                  (when gamescope is disabled)
        """
        instance_idx = instance_num - 1

        # 1. Build the innermost steam command
        steam_cmd = self._build_base_steam_command(instance_num, profile.use_gamescope)

        # 2. Build the bwrap command, which will wrap the steam command
        bwrap_cmd = self._build_bwrap_command(profile, instance_idx, device_info, instance_num, steam_data_path, steam_root_path)

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

    def _build_bwrap_command(self, profile: Profile, instance_idx: int, device_info: dict, instance_num: int, steam_data_path: Path, steam_root_path: Path) -> List[str]:
        """
        Builds the bwrap command for sandboxing using overlayfs for Steam data.
        """
        user_home = Path.home()
        host_steam_data_dir = user_home / ".local/share/Steam"
        host_steam_root_dir = user_home / ".steam"

        # These paths are the mount points *inside* the sandbox.
        sandboxed_steam_data_dir = host_steam_data_dir
        sandboxed_steam_root_dir = host_steam_root_dir

        cmd = [
            "bwrap",
            "--dev-bind", "/", "/",
            "--proc", "/proc",
            "--dev-bind", "/dev", "/dev",
            "--bind", "/tmp", "/tmp",
            "--share-net",
            "--die-with-parent",
        ]

        # Overlay for ~/.local/share/Steam
        if host_steam_data_dir.is_dir():
            upper_dir = steam_data_path / "upper"
            work_dir = steam_data_path / "work"
            cmd.extend([
                "--overlay-src", str(host_steam_data_dir),
                "--overlay", str(upper_dir), str(work_dir), str(sandboxed_steam_data_dir)
            ])
            self.logger.info(f"Instance {instance_num}: Setup overlay for Steam data at '{sandboxed_steam_data_dir}'")
        else:
            self.logger.warning(f"Host Steam data directory not found at '{host_steam_data_dir}', skipping overlay.")

        # Overlay for ~/.steam
        if host_steam_root_dir.is_dir():
            upper_dir = steam_root_path / "upper"
            work_dir = steam_root_path / "work"
            cmd.extend([
                "--overlay-src", str(host_steam_root_dir),
                "--overlay", str(upper_dir), str(work_dir), str(sandboxed_steam_root_dir)
            ])
            self.logger.info(f"Instance {instance_num}: Setup overlay for Steam root at '{sandboxed_steam_root_dir}'")
        else:
            self.logger.warning(f"Host Steam root directory not found at '{host_steam_root_dir}', skipping overlay.")

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
