# UMU Launcher Integration

Linux-Coop now supports using the **UMU launcher** (Unified Launcher for Windows games on Linux) as an alternative to traditional Proton execution. This integration allows you to leverage UMU's advanced features, including:

- Unified runtime environment similar to Steam's Proton
- Access to the umu-database for game-specific fixes
- Support for multiple game stores (Epic Games Store, GOG, etc.)
- Automatic download and management of Proton versions
- Better compatibility with non-Steam games

## What is UMU?

UMU (umu-launcher) is a unified launcher for Windows games on Linux that replicates Steam's Proton environment outside of Steam. It provides:

- Steam Runtime Tools containerization
- Automatic protonfixes application
- Multi-store game support
- No Steam installation required

For more information, visit: https://github.com/Open-Wine-Components/umu-launcher

## Installation

### Install UMU Launcher

Before using UMU with Linux-Coop, you need to install umu-launcher on your system.

#### Arch Linux
```bash
pacman -S umu-launcher
```

#### Nobara
```bash
dnf install umu-launcher
```

#### From Source
```bash
git clone https://github.com/Open-Wine-Components/umu-launcher.git
cd umu-launcher
./configure.sh --prefix=/usr
make
sudo make install
```

For other distributions and installation methods, see the [UMU installation guide](https://github.com/Open-Wine-Components/umu-launcher#installing).

## Configuration

To enable UMU launcher for a game profile, add the following fields to your profile JSON file:

### Basic UMU Configuration

```json
{
  "game_name": "MyGame",
  "exe_path": ".steam/Steam/steamapps/common/MyGame/game.exe",
  "use_umu": true,
  "players": [
    {
      "account_name": "Player1",
      "language": "english",
      "listen_port": "",
      "user_steam_id": "76561190000000001"
    },
    {
      "account_name": "Player2",
      "language": "english",
      "listen_port": "",
      "user_steam_id": "76561190000000002"
    }
  ],
  "instance_width": 1920,
  "instance_height": 1080,
  "player_physical_device_ids": ["", ""],
  "player_mouse_event_paths": ["", ""],
  "player_keyboard_event_paths": ["", ""],
  "app_id": "12345678",
  "game_args": "",
  "env_vars": {
    "MANGOHUD": "1"
  },
  "mode": "splitscreen",
  "splitscreen": {
    "orientation": "horizontal",
    "instances": 2
  }
}
```

### Advanced UMU Configuration

For advanced configuration with game-specific IDs and store types:

```json
{
  "game_name": "Epic Games Game",
  "exe_path": "/home/user/Games/epic-games-store/drive_c/Program Files/MyGame/game.exe",
  "use_umu": true,
  "umu_id": "umu-mygame",
  "umu_store": "egs",
  "umu_proton_path": "GE-Proton",
  "players": [
    {
      "account_name": "Player1",
      "language": "english",
      "listen_port": "",
      "user_steam_id": "76561190000000001"
    },
    {
      "account_name": "Player2",
      "language": "english",
      "listen_port": "",
      "user_steam_id": "76561190000000002"
    }
  ],
  "instance_width": 1920,
  "instance_height": 1080,
  "player_physical_device_ids": ["", ""],
  "player_mouse_event_paths": ["", ""],
  "player_keyboard_event_paths": ["", ""],
  "app_id": "12345678",
  "game_args": "-some-arg",
  "env_vars": {
    "MANGOHUD": "1",
    "DXVK_ASYNC": "1"
  },
  "mode": "splitscreen",
  "splitscreen": {
    "orientation": "vertical",
    "instances": 2
  }
}
```

## UMU Profile Fields

### Required Field

- **`use_umu`** (boolean): Set to `true` to enable UMU launcher instead of traditional Proton
  - Default: `false`

### Optional Fields

- **`umu_id`** (string): Game ID from the [umu-database](https://umu.openwinecomponents.org/)
  - Used to apply game-specific fixes
  - Default: `"umu-default"`
  - Example: `"umu-borderlands3"`

- **`umu_store`** (string): Store identifier for the game
  - Supported values: `"egs"` (Epic Games Store), `"gog"` (GOG), `"steam"`, `"none"`, etc.
  - Default: `"none"`
  - Used in combination with `umu_id` to find appropriate fixes

- **`umu_proton_path`** (string): Specific Proton version or path to use
  - Use `"GE-Proton"` to auto-download and use the latest GE-Proton
  - Or specify a full path: `"/home/user/.steam/steam/compatibilitytools.d/GE-Proton8-28"`
  - Default: Uses UMU-Proton (latest stable Valve Proton with UMU compatibility)

## How UMU Works with Linux-Coop

When you enable UMU in a profile:

1. **Dependency Check**: Linux-Coop verifies that `umu-run` is installed
2. **Environment Setup**: UMU-specific environment variables are configured:
   - `WINEPREFIX`: Points to the game instance's Wine prefix
   - `GAMEID`: Set from `umu_id` or defaults to `"umu-default"`
   - `STORE`: Set from `umu_store` or defaults to `"none"`
   - `PROTONPATH`: Set from `umu_proton_path` if specified
3. **Game Execution**: Instead of calling Proton directly, `umu-run` is used
4. **Runtime Container**: UMU automatically handles the Steam Runtime container setup
5. **Game Fixes**: UMU applies protonfixes from the umu-database if available

## Example Profiles

### Epic Games Store Game

```json
{
  "game_name": "Borderlands 3",
  "exe_path": "/home/user/Games/epic-games-store/drive_c/Program Files/Epic Games/Borderlands 3/OakGame/Binaries/Win64/Borderlands3.exe",
  "use_umu": true,
  "umu_id": "umu-borderlands3",
  "umu_store": "egs",
  "umu_proton_path": "GE-Proton",
  "players": [
    {
      "account_name": "Player1",
      "user_steam_id": "76561190000000001"
    },
    {
      "account_name": "Player2",
      "user_steam_id": "76561190000000002"
    }
  ],
  "instance_width": 1920,
  "instance_height": 1080,
  "app_id": "530380",
  "mode": "splitscreen",
  "splitscreen": {
    "orientation": "horizontal",
    "instances": 2
  }
}
```

### GOG Game with Auto-Download Latest GE-Proton

```json
{
  "game_name": "Witcher 3",
  "exe_path": "/home/user/Games/gog/The Witcher 3/bin/x64/witcher3.exe",
  "use_umu": true,
  "umu_id": "umu-witcher3",
  "umu_store": "gog",
  "umu_proton_path": "GE-Proton",
  "players": [
    {
      "account_name": "Player1",
      "user_steam_id": "76561190000000001"
    },
    {
      "account_name": "Player2",
      "user_steam_id": "76561190000000002"
    }
  ],
  "instance_width": 1920,
  "instance_height": 1080,
  "app_id": "292030",
  "mode": "splitscreen",
  "splitscreen": {
    "orientation": "vertical",
    "instances": 2
  }
}
```

### Simple UMU Setup (Minimal Configuration)

```json
{
  "game_name": "My Game",
  "exe_path": "/path/to/game.exe",
  "use_umu": true,
  "players": [
    {
      "account_name": "Player1",
      "user_steam_id": "76561190000000001"
    },
    {
      "account_name": "Player2",
      "user_steam_id": "76561190000000002"
    }
  ],
  "instance_width": 1920,
  "instance_height": 1080,
  "mode": "splitscreen",
  "splitscreen": {
    "orientation": "horizontal",
    "instances": 2
  }
}
```

## Comparing Proton vs UMU

### Traditional Proton Mode
```json
{
  "use_umu": false,
  "proton_version": "GE-Proton10-4"
}
```

### UMU Mode
```json
{
  "use_umu": true,
  "umu_proton_path": "GE-Proton"
}
```

## Benefits of Using UMU

1. **No Steam Required**: Run games without needing Steam installed
2. **Unified Fixes**: Access to centralized game fixes database
3. **Multi-Store Support**: Better support for Epic, GOG, and other stores
4. **Automatic Updates**: UMU can auto-download Proton versions
5. **Container Isolation**: Uses Steam Runtime container for better compatibility
6. **Protonfixes Integration**: Automatic application of game-specific tweaks

## Troubleshooting

### UMU not found error
```
DependencyError: umu-run is not installed
```
**Solution**: Install umu-launcher for your distribution (see Installation section)

### Game doesn't launch with UMU
**Solution**: Check logs in `~/.local/share/linux-coop/logs/` for detailed error messages

### Want to use specific Proton version
**Solution**: Set `umu_proton_path` to the full path of your Proton installation

### Need game-specific fixes
**Solution**: Check the [umu-database](https://umu.openwinecomponents.org/) for your game's `umu_id` and `store` values

## Additional Resources

- [UMU Launcher GitHub](https://github.com/Open-Wine-Components/umu-launcher)
- [UMU Database](https://umu.openwinecomponents.org/)
- [UMU Documentation](https://github.com/Open-Wine-Components/umu-launcher/blob/main/docs/umu.1.scd)
- [UMU FAQ](https://github.com/Open-Wine-Components/umu-launcher/wiki/Frequently-asked-questions-(FAQ))

## Support

If you encounter issues with UMU integration, please:

1. Check the logs in `~/.local/share/linux-coop/logs/`
2. Verify UMU is properly installed with `umu-run --help`
3. Test the game with standard UMU before using it with Linux-Coop
4. Report issues on the [Linux-Coop GitHub](https://github.com/Mallor705/Linux-Coop/issues)
