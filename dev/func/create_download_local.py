from pathlib import Path as SysPath
from tbcml import Path, PackFile, CountryCode, GameVersion, Data, GameFile

BASE = SysPath(__file__).resolve().parents[2]

# Folder containing extracted files for a pack
LOCAL_PACK_FOLDER = Path(BASE / "dev/workspace/DownloadLocal")
OUTPUT_PACK = Path(BASE / "dev/workspace/decompiled/root/assets/DownloadLocal.pack")
OUTPUT_LIST = Path(BASE / "dev/workspace/decompiled/root/assets/DownloadLocal.list")

OUTPUT_DIR = Path(BASE / "dev/workspace/decompiled/root/assets")

OUTPUT_DIR.generate_dirs()
LOCAL_PACK_FOLDER.generate_dirs()


def create_download_local(debug=True):
    if debug:
        print("creating downloadlocal \nif enemy/unit swap or randomize boss this may take a while")
    # Create new PackFile
    pack = PackFile("DownloadLocal", CountryCode.EN, GameVersion.from_string("15.2.0"))
    
    # Add each file in the folder
    for f in LOCAL_PACK_FOLDER.get_files():
        gf = GameFile(
            None,               # no original pack path
            f.get_file_name(),  # file name
            pack.pack_name,
            pack.country_code,
            pack.gv,
            dec_data=Data.from_file(f)
        )
        pack.add_file(gf)
    
    # Convert PackFile to pack + list data
    pack_name, pack_data, list_data = pack.to_pack_list_file()
    
    # Write the rebuilt pack and list
    # Write the rebuilt pack and list using string paths
    pack_data.to_file(OUTPUT_PACK.path)
    list_data.to_file(OUTPUT_LIST.path)
    
    print(f"Rebuilt {pack_name}.pack and .list successfully.")