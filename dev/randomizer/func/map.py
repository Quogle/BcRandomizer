
import dev.randomizer.enums.enemy as e
import dev.randomizer.enums.cats as c
from dev.randomizer.enums.files import *
from dev.randomizer.func.core import randinst
from dev.randomizer.parse_config import settings




def map_maker(estat,cstat):
    #sets map to max length
    map = []
    map_size = len(cstat)
    if len(estat) > map_size:
        map_size = len(estat)
    for x in range(0,map_size):
        map.append([])
    
    map = create_enemy_map(map,estat)

def create_enemy_map(map,estat):
    vanilla_traits = ["black","red","white","floating","relic","zombie","alien","angel","aku","metal"]
    settings["enemy"]
    metals_removed = settings["game"]["gameplay"]["remove_metals"]
    rando_mode = settings["enemy"]["traits"]["mode"]
    

    #get swaps
    swaps = [[],[]]
    specified_swaps = settings["enemy"]["traits"]["specified swaps"]
    

    















