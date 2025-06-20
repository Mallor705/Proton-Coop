import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from pathlib import Path
import json
from ..services.device_manager import DeviceManager

class ProfileEditorWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Linux Coop Profile Editor")
        self.set_default_size(1000, 700)

        self.device_manager = DeviceManager()
        self.detected_input_devices = self.device_manager.get_input_devices()
        self.detected_audio_devices = self.device_manager.get_audio_devices()
        
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        # Tab 1: General Settings
        self.general_settings_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.general_settings_page.set_border_width(10)
        self.notebook.append_page(self.general_settings_page, Gtk.Label(label="General Settings"))

        self.general_settings_grid = Gtk.Grid()
        self.general_settings_grid.set_column_spacing(10)
        self.general_settings_grid.set_row_spacing(10)
        self.general_settings_page.pack_start(self.general_settings_grid, False, False, 0)
        self.setup_general_settings()

        # Tab 2: Player Configurations
        self.player_configs_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.player_configs_page.set_border_width(10)
        self.notebook.append_page(self.player_configs_page, Gtk.Label(label="Player Configurations"))
        self.player_config_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5) # This should be outside _create_player_config_uis
        self.player_configs_page.pack_start(self.player_config_vbox, True, True, 0)
        self.setup_player_configs()
        
        self.show_all()

    def setup_general_settings(self):
        row = 0

        # Game Name
        self.general_settings_grid.attach(Gtk.Label(label="Game Name:", xalign=0), 0, row, 1, 1)
        self.game_name_entry = Gtk.Entry()
        self.general_settings_grid.attach(self.game_name_entry, 1, row, 1, 1)
        row += 1

        # Exe Path
        self.general_settings_grid.attach(Gtk.Label(label="Executable Path:", xalign=0), 0, row, 1, 1)
        self.exe_path_entry = Gtk.FileChooserButton(title="Select Game Executable")
        self.general_settings_grid.attach(self.exe_path_entry, 1, row, 1, 1)
        row += 1

        # Num Players
        self.general_settings_grid.attach(Gtk.Label(label="Number of Players:", xalign=0), 0, row, 1, 1)
        self.num_players_spin = Gtk.SpinButton.new_with_range(1, 4, 1)
        self.num_players_spin.connect("value-changed", self.on_num_players_changed)
        self.general_settings_grid.attach(self.num_players_spin, 1, row, 1, 1)
        row += 1

        # Proton Version
        self.general_settings_grid.attach(Gtk.Label(label="Proton Version:", xalign=0), 0, row, 1, 1)
        self.proton_version_entry = Gtk.Entry()
        self.general_settings_grid.attach(self.proton_version_entry, 1, row, 1, 1)
        row += 1

        # Instance Width
        self.general_settings_grid.attach(Gtk.Label(label="Instance Width:", xalign=0), 0, row, 1, 1)
        self.instance_width_spin = Gtk.SpinButton.new_with_range(640, 3840, 1)
        self.instance_width_spin.set_value(1920) # Default from example.json
        self.general_settings_grid.attach(self.instance_width_spin, 1, row, 1, 1)
        row += 1

        # Instance Height
        self.general_settings_grid.attach(Gtk.Label(label="Instance Height:", xalign=0), 0, row, 1, 1)
        self.instance_height_spin = Gtk.SpinButton.new_with_range(480, 2160, 1)
        self.instance_height_spin.set_value(1080) # Default from example.json
        self.general_settings_grid.attach(self.instance_height_spin, 1, row, 1, 1)
        row += 1

        # App ID
        self.general_settings_grid.attach(Gtk.Label(label="App ID:", xalign=0), 0, row, 1, 1)
        self.app_id_entry = Gtk.Entry()
        self.general_settings_grid.attach(self.app_id_entry, 1, row, 1, 1)
        row += 1

        # Game Args
        self.general_settings_grid.attach(Gtk.Label(label="Game Arguments:", xalign=0), 0, row, 1, 1)
        self.game_args_entry = Gtk.Entry()
        self.general_settings_grid.attach(self.game_args_entry, 1, row, 1, 1)
        row += 1

        # Use Goldberg Emu
        self.general_settings_grid.attach(Gtk.Label(label="Use Goldberg Emulator:", xalign=0), 0, row, 1, 1)
        self.use_goldberg_emu_check = Gtk.CheckButton()
        self.use_goldberg_emu_check.set_active(True) # Default from example.json
        self.general_settings_grid.attach(self.use_goldberg_emu_check, 1, row, 1, 1)
        row += 1

        # Mode (splitscreen or not)
        self.general_settings_grid.attach(Gtk.Label(label="Mode:", xalign=0), 0, row, 1, 1)
        self.mode_combo = Gtk.ComboBoxText()
        self.mode_combo.append_text("None")
        self.mode_combo.append_text("splitscreen")
        self.mode_combo.set_active(0) # Default to None
        self.general_settings_grid.attach(self.mode_combo, 1, row, 1, 1)
        self.mode_combo.connect("changed", self.on_mode_changed)
        row += 1

        # Splitscreen Orientation (initially hidden)
        self.splitscreen_orientation_label = Gtk.Label(label="Splitscreen Orientation:", xalign=0)
        self.general_settings_grid.attach(self.splitscreen_orientation_label, 0, row, 1, 1)
        self.splitscreen_orientation_combo = Gtk.ComboBoxText()
        self.splitscreen_orientation_combo.append_text("horizontal")
        self.splitscreen_orientation_combo.append_text("vertical")
        self.splitscreen_orientation_combo.set_active(0) # Default to horizontal
        self.general_settings_grid.attach(self.splitscreen_orientation_combo, 1, row, 1, 1)
        self.splitscreen_orientation_label.hide()
        self.splitscreen_orientation_combo.hide()
        row += 1

        # Env Vars
        env_vars_frame = Gtk.Frame(label="Environment Variables")
        env_vars_frame.set_margin_top(10)
        env_vars_frame.set_margin_bottom(10)
        self.general_settings_grid.attach(env_vars_frame, 0, row, 2, 1) # Span two columns
        
        env_vars_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        env_vars_frame.add(env_vars_vbox)

        self.env_vars_listbox = Gtk.ListBox()
        self.env_vars_listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        env_vars_vbox.pack_start(self.env_vars_listbox, True, True, 0)
        self.env_var_entries = [] # List to store (key_entry, value_entry) tuples

        # Add default env vars
        self._add_env_var_row("WINEDLLOVERRIDES", "")
        self._add_env_var_row("MANGOHUD", "1")

        add_env_var_button = Gtk.Button(label="Add Environment Variable")
        add_env_var_button.connect("clicked", self._on_add_env_var_clicked)
        env_vars_vbox.pack_start(add_env_var_button, False, False, 0)
        row += 1 # Increment row for the next element after env vars frame

        # Save Button (moved to general_settings_page, not grid)
        save_button = Gtk.Button(label="Save Profile")
        save_button.connect("clicked", self.on_save_button_clicked)
        self.general_settings_page.pack_end(save_button, False, False, 0)

    def _on_add_env_var_clicked(self, button):
        self._add_env_var_row()

    def _add_env_var_row(self, key="", value=""):
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        
        key_entry = Gtk.Entry()
        key_entry.set_placeholder_text("Variable Name")
        key_entry.set_hexpand(True)
        key_entry.set_text(key)
        hbox.pack_start(key_entry, True, True, 0)

        value_entry = Gtk.Entry()
        value_entry.set_placeholder_text("Value")
        value_entry.set_hexpand(True)
        value_entry.set_text(value)
        hbox.pack_start(value_entry, True, True, 0)

        remove_button = Gtk.Button(label="-")
        remove_button.set_relief(Gtk.ReliefStyle.NONE)
        remove_button.set_tooltip_text("Remove this environment variable")
        
        # Create a ListBoxRow and add the hbox to it
        list_box_row = Gtk.ListBoxRow()
        list_box_row.add(hbox)

        # Connect the remove button to a lambda that passes the ListBoxRow itself
        remove_button.connect("clicked", lambda btn, row=list_box_row, k_entry=key_entry, v_entry=value_entry: self._remove_env_var_row(btn, row, k_entry, v_entry))
        hbox.pack_end(remove_button, False, False, 0)

        self.env_vars_listbox.add(list_box_row)
        list_box_row.show_all()
        self.env_var_entries.append((key_entry, value_entry, list_box_row)) # Store entries and row for removal

    def _remove_env_var_row(self, button, row, key_entry, value_entry):
        self.env_vars_listbox.remove(row)
        # Remove the tuple from our tracking list
        self.env_var_entries.remove((key_entry, value_entry, row))


    def setup_player_configs(self):
        self.player_frames = [] # To hold a frame for each player's config
        self.player_device_combos = [] # To hold lists of combo boxes for each player
        
        # Initial creation of player config UIs based on default num_players
        self._create_player_config_uis(self.num_players_spin.get_value_as_int())

    def _create_player_config_uis(self, num_players: int):
        # Clear existing player config UIs
        for frame in self.player_frames:
            frame.destroy()
        self.player_frames.clear()
        self.player_device_combos.clear()

        # Clear existing widgets in player_config_vbox before repopulating
        for child in self.player_config_vbox.get_children():
            self.player_config_vbox.remove(child)

        for i in range(num_players):
            player_frame = Gtk.Frame(label=f"Player {i+1} Configuration")
            player_frame.set_margin_top(10)
            self.player_config_vbox.pack_start(player_frame, False, False, 0)
            self.player_frames.append(player_frame)

            player_grid = Gtk.Grid()
            player_grid.set_column_spacing(5)
            player_grid.set_row_spacing(5)
            player_grid.set_border_width(5)
            player_frame.add(player_grid)

            player_combos = {
                "account_name": Gtk.Entry(),
                "language": Gtk.Entry(),
                "listen_port": Gtk.Entry(),
                "user_steam_id": Gtk.Entry(),
                "physical_device_id": Gtk.ComboBoxText(),
                "mouse_event_path": Gtk.ComboBoxText(),
                "keyboard_event_path": Gtk.ComboBoxText(),
                "audio_device_id": Gtk.ComboBoxText()
            }
            self.player_device_combos.append(player_combos)

            # Populate combos with detected devices
            player_combos["physical_device_id"].append_text("None")
            for dev in self.detected_input_devices.get("physical_device_ids", []):
                player_combos["physical_device_id"].append_text(dev)
            player_combos["physical_device_id"].set_active(0)

            player_combos["mouse_event_path"].append_text("None")
            for dev in self.detected_input_devices.get("mouse_event_paths", []):
                player_combos["mouse_event_path"].append_text(dev)
            player_combos["mouse_event_path"].set_active(0)
            
            player_combos["keyboard_event_path"].append_text("None")
            for dev in self.detected_input_devices.get("keyboard_event_paths", []):
                player_combos["keyboard_event_path"].append_text(dev)
            player_combos["keyboard_event_path"].set_active(0)

            player_combos["audio_device_id"].append_text("None")
            for dev in self.detected_audio_devices:
                player_combos["audio_device_id"].append_text(dev)
            player_combos["audio_device_id"].set_active(0)

            # Add fields to player grid
            p_row = 0
            player_grid.attach(Gtk.Label(label="Account Name:", xalign=0), 0, p_row, 1, 1)
            player_grid.attach(player_combos["account_name"], 1, p_row, 1, 1)
            p_row += 1

            player_grid.attach(Gtk.Label(label="Language:", xalign=0), 0, p_row, 1, 1)
            player_grid.attach(player_combos["language"], 1, p_row, 1, 1)
            p_row += 1

            player_grid.attach(Gtk.Label(label="Listen Port:", xalign=0), 0, p_row, 1, 1)
            player_grid.attach(player_combos["listen_port"], 1, p_row, 1, 1)
            p_row += 1

            player_grid.attach(Gtk.Label(label="User Steam ID:", xalign=0), 0, p_row, 1, 1)
            player_grid.attach(player_combos["user_steam_id"], 1, p_row, 1, 1)
            p_row += 1

            player_grid.attach(Gtk.Label(label="Physical Device ID:", xalign=0), 0, p_row, 1, 1)
            player_grid.attach(player_combos["physical_device_id"], 1, p_row, 1, 1)
            p_row += 1

            player_grid.attach(Gtk.Label(label="Mouse Event Path:", xalign=0), 0, p_row, 1, 1)
            player_grid.attach(player_combos["mouse_event_path"], 1, p_row, 1, 1)
            p_row += 1

            player_grid.attach(Gtk.Label(label="Keyboard Event Path:", xalign=0), 0, p_row, 1, 1)
            player_grid.attach(player_combos["keyboard_event_path"], 1, p_row, 1, 1)
            p_row += 1

            player_grid.attach(Gtk.Label(label="Audio Device ID:", xalign=0), 0, p_row, 1, 1)
            player_grid.attach(player_combos["audio_device_id"], 1, p_row, 1, 1)
            p_row += 1
        self.player_config_vbox.show_all()
    
    def on_num_players_changed(self, spin_button):
        num_players = spin_button.get_value_as_int()
        self._create_player_config_uis(num_players)

    def on_mode_changed(self, combo):
        mode = combo.get_active_text()
        if mode == "splitscreen":
            self.splitscreen_orientation_label.show()
            self.splitscreen_orientation_combo.show()
        else:
            self.splitscreen_orientation_label.hide()
            self.splitscreen_orientation_combo.hide()

    def on_save_button_clicked(self, button):
        print("Save button clicked!")
        profile_data = self.get_profile_data()
        
        # Save the profile data to a JSON file
        profile_name = self.game_name_entry.get_text().replace(" ", "_").lower()
        if not profile_name:
            # Handle case where game name is empty
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK,
                                       "Game Name cannot be empty.")
            dialog.run()
            dialog.destroy()
            return

        profile_dir = Path.home() / ".config/linux-coop/profiles"
        profile_dir.mkdir(parents=True, exist_ok=True)
        profile_path = profile_dir / f"{profile_name}.json"

        try:
            with open(profile_path, "w", encoding="utf-8") as f:
                json.dump(profile_data, f, indent=2)
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK,
                                       f"Profile saved successfully to {profile_path}")
            dialog.run()
            dialog.destroy()
        except Exception as e:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK,
                                       f"Error saving profile: {e}")
            dialog.run()
            dialog.destroy()


    def get_profile_data(self):
        profile = {
            "GAME_NAME": self.game_name_entry.get_text(),
            "EXE_PATH": self.exe_path_entry.get_filename(),
            "NUM_PLAYERS": self.num_players_spin.get_value_as_int(),
            "PROTON_VERSION": self.proton_version_entry.get_text() if self.proton_version_entry.get_text() else None,
            "INSTANCE_WIDTH": self.instance_width_spin.get_value_as_int(),
            "INSTANCE_HEIGHT": self.instance_height_spin.get_value_as_int(),
            "APP_ID": self.app_id_entry.get_text() if self.app_id_entry.get_text() else None,
            "GAME_ARGS": self.game_args_entry.get_text() if self.game_args_entry.get_text() else None,
            "USE_GOLDBERG_EMU": self.use_goldberg_emu_check.get_active(),
            "ENV_VARS": {}, # Initialize empty dict for env vars
            "MODE": self.mode_combo.get_active_text() if self.mode_combo.get_active_text() != "None" else None,
        }

        # Populate ENV_VARS from the ListBox
        for key_entry, value_entry, _ in self.env_var_entries:
            key = key_entry.get_text().strip()
            value = value_entry.get_text().strip()
            if key:
                profile["ENV_VARS"][key] = value

        if profile["MODE"] == "splitscreen":
            profile["SPLITSCREEN"] = {
                "ORIENTATION": self.splitscreen_orientation_combo.get_active_text()
            }
        
        profile["PLAYERS"] = []
        profile["PLAYER_PHYSICAL_DEVICE_IDS"] = []
        profile["PLAYER_MOUSE_EVENT_PATHS"] = []
        profile["PLAYER_KEYBOARD_EVENT_PATHS"] = []
        profile["PLAYER_AUDIO_DEVICE_IDS"] = []

        for i in range(self.num_players_spin.get_value_as_int()):
            player_combos = self.player_device_combos[i]
            player_config = {
                "ACCOUNT_NAME": player_combos["account_name"].get_text() or f"Player{i+1}",
                "LANGUAGE": player_combos["language"].get_text() or "brazilian",
                "LISTEN_PORT": player_combos["listen_port"].get_text() or "47584",
                "USER_STEAM_ID": player_combos["user_steam_id"].get_text() or f"7656119000000000{i+1}"
            }
            profile["PLAYERS"].append(player_config)

            # Collect device paths for top-level lists
            profile["PLAYER_PHYSICAL_DEVICE_IDS"].append(player_combos["physical_device_id"].get_active_text() if player_combos["physical_device_id"].get_active_text() != "None" else "")
            profile["PLAYER_MOUSE_EVENT_PATHS"].append(player_combos["mouse_event_path"].get_active_text() if player_combos["mouse_event_path"].get_active_text() != "None" else "")
            profile["PLAYER_KEYBOARD_EVENT_PATHS"].append(player_combos["keyboard_event_path"].get_active_text() if player_combos["keyboard_event_path"].get_active_text() != "None" else "")
            profile["PLAYER_AUDIO_DEVICE_IDS"].append(player_combos["audio_device_id"].get_active_text() if player_combos["audio_device_id"].get_active_text() != "None" else "")

        return profile


class LinuxCoopApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.linuxcoop.app")

    def do_activate(self):
        window = ProfileEditorWindow(self)
        window.show_all()

def run_gui():
    app = LinuxCoopApp()
    app.run(None)

if __name__ == "__main__":
    run_gui() 