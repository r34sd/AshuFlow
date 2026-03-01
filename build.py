"""
Build script for AshuFlow - Creates standalone Windows executable
This bundles everything including auto-setup for FFmpeg
"""

import subprocess
import sys
import os

def ensure_pyinstaller():
    """Make sure PyInstaller is installed."""
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build():
    print("=" * 50)
    print("  Building AshuFlow Executable")
    print("=" * 50)

    ensure_pyinstaller()

    # First install all dependencies so they get bundled
    print("\nInstalling dependencies...")
    deps = ["customtkinter", "pillow", "yt-dlp", "spotdl", "requests"]
    for dep in deps:
        subprocess.run([sys.executable, "-m", "pip", "install", dep, "-q"])

    print("\nCreating executable...")

    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=AshuFlow",
        "--onefile",
        "--windowed",
        "--noconfirm",
        "--clean",
        "--hidden-import=customtkinter",
        "--hidden-import=PIL",
        "--hidden-import=PIL._tkinter_finder",
        "--hidden-import=yt_dlp",
        "--hidden-import=spotdl",
        "--collect-all=customtkinter",
        "--collect-all=yt_dlp",
        "ashuflow.py"
    ]

    try:
        subprocess.run(cmd, check=True)
        print("\n" + "=" * 50)
        print("  BUILD SUCCESSFUL!")
        print("=" * 50)
        print(f"\nExecutable: {os.path.abspath('dist/AshuFlow.exe')}")
        print("\nThe .exe is fully portable - just double-click to run!")
        print("FFmpeg will be downloaded automatically on first use.")
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build()
