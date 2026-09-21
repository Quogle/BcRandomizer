import sys
from pathlib import Path
import subprocess # no sense in it
from os.path import join

if getattr(sys, "frozen", False):
    TOOLS_DIR = Path(sys._MEIPASS) / "resources" / "tools"
else:
    TOOLS_DIR = Path(__file__).resolve().parents[3] / "resources" / "tools"

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parents[3]

# Tool Paths
if sys.platform == "win32":
    ZIPALIGN_PATH = TOOLS_DIR/"windows"/"zipalign.exe"
    APKSIGNER_PATH = TOOLS_DIR/"windows"/"apksigner.bat"
elif sys.platform == "linux":
    ZIPALIGN_PATH = TOOLS_DIR/"linux"/"zipalign"
    APKSIGNER_PATH = TOOLS_DIR/"linux"/"apksigner"
elif sys.platform == "darwin":
    ZIPALIGN_PATH = TOOLS_DIR/"macos"/"zipalign"
    APKSIGNER_PATH = TOOLS_DIR/"macos"/"apksigner"

APKTOOL_PATH = TOOLS_DIR/"apktool.jar"
KEYSTORE_PATH = (TOOLS_DIR/"keystore"/"bcrando.jks")


RESOURCES = Path("resources")
ASSETS = RESOURCES / "assets"
TOOLS = RESOURCES / "tools"


# Decompiled Apk Paths
WORKSPACE = Path("workspace")
DECOMPILED = WORKSPACE / "decoded"
RES = DECOMPILED / "res"
LIBPATH = DECOMPILED / "lib" / "x86_64" / "libnative-lib.so"
APKASSETS = DECOMPILED / "assets"
DOWNLOADLOCALPACK = APKASSETS / "DownloadLocal.pack"


# Game File Paths
DECRYPTED = WORKSPACE / "decrypted"
DOWNLOADLOCAL = DECRYPTED / "DownloadLocal"
SERVERDIRECTORY = WORKSPACE / "en_server" #this is where the server list/pack files are stored before being decrypted I believe
VANILLAFILES = DECRYPTED / "vanilla_files"
SERVERFILES = DECRYPTED / "server" #this is where the server pack files have their output?
LOCALFILES = DECRYPTED / "local"
GAMECACHEFILES = DECRYPTED / "cache"
RANDOMIZERASSETS = ASSETS / "randomizer_assets"


# Rebuilding Apk Paths
REBUILTAPK = WORKSPACE / "rebuilt.apk"
ALIGNEDAPK = WORKSPACE / "aligned.apk"
#SIGNEDAPK = WORKSPACE / "sign.apk" #I think u moved this?

