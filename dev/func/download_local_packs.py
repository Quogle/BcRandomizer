from pathlib import Path as SysPath
from tbcml import Path, PackFile, CountryCode, GameVersion, Data

BASE = SysPath(__file__).resolve().parents[1]

# Folders
LOCAL_ASSETS_FOLDER = Path(BASE / "workspace" / "decompiled" / "root" / "assets")
EXTRACTED_LOCAL_FOLDER = Path(BASE / "workspace" / "Extracted_Packs" / "local")
EXTRACTED_LOCAL_FOLDER.generate_dirs()

# Only extract these packs
PACK_NAMES = [
    "DataLocal", "DownloadLocal", "UnitLocal", "resLocal",
    "NumberLocal", "MapLocal", "ImageLocal", "ImageDataLocal"
]

def download_local_packs():
    # Loop over every pack in the list
    for pack_name in PACK_NAMES:
        pack_file = LOCAL_ASSETS_FOLDER.add(f"{pack_name}.pack")
        list_file = LOCAL_ASSETS_FOLDER.add(f"{pack_name}.list")

        if not pack_file.exists() or not list_file.exists():
            print(f"Skipping {pack_name}: missing .pack or .list")
            continue

        # Read encrypted list data
        enc_list_data = Data.from_file(list_file)

        # Load the pack
        pack = PackFile.from_pack_file(
            enc_list_data,
            pack_file,
            CountryCode.EN,
            pack_name,
            GameVersion.from_string("15.2.0")
        )

        # Extract all files to a subfolder named after the pack
        pack_download_folder = EXTRACTED_LOCAL_FOLDER.add(pack_name)
        pack_download_folder.generate_dirs()

        for f in pack.get_files():
            f.extract(pack_download_folder)
            print(f"Extracted {f.file_name} from {pack_name}")