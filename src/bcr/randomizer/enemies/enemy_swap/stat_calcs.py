
import math
import tadbcmc.data.enums.enemy as e
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn


""" post attack anims should be a global variable here or have some other way to access it """



#missing post attack anim stuff
def mag_ratio(unit1_stats,unit1_id,unit2_stats,unit2_id):
    """ calculates the correct ratio to mult the mag of 1 by to get the mag for 2 """
    #first take care of the post attack anims
    #for now all that can be done is set them to -1
    unit1_post_atk = -1
    unit2_post_atk = -1
    #now get stat values of each unit
    unit1_stat = _determine_unit_product_stat(unit1_stats,unit1_post_atk)
    unit2_stat = _determine_unit_product_stat(unit2_stats,unit2_post_atk)
    #now get the mag mult
    #my current idea is it should be the square root since that results in average stats
    mult = math.sqrt(unit2_stat/unit1_stat)
    return mult



def _determine_unit_product_stat(stats,post_attack_anim=-1):
    """ computes the product stat for that unit 
    \n its the product of dpf and health 
    \n input array is the 1D array of this units stats """
    #first get attack cycle
    attack_cycle = stats[e.s.tba]*2
    if attack_cycle == 0:
        if post_attack_anim == -1:
            attack_cycle += 15 #this is my default value
        else:
            attack_cycle += post_attack_anim
    final_preatk = stats[e.s.multiPreAtk3]
    if stats[e.s.multiPreAtk2] > final_preatk:
        final_preatk = stats[e.s.multiPreAtk2]
    if stats[e.s.preatk] > final_preatk:
        final_preatk = stats[e.s.preatk]
    attack_cycle += (final_preatk-1) #tba is measured from before attack it seems
    #now get total attack
    attack = stats[e.s.attack] + stats[e.s.multiDamage2] + stats[e.s.multiDamage3]
    #now get dpf
    dpf = attack/attack_cycle
    return max(0.01,dpf)*max(1,stats[e.s.hp])




def convert_swap_to_app_swap(swap:list[int],balance_mags:bool) -> list[list[int|float]]:
    """ turns the 1d swap array into a 2d app swap array """
    estats = gf.file_reader(fn.ENEMY_STATS) #uses current stats for balance purposes, (so it should be done after things like changing hp/attack)
    app_swap = []
    #why are we doing it into the range of the shortest, is there a reason for them to not be the same length?
    lower_length = min(len(estats),len(swap))
    for u_id in range(0,lower_length):
        unit2_id = swap[u_id]
        this_applyable = [unit2_id]
        if balance_mags: this_applyable.append(mag_ratio(estats[u_id],u_id,estats[unit2_id],unit2_id))
        else: this_applyable.append(1)
        #thats it
        app_swap.append(this_applyable)
    return app_swap





