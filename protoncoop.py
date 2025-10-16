#!/usr/bin/env python3
import sys
import argparse
from src.cli.commands import main as cli_main
from src.gui.app import run_gui
from src.core.config import Config

def main():
    """
    Main entry point for the Proton-Coop application.
    Parses command-line arguments to determine execution flow.
    """
    parser = argparse.ArgumentParser(
        description="Run games with isolated instances for local co-op."
    )
    parser.add_argument(
        "game_name",
        nargs="?",
        help="The name of the game to launch. If omitted, the GUI will start."
    )
    parser.add_argument(
        "--profile",
        type=str,
        required=False,
        help="The specific profile to use for the game."
    )
    parser.add_argument(
        "--parent-pid",
        type=int,
        help="The PID of a parent process to monitor for termination."
    )

    args = parser.parse_args()

    # Run migration only if not launching from another process that already did it.
    if not args.parent_pid:
        Config.migrate_legacy_paths()

    if not args.game_name:
        run_gui()
    else:
        if not args.profile:
            print("Error: --profile is required when a game_name is specified.", file=sys.stderr)
            sys.exit(1)
        cli_main(
            game_name=args.game_name,
            profile_name=args.profile,
            parent_pid=args.parent_pid
        )

if __name__ == "__main__":
    main()