import random
import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

ICON_XL = BASE / "dev" / "assets" / "apk_icons_xl"
WORKSPACE = BASE / "dev" / "workspace"
DECOMPILED = WORKSPACE / "decompiled"
RES = DECOMPILED / "resources" / "package_1" / "res"

UNIT = ["cat", "tank", "axe", "gross", "cow", "bird", "fish", "lizard", "titan", "super"]
TRAIT = ["red", "floating", "black", "angel", "alien", "zombie", "relic", "aku"]

DRAWABLE_FOLDERS = [
    "drawable",
    "drawable-xhdpi",
    "drawable-xxhdpi",
    "drawable-xxxhdpi"
]

def replace_icon():
    """Randomly replace the app icon in the decompiled APK."""
    print("Replacing app icon...")

    icon_unit = random.choice(UNIT)
    icon_trait = random.choice(TRAIT)

    new_icon_xl = ICON_XL / f"{icon_unit}_{icon_trait}.png"

    # Rare yaoi
    if random.randint(1, 4096) == 1:
        new_icon_xl = ICON_XL / "yaoi.png"

    if not new_icon_xl.exists():
        raise FileNotFoundError(f"Icon not found: {new_icon_xl}")

    # Copy icon to all drawable folders
    for folder in DRAWABLE_FOLDERS:
        target = RES / folder / "icon_foreground.png"
        shutil.copy(new_icon_xl, target)

    print(f"Icon used: {icon_unit}_{icon_trait}.png")
    print("Icon replaced in all drawable folders.")