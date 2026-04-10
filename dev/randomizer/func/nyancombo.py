from pathlib import Path 
import json
from dev.randomizer.parse_config import settings
from dev.randomizer.func.core import randinst as randinst
from dev.randomizer.func.unit import vanilla_cat_array
from dev.randomizer.func.unit import vanilla_unitbuy_array
import dev.randomizer.func.files as f
from dev.randomizer.data.filepaths import *
from dev.randomizer.enums.unitbuy import ub
import dev.randomizer.enums.nyancombo as cc

#id,combo set, IDFK, S1 id,S1 form,S2 id,S2 form,S3 id,S3 form,S4 id,S4 form,S5 id,S5 form,effect,level,always -1

BASE = Path(__file__).resolve().parents[2]
COMBO_FILE = "NyancomboData.csv"
COMBO_NAME_DATA = DOWNLOAD_LOCAL + "Nyancombo_en.csv"
COMBO_DATA = DOWNLOAD_LOCAL + COMBO_FILE
DATA_PATH = BASE / "randomizer" / "data" / "unit_blacklist.json"

with open(DATA_PATH) as datapath:
    data = json.load(datapath)

COLLAB = set(data["collab"])
VERSION_EXCLUSIVE = set(data["version_exclusive"])
UNOBTAINABLE = set(data["unobtainable"])
LIMITED = set(data["limited_event"])

UNIT_ID_POS = [3, 5, 7, 9, 11]
EFFECT_POS = 13
EFFECT_MAX = 27
MULT_POS = 14          # 0:sm, 1:M, 2:L, 3:XL, 4:DOWN
MULT_MAX = 4

UBER_RARE = 4
LEGEND_RARE = 5

def randomize_combos():
    cfg = config_settings()
    r = randinst(16)

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

    # Put allowed units in an array 
    allowable_units = [i for i in range(len(vanilla_cat_array)) if i not in disallowed]
    
        # Read first
    combos = f.file_reader(COMBO_FILE)    
    for combo in combos:

        #set cat ids
        has_cats = []

        current_uber_lr_count = 0

        for cat_id_pos in UNIT_ID_POS:
            #only add cats if the combo has them defaultly
            if combo[cat_id_pos] != -1:
                #get a random id and if its already added shift it by 1
                cat_id = r.randrange(0,len(allowable_units))
                if cat_id in has_cats:
                    cat_id += 1
                    if cat_id >= len(allowable_units):
                        cat_id -= 2

                # Enforce max uber count
                while is_uber_lr(allowable_units[cat_id], cfg) and current_uber_lr_count >= cfg["max_uber_count"]:
                   cat_id = r.randrange(0, len(allowable_units))

                #add unit and one of its existing forms to combo line
                has_cats.append(cat_id)
                combo[cat_id_pos] = allowable_units[cat_id]
                combo[cat_id_pos+1] = r.randrange(0,len(vanilla_cat_array[allowable_units[cat_id]]))

                # Increment if unit is an uber or legend rare
                if is_uber_lr(allowable_units[cat_id],cfg):
                    current_uber_lr_count += 1
        
        # randomize combos effect
        if cfg["randomize_effects"]:
            combo[EFFECT_POS] = r.randrange(0,EFFECT_MAX+1)
        if cfg["randomize_multipliers"]:
            if cfg["CUSTOM_MULTIPLIER_WEIGHTS"]:
                # Count how many units are in this combo
                unit_count = sum(1 for pos in UNIT_ID_POS if combo[pos] != -1)
                unit_count = max(1, unit_count)

                # Get the weights for this unit count
                weights_dict = cfg["multiplier_weights"][str(unit_count)]

                multipliers = [
                    cc.mult.sm,
                    cc.mult.m,
                    cc.mult.l,
                    cc.mult.xl,
                    cc.mult.down
                ]
                
                weights = [
                    weights_dict["sm"],
                    weights_dict["m"],
                    weights_dict["l"],
                    weights_dict["xl"],
                    weights_dict["down"]
                ]

                # Pick a weighted random multiplier
                combo[MULT_POS] = r.weighted_choice(multipliers, weights)
            else:
                # Uniform random if not using custom weights
                combo[MULT_POS] = r.randrange(0, MULT_MAX+1)

    all_units_down(r, combos)

    #write to dl
    f.file_writer(COMBO_FILE,combos)
    print(f"All {len(combos)} combos randomized and saved to {COMBO_FILE}")


