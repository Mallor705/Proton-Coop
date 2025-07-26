#!/usr/bin/env python3
import sys
import subprocess
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENTRY_SCRIPT = PROJECT_ROOT / "linuxcoop.py"
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"
SPEC_FILE = PROJECT_ROOT / "linuxcoop.spec"

def check_pyinstaller():
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("PyInstaller is not installed. Installing via pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def clean_previous_builds():
    for path in [DIST_DIR, BUILD_DIR, SPEC_FILE]:
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
    print("Previous builds cleaned.")

def build_pyinstaller(onefile=True, noconsole=False, extra_args=None):
    cmd = [
        "pyinstaller",
        "--name", "linuxcoop",
        "--paths", str(PROJECT_ROOT / "src"),
        "--hidden-import", "gi.repository.Gtk",
        "--hidden-import", "cairo",
        "--collect-all", "gi",
        str(ENTRY_SCRIPT)
    ]
    if onefile:
        cmd.append("--onefile")
    if noconsole:
        cmd.append("--noconsole")
    if extra_args:
        cmd.extend(extra_args)
    print("Executing:", " ".join(cmd))
    subprocess.check_call(cmd)

def print_usage():
    print(f"""
Script to compile Linux-Coop with PyInstaller.

Usage:
    python {__file__} [--onefile/--onedir] [--console/--noconsole] [--clean] [--help] [PyInstaller arguments]

Options:
    --onefile       Generates a single executable (default).
    --onedir        Generates a folder with files (onedir mode).
    --console       Displays console when running the executable.
    --noconsole     Does not display console (default for GUI apps).
    --clean         Removes previous builds before compiling.
    --help          Displays this message.

Example:
    python {__file__} --onefile --noconsole --clean

After compilation, the executable will be in: {DIST_DIR}/
""")

def main():
    onefile = True
    noconsole = False
    clean = False
    extra_args = []

    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        print_usage()
        return

    if "--onedir" in args:
        onefile = False
        args.remove("--onedir")
    if "--onefile" in args:
        onefile = True
        args.remove("--onefile")
    if "--console" in args:
        noconsole = False
        args.remove("--console")
    if "--noconsole" in args:
        noconsole = True
        args.remove("--noconsole")
    if "--clean" in args:
        clean = True
        args.remove("--clean")

    extra_args = args  # Any remaining args are passed to PyInstaller

    if clean:
        clean_previous_builds()

    check_pyinstaller()
    build_pyinstaller(onefile=onefile, noconsole=noconsole, extra_args=extra_args)

    print("\nCompilation finished!")
    print(f"Executable generated in: {DIST_DIR}/")

if __name__ == "__main__":
    main()
