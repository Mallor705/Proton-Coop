import os
import signal
from typing import Optional

from ..core.config import Config
from ..core.exceptions import LinuxCoopError, GameNotFoundError, ProfileNotFoundError
from ..core.logger import Logger
from ..models.game import Game
from ..models.profile import Profile, GameProfile
from ..services.game_manager import GameManager
from ..services.instance import InstanceService


class TerminateCLI(Exception):
    """Custom exception used to signal a controlled termination of the CLI."""
    pass


class LinuxCoopCLI:
    """
    The main command-line interface for Proton-Coop.
    """

    def __init__(self):
        """Initializes the CLI, setting up the logger and signal handlers."""
        self.logger = Logger("proton-coop", Config.LOG_DIR)
        self.game_manager = GameManager(self.logger)
        self._instance_service: Optional[InstanceService] = None
        self.setup_signal_handlers()

    @property
    def instance_service(self) -> InstanceService:
        """Provides lazy-loaded access to the InstanceService."""
        if self._instance_service is None:
            self._instance_service = InstanceService(self.logger)
        return self._instance_service

    def setup_signal_handlers(self):
        """Configures handlers for SIGINT and SIGTERM to ensure graceful shutdown."""
        def signal_handler(signum, frame):
            self.logger.info("Interrupt signal received. Triggering graceful shutdown...")
            # Simply raising the exception is enough. The `finally` block in `run`
            # will handle the actual termination.
            raise TerminateCLI()

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def run(self, game_name: str, profile_name: str, parent_pid: Optional[int] = None):
        """
        The main execution entry point for the CLI.
        """
        if not game_name or not profile_name:
            self.logger.error("Game name and profile name cannot be empty.")
            raise TerminateCLI()

        try:
            self._validate_dependencies()
            game, profile = self._load_game_and_profile(game_name, profile_name)

            # Create the unified GameProfile object for the instance service
            unified_profile = GameProfile(game=game, profile=profile)

            self.logger.info(f"Loaded profile '{profile.profile_name}' for game: {game.game_name}")

            # Pass the unified profile to the instance service
            self.instance_service.launch_instances(unified_profile, profile.profile_name)
            self.instance_service.monitor_and_wait(parent_pid)
            self.logger.info("Script completed.")

        except LinuxCoopError as e:
            self.logger.error(str(e))
            raise TerminateCLI()
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            if self._instance_service:
                self.instance_service.terminate_all()
            raise TerminateCLI()

    def _validate_dependencies(self):
        """Executes all necessary pre-run validations."""
        self.instance_service.validate_dependencies()

    def _load_game_and_profile(self, game_name: str, profile_name: str) -> tuple[Game, Profile]:
        """Loads a game and a specific profile for it."""
        game = self.game_manager.get_game_by_name(game_name)
        if not game:
            raise GameNotFoundError(f"Game '{game_name}' not found.")

        profiles = self.game_manager.get_profiles(game)

        # Find the specific profile by name
        target_profile = next((p for p in profiles if p.profile_name == profile_name), None)

        if not target_profile:
            raise ProfileNotFoundError(f"Profile '{profile_name}' not found for game '{game_name}'.")

        return game, target_profile


def main(game_name: str, profile_name: str, parent_pid: Optional[int] = None):
    """
    The main function for the command-line entry point.
    """
    cli = LinuxCoopCLI()
    try:
        cli.run(game_name, profile_name=profile_name, parent_pid=parent_pid)
    except TerminateCLI:
        pass