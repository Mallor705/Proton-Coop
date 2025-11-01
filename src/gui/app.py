import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gdk, GLib
from pathlib import Path
import json
import subprocess
import os
import signal
import time
import cairo
import sys
from typing import Dict, List, Tuple, Any, Optional

from ..services.device_manager import DeviceManager
from ..services.proton import ProtonService
from ..services.game_manager import GameManager
from ..models.game import Game
from ..models.profile import Profile, GameProfile, PlayerInstanceConfig, SplitscreenConfig
from ..core.logger import Logger
from ..core.config import Config
from .styles import initialize_styles, get_style_manager, StyleManagerError

class ProfileEditorWindow(Adw.ApplicationWindow):
    """
    The main window for the Linux Coop application.

    This class builds and manages the entire graphical user interface, including
    the game/profile library view, configuration tabs, and all associated

    widgets and logic for creating, loading, saving, and launching games.
    """
    def __init__(self, app):
        super().__init__(application=app, title="Linux Coop")
        self.set_default_size(1200, 800)

        # --- Main Layout with ToolbarView ---
        toolbar_view = Adw.ToolbarView()
        self.set_content(toolbar_view)

        # --- Header Bar ---
        header_bar = Adw.HeaderBar()
        toolbar_view.add_top_bar(header_bar)

        # --- Footer Bar ---
        self.footer_bar = Adw.HeaderBar()
        self.footer_bar.set_show_end_title_buttons(False)
        toolbar_view.add_bottom_bar(self.footer_bar)


        # Services and Managers
        self.logger = Logger(name="LinuxCoopGUI", log_dir=Config.LOG_DIR)
        self.game_manager = GameManager(self.logger)
        self.device_manager = DeviceManager()
        self.proton_service = ProtonService(self.logger)

        # State Tracking
        self.selected_game: Optional[Game] = None
        self.selected_profile: Optional[Profile] = None
        self.cli_process_pid: Optional[int] = None
        self.monitoring_timeout_id: Optional[int] = None
        self.game_row_to_profile_list: Dict[Adw.ExpanderRow, Gtk.ListBox] = {}

        # --- Initialize UI Widgets ---
        self._initialize_widgets()

        # --- Header Bar Actions (Now empty) ---

        # Main Layout
        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        toolbar_view.set_content(main_vbox)

        self.main_paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        main_vbox.append(self.main_paned)

        # --- Left Pane: Game and Profile Library ---
        self.sidebar_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.sidebar_vbox.set_size_request(250, -1)
        self.main_paned.set_start_child(self.sidebar_vbox)

        # Adwaita ListBox for games and profiles
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_vexpand(True)
        self.sidebar_vbox.append(scrolled_window)

        self.game_list_group = Adw.PreferencesGroup()
        scrolled_window.set_child(self.game_list_group)

        # Action Buttons
        self.add_game_button = Gtk.Button(label="➕ Add Game")
        self.add_game_button.set_tooltip_text("Add a new game to the library")
        self.add_game_button.connect("clicked", self._on_add_game_clicked)
        self.footer_bar.pack_start(self.add_game_button)

        self.delete_button = Gtk.Button(label="🗑️")
        self.delete_button.add_css_class("destructive-action")
        self.delete_button.set_tooltip_text("Delete selected game or profile")
        self.delete_button.set_sensitive(False)
        self.delete_button.connect("clicked", self._on_delete_clicked)
        self.footer_bar.pack_start(self.delete_button)

        # --- Right Pane: Configuration Notebook ---
        right_pane_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        right_pane_vbox.set_vexpand(True)
        right_pane_vbox.set_hexpand(True)
        self.main_paned.set_end_child(right_pane_vbox)

        # Use Adw.ViewStack and Adw.ViewSwitcher for a modern tabbed view
        self.view_stack = Adw.ViewStack()
        self.view_switcher = Adw.ViewSwitcher()
        self.view_switcher.set_stack(self.view_stack)

        # Add the ViewSwitcher to the HeaderBar and the ViewStack to the main content
        header_bar.set_title_widget(self.view_switcher)
        right_pane_vbox.append(self.view_stack)

        # --- Action Buttons (now in footer) ---

        self.save_button = Gtk.Button(label="💾 Save")
        self.save_button.connect("clicked", self.on_save_button_clicked)
        self.save_button.set_sensitive(False)
        self.footer_bar.pack_end(self.save_button)

        self.play_button = Gtk.Button(label="▶️ Launch")
        self.play_button.connect("clicked", self.on_play_button_clicked)
        self.play_button.set_sensitive(False)
        self.footer_bar.pack_end(self.play_button)

        # --- Setup Configuration Tabs ---
        self.setup_game_settings_tab()
        self.setup_profile_settings_tab()
        self.setup_window_layout_tab()

        # --- Connect Signals ---
        self._connect_layout_signals()

        # --- Finalize Initialization ---

        self.show()
        self._update_action_buttons_state()
        self._populate_game_library()
        self.connect("close-request", self._on_close_request)

    def _initialize_widgets(self):
        """Initializes all configuration widgets used across the UI."""
        # --- Device Detection ---
        self.detected_input_devices = self.device_manager.get_input_devices()
        self.detected_audio_devices = self.device_manager.get_audio_devices()
        self.detected_display_outputs = self.device_manager.get_display_outputs()

        self.device_name_to_id = {"None": None}
        self.device_id_to_name = {None: "None"}

        self.device_lists = {
            "joystick": [{"name": "None", "id": None}] + self.detected_input_devices.get("joystick", []),
            "mouse": [{"name": "None", "id": None}] + self.detected_input_devices.get("mouse", []),
            "keyboard": [{"name": "None", "id": None}] + self.detected_input_devices.get("keyboard", []),
            "audio": [{"name": "None", "id": None}] + self.detected_audio_devices,
            "display": [{"name": "None", "id": None}] + self.detected_display_outputs
        }

        for device_type in ["joystick", "mouse", "keyboard"]:
            for device in self.detected_input_devices.get(device_type, []):
                self.device_name_to_id[device["name"]] = device["id"]
                self.device_id_to_name[device["id"]] = device["name"]

        for device in self.detected_audio_devices:
            self.device_name_to_id[device["name"]] = device["id"]
            self.device_id_to_name[device["id"]] = device["name"]

        for device in self.detected_display_outputs:
            self.device_name_to_id[device["name"]] = device["id"]
            self.device_id_to_name[device["id"]] = device["name"]

        # --- Game Details ---
        self.game_name_entry = Gtk.Entry(placeholder_text="Ex: Palworld")
        self.exe_path_entry = Gtk.Entry(placeholder_text="~/.steam/steamapps/common/Palworld/Palworld.exe")
        self.app_id_entry = Gtk.Entry(placeholder_text="Optional (ex: 1621530)")
        self.game_args_entry = Gtk.Entry(placeholder_text="Optional (ex: -EpicPortal)")
        self.is_native_check = Gtk.CheckButton()

        # --- Profile Details ---
        self.profile_name_entry = Gtk.Entry(placeholder_text="Ex: Coop Campaign, Modded Playthrough")
        self.profile_selector_combo = Gtk.ComboBoxText()
        self.add_profile_button = Gtk.Button(label="➕")
        self.delete_profile_button = Gtk.Button(label="🗑️")

        # --- Launch Options ---
        self.proton_version_combo = Gtk.ComboBoxText()
        proton_versions = self.proton_service.list_installed_proton_versions()
        if not proton_versions:
            self.proton_version_combo.append_text("No Proton versions found")
            self.proton_version_combo.set_sensitive(False)
        else:
            self.proton_version_combo.append_text("None (Use Steam default)")
            for version in proton_versions:
                self.proton_version_combo.append_text(version)
            self.proton_version_combo.set_active(0)

        self.apply_dxvk_vkd3d_check = Gtk.CheckButton(active=True)
        self.winetricks_verbs_entry = Gtk.Entry(placeholder_text="Optional (e.g., vcrun2019 dotnet48)")

        # --- Layout & Display ---
        self.num_players_spin = Gtk.SpinButton.new_with_range(1, 4, 1)
        self.instance_width_spin = Gtk.SpinButton.new_with_range(640, 7680, 1)
        self.instance_height_spin = Gtk.SpinButton.new_with_range(480, 4320, 1)
        self.mode_combo = Gtk.ComboBoxText()
        self.mode_combo.append("fullscreen", "Fullscreen")
        self.mode_combo.append("splitscreen", "Splitscreen")
        self.splitscreen_orientation_combo = Gtk.ComboBoxText()
        self.splitscreen_orientation_combo.append("horizontal", "Horizontal")
        self.splitscreen_orientation_combo.append("vertical", "Vertical")

        # --- Environment Variables ---
        self.env_var_entries: List[Tuple[Gtk.Entry, Gtk.Entry, Adw.ActionRow]] = []

        # --- Player Configs ---
        self.player_config_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.player_frames = []
        self.player_device_combos = []
        self.player_checkboxes = []

        # --- Preview ---
        self.drawing_area = Gtk.DrawingArea(hexpand=True, vexpand=True, width_request=200, height_request=200)

    def setup_game_settings_tab(self):
        """Sets up the 'Game Settings' tab."""
        page_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15, margin_start=10, margin_end=10, margin_top=10, margin_bottom=10)
        scrolled_window = Gtk.ScrolledWindow(hscrollbar_policy=Gtk.PolicyType.NEVER, vscrollbar_policy=Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_child(page_vbox)

        # Add page to ViewStack
        self.view_stack.add_titled_with_icon(
            scrolled_window,
            "game_settings",
            "Game Settings",
            "applications-games-symbolic"
        )

        # --- Game Details Group ---
        game_details_group = Adw.PreferencesGroup(title="Game Details")
        page_vbox.append(game_details_group)

        # Game Name
        self.game_name_row = Adw.EntryRow(title="Game Name")
        game_details_group.add(self.game_name_row)

        # Executable Path
        self.exe_path_row = Adw.EntryRow(title="Executable Path")
        exe_path_button = Gtk.Button(label="Browse...")
        exe_path_button.connect("clicked", self.on_exe_path_button_clicked)
        self.exe_path_row.add_suffix(exe_path_button)
        game_details_group.add(self.exe_path_row)

        # App ID
        self.app_id_row = Adw.EntryRow(title="App ID (Steam)")
        game_details_group.add(self.app_id_row)

        # Game Arguments
        self.game_args_row = Adw.EntryRow(title="Game Arguments")
        game_details_group.add(self.game_args_row)

        # Is Native
        self.is_native_row = Adw.ActionRow(title="Is Native Game (Linux)?")
        self.is_native_check = Gtk.CheckButton()
        self.is_native_row.add_suffix(self.is_native_check)
        self.is_native_row.set_activatable_widget(self.is_native_check)
        game_details_group.add(self.is_native_row)

        # --- Profiles Group ---
        profiles_group = Adw.PreferencesGroup(title="Profiles")
        page_vbox.append(profiles_group)

        # Profile Selector
        self.profile_selector_row = Adw.ActionRow(title="Select Profile")
        self.profile_selector_combo.set_hexpand(True)
        self.profile_selector_row.add_suffix(self.profile_selector_combo)
        self.add_profile_button.set_tooltip_text("Add a new profile")
        self.add_profile_button.connect("clicked", self._on_add_profile_clicked)
        self.profile_selector_row.add_suffix(self.add_profile_button)
        self.delete_profile_button.set_tooltip_text("Delete selected profile")
        self.delete_profile_button.add_css_class("destructive-action")
        self.delete_profile_button.connect("clicked", self._on_delete_clicked)
        self.profile_selector_row.add_suffix(self.delete_profile_button)
        self.profile_selector_combo.connect("changed", self._on_profile_selected_from_combo)
        profiles_group.add(self.profile_selector_row)

        # --- Launch Options Group ---
        launch_options_group = Adw.PreferencesGroup(title="Launch Options")
        page_vbox.append(launch_options_group)

        # Proton Version
        self.proton_version_row = Adw.ActionRow(title="Proton Version")
        self.proton_version_row.add_suffix(self.proton_version_combo)
        launch_options_group.add(self.proton_version_row)

        # DXVK/VKD3D
        self.apply_dxvk_vkd3d_row = Adw.ActionRow(title="Apply DXVK/VKD3D")
        self.apply_dxvk_vkd3d_row.add_suffix(self.apply_dxvk_vkd3d_check)
        self.apply_dxvk_vkd3d_row.set_activatable_widget(self.apply_dxvk_vkd3d_check)
        launch_options_group.add(self.apply_dxvk_vkd3d_row)

        # Winetricks
        self.winetricks_verbs_row = Adw.EntryRow(title="Winetricks Verbs")
        launch_options_group.add(self.winetricks_verbs_row)

        # --- Environment Variables Group ---
        self.env_vars_group = Adw.PreferencesGroup(title="Custom Environment Variables")
        page_vbox.append(self.env_vars_group)

        add_env_var_button = Gtk.Button(label="Add Variable")
        add_env_var_button.connect("clicked", self._on_add_env_var_clicked)

        self.add_button_row = Adw.ActionRow()
        self.add_button_row.add_suffix(add_env_var_button)
        self.add_button_row.set_title("Add New Variable")
        self.env_vars_group.add(self.add_button_row)

        self._add_env_var_row("WINEDLLOVERRIDES", "")
        self._add_env_var_row("MANGOHUD", "1")

    def setup_profile_settings_tab(self):
        """Sets up the 'Profile Settings' tab."""
        page_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15, margin_start=10, margin_end=10, margin_top=10, margin_bottom=10)
        scrolled_window = Gtk.ScrolledWindow(hscrollbar_policy=Gtk.PolicyType.NEVER, vscrollbar_policy=Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_child(page_vbox)

        # Add page to ViewStack
        self.view_stack.add_titled_with_icon(
            scrolled_window,
            "profile_settings",
            "Profile Settings",
            "document-properties-symbolic"
        )


        # --- Profile Details ---
        profile_details_group = Adw.PreferencesGroup(title="Profile Details")
        page_vbox.append(profile_details_group)
        self.profile_name_row = Adw.EntryRow(title="Profile Name")
        profile_details_group.add(self.profile_name_row)

        # --- Layout and Display ---
        # --- Player Configurations ---
        players_frame = Gtk.Frame(label="Player Configurations")
        page_vbox.append(players_frame)
        players_frame.set_child(self.player_config_vbox)

    def setup_window_layout_tab(self):
        """Sets up the 'Window Layout' preview tab."""
        page = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin_start=10, margin_end=10, margin_top=10, margin_bottom=10)

        # Add page to ViewStack
        self.view_stack.add_titled_with_icon(
            page,
            "window_layout",
            "Window Layout",
            "video-display-symbolic"
        )

        # --- Settings Panel (Left) ---
        settings_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        settings_panel.set_size_request(300, -1)
        page.append(settings_panel)

        layout_group = Adw.PreferencesGroup()
        settings_panel.append(layout_group)

        # Number of Players
        self.num_players_row = Adw.SpinRow.new_with_range(1, 4, 1)
        self.num_players_row.set_title("Number of Players")
        layout_group.add(self.num_players_row)

        # Instance Width
        self.instance_width_row = Adw.SpinRow.new_with_range(640, 7680, 1)
        self.instance_width_row.set_title("Instance Width")
        layout_group.add(self.instance_width_row)

        # Instance Height
        self.instance_height_row = Adw.SpinRow.new_with_range(480, 4320, 1)
        self.instance_height_row.set_title("Instance Height")
        layout_group.add(self.instance_height_row)

        # Mode
        self.mode_row = Adw.ComboRow(title="Mode", model=Gtk.StringList.new(["Fullscreen", "Splitscreen"]))
        layout_group.add(self.mode_row)

        # Splitscreen Orientation
        self.splitscreen_orientation_row = Adw.ComboRow(title="Orientation", model=Gtk.StringList.new(["Horizontal", "Vertical"]))
        layout_group.add(self.splitscreen_orientation_row)

        # --- Preview Panel (Right) ---
        preview_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5, hexpand=True, vexpand=True)
        page.append(preview_panel)

        preview_label = Gtk.Label(label="Preview", halign=Gtk.Align.START, margin_bottom=5)
        preview_label.add_css_class("heading")
        preview_panel.append(preview_label)

        self.drawing_area.set_draw_func(self.on_draw_window_layout)
        preview_panel.append(self.drawing_area)

    def _connect_layout_signals(self):
        """Connects signals for widgets that affect the layout preview."""
        self.instance_width_row.connect("notify::value", self.on_layout_setting_changed)
        self.instance_height_row.connect("notify::value", self.on_layout_setting_changed)
        self.num_players_row.connect("notify::value", self.on_layout_setting_changed)
        self.mode_row.connect("notify::selected", self.on_layout_setting_changed)
        self.splitscreen_orientation_row.connect("notify::selected", self.on_layout_setting_changed)

        # Specific handlers
        self.mode_row.connect("notify::selected", self.on_mode_changed)
        self.num_players_row.connect("notify::value", self.on_num_players_changed)

    def _update_action_buttons_state(self):
        """Updates the sensitivity of all action buttons based on the current selection."""
        game_selected = self.selected_game is not None
        profile_selected = self.selected_profile is not None

        # Sidebar buttons
        self.delete_button.set_sensitive(game_selected) # The main delete button now only deletes games

        # Game Settings tab buttons
        self.add_profile_button.set_sensitive(game_selected)
        self.delete_profile_button.set_sensitive(profile_selected)

        # Bottom-bar buttons
        self.save_button.set_sensitive(game_selected) # Can always save game settings
        self.play_button.set_sensitive(profile_selected) # Can only launch with a profile

        # Play/Stop button state
        if self.cli_process_pid:
            self.play_button.set_label("⏹️ Stop")
            self.play_button.get_style_context().add_class("destructive-action")
            self.play_button.get_style_context().remove_class("suggested-action")
        else:
            self.play_button.set_label("▶️ Launch")
            self.play_button.get_style_context().add_class("suggested-action")
            self.play_button.get_style_context().remove_class("destructive-action")

    def on_exe_path_button_clicked(self, button):
        """Handles the 'Browse...' button click to select a game executable."""
        dialog = Gtk.FileChooserDialog(
            title="Select Game Executable",
            action=Gtk.FileChooserAction.OPEN
        )

        # Set parent after creation for GTK4 compatibility
        dialog.set_transient_for(self)
        dialog.set_modal(True)

        # Add buttons manually for GTK4 compatibility
        dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("_Open", Gtk.ResponseType.OK)

        dialog.connect("response", self._on_exe_path_dialog_response)
        dialog.present()

    def _on_exe_path_dialog_response(self, dialog, response):
        """Handles the response from the file chooser dialog for the executable path."""
        if response == Gtk.ResponseType.OK:
            file = dialog.get_file()
            if file:
                self.exe_path_entry.set_text(file.get_path())
        dialog.destroy()

    def _populate_game_library(self):
        """Populates the Adwaita list with games and profiles."""
        # Clear existing rows - GTK4 compatible way
        while child := self.game_list_group.get_first_child():
            self.game_list_group.remove(child)
        self.game_row_to_profile_list.clear()

        games = self.game_manager.get_games()
        for game in games:
            profiles = self.game_manager.get_profiles(game)
            game_row = Adw.ExpanderRow(title=game.game_name, subtitle=f"{len(profiles)} profiles")
            game_row.connect("activated", self._on_game_row_selected, game)
            self.game_list_group.add(game_row)

            for profile in profiles:
                profile_row = Adw.ActionRow(title=profile.profile_name)
                profile_row.set_activatable(True)
                profile_row.connect("activated", self._on_profile_row_selected, game, profile)
                game_row.add_row(profile_row)

    def _on_game_row_selected(self, row, game):
        """Handles when a game's ExpanderRow is selected."""
        self.selected_game = game
        self.selected_profile = None
        self._clear_all_fields()
        self._load_game_data(game)
        self._populate_profile_selector(game) # Keep this to update the combo on the settings page
        self._set_fields_sensitivity(is_game_selected=True, is_profile_selected=False)
        self._update_action_buttons_state()

    def _on_profile_row_selected(self, row, game, profile):
        """Handles when a profile row is selected."""
        self.selected_game = game
        self.selected_profile = profile
        self._load_profile_data(game, profile)
        self._set_fields_sensitivity(is_game_selected=True, is_profile_selected=True)
        self._update_action_buttons_state()

        # Ensure the correct profile is highlighted in the combo box
        if self.profile_selector_combo.get_model():
            model = self.profile_selector_combo.get_model()
            for i in range(model.get_n_items()):
                if self.profile_selector_combo.get_model().get_string(i) == profile.profile_name:
                    self.profile_selector_combo.set_active(i)
                    break

    def _populate_profile_selector(self, game: Optional[Game]):
        """Populates the profile selector ComboBox with profiles for the given game."""
        self.profile_selector_combo.remove_all()
        if game:
            profiles = self.game_manager.get_profiles(game)
            for profile in profiles:
                self.profile_selector_combo.append(profile.profile_name, profile.profile_name)
        self.profile_selector_combo.set_active(-1)

    def _on_profile_selected_from_combo(self, combo):
        """Handles selection changes in the profile ComboBox."""
        profile_name = combo.get_active_text()
        if profile_name and self.selected_game:
            profiles = self.game_manager.get_profiles(self.selected_game)
            self.selected_profile = next((p for p in profiles if p.profile_name == profile_name), None)
            if self.selected_profile:
                self._load_profile_data(self.selected_game, self.selected_profile)
                self._set_fields_sensitivity(is_game_selected=True, is_profile_selected=True)
        else:
            self.selected_profile = None
            # Re-load game data to clear profile-specific fields
            if self.selected_game:
                self._load_game_data(self.selected_game)
            self._set_fields_sensitivity(is_game_selected=(self.selected_game is not None), is_profile_selected=False)

        self._update_action_buttons_state()

    def _select_item_in_library(self, game_name: str, profile_name: Optional[str] = None):
        """Programmatically selects a game and profile in the new Adwaita list."""
        for game_row in self.game_list_group:
            if game_row.get_title() == game_name:
                game_row.set_expanded(True)
                if profile_name:
                    # Iterate through the ActionRows directly added to the ExpanderRow
                    for i in range(game_row.get_n_rows()):
                        profile_row = game_row.get_row_at_index(i)
                        if isinstance(profile_row, Adw.ActionRow) and profile_row.get_title() == profile_name:
                            profile_row.emit("activated")
                            # Visually highlight the row if possible (Adw.ActionRow is not selectable, activation is enough)
                            break
                else:
                    # Just activate the game row if no profile is specified
                    game_row.emit("activated")
                break

    def _on_add_env_var_clicked(self, button):
        """Handles the 'Add Variable' button click for environment variables."""
        self._add_env_var_row()

    def _add_env_var_row(self, key="", value=""):
        """Adds a new row for an environment variable."""
        row = Adw.ActionRow()

        key_entry = Gtk.Entry(placeholder_text="Variable Name", hexpand=True, text=key)
        row.add_suffix(key_entry)

        value_entry = Gtk.Entry(placeholder_text="Value", hexpand=True, text=value)
        row.add_suffix(value_entry)

        remove_button = Gtk.Button(icon_name="edit-delete-symbolic")
        remove_button.add_css_class("flat")
        remove_button.set_tooltip_text("Remove this environment variable")
        row.add_suffix(remove_button)

        # Insert the new row before the "Add Variable" button
        self.env_vars_group.add(row)
        self.env_vars_group.remove(self.add_button_row)
        self.env_vars_group.add(self.add_button_row)

        entry_tuple = (key_entry, value_entry, row)
        remove_button.connect("clicked", self._on_remove_env_var_clicked, entry_tuple)

        self.env_var_entries.append(entry_tuple)

    def _on_remove_env_var_clicked(self, button, entry_tuple):
        """Callback to remove an environment variable row."""
        key_entry, value_entry, row = entry_tuple
        self.env_vars_group.remove(row)
        self.env_var_entries.remove(entry_tuple)

    def _clear_environment_variables_ui(self):
        """Clears the environment variables from the UI."""
        for _, _, row in self.env_var_entries:
            self.env_vars_group.remove(row)
        self.env_var_entries.clear()

    def _add_default_environment_variables(self):
        """Adds the default environment variables to the UI."""
        self._add_env_var_row("WINEDLLOVERRIDES", "")
        self._add_env_var_row("MANGOHUD", "1")

    def _get_env_vars_from_ui(self) -> Dict[str, str]:
        """Gets the environment variables from the UI."""
        env_vars = {}
        for row_data in self.env_var_entries:
            key = row_data[0].get_text().strip()
            value = row_data[1].get_text().strip()
            if key:
                env_vars[key] = value
        return env_vars

    def _get_player_configs_from_ui(self) -> List[Dict[str, Any]]:
        """Gets the player configurations from the UI."""
        player_configs_data = []
        for i, player_widgets in enumerate(self.player_device_combos):
            config = {}
            for key, widget in player_widgets.items(): # key is "PHYSICAL_DEVICE_ID", etc.
                if isinstance(widget, Adw.ComboRow):
                    selected_index = widget.get_selected()
                    device_type = getattr(widget, 'device_type', "unknown")

                    device_list = self.device_lists.get(device_type, [])
                    # The model includes "None", so index 0 is "None", index 1 is device_list[0]
                    if selected_index > 0 and (selected_index - 1) < len(device_list):
                        device_id = device_list[selected_index - 1]["id"]
                    else:
                        device_id = None # "None" is selected or index is out of bounds

                    config[key] = device_id
                else:
                     # Handle other widget types if any, e.g., EntryRow
                    config[key] = widget.get_text().strip() if hasattr(widget, 'get_text') else None
            player_configs_data.append(config)
        self.logger.info(f"DEBUG: Collected player configurations data: {player_configs_data}")
        return player_configs_data

    def setup_player_configs(self):
        """Sets up the initial player configuration UI."""
        self.player_frames = []
        self.player_device_combos = []

        self._create_player_config_uis(self.num_players_spin.get_value_as_int())

    def _create_player_config_uis(self, num_players: int):
        """Creates or recreates the UI for the specified number of players using Adwaita widgets."""
        # Clear existing widgets
        while self.player_config_vbox.get_first_child():
            self.player_config_vbox.remove(self.player_config_vbox.get_first_child())

        self.player_device_combos = []
        self.player_checkboxes = []

        for i in range(num_players):
            player_group = Adw.PreferencesGroup(title=f"Player {i+1} Configuration")
            self.player_config_vbox.append(player_group)

            # Enable/Disable Checkbox
            enable_row = Adw.ActionRow(title=f"Enable Player {i+1}")
            check_button = Gtk.CheckButton(active=True)
            enable_row.add_suffix(check_button)
            enable_row.set_activatable_widget(check_button)
            self.player_checkboxes.append(check_button)
            player_group.add(enable_row)

            # Device selectors
            joystick_combo = Adw.ComboRow(
                title="Joystick Device",
                model=Gtk.StringList.new(self._create_device_list_store(self.device_lists["joystick"]))
            )
            mouse_combo = Adw.ComboRow(
                title="Mouse Device",
                model=Gtk.StringList.new(self._create_device_list_store(self.device_lists["mouse"]))
            )
            keyboard_combo = Adw.ComboRow(
                title="Keyboard Device",
                model=Gtk.StringList.new(self._create_device_list_store(self.device_lists["keyboard"]))
            )
            audio_combo = Adw.ComboRow(
                title="Audio Device",
                model=Gtk.StringList.new(self._create_device_list_store(self.device_lists["audio"]))
            )

            joystick_combo.device_type = "joystick"
            mouse_combo.device_type = "mouse"
            keyboard_combo.device_type = "keyboard"
            audio_combo.device_type = "audio"

            player_group.add(joystick_combo)
            player_group.add(mouse_combo)
            player_group.add(keyboard_combo)
            player_group.add(audio_combo)

            player_widgets = {
                "PHYSICAL_DEVICE_ID": joystick_combo,
                "MOUSE_EVENT_PATH": mouse_combo,
                "KEYBOARD_EVENT_PATH": keyboard_combo,
                "AUDIO_DEVICE_ID": audio_combo,
            }
            self.player_device_combos.append(player_widgets)

    def on_num_players_changed(self, spin_row, _):
        """Handles the 'Number of Players' spin row value change."""
        num_players = spin_row.get_value_as_int()
        self._create_player_config_uis(num_players)

    def on_mode_changed(self, combo_row, _):
        """Shows or hides the splitscreen orientation dropdown based on the selected mode."""
        is_splitscreen = (combo_row.get_selected() == 1) # 0: Fullscreen, 1: Splitscreen
        self.splitscreen_orientation_row.set_visible(is_splitscreen)

    def on_save_button_clicked(self, button):
        """Handles the 'Save' button click, saving data and restoring selection."""
        game_to_reselect = None
        profile_to_reselect = None

        if self.selected_profile and self.selected_game:
            # When a profile is selected, we need to save both game and profile data,
            # as shared settings (like Proton version) might have been changed.
            game_to_reselect = self.game_name_entry.get_text()
            profile_to_reselect = self.profile_name_entry.get_text()

            try:
                # First, save the game data
                updated_game = self._get_game_from_ui()
                self.game_manager.save_game(updated_game)

                # Then, save the profile data using the potentially updated game object
                updated_profile = self._get_profile_from_ui()
                self.game_manager.save_profile(updated_game, updated_profile)

                self.logger.info(f"Game and profile for '{updated_game.game_name}' saved.")
            except Exception as e:
                self.logger.error(f"Failed to save game/profile: {e}")

        elif self.selected_game:
            game_to_reselect = self.game_name_entry.get_text()
            try:
                updated_game = self._get_game_from_ui()
                self.game_manager.save_game(updated_game)
                self.logger.info(f"Game '{updated_game.game_name}' saved.")
            except Exception as e:
                self.logger.error(f"Failed to save game: {e}")

        self._populate_game_library()
        if game_to_reselect:
            self._select_item_in_library(game_to_reselect, profile_to_reselect)

    def _get_game_from_ui(self) -> Game:
        """Creates a Game object from the data in the UI fields."""
        proton_version = self.proton_version_combo.get_active_text()
        if proton_version == "None (Use Steam default)" or not proton_version:
            proton_version = None

        winetricks_text = self.winetricks_verbs_row.get_text().strip()
        winetricks_verbs = winetricks_text.split() if winetricks_text else None

        return Game(
            game_name=self.game_name_row.get_text(),
            exe_path=self.exe_path_row.get_text(),
            app_id=self.app_id_row.get_text() or None,
            game_args=self.game_args_row.get_text() or None,
            is_native=self.is_native_check.get_active(),
            proton_version=proton_version,
            apply_dxvk_vkd3d=self.apply_dxvk_vkd3d_check.get_active(),
            winetricks_verbs=winetricks_verbs,
            env_vars=self._get_env_vars_from_ui()
        )

    def _get_profile_from_ui(self) -> Profile:
        """Creates a Profile object from the data in the UI fields."""
        proton_version = self.proton_version_combo.get_active_text()
        if proton_version == "None (Use Steam default)" or not proton_version:
            proton_version = None

        splitscreen_config = None
        mode_map = {0: "fullscreen", 1: "splitscreen"}
        orientation_map = {0: "horizontal", 1: "vertical"}
        mode = mode_map.get(self.mode_row.get_selected(), "fullscreen")

        if mode == "splitscreen":
            splitscreen_config = SplitscreenConfig(
                orientation=orientation_map.get(self.splitscreen_orientation_row.get_selected(), "horizontal")
            )

        winetricks_text = self.winetricks_verbs_row.get_text().strip()
        winetricks_verbs = winetricks_text.split() if winetricks_text else None

        selected_players = [i + 1 for i, cb in enumerate(self.player_checkboxes) if cb.get_active()]

        return Profile(
            profile_name=self.profile_name_row.get_text(),
            proton_version=proton_version,
            num_players=self.num_players_row.get_value_as_int(),
            instance_width=self.instance_width_row.get_value_as_int(),
            instance_height=self.instance_height_row.get_value_as_int(),
            mode=mode,
            splitscreen=splitscreen_config,
            env_vars=self._get_env_vars_from_ui(),
            player_configs=self._get_player_configs_from_ui(),
            selected_players=selected_players,
            apply_dxvk_vkd3d=self.apply_dxvk_vkd3d_check.get_active(),
            winetricks_verbs=winetricks_verbs
        )

    def on_play_button_clicked(self, widget):
        """Handles clicks on the 'Launch Game' / 'Stop Game' button."""
        if self.cli_process_pid:
            self._stop_game()
            return

        if not self.selected_game or not self.selected_profile:
            self.logger.error("Launch clicked but no profile selected.")
            return

        # Store references before the auto-save potentially clears the selection
        game_to_launch = self.selected_game
        profile_to_launch = self.selected_profile

        self.logger.info("Starting game...")
        self.on_save_button_clicked(widget) # Auto-save before launch

        # The profile name for the CLI is the sanitized game name
        cli_game_name = game_to_launch.game_name.replace(" ", "_").lower()

        # Check if running as PyInstaller bundle
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # PyInstaller bundle - use the current executable
            script_path = Path(sys.executable)
            python_exec = str(script_path)
        else:
            # Normal Python execution
            script_path = Path(__file__).parent.parent.parent / "protoncoop.py"
            python_exec = sys.executable # Use o interpretador Python atual do ambiente virtual

        if not python_exec:
            self.logger.error("Python interpreter not found.")
            dialog = Adw.MessageDialog(
                heading="Launch Error",
                body="No Python interpreter found on the system.",
                modal=True,
            )
            dialog.add_response("ok", "Ok")
            dialog.set_response_enabled("ok", True)
            dialog.set_default_response("ok")
            dialog.set_transient_for(self)
            dialog.connect("response", lambda d, r: d.close())
            dialog.present()
            return

        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # PyInstaller bundle - call the executable directly
            command = [python_exec, cli_game_name, "--profile", profile_to_launch.profile_name]
        else:
            # Normal Python execution
            command = [python_exec, str(script_path), cli_game_name, "--profile", profile_to_launch.profile_name]

        # # Append --no-bwrap if requested via GUI
        # if getattr(self, 'disable_bwrap_check', None) and self.disable_bwrap_check.get_active():
        #     command.append("--no-bwrap")
        #     self.logger.info("Disabling bwrap as requested by user")

        # Pass the GUI's PID to the CLI process for monitoring
        gui_pid = os.getpid()
        command.extend(["--parent-pid", str(gui_pid)])
        self.logger.info(f"Passing parent PID {gui_pid} to CLI process.")

        self.logger.info(f"Executing command: {' '.join(command)}")

        self.play_button.set_sensitive(False)
        self.play_button.set_label("Iniciando...")

        try:
            # Launch the CLI script as a separate process group
            process = subprocess.Popen(command, preexec_fn=os.setsid)
            self.cli_process_pid = process.pid
            self.logger.info(f"Game '{cli_game_name}' launched successfully with PID: {self.cli_process_pid}.")
            self._update_action_buttons_state() # Update button to "Stop Gaming"
            # Start monitoring the process
            self.monitoring_timeout_id = GLib.timeout_add(1000, self._check_cli_process) # Corrigido para GLib.timeout_add
        except Exception as e:
            self.logger.error(f"Failed to launch game: {e}")
            dialog = Adw.MessageDialog(
                heading="Launch Error",
                body=f"Error launching game:\n{e}",
                modal=True,
            )
            dialog.add_response("ok", "Ok")
            dialog.set_response_enabled("ok", True)
            dialog.set_default_response("ok")
            dialog.set_transient_for(self)
            dialog.connect("response", lambda d, r: d.close())
            dialog.present()
            self.cli_process_pid = None # Reset PID on error
            self._update_action_buttons_state() # Reset button to "Launch Game"

    def _stop_game(self):
        """Terminates the running game process group."""
        if not self.cli_process_pid:
            self.logger.warning("Stop clicked but no game process to stop.")
            return

        self.logger.info("Stopping game...")
        self.play_button.set_sensitive(False)
        self.play_button.set_label("Parando...")

        try:
            # Terminate the process group
            os.killpg(os.getpgid(self.cli_process_pid), signal.SIGTERM)
            self.logger.info(f"Sent SIGTERM to process group {os.getpgid(self.cli_process_pid)}")

            # Give it a moment to terminate
            # Gtk.timeout_add(1000, self._check_cli_process_after_term, self.cli_process_pid)
            # More direct approach: busy-wait for a short period, then force kill if needed
            for _ in range(5): # Wait up to 5 seconds
                if not self._is_process_running(self.cli_process_pid):
                    break
                time.sleep(1)

            if self._is_process_running(self.cli_process_pid):
                os.killpg(os.getpgid(self.cli_process_pid), signal.SIGKILL)
                self.logger.warning(f"Sent SIGKILL to process group {os.getpgid(self.cli_process_pid)} as SIGTERM was not enough.")

        except ProcessLookupError:
            self.logger.info(f"Process {self.cli_process_pid} already terminated or not found.")
        except OSError as e:
            self.logger.error(f"Error terminating process group for PID {self.cli_process_pid}: {e}")
        except Exception as e:
            self.logger.error(f"An unexpected error occurred while stopping the game: {e}")

        self.cli_process_pid = None
        if self.monitoring_timeout_id:
            GLib.source_remove(self.monitoring_timeout_id) # Stop monitoring
            self.monitoring_timeout_id = None
        self.logger.info("Game stopped.")
        self._update_action_buttons_state() # Reset button to "Launch Game"

    def _is_process_running(self, pid):
        """Checks if a process with the given PID is running."""
        if pid is None:
            return False
        try:
            os.kill(pid, 0) # Check if process exists
            return True
        except OSError:
            return False

    def _check_cli_process(self):
        """Periodically checks if the launched CLI process is still running."""
        if self.cli_process_pid and not self._is_process_running(self.cli_process_pid):
            self.logger.info(f"Detected CLI process {self.cli_process_pid} has terminated.")
            self.cli_process_pid = None
            self._update_play_button_state()
            self.logger.info("Game process terminated.")
            if self.monitoring_timeout_id:
                GLib.source_remove(self.monitoring_timeout_id)
                self.monitoring_timeout_id = None
            return False # Stop the timeout
        return True # Continue monitoring

    def on_layout_setting_changed(self, widget):
        """Handles changes to any of the layout settings."""
        self.drawing_area.queue_draw()

    def on_draw_window_layout(self, widget, cr, width, height):
        """Draws the window layout preview."""
        try:
            # Get configuration from UI
            layout_settings = self._get_layout_settings()

            # Validate the data
            if not self._validate_layout_data(layout_settings):
                return

            # Calculate drawing parameters
            drawing_params = self._calculate_drawing_parameters(width, height, layout_settings)

            # Create preview profile
            profile = self._create_preview_profile(layout_settings)
            if not profile:
                return

            # Setup cairo context
            cr.set_line_width(2)

            # Draw the appropriate layout
            if layout_settings['mode'] == "splitscreen" and layout_settings['num_players'] > 1:
                self._draw_splitscreen_layout(cr, profile, drawing_params, layout_settings)
            else:
                self._draw_fullscreen_layout(cr, profile, drawing_params)

        except Exception as e:
            self.logger.error(f"Error drawing window layout: {e}")

    def _get_layout_settings(self):
        """Extracts layout settings from the UI widgets."""
        mode_map = {0: "fullscreen", 1: "splitscreen"}
        orientation_map = {0: "horizontal", 1: "vertical"}
        return {
            'instance_width': self.instance_width_row.get_value_as_int(),
            'instance_height': self.instance_height_row.get_value_as_int(),
            'num_players': max(1, self.num_players_row.get_value_as_int()),
            'mode': mode_map.get(self.mode_row.get_selected(), "fullscreen"),
            'orientation': orientation_map.get(self.splitscreen_orientation_row.get_selected(), "horizontal")
        }

    def _validate_layout_data(self, settings):
        """Validates the layout settings."""
        return (settings['instance_width'] > 0 and
                settings['instance_height'] > 0 and
                settings['num_players'] >= 1)

    def _calculate_drawing_parameters(self, drawing_width, drawing_height, settings):
        """Calculates the scale and offset for the drawing area."""
        scale_w = drawing_width / settings['instance_width']
        scale_h = drawing_height / settings['instance_height']
        scale = min(scale_w, scale_h) * 0.9

        scaled_total_width = settings['instance_width'] * scale
        scaled_total_height = settings['instance_height'] * scale

        return {
            'scale': scale,
            'x_offset': (drawing_width - scaled_total_width) / 2,
            'y_offset': (drawing_height - scaled_total_height) / 2
        }

    def _create_preview_profile(self, settings):
        """Creates a dummy GameProfile for the layout preview."""
        try:
            # Use model_construct to create the object without running validation,
            # which would fail on the non-existent dummy executable path.
            dummy_game = Game.model_construct(
                game_name="Preview",
                exe_path=Path("/tmp/dummy.exe"),
                is_native=False
            )
            dummy_profile = Profile(
                profile_name="Preview",
                num_players=settings['num_players'],
                instance_width=settings['instance_width'],
                instance_height=settings['instance_height'],
                mode=settings['mode'],
                splitscreen=SplitscreenConfig(orientation=settings['orientation']) if settings['mode'] == "splitscreen" else None,
                player_configs=[PlayerInstanceConfig() for _ in range(settings['num_players'])]
            )
            return GameProfile(game=dummy_game, profile=dummy_profile)
        except Exception as e:
            self.logger.error(f"Error creating preview profile: {e}")
            return None

    def _draw_splitscreen_layout(self, cr, profile, drawing_params, settings):
        """Draws the splitscreen layout."""
        for i in range(settings['num_players']):
            instance_w, instance_h = profile.get_instance_dimensions(i + 1)
            draw_w = instance_w * drawing_params['scale']
            draw_h = instance_h * drawing_params['scale']

            pos_x, pos_y = self._calculate_player_position(
                i, settings['num_players'], settings['orientation'],
                draw_w, draw_h, profile, drawing_params['scale']
            )

            self._draw_player_window(
                cr, i + 1, pos_x, pos_y, draw_w, draw_h,
                drawing_params['x_offset'], drawing_params['y_offset'],
                profile
            )

    def _draw_fullscreen_layout(self, cr, profile, drawing_params):
        """Draws the fullscreen layout."""
        instance_w, instance_h = profile.get_instance_dimensions(1)
        draw_w = instance_w * drawing_params['scale']
        draw_h = instance_h * drawing_params['scale']

        self._draw_player_window(
            cr, 1, 0, 0, draw_w, draw_h,
            drawing_params['x_offset'], drawing_params['y_offset'],
            profile
        )

    def _calculate_player_position(self, player_index, num_players, orientation, draw_w, draw_h, profile, scale):
        """Calculates the position of a player's window in the preview."""
        pos_x, pos_y = 0.0, 0.0

        if num_players == 2:
            if orientation == "horizontal":
                pos_x = player_index * draw_w
            else:  # vertical
                pos_y = player_index * draw_h
        elif num_players == 3:
            pos_x, pos_y = self._calculate_three_player_position(
                player_index, orientation, profile, scale
            )
        elif num_players == 4:
            # 2x2 grid
            row = player_index // 2
            col = player_index % 2
            pos_x = col * draw_w
            pos_y = row * draw_h
        else:  # Generic case for more than 4 players
            if orientation == "horizontal":  # Stacked vertically
                pos_y = player_index * draw_h
            else:  # vertical (Side by side)
                pos_x = player_index * draw_w

        return pos_x, pos_y

    def _calculate_three_player_position(self, player_index, orientation, profile, scale):
        """Calculates the position for a 3-player splitscreen layout."""
        p1_unscaled_w, p1_unscaled_h = profile.get_instance_dimensions(1)
        p2_unscaled_w, p2_unscaled_h = profile.get_instance_dimensions(2)

        p1_draw_w, p1_draw_h = p1_unscaled_w * scale, p1_unscaled_h * scale
        p2_draw_w, p2_draw_h = p2_unscaled_w * scale, p2_unscaled_h * scale

        if orientation == "horizontal":  # 1 large top, 2 small bottom
            if player_index == 0:  # Player 1 (top)
                return 0, 0
            elif player_index == 1:  # Player 2 (bottom-left)
                return 0, p1_draw_h
            elif player_index == 2:  # Player 3 (bottom-right)
                return p2_draw_w, p1_draw_h
        else:  # vertical: 1 large left, 2 small right
            if player_index == 0:  # Player 1 (left)
                return 0, 0
            elif player_index == 1:  # Player 2 (top-right)
                return p1_draw_w, 0
            elif player_index == 2:  # Player 3 (bottom-right)
                return p1_draw_w, p2_draw_h

        return 0, 0

    def _draw_player_window(self, cr, player_num, pos_x, pos_y, width, height, x_offset, y_offset, profile):
        """Draws a single player window in the preview."""
        # Draw window rectangle
        cr.rectangle(x_offset + pos_x, y_offset + pos_y, width, height)
        cr.set_source_rgb(1.0, 1.0, 1.0)  # White border
        cr.stroke()

        # Draw player text
        self._draw_player_text(cr, player_num, pos_x, pos_y, width, height, x_offset, y_offset)

        # Draw monitor info
        self._draw_monitor_info(cr, player_num - 1, pos_x, pos_y, width, height, x_offset, y_offset, profile)

    def _draw_player_text(self, cr, player_num, pos_x, pos_y, width, height, x_offset, y_offset):
        """Draws the player number text in the preview."""
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        font_size = max(10, min(width, height) // 5)
        cr.set_font_size(font_size)
        cr.set_source_rgb(1.0, 1.0, 1.0)  # White text

        text = f"P{player_num}"
        _, _, width_text, height_text, _, _ = cr.text_extents(text)
        text_x = x_offset + pos_x + (width - width_text) / 2
        text_y = y_offset + pos_y + (height + height_text) / 2
        cr.move_to(text_x, text_y)
        cr.show_text(text)

    def _draw_monitor_info(self, cr, player_index, pos_x, pos_y, width, height, x_offset, y_offset, profile):
        """Draws the monitor ID in the preview."""
        monitor_id_text = self._get_monitor_text(player_index, profile)

        if monitor_id_text:
            # Calculate font size relative to player text
            base_font_size = max(10, min(width, height) // 5)
            font_size = base_font_size * 0.7

            cr.set_font_size(font_size)
            cr.set_source_rgb(0.7, 0.7, 0.7)  # Gray text for monitor ID

            _, _, width_text, height_text, _, _ = cr.text_extents(monitor_id_text)
            text_x = x_offset + pos_x + (width - width_text) / 2
            text_y = y_offset + pos_y + (height + height_text) / 2 + (base_font_size * 0.8)
            cr.move_to(text_x, text_y)
            cr.show_text(monitor_id_text)

    def _get_monitor_text(self, player_index, profile):
        """Gets the monitor text for a player."""
        if (profile.player_configs and
            player_index < len(profile.player_configs)):
            player_instance = profile.player_configs[player_index]
            monitor_id_from_profile = player_instance.monitor_id
            if monitor_id_from_profile:
                return self.device_id_to_name.get(monitor_id_from_profile, "None")
        return ""

    def get_profile_data(self):
        """Gets the profile data from the UI."""
        proton_version = self.proton_version_combo.get_active_text()
        if proton_version == "None (Use Steam default)" or not proton_version:
            proton_version = None

        player_configs_data = self._get_player_configs_from_ui()

        splitscreen_config = None
        if self.mode_combo.get_active_text() == "splitscreen":
            selected_orientation = self.splitscreen_orientation_combo.get_active_text()
            self.logger.info(f"DEBUG: Selected splitscreen orientation from UI: {selected_orientation}")
            splitscreen_config = SplitscreenConfig(
                orientation=selected_orientation
            )
            self.logger.info(f"DEBUG: SplitscreenConfig orientation immediately after creation: {splitscreen_config.orientation}")

        # Correctly determine is_native_value by checking if the path ends with .exe
        exe_path_text = self.exe_path_entry.get_text()
        is_native_value = False
        if exe_path_text:
            is_native_value = not Path(exe_path_text).suffix.lower() == ".exe"

        mode = self.mode_combo.get_active_text()

        winetricks_text = self.winetricks_verbs_entry.get_text().strip()
        winetricks_verbs = winetricks_text.split() if winetricks_text else None

        profile_data = GameProfile(
            game_name=self.game_name_entry.get_text(),
            exe_path=self.exe_path_entry.get_text(),
            num_players=self.num_players_spin.get_value_as_int(),
            proton_version=proton_version,
            instance_width=self.instance_width_spin.get_value_as_int(),
            instance_height=self.instance_height_spin.get_value_as_int(),
            app_id=self.app_id_entry.get_text() or None,
            game_args=self.game_args_entry.get_text(),
            env_vars=self._get_env_vars_from_ui(),
            is_native=is_native_value,
            # use_gamescope=self.use_gamescope_check.get_active(),
            # disable_bwrap=self.disable_bwrap_check.get_active(),
            apply_dxvk_vkd3d=self.apply_dxvk_vkd3d_check.get_active(),
            winetricks_verbs=winetricks_verbs,
            mode=mode,
            splitscreen=splitscreen_config,
            player_configs=player_configs_data, # Use the already collected data
        )

        self.logger.info(f"DEBUG: Mode value before GameProfile instantiation: {mode}")

        if profile_data.splitscreen:
            self.logger.info(f"DEBUG: Splitscreen orientation in GameProfile object: {profile_data.splitscreen.orientation}")

        profile_dumped = profile_data.model_dump(by_alias=True, exclude_unset=False, exclude_defaults=False, mode='json')
        self.logger.info(f"DEBUG: Collecting {len(profile_dumped.get('PLAYERS') or [])} player configs for saving.")
        self.logger.info(f"DEBUG: USE_GAMESCOPE value being saved: {profile_dumped.get('USE_GAMESCOPE', 'NOT FOUND')}")
        self.logger.info(f"DEBUG: DISABLE_BWRAP value being saved: {profile_dumped.get('DISABLE_BWRAP', 'NOT FOUND')}")
        return profile_dumped

    def _clear_all_fields(self):
        """Clears all UI input fields to their default states."""
        # Game details
        self.game_name_row.set_text("")
        self.exe_path_row.set_text("")
        self.app_id_row.set_text("")
        self.game_args_row.set_text("")
        self.is_native_check.set_active(False)

        # Profile details
        self.profile_name_entry.set_text("")
        self.proton_version_combo.set_active(0)
        self.apply_dxvk_vkd3d_check.set_active(True)
        self.winetricks_verbs_row.set_text("")

        # Layout
        self.num_players_row.set_value(1)
        self.instance_width_row.set_value(1920)
        self.instance_height_row.set_value(1080)
        self.mode_row.set_selected(0)
        self.splitscreen_orientation_row.set_selected(0)

        # Env vars
        self._clear_environment_variables_ui()
        self._add_default_environment_variables()

        # Player configs
        self._create_player_config_uis(1)

        self.drawing_area.queue_draw()

    def _set_fields_sensitivity(self, is_game_selected: bool, is_profile_selected: bool):
        """Sets the sensitivity of all UI elements based on selection."""
        # Game-level fields are editable when a game is selected
        self.game_name_entry.set_sensitive(is_game_selected)
        self.exe_path_entry.set_sensitive(is_game_selected)
        self.app_id_entry.set_sensitive(is_game_selected)
        self.game_args_entry.set_sensitive(is_game_selected)
        self.is_native_check.set_sensitive(is_game_selected)
        self.proton_version_combo.set_sensitive(is_game_selected)
        self.apply_dxvk_vkd3d_check.set_sensitive(is_game_selected)
        self.winetricks_verbs_entry.set_sensitive(is_game_selected)
        self.env_vars_listbox.set_sensitive(is_game_selected)
        self.profile_selector_combo.set_sensitive(is_game_selected)

        # Profile-level fields are editable only when a profile is selected
        self.profile_name_row.set_sensitive(is_profile_selected)
        self.num_players_row.set_sensitive(is_profile_selected)
        self.instance_width_row.set_sensitive(is_profile_selected)
        self.instance_height_row.set_sensitive(is_profile_selected)
        self.mode_row.set_sensitive(is_profile_selected)
        self.splitscreen_orientation_row.set_sensitive(is_profile_selected)
        self.player_config_vbox.set_sensitive(is_profile_selected)

        # Set sensitivity for the view stack pages (tabs)
        game_settings_page = self.view_stack.get_child_by_name("game_settings")
        profile_settings_page = self.view_stack.get_child_by_name("profile_settings")
        window_layout_page = self.view_stack.get_child_by_name("window_layout")

        if game_settings_page:
            game_settings_page.set_sensitive(is_game_selected)
        if profile_settings_page:
            profile_settings_page.set_sensitive(is_profile_selected)
        if window_layout_page:
            window_layout_page.set_sensitive(is_profile_selected)


    def _load_game_data(self, game: Game):
        """Loads data from a Game object into the UI fields."""
        self._clear_all_fields()
        # Game Details
        self.game_name_row.set_text(game.game_name or "")
        self.exe_path_row.set_text(str(game.exe_path) or "")
        self.app_id_row.set_text(game.app_id or "")
        self.game_args_row.set_text(game.game_args or "")
        self.is_native_check.set_active(game.is_native)

        # Launch Options
        if game.proton_version:
            model = self.proton_version_combo.get_model()
            for i, row in enumerate(model):
                if row[0] == game.proton_version:
                    self.proton_version_combo.set_active(i)
                    break
        else:
            self.proton_version_combo.set_active(0)

        self.apply_dxvk_vkd3d_check.set_active(game.apply_dxvk_vkd3d)
        self.winetricks_verbs_row.set_text(" ".join(game.winetricks_verbs) if game.winetricks_verbs else "")

        # Env Vars
        self._clear_environment_variables_ui()
        if game.env_vars:
            for key, value in game.env_vars.items():
                self._add_env_var_row(key, value)
        else:
            self._add_default_environment_variables()

    def _load_profile_data(self, game: Game, profile: Profile):
        """Loads data from both a Game and a Profile object into the UI."""
        self._load_game_data(game)

        # Profile Details
        self.profile_name_row.set_text(profile.profile_name or "")

        # Layout & Display
        self.num_players_row.set_value(profile.num_players)
        self.instance_width_row.set_value(profile.instance_width)
        self.instance_height_row.set_value(profile.instance_height)

        mode_map = {"fullscreen": 0, "splitscreen": 1}
        self.mode_row.set_selected(mode_map.get(profile.mode, 0))

        if profile.is_splitscreen_mode and profile.splitscreen:
            orientation_map = {"horizontal": 0, "vertical": 1}
            self.splitscreen_orientation_row.set_selected(orientation_map.get(profile.splitscreen.orientation, 0))

        # Load Player Configs
        if profile.player_configs:
            self._create_player_config_uis(len(profile.player_configs))
            self._populate_player_configurations(profile.player_configs, profile)
        else:
            self._create_player_config_uis(profile.num_players)

        self.drawing_area.queue_draw()

    def _populate_player_configurations(self, player_configs: List[PlayerInstanceConfig], profile: Profile):
        """Populates the player configuration UI from a list of player config objects."""
        selected_players = profile.selected_players or []
        for i, player_config in enumerate(player_configs):
            if i < len(self.player_device_combos):
                player_widgets = self.player_device_combos[i]
                self.player_checkboxes[i].set_active((i + 1) in selected_players)

                # Set device dropdowns using the new Adw.ComboRow API
                self._set_device_dropdown(player_widgets["PHYSICAL_DEVICE_ID"], player_config.PHYSICAL_DEVICE_ID)
                self._set_device_dropdown(player_widgets["MOUSE_EVENT_PATH"], player_config.MOUSE_EVENT_PATH)
                self._set_device_dropdown(player_widgets["KEYBOARD_EVENT_PATH"], player_config.KEYBOARD_EVENT_PATH)
                self._set_device_dropdown(player_widgets["AUDIO_DEVICE_ID"], player_config.AUDIO_DEVICE_ID)

    def _set_device_dropdown(self, combo_row, device_id):
        """Sets the selected item in an Adw.ComboRow based on device ID."""
        device_type = getattr(combo_row, 'device_type', "unknown")
        device_list = self.device_lists.get(device_type, [])

        if device_id is None:
            combo_row.set_selected(0) # "None"
            return

        for i, device in enumerate(device_list):
            if device["id"] == device_id:
                # The model includes "None", so device indices are offset by 1
                combo_row.set_selected(i + 1)
                return

        combo_row.set_selected(0) # Default to "None" if not found


    def _get_dropdown_index_for_name(self, dropdown: Gtk.DropDown, name: str) -> int:
        """Gets the index of an item in a dropdown by its name."""
        model = dropdown.get_model()
        if model:
            for i in range(model.get_n_items()):
                item = model.get_item(i)
                if item and item.get_string() == name:
                    return i
        return 0 # Default to first item (e.g., "None") if not found or model is empty

    def _create_device_list_store(self, devices: List[Dict[str, str]]) -> List[str]:
        """Creates a list of strings for a device dropdown."""
        string_list_data = ["None"] # Add "None" as the first option
        for device in devices:
            # Truncate long device names with ellipsis
            device_name = device["name"]
            if len(device_name) > 22:
                device_name = device_name[:19] + "..."
            string_list_data.append(device_name)
        return string_list_data

    def _populate_profile_list(self):
        """Populates the profile listbox with available profiles."""
        # In Gtk4, Gtk.ListBox.get_children() is removed. Remove rows one by one.
        while self.profile_listbox.get_first_child():
            self.profile_listbox.remove(self.profile_listbox.get_first_child())

        profile_dir = Config.PROFILE_DIR
        profile_dir.mkdir(parents=True, exist_ok=True)

        profiles = sorted(profile_dir.glob("*.json"))

        if not profiles:
            label = Gtk.Label(label="No profiles found.\nCreate one and save it!")
            label.set_halign(Gtk.Align.CENTER)
            row = Gtk.ListBoxRow()
            row.set_child(label) # Changed from add
            self.profile_listbox.append(row) # Changed from add
            row.set_sensitive(False) # Make it non-selectable

            # Hide delete button when no profiles
            self.delete_profile_button.set_visible(False)
            self.selected_profile_name = None
        else:
            for profile_path in profiles:
                profile_name_stem = profile_path.stem # Get filename without extension
                try:
                    profile = GameProfile.load_from_file(profile_path) # Load profile, uses cache
                    display_name = profile.game_name or profile_name_stem # Use GAME_NAME, fallback to filename
                except Exception as e:
                    self.logger.warning(f"Could not load profile {profile_name_stem} for display in list: {e}")
                    display_name = profile_name_stem + " (Error)" # Indicate error

                row = Gtk.ListBoxRow()
                label = Gtk.Label(label=display_name)
                label.set_halign(Gtk.Align.START) # Align text to the start
                row.set_child(label) # Changed from add
                # Store the actual filename stem in the label's name property
                label.set_name(profile_name_stem)
                self.profile_listbox.append(row) # Changed from add

        # self.profile_listbox.show_all() # Not needed for Gtk4

    def _on_profile_selected_from_list(self, listbox, row):
        """Handles the selection of a profile from the listbox."""
        profile_name_stem = row.get_child().get_name() # Get the filename stem from the label's name property
        if not profile_name_stem:
            self.logger.warning("Attempted to select a profile without a stored filename property.")
            return

        # Update selected profile and show delete button
        self.selected_profile_name = profile_name_stem
        self.delete_profile_button.set_visible(True)

        profile_path = Config.PROFILE_DIR / f"{profile_name_stem}.json"
        self.logger.info(f"Loading profile from sidebar: {profile_name_stem}")

        try:
            profile = GameProfile.load_from_file(profile_path)
            self.load_profile_data(profile.model_dump(by_alias=True))
            self.logger.info(f"Profile loaded: {profile_name_stem}")
            # Switch to General Settings tab after loading
            self.view_stack.set_visible_child_name("game_settings")
        except Exception as e:
            self.logger.error(f"Failed to load profile {profile_name_stem}: {e}")
            # Show error dialog
            error_dialog = Adw.MessageDialog(
                heading="Load Error",
                body=f"Failed to load profile '{profile_name_stem}':\n{str(e)}"
            )
            error_dialog.add_response("ok", "OK")
            error_dialog.set_default_response("ok")
            error_dialog.set_close_response("ok")
            error_dialog.set_transient_for(self)
            error_dialog.connect("response", lambda d, r: d.close())
            error_dialog.present()

    def _on_add_game_clicked(self, button):
        """Handles the 'Add Game' button click by showing a dialog."""
        dialog = Gtk.Dialog(title="Add New Game", transient_for=self, modal=True)
        dialog.add_buttons(
            "_Cancel", Gtk.ResponseType.CANCEL,
            "_Add", Gtk.ResponseType.OK
        )
        dialog.get_widget_for_response(Gtk.ResponseType.OK).add_css_class("suggested-action")

        content_area = dialog.get_content_area()
        grid = Gtk.Grid(column_spacing=10, row_spacing=10, margin_start=10, margin_end=10, margin_top=10, margin_bottom=10)
        content_area.append(grid)

        grid.attach(Gtk.Label(label="Game Name:", xalign=0), 0, 0, 1, 1)
        name_entry = Gtk.Entry(placeholder_text="e.g., Elden Ring")
        grid.attach(name_entry, 1, 0, 1, 1)

        grid.attach(Gtk.Label(label="Executable Path:", xalign=0), 0, 1, 1, 1)

        exe_path_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        exe_path_entry = Gtk.Entry(placeholder_text="Path to game's .exe", hexpand=True)
        exe_path_box.append(exe_path_entry)

        browse_button = Gtk.Button(label="Browse...")

        def on_browse_clicked(btn):
            file_dialog = Gtk.FileChooserDialog(
                title="Select Game Executable",
                transient_for=dialog,
                action=Gtk.FileChooserAction.OPEN,
            )
            file_dialog.add_buttons("_Cancel", Gtk.ResponseType.CANCEL, "_Open", Gtk.ResponseType.OK)

            def on_file_dialog_response(d, response_id):
                if response_id == Gtk.ResponseType.OK:
                    file = d.get_file()
                    if file:
                        exe_path_entry.set_text(file.get_path())
                d.destroy()

            file_dialog.connect("response", on_file_dialog_response)
            file_dialog.show()

        browse_button.connect("clicked", on_browse_clicked)
        exe_path_box.append(browse_button)
        grid.attach(exe_path_box, 1, 1, 1, 1)

        def on_response(d, response_id):
            if response_id == Gtk.ResponseType.OK:
                game_name = name_entry.get_text().strip()
                exe_path = exe_path_entry.get_text().strip()
                if game_name and exe_path:
                    try:
                        new_game = Game(game_name=game_name, exe_path=Path(exe_path))
                        self.game_manager.add_game(new_game)
                        self._populate_game_library()
                        self.logger.info(f"Game '{game_name}' added successfully.")
                    except Exception as e:
                        self.logger.error(f"Failed to add game: {e}")
                else:
                    self.logger.warning("Add Game dialog submitted with empty name or path.")
            d.destroy()

        dialog.connect("response", on_response)
        dialog.show()

    def _on_add_profile_clicked(self, button):
        """Handles the 'Add Profile' button click by showing a dialog."""
        if not self.selected_game:
            self.logger.warning("Add Profile clicked but no game is selected.")
            return

        dialog = Gtk.Dialog(title=f"Add Profile to {self.selected_game.game_name}", transient_for=self, modal=True)
        dialog.add_buttons(
            "_Cancel", Gtk.ResponseType.CANCEL,
            "_Create", Gtk.ResponseType.OK
        )
        dialog.get_widget_for_response(Gtk.ResponseType.OK).add_css_class("suggested-action")

        content_area = dialog.get_content_area()
        grid = Gtk.Grid(column_spacing=10, row_spacing=10, margin_start=10, margin_end=10, margin_top=10, margin_bottom=10)
        content_area.append(grid)

        grid.attach(Gtk.Label(label="New Profile Name:", xalign=0), 0, 0, 1, 1)
        name_entry = Gtk.Entry(placeholder_text="e.g., Modded, Speedrun")
        grid.attach(name_entry, 1, 0, 1, 1)

        def on_response(d, response_id):
            if response_id == Gtk.ResponseType.OK:
                profile_name = name_entry.get_text().strip()
                if profile_name:
                    try:
                        # Create a default profile
                        new_profile = Profile(
                            profile_name=profile_name,
                            num_players=2,
                            instance_width=1920,
                            instance_height=1080,
                            player_configs=[PlayerInstanceConfig(), PlayerInstanceConfig()]
                        )
                        game_name = self.selected_game.game_name
                        self.game_manager.add_profile(self.selected_game, new_profile)
                        self.logger.info(f"Profile '{profile_name}' added to {game_name}.")
                        self._populate_game_library()
                    except Exception as e:
                        self.logger.error(f"Failed to add profile: {e}")
                else:
                    self.logger.warning("Add Profile dialog submitted with empty name.")
            d.destroy()

        dialog.connect("response", on_response)
        dialog.show()

    def _on_delete_clicked(self, button):
        """Handles the 'Delete' button click for either a game or a profile."""
        if self.selected_profile:
            # Delete profile logic
            self.logger.info(f"Deleting profile: {self.selected_profile.profile_name}")
            self.game_manager.delete_profile(self.selected_game, self.selected_profile)
        elif self.selected_game:
            # Delete game logic
            self.logger.info(f"Deleting game: {self.selected_game.game_name}")
            self.game_manager.delete_game(self.selected_game)

        self._populate_game_library()
        self._clear_all_fields()

    def _on_close_request(self, window):
        """Handles the window close request."""
        if self.cli_process_pid:
            self.logger.info("Close requested, but game is running. Stopping game first.")
            self._stop_game()

            # We can't immediately close because _stop_game is asynchronous in its effect.
            # We need to wait until the process is confirmed dead.
            # We can use a timeout to check for process termination.
            def check_if_can_close():
                if not self._is_process_running(self.cli_process_pid):
                    self.logger.info("Game has been stopped. Now closing the window.")
                    self.close() # Now we can close for real
                    return GLib.SOURCE_REMOVE # Stop the timeout
                return GLib.SOURCE_CONTINUE # Continue checking

            GLib.timeout_add(500, check_if_can_close)

            return True # Prevent the default close handler from running

        self.logger.info("No game running. Closing window.")
        return False # Allow the default close handler to run

    def _on_close_request(self, window):
        """Handles the window close request."""
        if self.cli_process_pid:
            self.logger.info("Close requested, but game is running. Stopping game first.")
            self._stop_game()

            # We can't immediately close because _stop_game is asynchronous in its effect.
            # We need to wait until the process is confirmed dead.
            # We can use a timeout to check for process termination.
            def check_if_can_close():
                if not self._is_process_running(self.cli_process_pid):
                    self.logger.info("Game has been stopped. Now closing the window.")
                    self.close() # Now we can close for real
                    return GLib.SOURCE_REMOVE # Stop the timeout
                return GLib.SOURCE_CONTINUE # Continue checking

            GLib.timeout_add(500, check_if_can_close)

            return True # Prevent the default close handler from running

        self.logger.info("No game running. Closing window.")
        return False # Allow the default close handler to run

class LinuxCoopApp(Adw.Application):
    """
    The main application class, inheriting from Adw.Application.

    This class is the entry point for the GUI. It handles application
    initialization, activation, styling, and signal handling for graceful
    shutdown.
    """
    def __init__(self):
        """Initializes the Adwaita application."""
        super().__init__(application_id="org.protoncoop.app")
        self.connect("activate", self.on_activate)

        # Initialize Adwaita
        Adw.init()

        # Configure proper Adwaita style manager to avoid warnings
        self._configure_adwaita_style()

        # Initialize styles using the professional StyleManager
        self._initialize_application_styles()

        # Set up a signal handler for SIGUSR1 to allow the child process to close the GUI
        GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGUSR1, self._handle_shutdown_signal, "SIGUSR1")
        # Set up a signal handler for SIGTERM to allow the system to close the GUI gracefully
        GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGTERM, self._handle_shutdown_signal, "SIGTERM")

    def _handle_shutdown_signal(self, signal_name):
        """Signal handler for SIGUSR1 or SIGTERM. Closes the main window."""
        self.logger.info(f"Received {signal_name}, closing the main window gracefully.")
        # Get the active window and close it. `self.quit()` is another option.
        window = self.get_active_window()
        if window:
            window.close() # This will trigger the _on_close_request logic
        else:
            # If there's no window, just quit the app
            self.quit()
        return True # Keep the signal handler active

    def _configure_adwaita_style(self):
        """Configures the Adwaita style manager to follow the system theme."""
        try:
            style_manager = Adw.StyleManager.get_default()
            # Use PREFER_DARK to automatically follow system theme preference
            # This will use dark theme when system prefers dark, light when system prefers light
            style_manager.set_color_scheme(Adw.ColorScheme.PREFER_DARK)

            # Optional: Connect to theme changes to update custom styles if needed
            style_manager.connect("notify::dark", self._on_theme_changed)

            # Log current theme state
            is_dark = style_manager.get_dark()
            theme_name = "dark" if is_dark else "light"
            self.logger = Logger(name="LinuxCoopGUI", log_dir=Path("./logs"))
            self.logger.info(f"Configured Adwaita to follow system theme. Current theme: {theme_name}")
        except Exception as e:
            # Fallback if AdwStyleManager is not available
            self.logger = Logger(name="LinuxCoopGUI", log_dir=Path("./logs"))
            self.logger.warning(f"Could not configure Adwaita style manager: {e}")

    def _on_theme_changed(self, style_manager, param):
        """Handles system theme changes."""
        try:
            is_dark = style_manager.get_dark()
            theme_name = "dark" if is_dark else "light"
            self.logger.info(f"System theme changed to: {theme_name}")

            # Trigger StyleManager to reload theme-specific styles
            from .styles import get_style_manager
            style_manager_instance = get_style_manager()
            style_manager_instance._load_theme_specific_styles()

            # Update window styling if needed
            self._update_window_for_theme(is_dark)
        except Exception as e:
            self.logger.warning(f"Error handling theme change: {e}")

    def _update_window_for_theme(self, is_dark: bool):
        """Updates the window styling based on the theme."""
        try:
            # Force refresh of all widgets to apply new theme
            self.queue_draw()

            # Update any theme-sensitive components
            if hasattr(self, 'drawing_area'):
                self.drawing_area.queue_draw()

        except Exception as e:
            self.logger.warning(f"Error updating window for theme: {e}")

    def _initialize_application_styles(self):
        """Initializes custom application-wide CSS styles."""
        try:
            initialize_styles()
            self.logger = Logger(name="LinuxCoopGUI", log_dir=Path("./logs"))
            self.logger.info("Successfully initialized application styles")
        except StyleManagerError as e:
            # Fallback to basic styling if StyleManager fails
            self.logger = Logger(name="LinuxCoopGUI", log_dir=Path("./logs"))
            self.logger.warning(f"Failed to initialize StyleManager: {e}")
            self._apply_fallback_styles()

    def _apply_fallback_styles(self):
        """Applies minimal fallback styles if the StyleManager fails."""
        try:
            style_manager = get_style_manager()
            fallback_css = """
            /* Minimal fallback styles */
            * { font-family: system-ui, sans-serif; }
            label { padding: 4px 0; min-height: 20px; }
            entry, button { padding: 6px; min-height: 28px; }
            """
            style_manager.load_css_from_string(fallback_css, "fallback")
        except Exception as e:
            self.logger.error(f"Even fallback styles failed: {e}")

    def on_activate(self, app):
        """
        Called when the application is activated.

        This method creates and presents the main `ProfileEditorWindow`.

        Args:
            app (LinuxCoopApp): The application instance.
        """
        window = ProfileEditorWindow(app)
        window.present() # Changed from show_all() or show()

def run_gui():
    """The main entry point function to start the GUI application."""
    app = LinuxCoopApp()
    app.run(None)

if __name__ == "__main__":
    # This ensures that the GUI is only started if the script is executed directly
    # and not when imported as a module.
    gi.require_version("Gtk", "4.0")
    gi.require_version("Adw", "1") # Added Adw require
    from gi.repository import Gtk, Gdk, Adw # Added Adw import
    import cairo # Import cairo here for drawing
    import time # Import time for busy-wait in _stop_game
    from gi.repository import GLib # Importado para usar GLib.timeout_add
    run_gui()