from pathlib import Path 
import json
from dev.randomizer.parse_config import settings
from dev.randomizer.func.random import randinst
import dev.randomizer.func.game_files as f
from dev.randomizer.data.filepaths import *
from dev.randomizer.enums.unitbuy import ub
import dev.randomizer.enums.nyancombo as cc

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

# 1 form large icon UnitServer//yellow uiXXX_f.png
# 2 form large icon UnitServer//yellow udiXXX_c.png 
# 3 form large icon UnitServer//yellow udiXXX_s.png
# 4 form large icon UnitServer//yellow udiXXX_u.png

# 1 form small icon UnitServer //yellow unfXXX_u00 
# 2 form small icon UnitServer//yellow uncXXX_u00
# 3 form small icon UnitServer//yellow unsXXX_u00
# 4 form small icon UnitServer//yellow uniXXX_u00

# 1 form sprite NumberServer//yellow XXX_f.png
# 2 form sprite NumberServer//yellow XXX_c.png
# 3 form sprite NumberServer//yellow XXX_s.png
# 4 form sprite NumberServer//yellow XXX_u.png

# 1 form imgcut ImageDataServer//lime XXX_f.imgcut
# 2 form imgcut ImageDataServer//lime XXX_c.imgcut
# 3 form imgcut ImageDataServer//lime XXX_s.imgcut
# 4 form imgcut ImageDataServer//lime XXX_u.imgcut

# 1 form mamodel ImageDataServer//lime XXX_f.mamodel
# 2 form mamodel ImageDataServer//lime XXX_c.mamodel
# 3 form mamodel ImageDataServer//lime XXX_s.mamodel
# 4 form mamodel ImageDataServer//lime XXX_u.mamodel

#//aqua GO FROM 00-03
# 1 form animations ImageDataServer//lime XXX_f00.maanim
# 1 form animations ImageDataServer//lime XXX_c00.maanim
# 1 form animations ImageDataServer//lime XXX_s00.maanim
# 1 form animations ImageDataServer//lime XXX_u00.maanim

# unit description resLocal//yellow Unit_ExplanationXXX_en.csv
# true form descriptions //yellow unitevolve_en.csv
# unit stats DataLocal//yellow unitXXX.csv
# unitbuy DataLocal//yellow unitbuy.csv
# how much stats are gained per levelup//yellow unitlevel.csv
# levelup unlocks//yellow unitlimit.csv

# gacha icon ImageServer//yellow gatyachara_XXX_f.png
# gacha icon shadow ImageServer//yellow gatyachara_XXX_z.png

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

    r = randinst(16)

    # create shuffled array
    ubers_shuffled = r.shuffle(allowed_ubers)
    other_shuffled = r.shuffle(allowed_units_other)

    # print mapping for ubers
    for original, new in zip(allowed_ubers, ubers_shuffled):
        print(f"swapped unit {original} with {new}")

    # print mapping for non-ubers
    for original, new in zip(allowed_units_other, other_shuffled):
        print(f"swapped unit {original} with {new}")


def is_uber_lr(unit_id, vanilla_unitbuy):
    # Return True if the unit counts toward the uber/lr limit
    rarity = vanilla_unitbuy[unit_id][ub.rarity]
    if rarity == UBER_RARE:
        return True
    if rarity == LEGEND_RARE:
        return True
    return False

def config_settings():
    # Blacklist options
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
    
