from pathlib import Path
import re
import dev.randomizer.enums.cats as c

BASE = Path(__file__).resolve().parents[2]
DATA_LOCAL_PATH = BASE / "workspace" / "Extracted_Packs" / "local" / "DataLocal"

TRAITS = {
    "red":[c.s.red],
    "floating":[c.s.floating],
    "black":[c.s.black],
    "white":[c.s.white],
    "angel":[c.s.angel],
    "alien":[c.s.alien],
    "zombie":[c.s.zombie],
    "relic":[c.s.relic],
    "aku":[c.s.aku],
    "metal":[c.s.metal],
}

def randomize_target():
    print(BASE)