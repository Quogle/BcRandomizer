from pathlib import Path
import subprocess
import shutil
from configs.internal_config import GAME_VERSION, MOD_VERSION

BASE = Path(__file__).resolve().parents[2]
JAVA_EXE = BASE / "dev" / "dependencies" / "jdk-21" / "bin" / "java.exe"

WORKSPACE = BASE / "dev" / "workspace"
MODDED_APKS = BASE / "moddedAPKS"

BUILD_TOOLS = BASE / "dev" / "dependencies" / "build-tools"
APKEDITOR = BASE / "dev" / "dependencies" / "apkeditor.jar"
ZIPALIGN = BUILD_TOOLS / "zipalign.exe"
APKSIGNER = BUILD_TOOLS / "apksigner.bat"
KEYSTORE = BASE / "dev" / "dependencies" / "keystore.jks"

PACKAGE = "jp.co.bcrando.battlecatsen"

OUTPUT = WORKSPACE / "output.apk"
ALIGNED_TEMP = WORKSPACE / f"BCR_aligned.apk"
MOD = MODDED_APKS / f"BCR_{MOD_VERSION}_{GAME_VERSION}.apk"
IDSIG = WORKSPACE / f"BCR_aligned.apk.idsig"

DECOMPILED = WORKSPACE / "decompiled"

# Ensure folders exist
WORKSPACE.mkdir(exist_ok=True)
MODDED_APKS.mkdir(exist_ok=True)

def compile():

    print("JAVA_EXE:", JAVA_EXE)
    print("JAVA EXISTS:", Path(JAVA_EXE).exists())
    
    print("APKEDITOR:", APKEDITOR)
    print("APKEDITOR EXISTS:", Path(APKEDITOR).exists())
    
    print("DECOMPILED:", DECOMPILED)
    print("OUTPUT:", OUTPUT)
    """Build APK from the decompiled folder."""
    print("Compiling APK...")
    subprocess.run([
        str(JAVA_EXE),
        "-jar",
        str(APKEDITOR),
        "b",
        "-i",
        str(DECOMPILED),
        "-o",
        str(OUTPUT)
    ], check=True)
    print("APK built:", OUTPUT)


def zipalign():
    """Zipalign the compiled APK."""
    print("Zipaligning APK...")
    if ALIGNED_TEMP.exists():
        ALIGNED_TEMP.unlink()

    subprocess.run([
        str(ZIPALIGN),
        "-p",
        "4",
        str(OUTPUT),
        str(ALIGNED_TEMP)
    ], check=True)

    print("Zipaligned APK:", ALIGNED_TEMP)


def sign():
    """Sign the zipaligned APK."""
    print("Signing APK...")
    subprocess.run([
        str(APKSIGNER),
        "sign",
        "--ks",
        str(KEYSTORE),
        "--ks-pass", "pass:modkey",
        str(ALIGNED_TEMP)
    ], check=True)

    if MOD.exists():
        MOD.unlink()

    shutil.move(ALIGNED_TEMP, MOD)

    if IDSIG.exists():
        IDSIG.unlink()
    
    if OUTPUT.exists():
        OUTPUT.unlink()

    print("Signed APK:", MOD)