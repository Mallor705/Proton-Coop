#!/usr/bin/env python3
from src.gui.app import run_gui
from src.core.config import Config

def main():
    """
    Main entry point for the MultiScope application.
    """
    Config.migrate_legacy_paths()
    run_gui()

if __name__ == "__main__":
    main()
