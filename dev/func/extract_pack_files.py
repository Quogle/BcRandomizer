from pathlib import Path as SysPath
from tbcml import PackFile, Data, Path, CountryCode, GameVersion, GamePacks
from configs.internal_config import SELECTED_VERSION

BASE = SysPath(__file__).resolve().parents[1]

# tbcml paths
DOWNLOAD_LOCAL_FOLDER = Path(BASE / "workspace" / "DownloadLocal")
DOWNLOAD_LOCAL_FOLDER.generate_dirs()

ASSETS_FOLDER = Path(BASE / "workspace" / "decompiled" / "root" / "assets")

# List of packs to process
PACK_NAMES = [
    "DataLocal", "DownloadLocal", "UnitLocal", "resLocal",
    "NumberLocal", "MapLocal", "ImageLocal", "ImageDataLocal"
]

FILES_TO_EXTRACT = ["t_unit.csv", "unitbuy.csv"]

def edit_packs():
    packs_dict = {}

    for pack_name in PACK_NAMES:
        pack_path = ASSETS_FOLDER.add(f"{pack_name}.pack")
        list_path = ASSETS_FOLDER.add(f"{pack_name}.list")

        if not pack_path.exists() or not list_path.exists():
            print(f"Skipping {pack_name}: missing .pack or .list")
            continue

        # Read encrypted list data
        enc_list_data = Data.from_file(list_path)

        # Load the pack
        pack_file = PackFile.from_pack_file(
            enc_list_data,
            pack_path,
            CountryCode.EN,
            pack_name,
            GameVersion.from_string(SELECTED_VERSION)
        )

        packs_dict[pack_name] = pack_file

    for pack_name, pack_file in packs_dict.items():
        for filename in FILES_TO_EXTRACT:
            file_obj = pack_file.get_file(filename)
            if file_obj:
                file_obj.extract(DOWNLOAD_LOCAL_FOLDER)
                print(f"{pack_name}/{filename} extracted to {DOWNLOAD_LOCAL_FOLDER.path.as_posix()}")