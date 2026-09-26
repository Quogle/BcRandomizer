""" the central module for the game stats part of the randomizer\n
everything that utilizes the players config to edit what ends up in download local must pass through here """
from ..randomizer import file_local
from ..config.defaults import DEFAULT_CONFIG
from ..randomizer.gameplay.zombie_fix import fix_zombie
from ..randomizer.stages.restrictions import apply_stage_restrictions



def randomize_according_to_config(config=DEFAULT_CONFIG,log=None):
    """ anything regarding what ends up in download local MUST passs through this function
    \n config and log should be passed here """
    #I will add stuff here as I go
    print("hey")
    if log != None:
        log("are u fr?")
    fix_zombie()
    apply_stage_restrictions(config)







