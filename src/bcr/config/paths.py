import sys
from pathlib import Path
import subprocess # no sense in it

if getattr(sys, "frozen", False):
    TOOLS_DIR = Path(sys._MEIPASS) / "resources" / "tools"
else:
    TOOLS_DIR = Path(__file__).resolve().parents[3] / "resources" / "tools"

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parents[3]

# Tool Paths
APKTOOL_PATH = TOOLS_DIR/"apktool.jar"
ZIPALIGN_PATH = TOOLS_DIR/"windows"/"build-tools"/"zipalign.exe"
APKSIGNER_PATH = (TOOLS_DIR/"windows"/"build-tools"/"apksigner.bat")
KEYSTORE_PATH = (TOOLS_DIR/"keystore"/"bcrando.jks")


# Decompiled Apk Paths
WORKSPACE = Path("workspace")
DECOMPILED = WORKSPACE / "decoded"
RES = DECOMPILED / "res"