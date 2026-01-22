import sys
from pathlib import Path

# --- HACK: add local library to import path ---
ROOT = Path(__file__).resolve().parent
LIB_SRC = ROOT / "waveshare-epd-image" / "src"
sys.path.insert(0, str(LIB_SRC))
# ---------------------------------------------

# This is a dumb way of doing it but whatever.

from epd_image import display_image