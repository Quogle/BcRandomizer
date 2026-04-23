import shutil
import os

CONFIGS = "configs\\"
DEFAULTS = "defaults\\"
CAT_CONFIG = "cat config.toml"
ENEMY_CONFIG = "enemy config.toml"
GAME_CONFIG = "game config.toml"


def wipe():
    c = [CAT_CONFIG,ENEMY_CONFIG,GAME_CONFIG]
    for each in c:
        shutil.copy(CONFIGS+DEFAULTS+each,CONFIGS+each)
    if os.path.exists(CONFIGS + "enemy_info.csv"):
        os.remove(CONFIGS + "enemy_info.csv")


wipe()













