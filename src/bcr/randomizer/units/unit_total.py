""" has func that does all the cat things """
from ...config.defaults import DEFAULT_CONFIG
from ...config.version_config.get_version_config import DEFAULT_VC_CONFIG
from ..units import balancing
from ..units import trait_changer

import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn










def unit_rand(config=DEFAULT_CONFIG,version_config=DEFAULT_VC_CONFIG,log=None):
    """ does all things requested in config under enemy
    \n also does things under gameplay/modifications that are relevant to enemies """
    #start by getting the intended start of modded unit array
    cstat = balancing.early_rebalance(config=config) #thisll prolly need vc at some point
    #why are these even separate? I guess its just incase other parts want to access the 'modded vanilla' of early rebalance
    cstat = balancing.pre_trait_change_rebalance(cstat,config=config)
    #now randomize its traits if config so desires
    cstat = trait_changer.change_traits_according_to_config(cstat,config=config,version_config=version_config,log=log)
    #fix certain enemies traits and handle starred and disallowing aliens in itf and shit
    cstat = balancing.post_trait_change_rebalance(cstat,config)
    #now do ability rand
    #estat = ability_randomization.randomize_abilities(estat,config=config,log=log,post_attack_anims=[])
    

    gf.write_cat_stats(cstat,also_write_to_cache=True)

    


def final_unit_changes(config=DEFAULT_CONFIG,log=None):
    """ changes to unit that should happen at the end of the program
    \n includes things which will break sprites and whatnot, maybe witch fix
    \n also includes modded units that shouldnt be changed or accessed in any way """
    """
    estat = gf.file_reader(fn.ENEMY_STATS)
    estat = balancing.end_rebalance(stats=estat,config=config)

    #something about modded enemies
    gf.file_writer(fn.ENEMY_STATS,estat)
    """
