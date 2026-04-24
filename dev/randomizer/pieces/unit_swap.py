from pathlib import Path 
import json
from dev.randomizer.parse_config import settings
from dev.randomizer.func.random import randinst
import dev.randomizer.func.file_handler as fh
import dev.randomizer.func.game_files as f
from dev.randomizer.data.filepaths import *
from dev.randomizer.enums.unitbuy import ub
import shutil

BASE = Path(__file__).resolve().parents[2]
DATA_PATH = BASE / "randomizer" / "data" / "unit_blacklist.json"

with open(DATA_PATH) as datapath:
    data = json.load(datapath)

COLLAB = set(data["collab"])
VERSION_EXCLUSIVE = set(data["version_exclusive"])
UNOBTAINABLE = set(data["unobtainable"])
LIMITED = set(data["limited_event"])

UBER_RARE = 4
LEGEND_RARE = 5

# Other files units need to have edited
UNITBUY_FILE  # DataLocal
TALENT_FILE
TALENT_ORB_FILE
TRUE_FORM_DESCRIPTIONS
LEVEL_STAT_GAIN
LEVEL_LIMIT_UNLOCK

FORM_ASSETS = [
    "large_icons",
    "small_icons",
    "spritesheet",
    "imgcut",
    "mamodel",
]

def swap_units():
    vanilla_unitbuy = f.file_reader(DATA_LOCAL + UNITBUY_FILE)
    vanilla_talents = f.file_reader(DATA_LOCAL + TALENT_FILE)
    
    cfg = config_settings()
    units = f.get_cat_stats(True)

    ubers = [i for i in range(len(units)) if is_uber_lr(i,vanilla_unitbuy)]
    units_other = [i for i in range(len(units)) if not is_uber_lr(i,vanilla_unitbuy)]

    # Decide which units are allowed
    disallowed = set()
    if cfg["blacklist_collab"]:
        disallowed.update(COLLAB)
    if cfg["blacklist_version_exclusive"]:
        disallowed.update(VERSION_EXCLUSIVE)
    if cfg["blacklist_unobtainable"]:
        disallowed.update(UNOBTAINABLE)
    if cfg["blacklist_limited_event"]:
        disallowed.update(LIMITED)

    swap_split(ubers, units_other, disallowed,vanilla_talents)

def swap_split(ubers, units_other, disallowed,vanilla_talents):
    # filter allowed units
    allowed_ubers = [u for u in ubers if u not in disallowed]
    allowed_units_other = [u for u in units_other if u not in disallowed]

    r = randinst(17)

    # create shuffled array
    ubers_shuffled = r.shuffle(allowed_ubers)
    other_shuffled = r.shuffle(allowed_units_other)

    process_file_swaps(allowed_ubers, ubers_shuffled,vanilla_talents)
    process_file_swaps(allowed_units_other, other_shuffled,vanilla_talents)

