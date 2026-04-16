import dev.randomizer.enums.enemy as e
import dev.randomizer.func.game_files as f
from dev.randomizer.func.random import randinst
from dev.randomizer.data.filepaths import *
from dev.randomizer.func.misc import *
from dev.randomizer.parse_config import settings






















def calc_change(base_chance,value1,value2):
    """
    calculates the chance adjusted for distance
    \n conditional for some reason
    """
    swap_in_class = settings["enemy"]["extras"]["swap_only_in_class"]
    balanced = settings["enemy"]["extras"]["balanced_swap"]
    if swap_in_class: #just straight up 0% chance if theyre different classes
        first_class = int(value1/10)
        second_class = int(value2/10)
        if first_class != second_class:
            return 0
    if balanced:
        strictness = settings["enemy"]["extras"]["balance_strictness"]
        try:
            strictness = float(strictness)
        except:
            strictness = 10
        
        
    
    



