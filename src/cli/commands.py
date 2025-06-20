import signal
import subprocess
from functools import lru_cache
from typing import Optional
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
        """Inicializa a CLI com logger e configuração de sinais."""
        self.logger = Logger("linux-coop", Config.LOG_DIR)
        self._instance_service: Optional[InstanceService] = None
        self.setup_signal_handlers()
    
    @property
    def instance_service(self) -> InstanceService:
        """Lazy loading do InstanceService."""
        if self._instance_service is None:
            self._instance_service = InstanceService(self.logger)
        return self._instance_service
    
    def setup_signal_handlers(self):
        """Configura os handlers de sinal para garantir limpeza ao encerrar."""
        def signal_handler(signum, frame):
            self.logger.info("Received interrupt signal. Terminating instances...")
            if self._instance_service is not None:
                self._instance_service.terminate_all()
            raise TerminateCLI()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def run(self, profile_name: str):
        """Fluxo principal de execução da CLI."""
        if not profile_name or not profile_name.strip():
            self.logger.error("O nome do perfil não pode ser vazio.")
            raise TerminateCLI()
        try:
            # Validações em lote
            self._batch_validate(profile_name)
            
            # Carrega perfil (com cache)
            profile = self._load_profile(profile_name)
            self.logger.info(f"Loaded profile env_vars: {profile.env_vars}")
            
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
    
    def _batch_validate(self, profile_name: str):
        """Executa todas as validações necessárias em lote."""
        # Validate dependencies (cached in InstanceService)
        self.instance_service.validate_dependencies()
        
        # Validate profile exists
        profile_path = Config.PROFILE_DIR / f"{profile_name}.json"
        if not profile_path.exists():
            self.logger.error(f"Profile not found: {profile_path}")
            raise ProfileNotFoundError(f"Profile '{profile_name}' not found")
    
    @lru_cache(maxsize=16)
    def _load_profile(self, profile_name: str) -> GameProfile:
        """Carrega perfil com cache."""
        profile_path = Config.PROFILE_DIR / f"{profile_name}.json"
        return GameProfile.load_from_file(profile_path)

def main(profile_name):
    """Lança instâncias do jogo usando o perfil especificado."""
    cli = LinuxCoopCLI()
    try:
        cli.run(profile_name)
    except TerminateCLI:
        pass