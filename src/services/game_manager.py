import json
import shutil
from pathlib import Path
from typing import List, Optional

from ..core.config import Config
from ..core.logger import Logger
from ..models.game import Game
from ..models.profile import Profile


class GameManager:
    """
    Manages the game and profile library stored on the file system.

    This service abstracts all file operations related to creating, reading,
    updating, and deleting games and their associated profiles. It enforces
    the new directory structure: `~/.config/proton-coop/games/[game_name]/`.
    """

    def __init__(self, logger: Logger):
        self.logger = logger
        self.games_dir = Config.GAMES_DIR
        self.games_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _sanitize_filename(name: str) -> str:
        """Creates a safe filename from a game or profile name."""
        return name.strip().replace(" ", "_").lower()

    def get_game_dir(self, game_name: str) -> Path:
        """Returns the specific directory for a given game."""
        return self.games_dir / self._sanitize_filename(game_name)

    def get_profiles_dir(self, game_name: str) -> Path:
        """Returns the profiles directory for a given game."""
        return self.get_game_dir(game_name) / "profiles"

    def get_games(self) -> List[Game]:
        """Scans the games directory and loads all found games."""
        games = []
        for game_dir in self.games_dir.iterdir():
            if game_dir.is_dir():
                game_file = game_dir / "game.json"
                if game_file.exists():
                    try:
                        game = Game.load_from_file(game_file)
                        games.append(game)
                    except Exception as e:
                        self.logger.error(f"Failed to load game from {game_file}: {e}")
        return sorted(games, key=lambda g: g.game_name)

    def get_game_by_name(self, game_name: str) -> Optional[Game]:
        """Finds and loads a single game by its name."""
        safe_name = self._sanitize_filename(game_name)
        game_dir = self.games_dir / safe_name
        game_file = game_dir / "game.json"
        if game_file.exists():
            try:
                return Game.load_from_file(game_file)
            except Exception as e:
                self.logger.error(f"Failed to load game '{game_name}' from {game_file}: {e}")
        return None

    def get_profiles(self, game: Game) -> List[Profile]:
        """Loads all profiles for a specific game."""
        profiles_dir = self.get_profiles_dir(game.game_name)
        if not profiles_dir.exists():
            return []

        profiles = []
        for profile_file in profiles_dir.glob("*.json"):
            try:
                profile = Profile.load_from_file(profile_file)
                profiles.append(profile)
            except Exception as e:
                self.logger.error(f"Failed to load profile from {profile_file}: {e}")
        return sorted(profiles, key=lambda p: p.profile_name)

    def save_game(self, game: Game):
        """Saves a game's data to its game.json file."""
        game_dir = self.get_game_dir(game.game_name)
        game_file = game_dir / "game.json"
        game.save_to_file(game_file)
        self.logger.info(f"Game '{game.game_name}' saved to {game_file}.")

    def save_profile(self, game: Game, profile: Profile):
        """Saves a profile to a JSON file within its game's directory."""
        profiles_dir = self.get_profiles_dir(game.game_name)
        profile_filename = f"{self._sanitize_filename(profile.profile_name)}.json"
        profile_path = profiles_dir / profile_filename
        profile.save_to_file(profile_path)
        self.logger.info(f"Profile '{profile.profile_name}' for game '{game.game_name}' saved to {profile_path}.")

    def add_game(self, game: Game) -> None:
        """Adds a new game to the library."""
        game_dir = self.get_game_dir(game.game_name)
        if game_dir.exists():
            raise FileExistsError(f"A game with the name '{game.game_name}' already exists.")

        # Create directories and save the game file
        profiles_dir = self.get_profiles_dir(game.game_name)
        profiles_dir.mkdir(parents=True, exist_ok=True)
        self.save_game(game)
        self.logger.info(f"Added new game '{game.game_name}' at {game_dir}")

    def add_profile(self, game: Game, profile: Profile) -> None:
        """Adds a new profile to a game."""
        profiles_dir = self.get_profiles_dir(game.game_name)
        profile_filename = f"{self._sanitize_filename(profile.profile_name)}.json"
        profile_path = profiles_dir / profile_filename

        if profile_path.exists():
            raise FileExistsError(f"A profile with the name '{profile.profile_name}' already exists for this game.")

        self.save_profile(game, profile)
        self.logger.info(f"Added new profile '{profile.profile_name}' to game '{game.game_name}'.")

    def delete_game(self, game: Game):
        """Deletes a game and all its associated profiles."""
        game_dir = self.get_game_dir(game.game_name)
        if game_dir.exists():
            shutil.rmtree(game_dir)
            self.logger.info(f"Deleted game '{game.game_name}' and all its data from {game_dir}.")
        else:
            self.logger.warning(f"Attempted to delete non-existent game directory: {game_dir}")

    def delete_profile(self, game: Game, profile: Profile):
        """Deletes a specific profile from a game."""
        profiles_dir = self.get_profiles_dir(game.game_name)
        profile_filename = f"{self._sanitize_filename(profile.profile_name)}.json"
        profile_path = profiles_dir / profile_filename

        if profile_path.exists():
            profile_path.unlink()
            self.logger.info(f"Deleted profile '{profile.profile_name}' from game '{game.game_name}'.")
        else:
            self.logger.warning(f"Attempted to delete non-existent profile file: {profile_path}")