def process_file_swaps(original_list, shuffled_list,vanilla_talents):
    for original, new in zip(original_list, shuffled_list):
        old_files = unit_files(original)
        new_files = unit_files(new)

        for asset in FORM_ASSETS:
            for form, filename in old_files[asset].items():

                source = fh.search_for_file(filename, True)
                if source is None:
                    continue

                destination = Path(DOWNLOAD_LOCAL) / new_files[asset][form]
                destination.parent.mkdir(parents=True, exist_ok=True)


                # Special case to replace ID in MaModel
                if asset == "mamodel":
                    data = f.file_reader(source)
                    if data is None:
                        continue

                    for row in data:
                        if len(row) > 1:
                            try:
                                if int(row[1]) == original:
                                    row[1] = new
                            except:
                                pass

                    f.file_writer(new_files[asset][form], data, old_file_name=filename)

                # Replace png in imgcut
                elif asset == "imgcut":
                    data = f.file_reader(source)
                    if data is None:
                        continue

                    if len(data) > 1:
                        data[1][0] = new_files["spritesheet"][form]

                    f.file_writer(new_files[asset][form], data, old_file_name=filename)

                else:
                    shutil.copyfile(source, destination)

                print(f"[{asset}] {filename} -> {new_files[asset][form]}")

        # maanim
        for form in old_files["maanim"]:
            for i, filename in enumerate(old_files["maanim"][form]):

                source = fh.search_for_file(filename, True)
                if source is None:
                    continue

                destination = Path(DOWNLOAD_LOCAL) / new_files["maanim"][form][i]
                destination.parent.mkdir(parents=True, exist_ok=True)

                shutil.copyfile(source, destination)

                print(f"[maanim:{form}:{i}] {filename} -> {new_files['maanim'][form][i]}")

        # single files
        for key, filename in old_files["single_files"].items():

            source = fh.search_for_file(filename, True)
            if source is None:
                continue

            destination = Path(DOWNLOAD_LOCAL) / new_files["single_files"][key]
            destination.parent.mkdir(parents=True, exist_ok=True)

            shutil.copyfile(source, destination)

            print(f"[single:{key}] {filename} -> {new_files['single_files'][key]}")

            # talent thing 
            id_map = dict(zip(original_list, shuffled_list))

            new_talents = [row[:] for row in vanilla_talents]

            for row in new_talents:
                if row[0] in id_map:
                    row[0] = id_map[row[0]]

            f.file_writer(TALENT_FILE, new_talents)
            


def is_uber_lr(unit_id, vanilla_unitbuy):
    # Return True if the unit counts toward the uber/lr limit
    rarity = vanilla_unitbuy[unit_id][ub.rarity]
    if rarity == UBER_RARE:
        return True
    if rarity == LEGEND_RARE:
        return True
    return False


def unit_files(unit_id):
    unit_id = int(unit_id)
    forms = ["f", "c", "s", "u"]
    frames = range(4)


    form_assets = {
        "large_icons": {form: f"udi{unit_id:03d}_{form}.png" for form in forms},    # UnitServer
        "small_icons": {form: f"uni{unit_id:03d}_{form}00.png" for form in forms},  # UnitServer
        "spritesheet": {form: f"{unit_id:03d}_{form}.png" for form in forms},       # NumberServer
        "imgcut": {form: f"{unit_id:03d}_{form}.imgcut" for form in forms},         # ImageDataServer
        "mamodel": {form: f"{unit_id:03d}_{form}.mamodel" for form in forms},       # ImageDataServer
    }

    maanim = {                                                                      # ImageDataServer
        form: [f"{unit_id:03d}_{form}{i:02d}.maanim" for i in frames]
        for form in forms
    }     

    single_files = {
        "stats": f"unit{unit_id + 1:03d}.csv",                                          # DataLocal
        "description": f"Unit_Explanation{unit_id + 1:03d}_en.csv",                     # ResLocal
        "gacha_icon": f"gatyachara_{unit_id:03d}_f.png",                            # ImageServer
        "gacha_silhouette": f"gatyachara_{unit_id:03d}_z.png",                      # ImageServer
    }

    return {
        **form_assets,
        "maanim": maanim,
        "single_files": single_files,
    }
    

def config_settings():
    blacklist_collab = settings["game"]["catcombo"]["blacklist"]["collab"]
    blacklist_version_exclusive = settings["game"]["catcombo"]["blacklist"]["version_exclusive"]
    blacklist_unobtainable = settings["game"]["catcombo"]["blacklist"]["unobtainable"]
    blacklist_limited_event = settings["game"]["catcombo"]["blacklist"]["limited_event"]
    return {
        "blacklist_collab": blacklist_collab,
        "blacklist_version_exclusive": blacklist_version_exclusive,
        "blacklist_unobtainable": blacklist_unobtainable,
        "blacklist_limited_event": blacklist_limited_event,
    }
    
