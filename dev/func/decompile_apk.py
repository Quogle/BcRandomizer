import subprocess
import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

APKEDITOR = BASE / "dev" / "dependencies" / "apkeditor.jar"

WORKSPACE = BASE / "dev" / "workspace"
DECOMPILED = WORKSPACE / "decompiled"

WORKSPACE.mkdir(exist_ok=True)

def find_apk():
    """Find the first APK in the project root."""
    apks = list(BASE.glob("*.apk"))

    if not apks:
        raise FileNotFoundError("No APK files found in the project folder.")

    return apks[0]


def decompile(apk_path: Path):
    """Decompile the APK using APKEditor."""
    print("Decompiling APK:", apk_path)

    if DECOMPILED.exists():
        print("Removing old decompiled folder...")
        shutil.rmtree(DECOMPILED)

    subprocess.run([
        "java",
        "-jar",
        str(APKEDITOR),
        "d",
        "-i",
        str(apk_path),
        "-o",
        str(DECOMPILED)
    ], check=True)

    print("Decompiled to:", DECOMPILED)

    return DECOMPILED