""" because this module pulls from currently saved enemy stats and edits all stages in both vanilla and dl,\n
it is probably best to fall after most 'general' changes to enemy stats happen\n
but must necessarily be before any stages that should not be changed are added to dl """
from tadbcmc.data.collated_info.enemy_info import *
set_ENEMY_INFO_unlogged()
import tadbcmc.core.simple_funcs as simp
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.unit_info as ui
import tadbcmc.core.seeded_randomization as srand
import copy
import tadbcmc.data.enums.enemy as e
import math
import tadbcmc.core.stnmp as stnmp
from typing import Dict,List




"""
current thoughts on how to do enemy swap
per stage:
    literally just gonna balance swap each enemy in the stage with a different 'available' enemy in that stage
    it doesnt have to be perfect since theres never gonna be more than 10 enemy types in a single stage
variant swap:
    I think if this is on Im just gonna have that be done before the rest of the swaps
    that way all the variants will be filled out in the swaps array and it functions that same as collabs/disallowed do
whole game:
    my current thoughts are what if I multiply the balance array times the ratio of the size of each category compared to the average
    maybe then if I just take proportions based on the result Ill get something accurate? Ill have to do the math on this

    my old method is using the relative sizes of each category and multiplying them by balance array to get chances of each 'strength' in order to choose a particular strength
    and then within that strength it chooses an enemy at random to set and removes it from the list



"""
"""VARIABLE EXPLANATION:
swap - a 1D array where the value x and index y means y swaps to x
    while being made values that should not be swapped are set to themselves while things that have yet to find something to swap to are set to -1
unit_info - a 2D array where the values [x,y,z] at index w refer to the x:swap_strength y:included_in_swap z:variant_id for a unit with id w
scalor - a 1D array comprising the relative chances for something swapping to a strength difference of the value at difference index
variant_dict - a dictionary of keys:variant_id values:list of unit_ids in that variant
absent_dict - a dictionary of keys:swap_strengths and values:list of unit_ids yet to be used with that strength
base_mult_dict - a dictionary with keys of each strength in this swap half where the value of key x is:
    a dictionary with keys of each strength that strength x can swap to, as controlled by keep class and consider strength, where the value of key y is:
        a float for the base chance of something of x strength swapping to y strength (the sum of floats is 1)
appswap - a 2d array where the list [x,y] at index z means z swaps to x and its magnification is multiplied by y



"""
""" per game algorithm
do each side of the id split line seperately
first get the unit info for all units in this swap half
using that unit info create the initial swap with all units not included set to themself and all else set to -1
start by running variant swap on attacking enemy bases as these cannot swap to anything but another enemy base (if they did not end up in variant swap due to lack of 2+ bases on this side of the dividing line then just set enemy bases to themself)
now if variant swap enabled run variant swap:
    for each variant list randomly order the list and then rotate a copy to create from and to lists and then apply them
now if general swap enabled run general swap:
    create a randomly ordered list of all units in swap that have yet to be placed
    if that order, for each unit compute what strength it should swap to:
        the relative chance of each strength is obtained by looping through all possible strengths base chances as specified in base_mult_dict and multiplying each float by the number of units currently remaing with that strength (as obtained from the lists in absent dicts)
        now obtain all units at that strength (from absent dict) and choose a random one, set this unit to it and remove it from absent dict
        last man standing ends up set to self
now all remaing units not filled are set to self (likely just because general swap was not requested)
applyable swap (appswap) is created, the formula for magnification is the square root of the product of hp and dpf ratios
apply appswap to all files, currently eoc is not treated distinctly
"""









""" functions for establishing initial information """
def _get_unit_information(info=ENEMY_INFO,starting_id=0,ending_id=-1) -> List[List[int]]:
    """ gets the information [strength,included,variant] for all units in range """
    #first get the size of the swap info
    if ending_id == -1:
        ending_id = len(info)
    size = ending_id-starting_id
    #now get the swap info [strength,included,variant]
    unit_info = []
    for u_id in range(0,size): #the actual position in info is NOT u_id
        real_id = starting_id+u_id
        this_info = [-1,True,0]
        this_info[0] = info[real_id][ui.e.swap_strength]
        this_info[1] = info[real_id][ui.e.included_in_swap]
        this_info[2] = info[real_id][ui.e.variant_id]
        unit_info.append(this_info)
    return unit_info

