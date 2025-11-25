# MultiScope

[Ver en portugués](README.pt.md) | [Ver en inglés](../README.md) | [Ver en francés](README.fr.md)

# MultiScope

![Banner de MultiScope](https://github.com/Mallor705/MultiScope/assets/80993074/399081e7-295e-4c55-b040-02d242407559)

Permite jugar títulos de Windows en modo cooperativo local en Linux, ejecutando múltiples instancias del mismo juego a través de Proton y Gamescope, con perfiles independientes y soporte para controladores.

## Características Principales

- **Cooperativo Local Avanzado:** Ejecuta hasta dos instancias del mismo juego simultáneamente para una experiencia cooperativa local fluida.
- **Perfiles de Juego Aislados:** Mantén guardados y configuraciones independientes para cada juego a través de perfiles personalizables.
- **Flexibilidad de Ejecución:** Admite la selección de cualquier ejecutable `.exe` y varias versiones de Proton, incluido GE-Proton.
- **Resolución Personalizable:** Ajusta la resolución para cada instancia del juego individualmente.
- **Depuración Simplificada:** Generación automática de registros para facilitar la identificación y corrección de problemas.
- **Mapeo de Controladores:** Configura controladores físicos específicos para cada jugador.
- **Amplia Compatibilidad:** Admite múltiples juegos a través del sistema de perfiles.

## Estado del Proyecto

- **Funcionalidad Principal:** Los juegos se abren en instancias separadas con guardados independientes.
- **Rendimiento:** Rendimiento optimizado para una experiencia de juego fluida.
- **Gestión de Proton:** Versión de Proton totalmente seleccionable, incluido el soporte para GE-Proton.
- **Organización:** Perfiles dedicados para cada juego.

### Problemas Conocidos

- **Reconocimiento de Controladores:** En algunos casos, es posible que los controladores no sean reconocidos (prioridad para la corrección).
- **Disposición de Ventanas:** Las instancias pueden abrirse en el mismo monitor, lo que requiere un movimiento manual.

## Requisitos del Sistema

Para asegurar el correcto funcionamiento de MultiScope, los siguientes requisitos previos son esenciales:

- **Steam:** Debe estar instalado y configurado en tu sistema.
- **Proton:** Instala Proton (o GE-Proton) a través de Steam.
- **Gamescope:** Instala Gamescope siguiendo las [instrucciones oficiales](https://github.com/ValveSoftware/gamescope).
- **Bubblewrap (`bwrap`):** Herramienta esencial para el aislamiento de procesos.
- **Permisos de Dispositivo:** Asegura los permisos de acceso a los dispositivos de control en `/dev/input/by-id/`.
- **Utilidades de Linux:** Bash y utilidades básicas del sistema Linux.
- **Python 3.8+:** El proyecto requiere la versión de Python 3.8 o superior.

## Instalación

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/Mallor705/MultiScope.git
    cd MultiScope
    ```
2.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

    Alternativamente, si estás desarrollando o prefieres una instalación editable:

    ```bash
    pip install -e .
    ```

## Cómo Usar

### 1. Crea un Perfil de Juego

Crea un archivo JSON en la carpeta `profiles/` con un nombre descriptivo (ej: `MiJuego.json`).

**Contenido de Ejemplo para Pantalla Dividida Horizontal:**

```json
{
  "game_name": "JUEGO",
  "game_name": "GAME",
  "exe_path": ".steam/Steam/steamapps/common/GAME/game.exe",
  "players": [
    {
      "account_name": "Player1",
      "language": "brazilian",
      "listen_port": "",
      "user_steam_id": "76561190000000001"
    },
    {
      "account_name": "Player2",
      "language": "brazilian",
      "listen_port": "",
      "user_steam_id": "76561190000000002"
    }
  ],
  "proton_version": "GE-Proton10-4",
  "instance_width": 1920,
  "instance_height": 1080,
  "player_physical_device_ids": [
    "",
    ""
  ],
  "player_mouse_event_paths": [
    "",
    ""
  ],
  "player_keyboard_event_paths": [
    "",
    ""
  ],
  "app_id": "12345678",
  "game_args": "",
  "use_goldberg_emu": false,
  "env_vars": {
    "WINEDLLOVERRIDES": "",
    "MANGOHUD": "1"
  },
  "is_native": false,
  "mode": "splitscreen",
  "splitscreen": {
    "orientation": "horizontal",
    "instances": 2
  }
}
```

**Example Content for Vertical Splitscreen:**

```json
{
  "game_name": "GAME",
  "exe_path": ".steam/Steam/steamapps/common/GAME/game.exe",
  "players": [
    {
      "account_name": "Player1",
      "language": "brazilian",
      "listen_port": "",
      "user_steam_id": "76561190000000001"
    },
    {
      "account_name": "Player2",
      "language": "brazilian",
      "listen_port": "",
      "user_steam_id": "76561190000000002"
    }
  ],
  "proton_version": "GE-Proton10-4",
  "instance_width": 1920,
  "instance_height": 1080,
  "player_physical_device_ids": [
    "/dev/input/by-id/...",
    "/dev/input/by-id/..."
  ],
  "player_mouse_event_paths": [
    "/dev/input/by-id/...",
    "/dev/input/by-id/..."
  ],
  "player_keyboard_event_paths": [
    "/dev/input/by-id/...",
    "/dev/input/by-id/..."
  ],

  "player_audio_device_ids": [
    "",
    ""
  ],


  "app_id": "12345678",
  "game_args": "",
  "use_goldberg_emu": false,
  "env_vars": {
    "WINEDLLOVERRIDES": "",
    "MANGOHUD": "1"
  },
  "is_native": false,
  "mode": "splitscreen",
  "splitscreen": {
    "orientation": "vertical",
    "instances": 2
  }
}
```

### 2. Run the Main Script

From the project root, execute the command, replacing `<profile_name>` with the name of your profile JSON file (without the `.json` extension):

```bash
python ./multiscope.py <profile_name>
# Or, if installed via setuptools:
multi-scope <profile_name>
```

Upon execution, the script will:

- Validate all necessary dependencies.
- Load the specified game profile.
- Create separate Proton prefixes for each game instance.
- Launch both game windows via Gamescope.
- Generate detailed logs in `~/.local/share/multi-scope/logs/` for debugging.

### 3. Controller Mapping

- Controllers are configured in the profile file or in specific files within `controller_config/`.
- To avoid conflicts, controller blacklists (e.g., `Player1_Controller_Blacklist`) are automatically generated.
- **Important:** Connect all your physical controllers before starting the script.

## Testing the Installation

To verify that the prerequisites are correctly installed, run the following commands:

```bash
gamescope --version
bwrap --version
```

## Tips and Troubleshooting

-   **Controllers not recognized:** Check permissions in `/dev/input/by-id/` and confirm that device IDs are correct in your profile file.
-   **Proton not found:** Ensure that the Proton version name in your profile exactly matches the installation name in Steam.
-   **Instances on the same monitor:** Game instances may open on the same monitor. To move and organize them, you can use the following keyboard shortcuts. **Note that shortcuts may vary depending on your Linux desktop environment and personalized settings:**
      *   `Super + W` (or `Ctrl + F9` / `Ctrl + F10`): Displays an overview of all workspaces and open windows (Activities/Overview), similar to hovering the mouse in the top-left corner.
      *   `Super + Arrows (↑ ↓ ← →)`: Moves and snaps the active window to one side of the screen.
      *   `Super + PgDn`: Minimizes the active window.
      *   `Super + PgUp`: Maximizes the active window.
      *   `Alt + Tab`: Switches between open windows of different applications.
      *   `Super + D`: Minimizes all windows and shows the desktop.
-   **Debugging logs:** Consult the `~/.local/share/multi-scope/logs/` directory for detailed information about errors and script behavior.

## Important Notes

-   Tested and optimized with Palworld, but may be compatible with other games (might require adjustments in the profile file).
-   Currently, the script only supports a two-player setup.
-   For games that do not natively support multiple instances, additional solutions such as sandboxes or separate Steam accounts might be necessary.

## Contribution

Contributions are welcome! Feel free to open issues or pull requests.

## License

This project is distributed under the MIT license. Consult the `LICENSE` file in the repository for more details.
