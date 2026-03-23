from pathlib import Path
import json
from configs.internal_config import UNIT_COUNT
import csv
import random

BASE = Path(__file__).resolve().parents[2]
DOWNLOAD_LOCAL = BASE / "workspace" / "DownloadLocal"
COMBO_DATA = DOWNLOAD_LOCAL / "NyancomboData.csv"
DATA_PATH = BASE / "randomizer" / "data" / "unit_blacklist.json"

with open(DATA_PATH) as f:
    data = json.load(f)

COLLAB = set(data["collab"])
VERSION_EXCLUSIVE = set(data["version_exclusive"])
UNOBTAINABLE = set(data["unobtainable"])
LIMITED = set(data["limited_event"])

UNIT_ID = [3, 5, 7, 9, 11]
UNIT_FORM = [4, 6, 8, 10, 12]
UNIT_FORM_MAX = 0   # temp set to 0
EFFECT = 13
EFFECT_MAX = 27
LEVEL = 14          # 0:sm, 1:M, 2:L, 3:XL, 4:DOWN
LEVEL_MAX = 4

def randomize_combos():
    # Read first
    with open(COMBO_DATA, newline='') as infile:
        reader = csv.reader(infile)
        rows = list(reader)

    # Modify all rows
    for row in rows:
        # update unit ID columns
        for col in UNIT_ID:
            if row[col] != "-1":
                row[col] = str(random.randint(1, UNIT_COUNT)) # TODO: add ways to filter out collab / rarities/ uber amounts
        # update unit form columns
        for col in UNIT_FORM:
            if row[col] != "-1":
                row[col] = str(random.randint(0, UNIT_FORM_MAX)) # TODO: read unit file to make the maximum up to what form the unit has
        # Update effect column
        row[EFFECT] = str(random.randint(0, EFFECT_MAX)) 
        row[LEVEL] = str(random.randint(0, LEVEL_MAX)) 

    # Write back to same CSV
    with open(COMBO_DATA, "w", newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)