def _get_strength_base_mult_dict(unit_info,maintain_grouping,consider_strength) -> Dict[str,Dict[str,float]]:
    """ gets the dictionary where at each strength is a dictionary containing float multipliers for each strength
    \n the floats in each dict sum to 1 """
    #first get the scalor to use for setting the multiples
    scalor = _get_scalor_array(consider_strength)
    #get which strengths are even used
    used_swap_strengths = []
    for u_id in range(0,len(unit_info)):
        if unit_info[u_id][0] not in used_swap_strengths:
            used_swap_strengths.append(unit_info[u_id][0])
    used_swap_strengths.sort()
    #now create the dict
    base_mult_dict = {}
    for strength in used_swap_strengths:
        #first step is determining what groups it can even swap to
        #lower bound is the lowest group allowed, upper bound is 1 beyond the highest group allowed
        if maintain_grouping:
            lower_bound = 10*int(strength/10)
            upper_bound = lower_bound + 10
        else:
            lower_bound = simp.clamp(strength-9,0,100)
            upper_bound = lower_bound + 19
        #patch for chaos
        if not consider_strength:
            lower_bound = used_swap_strengths[0]
            upper_bound = used_swap_strengths[-1] + 1
        #now create the dictionary containing only those groups
        this_dict = {}
        for x in range(lower_bound,upper_bound):
            if x in used_swap_strengths: #no sense in including anything that doesnt exist
                diff = abs(x-strength)
                if diff >= 10: #this is just for chaos mode
                    diff = 10
                this_dict[str(x)] = scalor[diff]
        #now get the sum of all in that dict so the total sum can be set to 1
        sum = 0
        for each in this_dict:
            sum += this_dict[each]
        for each in this_dict:
            this_dict[each] *= (1/sum) #sets total sum to 1
        #now set it as the dict under this strength
        base_mult_dict[str(strength)] = this_dict
    #should be all good
    return base_mult_dict

def _get_scalor_array(consider_strength=True) -> List[float]:
    """ gets the balance array to scale the chance of groups by
    \n index in array is the difference between the swap strengths
    \n len(array) = 11 """
    balance_scalor = []
    for x in range(0,10):
        scale = 1/((0.9 + 0.20*x)**2)-0.01*x
        balance_scalor.append(scale)
    balance_scalor.append(0) #this is so anything outside the range can just call to -1 and it nullifies the chance
    if not consider_strength: #set all proportions to 1
        for x in range(0,len(balance_scalor)):
            balance_scalor[x] = 1
    return balance_scalor
    """ relative proportions when considering strength:
    0:1.23x
    1:0.82x
    2:0.57x
    3:0.41x
    4:0.31x
    5:0.23x
    6:0.17x
    7:0.12x
    8:0.08x
    9:0.047x
    10:0x
    """

def _get_variant_dict(swap_info:list) -> Dict[str,List[int]]:
    """ gets all the variants in in swap info
    \n discards are variants with only one unit included """
    variant_dict = {}
    for u_id in range(0,len(swap_info)):
        this_variant = str(swap_info[u_id][2])
        included = swap_info[u_id][1]
        if included:
            if this_variant not in variant_dict:
                variant_dict[this_variant] = []
            variant_dict[this_variant].append(u_id)
    #now remove all with only one variant
    for each in variant_dict:
        if len(variant_dict[each]) < 2:
            variant_dict.pop(each)
    #that should be the full variant dict for this half
    return variant_dict

def _get_initial_swap(unit_info) -> List[int]:
    """ gets the initial swap array for this half where entities included in the swap are -1
    \n this not to be swapped are excluded by putting their id at their own index (so they swap to themself) """
    swaps = []
    for u_id in range(0,len(unit_info)):
        #if its not allowed set it equal to itself
        if unit_info[u_id][1]:
            swaps.append(-1)
        else:
            swaps.append(u_id)
    return swaps

