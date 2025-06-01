import os
import time
import shutil
from pathlib import Path
from typing import List, Optional
from ..core.config import Config
from ..core.exceptions import DependencyError
from ..core.logger import Logger
from ..models.profile import GameProfile
from ..models.instance import GameInstance
from .proton import ProtonService
from .process import ProcessService

class InstanceService:
    """Serviço responsável por gerenciar instâncias do jogo, incluindo validação de dependências, criação, lançamento e monitoramento."""
    def __init__(self, logger: Logger):
        """Inicializa o serviço de instâncias com logger, ProtonService e ProcessService."""
        self.logger = logger
        self.proton_service = ProtonService(logger)
        self.process_service = ProcessService(logger)

    def validate_dependencies(self) -> None:
        """Valida se todos os comandos necessários estão disponíveis no sistema."""
        self.logger.info("Validating dependencies...")
        for cmd in Config.REQUIRED_COMMANDS:
            if not shutil.which(cmd):
                raise DependencyError(f"Required command '{cmd}' not found")
        self.logger.info("Dependencies validated successfully")

    def launch_instances(self, profile: GameProfile, profile_name: str) -> None:
        """Lança todas as instâncias do jogo conforme o perfil fornecido."""
        if profile.is_native:
            proton_path = None
            steam_root = None
        else:
            proton_path, steam_root = self.proton_service.find_proton_path(profile.proton_version or "Experimental")

        self.process_service.cleanup_previous_instances(proton_path, profile.exe_path)

        Config.LOG_DIR.mkdir(parents=True, exist_ok=True)
        (Path.home() / '.config/protonfixes').mkdir(parents=True, exist_ok=True)
        Config.PREFIX_BASE_DIR.mkdir(parents=True, exist_ok=True)

        instances = self._create_instances(profile, profile_name)

        self.logger.info(f"Launching {profile.num_players} instance(s) of '{profile.game_name}'...")

        original_game_path = profile.exe_path.parent

        for instance in instances:
            self._launch_single_instance(instance, profile, proton_path, steam_root, original_game_path)
            time.sleep(5)

        self.logger.info(f"All {profile.num_players} instances launched")
        self.logger.info(f"PIDs: {self.process_service.pids}")
        self.logger.info("Press CTRL+C to terminate all instances")

    def _create_instances(self, profile: GameProfile, profile_name: str) -> List[GameInstance]:
        """Cria os modelos de instância para cada jogador."""
        instances = []
        for i in range(1, profile.num_players + 1):
            prefix_dir = Config.PREFIX_BASE_DIR / f"{profile_name}_instance_{i}"
            log_file = Config.LOG_DIR / f"{profile_name}_instance_{i}.log"
            prefix_dir.mkdir(parents=True, exist_ok=True)
            (prefix_dir / "pfx").mkdir(exist_ok=True)
            instance = GameInstance(
                instance_num=i,
                profile_name=profile_name,
                prefix_dir=prefix_dir,
                log_file=log_file
            )
            instances.append(instance)
        return instances

    def _create_game_directory_symlink_structure(self, instance: GameInstance, original_game_path: Path, original_exe_path: Path, profile: GameProfile) -> Path:
        """Cria uma estrutura de diretórios espelhada com symlinks para a pasta original do jogo.
        Retorna o caminho para o link simbólico do executável principal.
        """
        instance_game_root = instance.prefix_dir / "game_files"
        instance_game_root.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"Instance {instance.instance_num}: Creating symlink structure for {original_game_path} at {instance_game_root}")

        # Determina o caminho relativo do executável original em relação à pasta raiz do jogo.
        try:
            relative_exe_path = original_exe_path.relative_to(original_game_path)
        except ValueError as e:
            # Isso pode acontecer se original_exe_path não estiver dentro de original_game_path
            self.logger.error(f"Instance {instance.instance_num}: Executable path {original_exe_path} is not inside game path {original_game_path}. Error: {e}")
            raise

        # Caminho esperado para o link simbólico do executável
        symlinked_exe_path_target = instance_game_root / relative_exe_path

        self._process_game_files(instance, original_game_path, instance_game_root, profile)
        self._verify_executable_symlink(instance, symlinked_exe_path_target, original_exe_path)

        return symlinked_exe_path_target

    def _process_game_files(self, instance: GameInstance, original_game_path: Path, instance_game_root: Path, profile: GameProfile) -> None:
        """Processa todos os arquivos do jogo, criando symlinks ou copiando conforme necessário."""
        config_files_to_copy = [
            "account_name.txt",
            "language.txt",
            "listen_port.txt",
            "user_steam_id.txt"
        ]

        for item in original_game_path.rglob("*"):
            relative_item_path = item.relative_to(original_game_path)
            target_path_for_item = instance_game_root / relative_item_path

            # Garante que o diretório pai do item (seja arquivo ou diretório) exista na estrutura de destino
            target_path_for_item.parent.mkdir(parents=True, exist_ok=True)

            if item.is_dir():
                target_path_for_item.mkdir(parents=True, exist_ok=True)
            else:
                self._process_game_file(instance, item, target_path_for_item, config_files_to_copy, profile)

    def _process_game_file(self, instance: GameInstance, item: Path, target_path_for_item: Path, config_files_to_copy: List[str], profile: GameProfile) -> None:
        """Processa um arquivo individual do jogo."""
        if target_path_for_item.exists() or target_path_for_item.is_symlink():
            target_path_for_item.unlink()

        if item.name in config_files_to_copy:
            self._handle_config_file(instance, item, target_path_for_item, profile)
        else:
            target_path_for_item.symlink_to(item)
            self.logger.info(f"Instance {instance.instance_num}: Created symlink: {target_path_for_item} -> {item}")

    def _handle_config_file(self, instance: GameInstance, item: Path, target_path_for_item: Path, profile: GameProfile) -> None:
        """Manipula arquivos de configuração, copiando e customizando conforme necessário."""
        shutil.copy2(item, target_path_for_item)
        self.logger.info(f"Instance {instance.instance_num}: Copied config file: {target_path_for_item} from {item}")

        # Verifica se há configurações específicas da instância para este arquivo
        if profile.player_configs and (instance.instance_num - 1) < len(profile.player_configs):
            instance_config = profile.player_configs[instance.instance_num - 1]
            content_to_write = self._get_config_content(item.name, instance_config)

            if content_to_write is not None:
                with open(target_path_for_item, 'w') as f_config:
                    f_config.write(str(content_to_write) + '\n')
                self.logger.info(f"Instance {instance.instance_num}: Customized config file {target_path_for_item} with value: '{content_to_write}'")

    def _get_config_content(self, filename: str, instance_config) -> Optional[str]:
        """Retorna o conteúdo personalizado para um arquivo de configuração específico."""
        if filename == "account_name.txt" and instance_config.account_name is not None:
            return instance_config.account_name
        elif filename == "language.txt" and instance_config.language is not None:
            return instance_config.language
        elif filename == "listen_port.txt" and instance_config.listen_port is not None:
            return instance_config.listen_port
        elif filename == "user_steam_id.txt" and instance_config.user_steam_id is not None:
            return instance_config.user_steam_id
        return None

    def _verify_executable_symlink(self, instance: GameInstance, symlinked_exe_path_target: Path, original_exe_path: Path) -> None:
        """Verifica se o link simbólico para o executável foi criado corretamente."""
        if not symlinked_exe_path_target.exists() or not symlinked_exe_path_target.is_symlink():
            self.logger.error(f"Instance {instance.instance_num}: Expected symlinked executable at {symlinked_exe_path_target} was not found or is not a symlink.")
            # Adicionalmente, verificar se o alvo do symlink é o executável original
            if symlinked_exe_path_target.is_symlink() and Path(os.readlink(str(symlinked_exe_path_target))) != original_exe_path:
                 self.logger.error(f"Instance {instance.instance_num}: Symlink {symlinked_exe_path_target} points to {os.readlink(str(symlinked_exe_path_target))}, not {original_exe_path}")
            raise FileNotFoundError(f"Failed to create or verify symlink for executable {original_exe_path} at {symlinked_exe_path_target}")

        self.logger.info(f"Instance {instance.instance_num}: Symlinked executable verified at: {symlinked_exe_path_target}")

    def _launch_single_instance(self, instance: GameInstance, profile: GameProfile,
                              proton_path: Optional[Path], steam_root: Optional[Path], original_game_path: Path) -> None:
        """Lança uma única instância do jogo."""
        self.logger.info(f"Preparing instance {instance.instance_num}...")

        symlinked_executable_path = self._create_game_directory_symlink_structure(
            instance,
            original_game_path,
            profile.exe_path,
            profile # Passando o objeto profile completo
        )

        env = self._prepare_environment(instance, steam_root, profile)
        cmd = self._build_command(profile, proton_path, instance, symlinked_executable_path)
        self.logger.info(f"Launching instance {instance.instance_num} (Log: {instance.log_file})")
        pid = self.process_service.launch_instance(cmd, instance.log_file, env)
        instance.pid = pid
        self.logger.info(f"Instance {instance.instance_num} started with PID: {pid}")

    def _prepare_environment(self, instance: GameInstance, steam_root: Optional[Path], profile: Optional[GameProfile] = None) -> dict:
        """Prepara as variáveis de ambiente para a instância do jogo, incluindo isolamento de controles e configuração XKB."""
        env = os.environ.copy()
        env['PATH'] = os.environ['PATH']

        # Limpar variáveis Python potencialmente conflitantes
        env.pop('PYTHONHOME', None)
        env.pop('PYTHONPATH', None)

        if not profile.is_native if profile else False:
            if steam_root:
                env['STEAM_COMPAT_CLIENT_INSTALL_PATH'] = str(steam_root)
            env['STEAM_COMPAT_DATA_PATH'] = str(instance.prefix_dir)
            env['WINEPREFIX'] = str(instance.prefix_dir / 'pfx')
            env['DXVK_ASYNC'] = '1'
            env['DXVK_LOG_LEVEL'] = 'info'

            self.logger.info(f"Instance {instance.instance_num}: Setting DXVK_ASYNC=1 for async shader compilation")
            self.logger.info(f"Instance {instance.instance_num}: Setting DXVK_LOG_LEVEL=info and DXVK_HUD=compiler for debugging")
            if profile and profile.app_id:
                env['SteamAppId'] = profile.app_id
                env['SteamGameId'] = profile.app_id
                self.logger.info(f"Instance {instance.instance_num}: Setting SteamAppId={profile.app_id} and SteamGameId={profile.app_id}")

        # Configuração XKB para layout de teclado
        xkb_vars = [
            'XKB_DEFAULT_LAYOUT', 'XKB_DEFAULT_VARIANT', 'XKB_DEFAULT_RULES',
            'XKB_DEFAULT_MODEL', 'XKB_DEFAULT_OPTIONS'
        ]
        for var in xkb_vars:
            if var in os.environ:
                env[var] = os.environ[var]
                self.logger.info(f"Instance {instance.instance_num}: Setting XKB var {var}={os.environ[var]}")

        assigned_joystick_path = None
        if profile and profile.player_physical_device_ids:
            idx = instance.instance_num - 1
            if 0 <= idx < len(profile.player_physical_device_ids):
                device_from_profile = profile.player_physical_device_ids[idx]
                if device_from_profile and device_from_profile.strip():
                    if Path(device_from_profile).exists():
                        self.logger.info(f"Instance {instance.instance_num}: Valid joystick device '{device_from_profile}' found. Assigning for SDL.")
                        assigned_joystick_path = device_from_profile
                    else:
                        self.logger.warning(f"Instance {instance.instance_num}: Joystick device '{device_from_profile}' from profile not found on host.")
                else:
                    self.logger.info(f"Instance {instance.instance_num}: No joystick device configured in profile for this instance.")

        if assigned_joystick_path:
            env['SDL_JOYSTICK_DEVICE'] = assigned_joystick_path
            self.logger.info(f"Instance {instance.instance_num}: SDL_JOYSTICK_DEVICE set to '{assigned_joystick_path}'")
        else:
            # Se nenhum joystick específico for atribuído, é importante não definir SDL_JOYSTICK_DEVICE
            # ou defini-lo para algo que efetivamente o desabilite, se necessário,
            # para evitar que a SDL pegue o primeiro joystick disponível no sandbox do bwrap.
            # No entanto, com o bwrap vinculando dispositivos específicos, isso pode não ser estritamente necessário.
            # Por segurança e clareza, vamos remover qualquer configuração SDL_JOYSTICK_DEVICE pré-existente se nenhum dispositivo for atribuído.
            if 'SDL_JOYSTICK_DEVICE' in env:
                del env['SDL_JOYSTICK_DEVICE']
            self.logger.info(f"Instance {instance.instance_num}: No specific joystick device assigned. SDL_JOYSTICK_DEVICE unset.")

        return env

    def _build_command(self, profile: GameProfile, proton_path: Optional[Path], instance: GameInstance, symlinked_exe_path: Path) -> List[str]:
        """Monta o comando para executar o gamescope e o jogo (nativo ou via Proton), usando bwrap para isolar o controle."""
        instance_idx = instance.instance_num - 1

        # Validar dispositivos de entrada
        device_info = self._validate_input_devices(profile, instance_idx, instance.instance_num)

        # Construir comando do Gamescope
        gamescope_cmd = self._build_gamescope_command(profile, device_info['should_add_grab_flags'], instance.instance_num)

        # Construir comando base do jogo
        base_cmd = self._build_base_game_command(profile, proton_path, symlinked_exe_path, gamescope_cmd, instance.instance_num)

        # Construir comando bwrap com dispositivos
        bwrap_cmd = self._build_bwrap_command(profile, instance_idx, device_info, instance.instance_num)

        final_cmd = bwrap_cmd + base_cmd
        final_bwrap_cmd_str = ' '.join(final_cmd)
        self.logger.info(f"Instance {instance.instance_num}: Full bwrap command: {final_bwrap_cmd_str}")

        return final_cmd

    def _validate_input_devices(self, profile: GameProfile, instance_idx: int, instance_num: int) -> dict:
        """Valida dispositivos de entrada e retorna informações sobre eles."""
        # Determinar se esta instância terá mouse e teclado dedicados e válidos
        has_dedicated_mouse = False
        mouse_path_str_for_instance = None
        if profile.player_mouse_event_paths and 0 <= instance_idx < len(profile.player_mouse_event_paths):
            mouse_path_str_for_instance = profile.player_mouse_event_paths[instance_idx]
            if mouse_path_str_for_instance and mouse_path_str_for_instance.strip():
                mouse_path_obj = Path(mouse_path_str_for_instance)
                if mouse_path_obj.exists() and mouse_path_obj.is_char_device():
                    has_dedicated_mouse = True
                else:
                    self.logger.warning(f"Instance {instance_num}: Mouse device '{mouse_path_str_for_instance}' specified in profile but not found or not a char device.")

        has_dedicated_keyboard = False
        keyboard_path_str_for_instance = None
        if profile.player_keyboard_event_paths and 0 <= instance_idx < len(profile.player_keyboard_event_paths):
            keyboard_path_str_for_instance = profile.player_keyboard_event_paths[instance_idx]
            if keyboard_path_str_for_instance and keyboard_path_str_for_instance.strip():
                keyboard_path_obj = Path(keyboard_path_str_for_instance)
                if keyboard_path_obj.exists() and keyboard_path_obj.is_char_device():
                    has_dedicated_keyboard = True
                else:
                    self.logger.warning(f"Instance {instance_num}: Keyboard device '{keyboard_path_str_for_instance}' specified in profile but not found or not a char device.")

        return {
            'has_dedicated_mouse': has_dedicated_mouse,
            'mouse_path_str_for_instance': mouse_path_str_for_instance,
            'has_dedicated_keyboard': has_dedicated_keyboard,
            'keyboard_path_str_for_instance': keyboard_path_str_for_instance,
            'should_add_grab_flags': has_dedicated_mouse and has_dedicated_keyboard
        }

    def _build_gamescope_command(self, profile: GameProfile, should_add_grab_flags: bool, instance_num: int) -> List[str]:
        """Constrói o comando do Gamescope."""
        gamescope_path = 'gamescope'
        gamescope_cli_options = [
            gamescope_path,
            '-W', str(profile.instance_width),
            '-H', str(profile.instance_height),
            '-w', str(profile.instance_width),
            '-h', str(profile.instance_height),
            '-f',
            '--adaptive-sync',
        ]

        if should_add_grab_flags:
            self.logger.info(f"Instance {instance_num}: Using dedicated mouse and keyboard. Adding --grab and --force-grab-cursor to Gamescope.")
            gamescope_cli_options.extend(['--grab', '--force-grab-cursor'])

        return gamescope_cli_options

    def _build_base_game_command(self, profile: GameProfile, proton_path: Optional[Path], symlinked_exe_path: Path, gamescope_cmd: List[str], instance_num: int) -> List[str]:
        """Constrói o comando base do jogo."""
        # Adiciona os argumentos do jogo definidos no perfil, se houver
        game_specific_args = []
        if profile.game_args:
            game_specific_args = profile.game_args.split()
            self.logger.info(f"Instance {instance_num}: Adding game arguments: {game_specific_args}")

        base_cmd_prefix = gamescope_cmd + ['--']  # Separador para o comando a ser executado

        if profile.is_native:
            base_cmd = list(base_cmd_prefix)
            if symlinked_exe_path:
                base_cmd.append(str(symlinked_exe_path))
                base_cmd.extend(game_specific_args)
        else:
            base_cmd = list(base_cmd_prefix)
            if proton_path and symlinked_exe_path:
                base_cmd.extend([str(proton_path), 'run', str(symlinked_exe_path)])
                base_cmd.extend(game_specific_args)

        return base_cmd

    def _build_bwrap_command(self, profile: GameProfile, instance_idx: int, device_info: dict, instance_num: int) -> List[str]:
        """Constrói o comando bwrap com dispositivos de entrada."""
        bwrap_cmd = [
            'bwrap',
            '--dev-bind', '/', '/',
            '--proc', '/proc',
            '--tmpfs', '/tmp',
            '--cap-add', 'all',
        ]

        # Ensure ProtonFixes config directory is accessible inside bwrap
        protonfixes_config_dir = Path.home() / '.config' / 'protonfixes'
        bwrap_cmd.extend(['--bind', str(protonfixes_config_dir), str(protonfixes_config_dir)])
        self.logger.info(f"Instance {instance_num}: Added bwrap bind for ProtonFixes: {protonfixes_config_dir}")

        device_paths_to_bind = self._collect_device_paths(profile, instance_idx, device_info, instance_num)

        if device_paths_to_bind:
            bwrap_cmd.extend(['--tmpfs', '/dev/input'])
            for device_path in device_paths_to_bind:
                bwrap_cmd.extend(['--dev-bind', device_path, device_path])
                self.logger.info(f"Instance {instance_num}: bwrap will bind '{device_path}' to '{device_path}'.")
        else:
            self.logger.info(f"Instance {instance_num}: No specific input devices to bind with bwrap. Creating an empty isolated /dev/input.")
            bwrap_cmd.extend(['--tmpfs', '/dev/input'])

        return bwrap_cmd

    def _collect_device_paths(self, profile: GameProfile, instance_idx: int, device_info: dict, instance_num: int) -> List[str]:
        """Coleta os caminhos dos dispositivos a serem vinculados."""
        device_paths_to_bind = []

        # Joysticks
        if profile.player_physical_device_ids and 0 <= instance_idx < len(profile.player_physical_device_ids):
            joystick_path_str = profile.player_physical_device_ids[instance_idx]
            if joystick_path_str and joystick_path_str.strip():
                joystick_path = Path(joystick_path_str)
                if joystick_path.exists() and joystick_path.is_char_device():
                    device_paths_to_bind.append(str(joystick_path))
                    self.logger.info(f"Instance {instance_num}: Queued joystick '{joystick_path}' for bwrap binding.")
                else:
                    self.logger.warning(f"Instance {instance_num}: Joystick device '{joystick_path_str}' specified in profile but not found or not a char device. Not binding.")

        # Mouses - usa as variáveis já validadas
        if device_info['has_dedicated_mouse']:
            device_paths_to_bind.append(device_info['mouse_path_str_for_instance'])
            self.logger.info(f"Instance {instance_num}: Queued mouse device '{device_info['mouse_path_str_for_instance']}' for bwrap binding.")

        # Teclados - usa as variáveis já validadas
        if device_info['has_dedicated_keyboard']:
            device_paths_to_bind.append(device_info['keyboard_path_str_for_instance'])
            self.logger.info(f"Instance {instance_num}: Queued keyboard device '{device_info['keyboard_path_str_for_instance']}' for bwrap binding.")

        return device_paths_to_bind

    def monitor_and_wait(self) -> None:
        """Monitora as instâncias até que todas sejam finalizadas."""
        while self.process_service.monitor_processes():
            time.sleep(5)

        self.logger.info("All instances have terminated")

    def terminate_all(self) -> None:
        """Finaliza todas as instâncias do jogo gerenciadas pelo serviço."""
        self.process_service.terminate_all()
