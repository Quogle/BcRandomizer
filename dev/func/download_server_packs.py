from pathlib import Path as SysPath
from tbcml import Path, Apk, PackFile, CountryCode, GameVersion
from tbcml import Data
import os
import shutil

DOCUMENTS = SysPath(os.path.expanduser("~")) / "Documents"
LIB_FOLDER = DOCUMENTS  / "tbcml" / "APKs" / "0.0.0en" / "extracted" / "config.arm64_v8a" / "lib" / "arm64-v8a"
ASSETS_AREA = DOCUMENTS / "tbcml" / "APKs" / "0.0.0en" / "extracted" / "InstallPack"

BASE = SysPath(__file__).resolve().parents[1]
EXTRACTED_SERVER_FOLDER = Path(BASE / "workspace" / "Extracted_Packs" / "server")
EXTRACTED_SERVER_FOLDER.generate_dirs()

LIB_FILE = SysPath(BASE / "workspace" / "decompiled" / "root" / "lib" / "arm64-v8a" / "libnative-lib.so")
ASSETS_FOLDER = SysPath(BASE / "workspace" / "decompiled" / "root" / "assets")

def download_server_packs():

    LIB_FOLDER.mkdir(parents=True, exist_ok=True)
    ASSETS_AREA.mkdir(parents=True, exist_ok=True)

    shutil.copy2(LIB_FILE, LIB_FOLDER / LIB_FILE.name)
    shutil.copytree(ASSETS_FOLDER, ASSETS_AREA / "assets", dirs_exist_ok=True)
    
    # Load the APK (for server path info)
    apk = Apk(game_version="0.0.0", country_code="en")
    
    # Make sure server files are downloaded/extracted
    print("Fetching Server Files... May take awhile")
    apk.download_server_files(force=True)

   
    
    # Get server folder path
    server_folder = apk.get_server_path()
    
    # Loop over every server pack
    for file in server_folder.get_files():
        if file.path.endswith(".pack"):
            # find matching list
            list_file = server_folder.add(file.get_file_name().replace(".pack", ".list"))
            if list_file.exists():
                enc_list = Data.from_file(list_file)
                pack = PackFile.from_pack_file(
                    enc_list,
                    file,
                    CountryCode.EN,
                    file.get_file_name().replace(".pack", ""),
                    GameVersion.from_string("")
                )
    
                # extract all files to a subfolder named after the pack
                pack_download_folder = EXTRACTED_SERVER_FOLDER.add(file.get_file_name().replace(".pack", ""))
                pack_download_folder.generate_dirs()
                for f in pack.get_files():
                    f.extract(pack_download_folder)
                    print(f"Extracted {f.file_name} from {file.get_file_name()}")