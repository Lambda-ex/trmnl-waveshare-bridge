import sys
from pathlib import Path

# --- HACK: add local library to import path ---
ROOT = Path(__file__).resolve().parent
LIB_SRC = ROOT / "waveshare-epd-image" / "src"
sys.path.insert(0, str(LIB_SRC))
# ---------------------------------------------

# This is a dumb way of doing it but whatever...
# I'm not packaging this library properly for others to use it easily.

# Anyways. This script is called from /usr/local/bin/
# there, a custom "show_img" I made points to here

from epd_image import display_image


# Get the arguments passed from go
def parse_args(argv):
    args = {}
    for arg in argv:
        if "=" in arg:
            k, v = arg.split("=", 1)
            args[k] = v
    return args

args = parse_args(sys.argv[1:])

image_path = args.get("file")
invert = args.get("invert", "false").lower() == "true"
mode = args.get("mode", "partial")

print("TRMNL image path:", image_path)
print("invert:", invert)
print("mode:", mode)

# Take logic from trmnl, if fast mode is selected, do not refresh
doRefresh = not (mode == "fast")
print("mode determins: doRefresh:", doRefresh)

# Display the image on the e-paper display
display_image(
    image_path,
    mode="fit",
    model="epd5in65f",
    rotation=90,
    refresh=doRefresh
)