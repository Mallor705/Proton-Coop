import click
import shutil
import signal
import subprocess
from ..core.config import Config
from ..core.logger import Logger
from ..core.exceptions import LinuxCoopError, ProfileNotFoundError
from ..models.profile import GameProfile
from ..services.instance import InstanceService

class TerminateCLI(Exception):
    """Exceção para finalizar a CLI de forma controlada."""
    pass

class LinuxCoopCLI:
    """Interface de linha de comando para o Linux-Coop."""
    def __init__(self):
        """Inicializa a CLI com logger e serviços necessários."""
        self.logger = Logger("linux-coop", Config.LOG_DIR)
        self.instance_service = InstanceService(self.logger)
        self.setup_signal_handlers()
    
    def setup_signal_handlers(self):
        """Configura os handlers de sinal para garantir limpeza ao encerrar."""
        def signal_handler(signum, frame):
            self.logger.info("Received interrupt signal. Terminating instances...")
            self.instance_service.terminate_all()
            raise TerminateCLI()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def run(self, profile_name: str):
        """Fluxo principal de execução da CLI."""
        if not profile_name or not profile_name.strip():
            self.logger.error("O nome do perfil não pode ser vazio.")
            raise TerminateCLI()
        try:
            self._prompt_sudo()
            self.instance_service.validate_dependencies()
            
            # Carrega apenas perfil JSON
            profile_path = Config.PROFILE_DIR / f"{profile_name}.json"

            if not profile_path.exists():
                self.logger.error(f"Profile not found: {profile_path}")
                raise ProfileNotFoundError(f"Profile '{profile_name}' not found")

            profile = GameProfile.load_from_file(profile_path)
            
            self.logger.info(f"Loading profile: {profile.game_name} for {profile.effective_num_players} players")

            self.instance_service.launch_instances(profile, profile_name)
            self.instance_service.monitor_and_wait()
            self.logger.info("Script completed")
        except LinuxCoopError as e:
            self.logger.error(str(e))
            raise TerminateCLI()
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            raise TerminateCLI()
    
    def _prompt_sudo(self):
        """Solicita senha sudo usando interface gráfica (zenity) ou terminal."""
        # Primeiro verifica se já tem privilégios sudo válidos
        try:
            subprocess.run(['sudo', '-n', 'true'], check=True, capture_output=True)
            self.logger.info("Sudo credentials already valid.")
            return
        except subprocess.CalledProcessError:
            pass  # Precisa solicitar senha
        
        # Tenta usar zenity para interface gráfica
        if shutil.which('zenity'):
            try:
                self.logger.info("Requesting sudo password via graphical interface...")
                result = subprocess.run([
                    'zenity', '--password', 
                    '--title=Linux-Coop', 
                    '--text=Digite sua senha para continuar:'
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    password = result.stdout.strip()
                    # Testa a senha com sudo
                    sudo_process = subprocess.Popen(
                        ['sudo', '-S', 'true'], 
                        stdin=subprocess.PIPE, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    stdout, stderr = sudo_process.communicate(input=password + '\n')
                    
                    if sudo_process.returncode == 0:
                        self.logger.info("Sudo credentials obtained successfully.")
                        return
                    else:
                        self.logger.error("Invalid sudo password provided")
                        raise TerminateCLI()
                else:
                    self.logger.error("Password dialog cancelled by user")
                    raise TerminateCLI()
                    
            except FileNotFoundError:
                self.logger.warning("zenity not found, falling back to terminal prompt")
            except Exception as e:
                self.logger.warning(f"zenity failed: {e}, falling back to terminal prompt")
        
        # Fallback para prompt de terminal
        try:
            self.logger.info("Requesting sudo password via terminal...")
            subprocess.run(['sudo', '-v'], check=True)
            self.logger.info("Sudo credentials obtained successfully.")
        except subprocess.CalledProcessError:
            self.logger.error("Failed to validate sudo credentials")
            raise TerminateCLI()
        except FileNotFoundError:
            self.logger.error("'sudo' command not found. Cannot acquire root privileges.")
            raise TerminateCLI()

@click.command()
@click.argument('profile_name')
def main(profile_name):
    """Lança instâncias do jogo usando o perfil especificado."""
    cli = LinuxCoopCLI()
    try:
        cli.run(profile_name)
    except TerminateCLI:
        pass