""" initial information for filling out a general swap """
def _get_unit_look_order(swap) -> List[int]:
    """ gets a randomized order of indexes that still need to be filled """
    #get the list of indexes that need filling
    missing_units = []
    for x in range(0,len(swap)):
        if swap[x] == -1:
            missing_units.append(x)
    #now randomize its order
    randomized_order = []
    r = srand.randinst(807)
    while len(missing_units) > 0:
        randomized_order.append(missing_units.pop(r.randrange(0,len(missing_units))))
    #all set
    return randomized_order

def _get_inital_absent_dict(swap_info,swap) -> Dict[str,List[int]]:
    """ gets a dictionary of all currently unused unit ids at each power """
    absent_dict = {}
    #first get all the unused units
    units = []
    for u_id in range(0,len(swap)):
        if u_id not in swap:
            units.append(u_id)
    #now add each of those unit to arrays in their respective powers
    for u_id in units:
        this_strength = str(swap_info[u_id][0])
        if this_strength not in absent_dict:
            absent_dict[this_strength] = []
        absent_dict[this_strength].append(u_id)
    #should be all good
    return absent_dict

""" parts of completing a general swap """
def _get_this_units_new_strength(unit_id:int,self_strength:int,absent_dict:Dict[str,List[int]],base_mult_dict:Dict[str,Dict[str,float]],random_number=0,log=None):
    """ determines what strength this unit is swapping to
    \n takes a random number between 0 and 100,000 """
    """ 
    works by setting each allowed strength as (strength unit count)*(strength base mult)
    then these chances are adjusted to sum to 100k and where random number falls in that range determines the strength
    """
    #first snag the base mult for this strength
    chance_dict = copy.deepcopy(base_mult_dict[str(self_strength)])
    #now multiply each of those chances by the number of units at that strength, count the total number of units
    for strength in chance_dict:
        count = len(absent_dict[strength])
        if unit_id in absent_dict[strength]:
            count -= 1
        chance_dict[strength] *= count
        total_unit_number += count
    #now get the sum of chances, and multiply each chance by 100/sum in order to scale it to 100
    sum = 0
    for each in chance_dict:
        sum += chance_dict[each]
    if sum == 0:
        if log != None:
            log("there were no enemies for " + str(unit_id) + " to swap to, it is common to see 1-2 of these errors")
        return -1
    for each in chance_dict:
        chance_dict[each] *= (100000/sum) #maybe I should reduce this by one for fp errors?
    #now get a random number between 0-100000 and loop through chance dict until its in that range and return it
    for each in chance_dict:
        if random_number <= chance_dict[each]:
            return int(each)
        else:
            random_number -= chance_dict[each]
    if log != None:
        log("failed to properly reduce random number in _get_this_units_new_strength (e)")
        log("remainder: " + str(random_number))
    return -1

def _general_swap(swap:List[int],unit_info:List[List[int]],maintain_grouping=True,consider_strength=True,log=None):
    """ fills out all remaining entries in the swap and returns """
    #fuck python
    swap = copy.deepcopy(swap)
    #get the order of indexes to fill
    unit_order = _get_unit_look_order(swap)
    #get the absent dict and base mult dict
    absent_dict = _get_inital_absent_dict(swap)
    base_mult_dict = _get_strength_base_mult_dict(unit_info,maintain_grouping,consider_strength)
    #ok so from here on out I assume that all the units available for swapping to are also the units needing swapping from
    #I think this is a fine assumption because no matter how I do this it literally cant work if that isnt the case
    for unit_id in unit_order:
        own_strength = unit_info[unit_id][0]
        r = srand.randinst(unit_id+100) #this is prolly fine
        #first step is getting the strength to swap to
        new_strength = _get_this_units_new_strength(unit_id,own_strength,absent_dict,base_mult_dict,r.randrange(0,100000),log)
        #what do I do when it fails? just set it to itself I guess
        if new_strength == -1:
            if log != None:
                log("forced to set " + str(unit_id) + " to self")
            swap[unit_id] = unit_id
        else:
            #now I should be good to duplicate the strength array and remove self from it
            available_at_strength = copy.deepcopy(absent_dict[str(new_strength)])
            if unit_id in available_at_strength:
                available_at_strength.remove(unit_id)
            #now its all fine and dandy to choose a unit and remove it from absent dict
            second_r = srand.randinst(unit_id+300)
            new_id = available_at_strength[second_r.randrange(0,len(available_at_strength))]
            swap[unit_id] = new_id
            absent_dict[str(new_strength)].remove(new_id)
    #all good
    return swap


