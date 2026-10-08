""" has func that does all the enemy things 
\n needs establish_working_information to be called after game files exist """
from ...config.defaults import DEFAULT_CONFIG
from ...config.version_config.get_version_config import DEFAULT_VC_CONFIG
from ..enemies import ability_randomization
from ..enemies import balancing
#from ..enemies import enemy_id_swap
from ..enemies import trait_changer
from ..enemies import trait_gimmicks
#from ..enemies import 
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn



def establish_working_information():
    """ to be called once the game files actually exist """
    #there are none in this file
    #enemy_id_swap.establish_working_information()
    balancing.establish_working_information()





#None of these functions properly consider version config, that needs to be changed before actual first release but its fine for now
#THIS IS HIGHEST LINK IN THE POST ATTACK ANIM CHAIN CURRENTLY
def enemy_rand(config=DEFAULT_CONFIG,log=None,version_config=DEFAULT_VC_CONFIG,debug=False):
    """ does all things requested in config under enemy
    \n also does things under gameplay/modifications that are relevant to enemies """
    #since this is the master function establish working information here
    establish_working_information()
    #start by getting the intended start of modding enemy array
    estat = balancing.early_rebalance(config=config)
    #why are these even separate? I guess its just incase other parts want to access the 'modded vanilla' of early rebalance
    estat = balancing.pre_trait_change_rebalance(estat,config=config)
    #now randomize its traits if config so desires
    estat = trait_changer.change_traits_according_to_config(estat,config=config,log=log,debug=debug)
    #fix certain enemies traits and handle starred and disallowing aliens in itf and shit
    estat = balancing.post_trait_rand_pre_gimmick_rebalance(estat,config)
    #now apply gimmicks
    estat = trait_gimmicks.apply_all_gimmicks(estat,config=config,post_attack_anim=[])
    #what is there to apply after trait gimmicks?
    estat = balancing.post_gimmick_rebalance(estat,config=config)
    #now do ability rand
    estat = ability_randomization.randomize_abilities(estat,config=config,log=log,post_attack_anims=[])
    #is there anything post this rn?
    gf.file_writer(fn.ENEMY_STATS,estat)
    #now we can do enemy swap (actually since it needs to be done after treasures I decided against doing it in enemy total)
    #enemy_id_swap.do_enemy_swap(config=config,log=log,post_attack_anims=[],version_config=version_config)
    #theres nothing else right?
    #buffing the mags of things and whatnot is done in treasure not enemies so Im not including it here, WAIT, that needs to run before enemy swap? otherwise the mags of things which swap to them arent gonna be buffed (Ill deal with that later)
    #however it does need to run after this function


def final_enemy_changes(config=DEFAULT_CONFIG,log=None):
    """ changes to enemies that should happen at the end of the program
    \n includes things which will break sprites and whatnot, maybe witch fix
    \n also includes modded enemies that shouldnt be changed or accessed in any way """
    estat = gf.file_reader(fn.ENEMY_STATS)
    estat = balancing.end_rebalance(stats=estat,config=config)

    #something about modded enemies
    gf.file_writer(fn.ENEMY_STATS,estat)





