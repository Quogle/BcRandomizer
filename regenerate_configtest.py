import shutil
from dev.randomizer.parse_config import CAT_CONFIG
from dev.randomizer.parse_config import ENEMY_CONFIG
from dev.randomizer.parse_config import GAME_CONFIG
from dev.randomizer.parse_config import CONFIGS
from dev.randomizer.parse_config import DEFAULTS


def wipe():
    c = [CAT_CONFIG,ENEMY_CONFIG,GAME_CONFIG]
    for each in c:
        shutil.copy(CONFIGS+DEFAULTS+each,CONFIGS+each)


wipe()













