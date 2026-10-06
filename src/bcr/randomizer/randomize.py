""" the central module for the game stats part of the randomizer\n
everything that utilizes the players config to edit what ends up in download local must pass through here """
from ..randomizer import file_local
from ..config.defaults import DEFAULT_CONFIG
from ..config.version_config import get_version_config
from ..randomizer.gameplay.zombie_fix import fix_zombie
from ..randomizer.stages.restrictions import apply_stage_restrictions
from .enemies import enemy_total
from .units import unit_total
from .enemies.enemy_swap import swap_total




def randomize_according_to_config(config=DEFAULT_CONFIG,log=None,debug=False):
    """ anything regarding what ends up in download local MUST passs through this function
    \n config and log should be passed here """
    #I will add stuff here as I go
    #first get the version config to use
    version_config = get_version_config.VC_from_config(config=config)
    print("hey")
    if log != None:
        log("are u fr?")
    #fix_zombie()
    apply_stage_restrictions(config)
    enemy_total.enemy_rand(config=config,log=log,version_config=version_config)
    unit_total.unit_rand(config=config,version_config=version_config,log=log)
    swap_total.do_enemy_swap(config=config,version_config=version_config,log=log,debug=debug)






