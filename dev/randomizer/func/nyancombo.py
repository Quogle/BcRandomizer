from pathlib import Path 
import json
#from configs.internal_config import UNIT_COUNT
import csv
import random
from dev.randomizer.func.core import randinst as randinst
from dev.randomizer.func.unit import vanilla_cat_array
import dev.randomizer.func.files as f
#id,combo set, IDFK, S1 id,S1 form,S2 id,S2 form,S3 id,S3 form,S4 id,S4 form,S5 id,S5 form,effect,level,always -1

BASE = Path(__file__).resolve().parents[2]
DOWNLOAD_LOCAL = BASE / "workspace" / "DownloadLocal"
COMBO_FILE = "NyancomboData.csv"
COMBO_DATA = DOWNLOAD_LOCAL / COMBO_FILE
DATA_PATH = BASE / "randomizer" / "data" / "unit_blacklist.json"

with open(DATA_PATH) as f:
    data = json.load(f)

COLLAB = set(data["collab"])
VERSION_EXCLUSIVE = set(data["version_exclusive"])
UNOBTAINABLE = set(data["unobtainable"])
LIMITED = set(data["limited_event"])

UNIT_ID_POS = [3, 5, 7, 9, 11]
EFFECT_POS = 13
EFFECT_MAX = 27
LEVEL_POS = 14          # 0:sm, 1:M, 2:L, 3:XL, 4:DOWN
LEVEL_MAX = 4

def randomize_combos():
    r = randinst(16)
    # Read first
    combos = f.file_reader(COMBO_FILE)

    allowable_units = []
    disallowed = []
    for each in COLLAB:
        disallowed.append(int(each))
    for each in VERSION_EXCLUSIVE:
        disallowed.append(int(each))
    for each in UNOBTAINABLE:
        disallowed.append(int(each))
    for each in LIMITED:
        disallowed.append(int(each))
    #add something to remove my beloeved collab and special cats
    
    for x in range(0,len(vanilla_cat_array)):
        if x not in disallowed:
            allowable_units.append(x)

    
    for combo in combos:

        #set cat ids
        has_cats = []
        for cat_id_pos in UNIT_ID_POS:
            #only add cats if the combo has them defaultly
            if combo[cat_id_pos] != -1:
                #get a random id and if its already added shift it by 1
                cat_id = r.randrange(0,len(allowable_units))
                if cat_id in has_cats:
                    cat_id += 1
                    if cat_id >= len(allowable_units):
                        cat_id -= 2
                #add unit and one of its existing forms to combo line
                has_cats.append(cat_id)
                combo[cat_id_pos] = allowable_units[cat_id]
                combo[cat_id_pos+1] = r.randrange(0,len(vanilla_cat_array[allowable_units[cat_id]]))
        
        #set combos effect
        combo[EFFECT_POS] = r.randrange(0,EFFECT_MAX+1)
        combo[LEVEL_POS] = r.randrange(0,LEVEL_MAX+1)

    #write to dl
    f.file_writer(COMBO_FILE,combos)