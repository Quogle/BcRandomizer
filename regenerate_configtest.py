import shutil
from dev.randomizer.parse_config import *


def wipe():
    c = [CAT_CONFIG,ENEMY_CONFIG,GAME_CONFIG]
    for each in c:
        shutil.copy(CONFIGS+DEFAULTS+each,CONFIGS+each)


wipe()













