import subprocess
import re
from pathlib import Path
from typing import List, Dict

class DeviceManager:
    def __init__(self):
        pass

    def _run_command(self, command: str) -> str:
        """Helper to run shell commands and return stdout."""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            # print(f"Error executing command '{command}': {e}")
            # print(f"Stderr: {e.stderr}")
            return "" # Return empty string on error, the calling method should handle it

    def get_input_devices(self) -> Dict[str, List[str]]:
        """
        Detects and returns input devices categorized by type.
        Returns a dictionary with keys:
        - 'keyboard_event_paths': List of event paths for keyboards.
        - 'mouse_event_paths': List of event paths for mice.
        - 'joystick_event_paths': List of event paths for joysticks.
        - 'physical_device_ids': List of physical device paths (e.g., /dev/input/jsX, /dev/input/mouseX).
        """
        detected_devices: Dict[str, List[str]] = {
            "keyboard_event_paths": [],
            "mouse_event_paths": [],
            "joystick_event_paths": [],
            "physical_device_ids": []
        }

        by_id_output = self._run_command("ls -l /dev/input/by-id/")
        
        for line in by_id_output.splitlines():
            # Example line: lrwxrwxrwx 1 root root 9 jun 20 12:20 usb-Rapoo_Rapoo_Gaming_Device-if01-event-kbd -> ../event3
            match = re.match(r".*?\s+([^\s]+)\s+->\s+\.\.(/event\d+|/mouse\d+|/js\d+)", line)
            if match:
                device_name_id = match.group(1) # e.g., usb-Rapoo_Rapoo_Gaming_Device-if01-event-kbd
                relative_path = match.group(2) # e.g., /event3
                full_path = "/dev/input" + relative_path

                if "event-kbd" in device_name_id:
                    detected_devices["keyboard_event_paths"].append(full_path)
                elif "event-mouse" in device_name_id:
                    detected_devices["mouse_event_paths"].append(full_path)
                elif "event-joystick" in device_name_id:
                    detected_devices["joystick_event_paths"].append(full_path)
                
                # Physical device IDs are typically /dev/input/jsX or /dev/input/mouseX
                # The 'by-id' also lists these directly.
                if "joystick" in device_name_id and relative_path.startswith("/js"):
                    detected_devices["physical_device_ids"].append(full_path)
                elif "mouse" in device_name_id and relative_path.startswith("/mouse"):
                    detected_devices["physical_device_ids"].append(full_path)
        
        # Ensure unique paths
        detected_devices["keyboard_event_paths"] = sorted(list(set(detected_devices["keyboard_event_paths"])))
        detected_devices["mouse_event_paths"] = sorted(list(set(detected_devices["mouse_event_paths"])))
        detected_devices["joystick_event_paths"] = sorted(list(set(detected_devices["joystick_event_paths"])))
        detected_devices["physical_device_ids"] = sorted(list(set(detected_devices["physical_device_ids"])))

        return detected_devices

    def get_audio_devices(self) -> List[str]:
        """
        Detects and returns available audio output devices (sinks).
        Returns a list of audio device IDs (sink names).
        """
        audio_sinks = []
        pactl_output = self._run_command("pactl list short sinks")
        for line in pactl_output.splitlines():
            parts = line.split('\t')
            if len(parts) > 1:
                sink_name = parts[1] # The second column is the sink name/ID
                audio_sinks.append(sink_name)
        return sorted(list(set(audio_sinks))) # Ensure unique and sorted 