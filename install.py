"""
AshuFlow - Python Dependency Installer
Run this after Python is installed to set up all required packages.
Usage: python install.py
"""

import subprocess
import sys
import os
from pathlib import Path

APP_DIR = Path(__file__).parent.absolute()

REQUIRED_PACKAGES = [
    ("customtkinter", "customtkinter>=5.2.0"),
    ("PIL", "pillow>=10.0.0"),
    ("yt_dlp", "yt-dlp>=2024.0.0"),
    ("requests", "requests>=2.31.0"),
    ("spotdl", "spotdl>=4.2.0"),
]


def print_header():
    print("=" * 50)
    print("  AshuFlow - Dependency Installer")
    print("=" * 50)
    print()


def ensure_pip():
    """Make sure pip is available."""
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("  Installing pip...")
        subprocess.check_call([sys.executable, "-m", "ensurepip", "--default-pip"])
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip", "-q"]
        )


def install_from_requirements():
    """Install packages from requirements.txt if it exists."""
    req_file = APP_DIR / "requirements.txt"
    if req_file.exists():
        print("  Installing from requirements.txt...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(req_file)],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return True
        else:
            print(f"  Warning: {result.stderr.strip()}")
            return False
    return False


def install_packages():
    """Install all required packages individually with status output."""
    total = len(REQUIRED_PACKAGES)
    failed = []

    for i, (module_name, pip_name) in enumerate(REQUIRED_PACKAGES, 1):
        # Check if already installed
        try:
            __import__(module_name)
            print(f"  [{i}/{total}] {pip_name} - already installed")
            continue
        except ImportError:
            pass

        print(f"  [{i}/{total}] Installing {pip_name}...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", pip_name, "-q"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"           Done!")
        else:
            print(f"           FAILED: {result.stderr.strip()[:200]}")
            failed.append(pip_name)

    return failed


def verify_installation():
    """Verify all packages can be imported."""
    print("\n  Verifying installation...")
    all_ok = True
    for module_name, pip_name in REQUIRED_PACKAGES:
        try:
            __import__(module_name)
            print(f"    [OK] {pip_name}")
        except ImportError:
            print(f"    [FAIL] {pip_name}")
            all_ok = False
    return all_ok


def main():
    print_header()

    print(f"  Python: {sys.version}")
    print(f"  App directory: {APP_DIR}")
    print()

    # Step 1: Ensure pip
    print("[1/3] Checking pip...")
    ensure_pip()
    print("  [OK] pip is available")
    print()

    # Step 2: Install packages
    print("[2/3] Installing packages...")
    if not install_from_requirements():
        failed = install_packages()
        if failed:
            print(f"\n  Warning: These packages failed to install: {', '.join(failed)}")
    print()

    # Step 3: Verify
    print("[3/3] Verification...")
    if verify_installation():
        print()
        print("=" * 50)
        print("  Setup Complete! All packages installed.")
        print("=" * 50)
        print()
        print("  Run AshuFlow with:")
        print(f"    {sys.executable} ashuflow.py")
        print("  Or double-click AshuFlow.bat")
        print()
    else:
        print()
        print("=" * 50)
        print("  Setup finished with errors.")
        print("  Some packages could not be installed.")
        print("  Try running this script again or install manually:")
        print(f"    {sys.executable} -m pip install -r requirements.txt")
        print("=" * 50)
        print()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
