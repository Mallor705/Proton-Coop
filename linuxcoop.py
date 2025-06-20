#!/usr/bin/env python3
import sys
from src.cli.commands import main as cli_main
from src.gui.app import run_gui

def main():
    args = sys.argv[1:] # Get arguments excluding the script name

    if not args:
        print("Usage: linuxcoop.py [PROFILE_NAME | gui]")
        print("  PROFILE_NAME: Launch game instances using the specified profile (CLI mode).")
        print("  gui: Launch the Linux-Coop Profile Editor GUI.")
        sys.exit(1)
    
    arg = args[0]

    if arg == "gui":
        if len(args) > 1:
            print("Erro: O comando 'gui' não aceita argumentos adicionais.", file=sys.stderr)
            sys.exit(1)
        run_gui()
    else:
        # Assume it's a profile name for CLI mode
        if len(args) > 1:
            print(f"Aviso: Argumentos adicionais ignorados para o perfil '{arg}'.", file=sys.stderr)
        cli_main(arg)

if __name__ == "__main__":
    main()