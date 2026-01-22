#!/usr/bin/env python3
"""
setup.py - TRMNL Waveshare bridge installer

Run:
  sudo python3 setup.py

What it does:
- Installs/updates /usr/local/bin/show_img as a shell wrapper
  that calls this repo's display_trmnl.py.
- Backs up any existing /usr/local/bin/show_img first.
"""

# warning! only run if my version of /usr/local/bin/show_img is broken or doesn't exist!
from __future__ import annotations

import os
import platform
import shutil
import stat
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=check, text=True, capture_output=True)


def require_root() -> None:
    if os.geteuid() != 0:
        print("ERROR: This script must be run as root (use sudo).", file=sys.stderr)
        sys.exit(1)


def sanity_check_platform() -> None:
    if platform.system().lower() != "linux":
        print("WARNING: This installer is intended for Linux (Raspberry Pi).", file=sys.stderr)


def main() -> None:
    require_root()
    sanity_check_platform()

    # Resolve repo root as the directory containing this setup.py
    repo_root = Path(__file__).resolve().parent
    py_script = repo_root / "display_trmnl.py"

    if not py_script.exists():
        print(f"ERROR: Can't find {py_script}", file=sys.stderr)
        print("Make sure setup.py is in the same folder as display_trmnl.py.", file=sys.stderr)
        sys.exit(1)

    target = Path("/usr/local/bin/show_img")
    target.parent.mkdir(parents=True, exist_ok=True)

    # Backup existing show_img in /usr/local/bin (if any)
    if target.exists() or target.is_symlink():
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = Path(f"{target}.bak.{ts}")
        print(f"Backing up existing {target} -> {backup}")
        target.rename(backup)

    # Build wrapper script content
    # Use python3 from PATH. (If you later want a venv, hardcode its python path here.)
    wrapper = f"""#!/usr/bin/env bash
set -euo pipefail

echo "[show_img wrapper] called with args: $*" >&2
echo "[show_img wrapper] running python: {py_script}" >&2

exec python3 "{py_script}" "$@"
"""

    print(f"Writing wrapper to {target}")
    target.write_text(wrapper, encoding="utf-8")

    # Make executable: chmod 755
    mode = target.stat().st_mode
    target.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    # Show what will run on PATH
    try:
        resolved = run(["bash", "-lc", "command -v show_img"], check=True).stdout.strip()
    except subprocess.CalledProcessError as e:
        resolved = ""
        print("WARNING: could not resolve show_img on PATH.", file=sys.stderr)
        print(e.stderr, file=sys.stderr)

    print("\nInstalled.")
    print(f"Expected show_img path : {target}")
    print(f"Resolved show_img path : {resolved or '(not found)'}")

    # Print the installed wrapper (first few lines)
    print("\nshow_img contents (first 20 lines):")
    try:
        lines = target.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines[:20], start=1):
            print(f"{i:02d}: {line}")
    except Exception as e:
        print(f"(could not read wrapper back: {e})", file=sys.stderr)

    # Optional smoke test (doesn't fail setup)
    print("\nOptional smoke test:")
    print("  show_img file=/tmp/test.png invert=false mode=partial")
    print("Note: this will fail if /tmp/test.png doesn't exist; that's OK.")

    print("\nDone.")


if __name__ == "__main__":
    main()