""" parts of completing a variant swap """
def _process_variant(swap:List[int],variant_list:List[int],random_number:int):
    """ takes a swap and a list of all ids at that variant and fills out the swap with that variant """
    r = srand.randinst(random_number)
    #first get the before/after array in the usual random order rotated fasion
    before = []
    temp_l = copy.deepcopy(variant_list)
    for x in range(0,len(temp_l)):
        before.append(temp_l.pop(r.randrange(0,len(temp_l))))
    after = copy.deepcopy(before)
    after.append(after.pop(0)) #it only needs to be rotated one entry
    #now apply before/after to swap and return it
    for x in range(0,len(before)):
        swap[before[x]] = after[x]
    return swap

def _process_all_variants(swap:List[int],variant_dict:Dict[str,List[int]],random_number:int):
    """ fills out swap by processing all variants in variant dict and returns swap """
    r = srand.randinst(random_number)
    #for each variant just process them individually
    for variant in variant_dict:
        this_random_number = r.randrange(0,1000)
        swap = _process_variant(swap,variant_dict[variant],this_random_number)
    return swap

""" full function for creating a swap half """
def create_swap_half(starting_id=0,ending_id=-1,maintain_grouping=True,consider_strength=True,general_swap=False,variant_swap=False,log=None):
    """ creates the swap across input unit ids from scratch """
    #first step is getting the correct unit info
    unit_info = _get_unit_information(ENEMY_INFO,starting_id,ending_id)
    #now get all the initial information resulting from it
    swap = _get_initial_swap(unit_info)
    variant_dict = _get_variant_dict(unit_info)
    #now first step in filling out the swap is enemy bases
    #manually inputting attacking bases for now
    if "94" not in variant_dict:
        #if it isnt in variant dict I have to do this manually
        #just set all unit ids with a variant id of 94 to themself
        for unit_id in range(0,len(swap)):
            if unit_info[unit_id][2] == 94:
                swap[unit_id] = unit_id
    else:
        swap = _process_variant(swap,variant_dict.pop("94"),94)
    #now all other variants are good to be filled in
    if variant_swap:
        swap = _process_all_variants(swap,variant_dict,603)
    #now general swap is good to be done
    if general_swap:
        swap = _general_swap(swap,unit_info,maintain_grouping,consider_strength,log)
    #now all remaining entries should be set to themself
    for unit_id in range(0,len(swap)):
        if swap[unit_id] == -1:
            swap[unit_id] = unit_id
    #now shift all the unit ids up to where they should be
    for unit_id in range(0,len(swap)):
        swap[unit_id] = unit_id + starting_id
    #should be all good to return this swap
    return swap

#please dont call this function if both variant and general swap are off but per game is on that is a massive waste of time
""" full per game function """
def swap_per_game(first_enemy_not_considered=-1,variant_swap=False,general_swap=False,maintain_grouping=True,consider_strength=True,adjust_mags=True,include_eoc=False,log=None,post_attack_anims=[]):
    """ creates a swap for the whole game and applies it """
    #first step, create the two halves of the total swap
    swap1 = create_swap_half(0,first_enemy_not_considered,maintain_grouping,consider_strength,general_swap,variant_swap,log)
    if first_enemy_not_considered == -1:
        swap = swap1
    else:
        swap2 = create_swap_half(first_enemy_not_considered,-1,maintain_grouping,consider_strength,general_swap,variant_swap,log)
        swap = swap1 + swap2
    #now turn that swap into an applyable swap
    app_swap = _turn_swap_into_applyable_swap(swap,balance_mag=adjust_mags,post_attack_anims=post_attack_anims)
    #now apply that swap to all the files
    #for now it is using the eoc bool, when I make eoc actually use different enemies I need to have it be entirely separate since they arent goint to swap to the right enemy otherwise
    _apply_app_swap_to_stages(app_swap,include_eoc)
    

