import gi
import os
from ..models.profile import Profile, SplitscreenConfig, PlayerInstanceConfig

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from ..services.device_manager import DeviceManager
from gi.repository import Adw, Gdk, GObject, Gtk

class LayoutSettingsPage(Adw.PreferencesPage):
    __gsignals__ = {
        "settings-changed": (GObject.SIGNAL_RUN_FIRST, None, ()),
    }

    def __init__(self, profile, logger, **kwargs):
        super().__init__(**kwargs)
        self._is_loading = False
        self.profile = profile
        self.player_rows = []
        self.logger = logger

        self.device_manager = DeviceManager()
        self.input_devices = self.device_manager.get_input_devices()
        self.audio_devices = self.device_manager.get_audio_devices()
        self.display_outputs = self.device_manager.get_display_outputs()

        self._build_ui()
        self.load_profile_data()

    def _build_ui(self):
        self.set_title("Layout Settings")

        layout_group = Adw.PreferencesGroup(title="General Layout")
        self.add(layout_group)

        self.num_players_row = Adw.SpinRow(
            title="Number of Instances",
            subtitle="How many Steam instances to launch",
        )
        adjustment = Gtk.Adjustment(value=2, lower=1, upper=8, step_increment=1)
        self.num_players_row.set_adjustment(adjustment)
        adjustment.connect("value-changed", self._on_num_players_changed)
        layout_group.add(self.num_players_row)

        self.resolutions = ["Custom", "1920x1080", "2560x1440", "1280x720", "800x600"]
        self.resolution_row = Adw.ComboRow(
            title="Base Resolution", model=Gtk.StringList.new(self.resolutions)
        )
        self.resolution_row.connect("notify::selected-item", self._on_resolution_changed)
        self.resolution_row.connect("notify::selected-item", self._on_setting_changed)
        layout_group.add(self.resolution_row)

        self.instance_width_row = Adw.EntryRow(title="Custom Width")
        self.instance_width_row.connect("changed", self._on_setting_changed)
        layout_group.add(self.instance_width_row)

        self.instance_height_row = Adw.EntryRow(title="Custom Height")
        self.instance_height_row.connect("changed", self._on_setting_changed)
        layout_group.add(self.instance_height_row)
        
        self.screen_modes = ["Fullscreen", "Splitscreen"]
        self.screen_mode_row = Adw.ComboRow(
            title="Screen Mode", model=Gtk.StringList.new(self.screen_modes)
        )
        self.screen_mode_row.connect("notify::selected-item", self._on_screen_mode_changed)
        layout_group.add(self.screen_mode_row)

        self.orientations = ["Horizontal", "Vertical"]
        self.orientation_row = Adw.ComboRow(
            title="Splitscreen Orientation", model=Gtk.StringList.new(self.orientations)
        )
        self.orientation_row.connect("notify::selected-item", self._on_setting_changed)
        layout_group.add(self.orientation_row)

        self.players_group = Adw.PreferencesGroup(title="Instance Configurations")
        self.add(self.players_group)

    def load_profile_data(self):
        self._is_loading = True
        
        adj = self.num_players_row.get_adjustment()
        adj.set_value(self.profile.num_players)

        res_str = f"{self.profile.instance_width}x{self.profile.instance_height}"
        if res_str in self.resolutions:
            self.resolution_row.set_selected(self.resolutions.index(res_str))
        else:
            self.resolution_row.set_selected(0) # Custom
        
        self.instance_width_row.set_text(str(self.profile.instance_width or ""))
        self.instance_height_row.set_text(str(self.profile.instance_height or ""))
        
        is_custom = self.resolution_row.get_selected() == 0
        self.instance_width_row.set_visible(is_custom)
        self.instance_height_row.set_visible(is_custom)

        is_splitscreen = self.profile.mode == "splitscreen"
        self.screen_mode_row.set_selected(1 if is_splitscreen else 0)
        self.orientation_row.set_visible(is_splitscreen)

        if is_splitscreen and self.profile.splitscreen:
            orientation = self.profile.splitscreen.orientation.capitalize()
            self.orientation_row.set_selected(self.orientations.index(orientation))
        
        self.rebuild_player_rows()
        for i, row_dict in enumerate(self.player_rows):
            if i < len(self.profile.player_configs):
                config = self.profile.player_configs[i]
                self._set_combo_row_selection(row_dict["joystick"], self.input_devices["joystick"], config.PHYSICAL_DEVICE_ID)
                self._set_combo_row_selection(row_dict["mouse"], self.input_devices["mouse"], config.MOUSE_EVENT_PATH)
                self._set_combo_row_selection(row_dict["keyboard"], self.input_devices["keyboard"], config.KEYBOARD_EVENT_PATH)
                self._set_combo_row_selection(row_dict["audio"], self.audio_devices, config.AUDIO_DEVICE_ID)
        
        self._is_loading = False

    def _set_combo_row_selection(self, combo_row, device_list, device_id):
        if not device_id:
            combo_row.set_selected(0)
            return
        
        try:
            canonical_id = os.path.realpath(device_id)
            for i, device in enumerate(device_list):
                if os.path.realpath(device["id"]) == canonical_id:
                    combo_row.set_selected(i + 1)
                    return
        except Exception as e:
            self.logger.error(f"Error matching device {device_id}: {e}")

        combo_row.set_selected(0)

    def get_updated_data(self) -> Profile:
        self.profile.num_players = int(self.num_players_row.get_value())
        
        selected_res = self.resolution_row.get_selected_item().get_string()
        if selected_res == "Custom":
            self.profile.instance_width = int(self.instance_width_row.get_text() or 0)
            self.profile.instance_height = int(self.instance_height_row.get_text() or 0)
        else:
            width, height = map(int, selected_res.split("x"))
            self.profile.instance_width = width
            self.profile.instance_height = height
            
        self.profile.mode = self.screen_mode_row.get_selected_item().get_string().lower()
        if self.profile.mode == "splitscreen":
            orientation = self.orientation_row.get_selected_item().get_string().lower()
            self.profile.splitscreen = SplitscreenConfig(orientation=orientation)
        else:
            self.profile.splitscreen = None

        new_configs = []
        for i in range(self.profile.num_players):
            if i < len(self.player_rows):
                row_dict = self.player_rows[i]
                new_config = PlayerInstanceConfig(
                    PHYSICAL_DEVICE_ID=self._get_combo_row_device_id(row_dict["joystick"], self.input_devices["joystick"]),
                    MOUSE_EVENT_PATH=self._get_combo_row_device_id(row_dict["mouse"], self.input_devices["mouse"]),
                    KEYBOARD_EVENT_PATH=self._get_combo_row_device_id(row_dict["keyboard"], self.input_devices["keyboard"]),
                    AUDIO_DEVICE_ID=self._get_combo_row_device_id(row_dict["audio"], self.audio_devices),
                )
                new_configs.append(new_config)
            else:
                new_configs.append(PlayerInstanceConfig()) # Add empty config for new players
        self.profile.player_configs = new_configs
        
        return self.profile

    def _on_setting_changed(self, *args):
        if not self._is_loading:
            self.emit("settings-changed")

    def _on_num_players_changed(self, adjustment):
        if not self._is_loading:
            self.rebuild_player_rows()
            self.emit("settings-changed")

    def _on_resolution_changed(self, combo_row, *args):
        is_custom = combo_row.get_selected() == 0
        self.instance_width_row.set_visible(is_custom)
        self.instance_height_row.set_visible(is_custom)
        if not self._is_loading:
            self.emit("settings-changed")

    def _on_screen_mode_changed(self, combo_row, *args):
        is_splitscreen = combo_row.get_selected_item().get_string().lower() == "splitscreen"
        self.orientation_row.set_visible(is_splitscreen)
        if not self._is_loading:
            self.emit("settings-changed")

    def rebuild_player_rows(self):
        for row_dict in self.player_rows:
            self.players_group.remove(row_dict["expander"])
        self.player_rows = []

        num_players = int(self.num_players_row.get_value())
        # Ensure player_configs list is long enough
        while len(self.profile.player_configs) < num_players:
            self.profile.player_configs.append(PlayerInstanceConfig())

        for i in range(num_players):
            expander = Adw.ExpanderRow(title=f"Instance {i + 1}")
            self.players_group.add(expander)

            checkbox = Gtk.CheckButton()
            checkbox.set_active(True)
            expander.add_prefix(checkbox)

            def create_device_row(title, device_type):
                devices = self.input_devices.get(device_type, [])
                model = Gtk.StringList.new(["None"] + [d["name"] for d in devices])
                row = Adw.ComboRow(title=title, model=model)
                row.connect("notify::selected-item", self._on_setting_changed)
                expander.add_row(row)
                return row

            joystick_row = create_device_row("Gamepad", "joystick")
            mouse_row = create_device_row("Mouse", "mouse")
            keyboard_row = create_device_row("Keyboard", "keyboard")

            audio_model = Gtk.StringList.new(["None"] + [d["name"] for d in self.audio_devices])
            audio_row = Adw.ComboRow(title="Audio Device", model=audio_model)
            audio_row.connect("notify::selected-item", self._on_setting_changed)
            expander.add_row(audio_row)

            self.player_rows.append({
                "checkbox": checkbox,
                "expander": expander,
                "joystick": joystick_row,
                "mouse": mouse_row,
                "keyboard": keyboard_row,
                "audio": audio_row,
            })

    def get_selected_players(self) -> list[int]:
        return [i + 1 for i, r in enumerate(self.player_rows) if r["checkbox"].get_active()]

    def _get_combo_row_device_id(self, combo_row, device_list):
        selected_idx = combo_row.get_selected()
        if selected_idx > 0 and (selected_idx - 1) < len(device_list):
            return device_list[selected_idx - 1]["id"]
        return None
