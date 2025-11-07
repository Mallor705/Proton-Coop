# Proton-Coop

![Proton-Coop Banner](https://github.com/Mallor705/Proton-Coop/assets/80993074/399081e7-295e-4c55-b040-02d242407559)

**Proton-Coop** is a powerful tool for Linux that enables local co-op for PC games that don't natively support it. It works by running multiple instances of a game simultaneously, each sandboxed with its own Proton prefix, controller, and display settings. This allows you to play games with separate saves and configurations on the same machine, as if you were on different computers.

## 🚀 Key Features

- **Game-Centric Library:** Manage a library of games, each with its own set of profiles (layouts).
- **Multi-Instance Gaming:** Launch multiple instances of a game simultaneously.
- **GUI Profile Editor:** An intuitive graphical interface to create, manage, and launch game profiles.
- **Complete Isolation:** Each instance runs in its own sandbox (`bwrap`) with a separate Wine prefix, ensuring no conflicts with saves or configurations.
- **Device Management:** Assign specific keyboards, mice, and controllers to each game instance for a true local co-op feel.
- **Display & Audio Control:** Run each instance on a specific monitor and direct audio to a specific output device.
- **Flexible Launch Options:**
    - Choose any installed Proton version (including GE-Proton and others).
    - Apply DXVK/VKD3D and run custom Winetricks verbs per game.
    - Set custom environment variables.
    - Toggle MangoHud for performance monitoring.
- **Splitscreen & Fullscreen Modes:**
    - **Fullscreen:** Each instance runs on a separate monitor.
    - **Splitscreen:** Automatically arrange multiple instances on a single monitor, with horizontal or vertical layouts.
- **CLI and GUI:** Use the powerful command-line interface for scripting and automation, or the user-friendly GUI for easy profile management.

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Steam:** Required for managing and finding Proton versions.
- **Proton:** At least one version of Proton (e.g., Proton Experimental, GE-Proton) must be installed through Steam.
- **Gamescope:** For window management and performance optimization.
- **Bubblewrap (`bwrap`):** For sandboxing and process isolation.
- **Python 3.8+** and `pip`.
- **PyGObject & Adwaita:** For the graphical user interface. On Debian/Ubuntu, you can install these with:
  ```bash
  sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1
  ```
- **umu-run:** For launching non-native games.

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Mallor705/Proton-Coop.git
    cd Proton-Coop
    ```
2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the application:**
    - To start the GUI:
      ```bash
      ./run.sh
      ```
    - To use the CLI:
      ```bash
      ./protoncoop.py <game_name> --profile <profile_name>
      ```

## 🎮 How to Use

### Using the GUI (Recommended)

The easiest way to get started is with the graphical user interface.

1.  **Launch the GUI:**
    ```bash
    ./run.sh
    ```
2.  **Add a New Game:** Click the "+" button in the header bar and provide a name and path to the game's executable.
3.  **Configure the Game:**
    - Select the game in the sidebar.
    - **Layout Settings:** Create and manage profiles (layouts) for the selected game.
    - **Advanced Settings:** Configure Proton version, DXVK/VKD3D, Winetricks, environment variables, and MangoHud.
4.  **Launch a Game:** Select a game and a profile, then click the "Launch" button.

### Using the CLI

For advanced users and automation, the CLI provides full control.

1.  **Create a Game and Profile:** You can create a game and profile using the GUI first, or manually create the necessary `.json` files.
2.  **Launch a Game:**
    ```bash
    ./protoncoop.py <game_name> --profile <profile_name>
    ```
    (Replace `<game_name>` with the name of the game and `<profile_name>` with the name of the profile).

### Configuration File Structure

Proton-Coop uses a game-centric configuration structure. Each game has its own directory in `~/.config/proton-coop/games/`, which contains a `game.json` file and a `profiles` subdirectory.

#### `game.json`

This file stores the core information about a game.

```json
{
    "GAME_NAME": "Stew Valley",
    "EXE_PATH": "/home/user/.steam/steam/steamapps/common/Stardew Valley/Stardew Valley.exe",
    "APP_ID": "413150",
    "GAME_ARGS": "",
    "IS_NATIVE": false,
    "PROTON_VERSION": "GE-Proton8-25",
    "APPLY_DXVK_VKD3D": true,
    "WINETRICKS_VERBS": [],
    "ENV_VARS": {
        "MANGOHUD": "1"
    },
    "USE_MANGOHUD": true
}
```

#### `profile.json`

Each profile is a separate `.json` file in the `profiles` subdirectory of a game.

```json
{
    "PROFILE_NAME": "Co-op",
    "NUM_PLAYERS": 2,
    "INSTANCE_WIDTH": 1920,
    "INSTANCE_HEIGHT": 1080,
    "MODE": "splitscreen",
    "SPLITSCREEN": {
        "ORIENTATION": "horizontal"
    },
    "PLAYERS": [
        {
            "PHYSICAL_DEVICE_ID": "/dev/input/by-id/usb-Sony_Interactive_Entertainment_Wireless_Controller-if03-event-joystick"
        },
        {
            "MOUSE_EVENT_PATH": "/dev/input/by-id/usb-Logitech_USB_Receiver-if02-event-mouse",
            "KEYBOARD_EVENT_PATH": "/dev/input/by-id/usb-Logitech_USB_Receiver-event-kbd"
        }
    ]
}
```

## 🛠️ Project Structure

The project is organized into the following directories:

-   `src/`: The main source code for the application.
    -   `cli/`: Command-line interface logic.
    -   `core/`: Core components like configuration, logging, and custom exceptions.
    -   `gui/`: The GTK4/Adwaita graphical user interface.
    -   `models/`: Pydantic data models for games, profiles, and instances.
    -   `services/`: Business logic for managing instances, devices, and dependencies.
-   `docs/`: Documentation files.

## 🤝 Contributing

Contributions are welcome! If you'd like to contribute, please feel free to fork the repository, make your changes, and open a pull request.

## 📄 License

This project is distributed under the MIT License.