""" full per stage function """
#Ill do this later


""" parts for calculating stats """

def _turn_swap_into_applyable_swap(swap,balance_mag=True,post_attack_anims=[]):
    """ takes a swap array and turns it into an equal length array
    \n each index contains [id to swap to,amount to multiply mag by] """
    #first step is getting the correct stat array to use (Ive decided it should be the actually current version of enemy stats)
    estat = gf.file_reader(fn.ENEMY_STATS)
    #now get which of the two lists is shorter
    shorter = len(estat)
    if len(swap) < shorter:
        shorter = len(swap)
    #now only do up to that len
    applyable = []
    for x in range(0,shorter):
        this_applicable = [swap[x]]
        #now get the mag ratio
        if balance_mag:
            this_applicable.append(_mag_ratio(x,swap[x],estat,post_attack_anims))
        else:
            this_applicable.append(1)
        #now slap that thang on
        applyable.append(this_applicable)
    #all good
    return applyable

def _mag_ratio(unit1,unit2,stats,post_attack_anims=[]):
    """ calculates the correct ratio to mult the mag of 1 by to get the mag for 2 """
    #first take care of attack anims
    if len(post_attack_anims) > 0:
        unit1_anim = post_attack_anims[unit1]
        unit2_anim = post_attack_anims[unit2]
    else:
        unit1_anim = -1
        unit2_anim = -1
    #now get stat values of each unit
    unit1_stat = _determine_unit_product_stat(stats[unit1],unit1_anim)
    unit2_stat = _determine_unit_product_stat(stats[unit2],unit2_anim)
    #now get the mag mult
    #my current idea is it should be the square root since that results in average stats
    mult = math.sqrt(unit2_stat/unit1_stat)
    return mult

def _determine_unit_product_stat(stats,post_attack_anim=-1):
    """ computes the product stat for that unit 
    \n its the product of dpf and health 
    \n input array is the 1D array of this units stats """
    #first get attack cycle
    attack_cycle = stats[e.s.tba]
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
    return dpf*stats[e.s.hp]

""" applying swap to the game files """

def _apply_app_swap_to_stages(app_swap,include_eoc=False):
    """ applies the swap to all stages """
    #first step is getting all the stages
    all_stages = gf.get_names_of_all_stages(include_dl=True,include_eoc=include_eoc)
    #also get a dummy stage to pull stage variables from
    d = stnmp.stage()
    #now loop through all those stages
    for stage_name in all_stages:     #this does not use stnmp because its slower and this should be as fast as possible
        stage_sche = gf.file_reader(stage_name)
        edited = False
        #number of starting lines check
        if stage_sche[1][0] > 2000: #this is checking stage length
            number_starting_lines = 2
        else:
            number_starting_lines = 1
        #enemy base swapping
        if stage_sche[number_starting_lines-1][d.animated_base] != 0:
            stage_sche[number_starting_lines-1][d.animated_base] = app_swap[stage_sche[number_starting_lines-1][d.animated_base]][0]
        #now loop through each line from there till the end attempting to edit it
        for enemy_line in range(number_starting_lines,len(stage_sche)):
            enemy_id = enemy_line[d.enemy_id]
            #check if real then, if enemy doesnt route to self
            if enemy_id != 0 and enemy_id != app_swap[enemy_id][0]:
                edited = True
                enemy_line[d.enemy_id] = app_swap[enemy_id][0]
                new_mag = enemy_line[d.magnification]*app_swap[enemy_id][1]
                if new_mag < 1:
                    new_mag = 1
                enemy_line[d.magnification] = int(new_mag)
        if edited:
            gf.file_writer(stage_name,stage_sche)
    