def all_units_down(r, combos):
 
    # id for cat combo
    next_id = 20000

    for unit_id in range(len(vanilla_cat_array)):
        # Create empty combo row (match CSV structure length)
        combo = [-1] * len(combos[0])

        # Basic identifiers
        combo[0] = next_id        # id
        combo[1] = cc.set.Eoc1
        combo[2] = -1             # unknown field

        # Put unit in first slot
        combo[UNIT_ID_POS[0]] = unit_id
        combo[UNIT_ID_POS[0] + 1] = 0  # default form

        # Set effect (pick something valid or leave as-is)
        combo[EFFECT_POS] = r.randrange(0,EFFECT_MAX+1)  # or whatever default you want

        # Force DOWN multiplier
        combo[MULT_POS] = cc.mult.down

        combos.append(combo)
        next_id += 1

    f.file_writer(COMBO_FILE, combos)

    print(f"Added {len(vanilla_cat_array)} 'DOWN' combos.")

def is_uber_lr(unit_id, cfg):
    # Return True if the unit counts toward the uber/lr limit
    rarity = vanilla_unitbuy_array[unit_id][ub.rarity]
    if rarity == UBER_RARE:
        return True
    if rarity == LEGEND_RARE and cfg["allow_legend_rares"]:
        return True
    return False

def config_settings():
    RANDOMIZE_COMBOS = settings["game"]["catcombo"]["RANDOMIZE_COMBOS"]
    
    # Randomization toggles
    randomize_units = settings["game"]["catcombo"]["randomize_units"]
    randomize_multipliers = settings["game"]["catcombo"]["randomize_multipliers"]
    randomize_effects = settings["game"]["catcombo"]["randomize_effects"]
    max_uber_count = settings["game"]["catcombo"]["max_uber_count"]
    allow_legend_rares = settings["game"]["catcombo"]["allow_legend_rares"]

    # Blacklist options
    blacklist_collab = settings["game"]["catcombo"]["blacklist"]["collab"]
    blacklist_version_exclusive = settings["game"]["catcombo"]["blacklist"]["version_exclusive"]
    blacklist_unobtainable = settings["game"]["catcombo"]["blacklist"]["unobtainable"]
    blacklist_limited_event = settings["game"]["catcombo"]["blacklist"]["limited_event"]

    # Size multipliers
    CUSTOM_MULTIPLIER_WEIGHTS = settings["game"]["catcombo"]["size"]["CUSTOM_MULTIPLIER_WEIGHTS"]
    multiplier_weights = {
        "1": settings["game"]["catcombo"]["size"]["1"],
        "2": settings["game"]["catcombo"]["size"]["2"],
        "3": settings["game"]["catcombo"]["size"]["3"],
        "4": settings["game"]["catcombo"]["size"]["4"],
        "5": settings["game"]["catcombo"]["size"]["5"]
    }

    # Unit count options
    preserve_combo_unit_count = settings["game"]["catcombo"]["size"]["preserve_combo_unit_count"]
    CUSTOM_UNIT_COUNT_WEIGHTS = settings["game"]["catcombo"]["size"]["CUSTOM_UNIT_COUNT_WEIGHTS"]
    unit_count_weights = settings["game"]["catcombo"]["size"]["unit_count_weights"]

    return {
        "RANDOMIZE_COMBOS": RANDOMIZE_COMBOS,
        "randomize_units": randomize_units,
        "randomize_multipliers": randomize_multipliers,
        "randomize_effects": randomize_effects,
        "max_uber_count": max_uber_count,
        "allow_legend_rares": allow_legend_rares,
        "blacklist_collab": blacklist_collab,
        "blacklist_version_exclusive": blacklist_version_exclusive,
        "blacklist_unobtainable": blacklist_unobtainable,
        "blacklist_limited_event": blacklist_limited_event,
        "CUSTOM_MULTIPLIER_WEIGHTS": CUSTOM_MULTIPLIER_WEIGHTS,
        "multiplier_weights": multiplier_weights,
        "preserve_combo_unit_count": preserve_combo_unit_count,
        "CUSTOM_UNIT_COUNT_WEIGHTS": CUSTOM_UNIT_COUNT_WEIGHTS,
        "unit_count_weights": unit_count_weights
    }