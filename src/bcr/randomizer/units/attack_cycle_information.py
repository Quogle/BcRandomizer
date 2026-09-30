""" contains the attack cycle for each unit in the game
\n Please star import this module
\n updating the array can take a cat array, or otherwise just uses the latest version saved to file
\n it can consider animations if they exist """
import tadbcmc.core.game_files as gf
import tadbcmc.data.enums.cats as c







ATTACK_CYCLE_ARRAY = []

def update_attack_cycle_array(cat_stats:list=gf.get_cat_stats(),include_animations:bool=False):
    """ updates the attack cycle array based on the current unit stats and if desired looks through existing animations to get post attack times for 0tba units """
    global ATTACK_CYCLE_ARRAY
    #first step literally just kill it
    ATTACK_CYCLE_ARRAY = []
    for u_id in range(0,len(cat_stats)):
        this_units_attack_cycles = []
        for form in range(0,len(cat_stats[u_id])):
            this_cycle = cat_stats[u_id][form][c.s.tba]*2
            if this_cycle == 0:
                pass #this is where animation checking should go if desired
            last_attack = cat_stats[u_id][form][c.s.multi_preatk_3]
            if last_attack == 0:
                last_attack = cat_stats[u_id][form][c.s.multi_preatk_2]
            if last_attack == 0:
                last_attack = cat_stats[u_id][form][c.s.preatk]
            this_cycle += last_attack
            #slap it on
            this_units_attack_cycles.append(this_cycle)
        #slap unit on
        ATTACK_CYCLE_ARRAY.append(this_units_attack_cycles)
    
