from pathlib import Path 
import json
from dev.randomizer.parse_config import settings
from dev.randomizer.func.random import randinst
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

def swap_units():
    vanilla_unitbuy = f.file_reader(DATA_LOCAL + UNITBUY_FILE)
    
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

    swap_split(ubers, units_other, disallowed)

def swap_split(ubers, units_other, disallowed):
    # filter allowed units
    allowed_ubers = [u for u in ubers if u not in disallowed]
    allowed_units_other = [u for u in units_other if u not in disallowed]

    r = randinst(17)

    # create shuffled array
    ubers_shuffled = r.shuffle(allowed_ubers)
    other_shuffled = r.shuffle(allowed_units_other)

    # print mapping for ubers
    for original, new in zip(allowed_ubers, ubers_shuffled):
        # Make an array of file names for the original units and the unit they will swap to in same position
        old_files = unit_files(original)
        new_files = unit_files(new)

        # Loop through all the unit files and change them to the new random unit
        # large icons
 
            
        print(f"changed large icons: {original} -> {new}")

    # print mapping for non-ubers
    for original, new in zip(allowed_units_other, other_shuffled):
        print(f"changed files of unit {original} to unit {new}")

       
    files = unit_files(34)
    print(files)

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

    large_icons = {form: f"udi{unit_id:03d}_{form}.png" for form in forms}         # UnitServer
    small_icons = {form: f"uni{unit_id:03d}_{form}00.png" for form in forms}       # UnitServer
    spritesheet = {form: f"{unit_id:03d}_{form}.png" for form in forms}            # NumberServer
    imgcut = {form: f"{unit_id:03d}_{form}.imgcut" for form in forms}              # ImageDataServer
    mamodel = {form: f"{unit_id:03d}_{form}.mamodel" for form in forms}            # ImageDataServer
    maanim = {                                                                     # ImageDataServer
        form: [f"{unit_id:03d}_{form}{i:02d}.maanim" for i in frames]
        for form in forms
    }     
    stats = f"unit{unit_id:03d}.csv"                                                   # DataLocal
    description = f"Unit_Explanation{unit_id:03d}_en.csv"                              # ResLocal
    gacha_icon = f"gatyachara_{unit_id:03d}_f.png"                                     # ImageServer
    gacha_silhouette = f"gatyachara_{unit_id:03d}_z.png"                               # ImageServer

    return {
    "large_icons": large_icons,
    "small_icons": small_icons,
    "spritesheet": spritesheet,
    "imgcut": imgcut,
    "mamodel": mamodel,
    "maanim": maanim,
    "stats": stats,
    "description": description,
    "gacha_icon": gacha_icon,
    "gacha_silhouette": gacha_silhouette,
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
    
