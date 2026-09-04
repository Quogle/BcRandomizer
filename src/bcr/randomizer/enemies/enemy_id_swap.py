from tadbcmc.data.collated_info.enemy_info import *
set_ENEMY_INFO_unlogged()
import tadbcmc.core.simple_funcs as simp
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.unit_info as ui
from ...config import defaults
import tadbcmc.core.seeded_randomization as rand
import copy
from .balancing import early_rebalance #should it be early or middle? my guess is early since middle does nothing on its own and I would need it anyways
import tadbcmc.data.enums.enemy as e
import math
import tadbcmc.core.stnmp as stnmp





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
""" VARIABLE EXPLANATION
swaps:
    the value and index is the new id cat with index should become (a 300 at 2 means doge becomes whatever 300 is)
    when initially made all units not to be randomized have their own index as the value
    all units to be randomized have their value set to -1


absent_dict:
    this is all unit ids currently available for swapping to
        each swap strength is an array of them

balance scalor:
    an array where each index is the scalor for proportion at index strength difference

initial chance dict:
    a dictionary populated with strengths
        the value at each strength x is itself a dictionary of strengths y
            contains only the strengths allowed for something of strength x to swap to
                the value of each y is the result of the difference between x and y in balance scalor
        the sum of each dictionaries values is 1 so they make for raw ratios


"""
















    




""" functions for getting initial information """



def _get_initial_balance_scalor(chaos=False):
    """ gets the balance array to scale the chance of groups by
    \n index in array is the difference between the swap strengths
    \n caps out at 9 difference """
    balance_scalor = []
    for x in range(0,10):
        scale = 1/((0.9 + 0.20*x)**2)-0.01*x
        balance_scalor.append(scale)
    balance_scalor.append(0) #this is so anything outside the range can just call to -1 and it nullifies the chance
    if chaos: #set all proportions to 1
        for x in range(0,len(balance_scalor)):
            balance_scalor[x] = 1
    return balance_scalor
    """ relative proportions:
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

def _get_initial_chance_dict(balance_scalor=_get_initial_balance_scalor(),maintain_grouping=True,chaos=False):
    """ makes a base chance dict for each strength
    \n so a unit with a strength of 15 will call dict["15"] and get a dictionary with say 11-19 as its keys
     each key has its distance from 15 used to set the base amount
    \n the sum of the initial chances is 1 (so it can be looped through for a proportion that ignores all else) """
    #get which ids are even used
    used_swap_strengths = []
    for each in ENEMY_INFO:
        if each[ui.e.swap_strength] not in used_swap_strengths:
            used_swap_strengths.append(each[ui.e.swap_strength])
    if -1 in used_swap_strengths:
        used_swap_strengths.remove(-1)
    used_swap_strengths.sort()
    #now create the initial chance dict
    initial_chance_dict = {}
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
        if chaos:
            lower_bound = used_swap_strengths[0]
            upper_bound = used_swap_strengths[-1] + 1
        #now create the dictionary containing only those groups
        this_dict = {}
        for x in range(lower_bound,upper_bound):
            if x in used_swap_strengths: #no sense in including anything that doesnt exist
                diff = abs(x-strength)
                if diff >= 10: #this is just for chaos mode
                    diff = 10
                this_dict[str(x)] = balance_scalor[diff]
        #now get the sum of all in that dict so the total sum can be set to 1
        sum = 0
        for each in this_dict:
            sum += this_dict[each]
        for each in this_dict:
            this_dict[each] *= (1/sum) #sets total sum to 1
        #now set it as the dict under this strength
        initial_chance_dict[str(strength)] = this_dict
    #should be all good
    return initial_chance_dict

def _get_initial_swaps():
    """ gets the initial swap array where entities included in the swap are -1
    \n collabs and things with a swap strength of -1 are excluded by putting their id at their own index (so they swap to themself) """
    swaps = []
    vanilla_stats = gf.file_reader(fn.ENEMY_STATS,vanilla=True)
    for x in range(0,len(vanilla_stats)):
        swaps.append(-1)
        if ENEMY_INFO[x][ui.e.collab] == 1:
            swaps[-1] = x
        if ENEMY_INFO[x][ui.e.swap_strength] < 0: #are these two conditions alone enough?
            swaps[-1] = x
    return swaps

def _get_initial_variant_dict(start_from=0,run_till=-1):
    """ gets a dictionary where the values at each key is an array of unit id in that variant
    \n so doge variant 1 would be [2,48,169,...] for doge ddark shib and so on"""
    variant_dict = {}
    if run_till == -1:
        end_point = len(ENEMY_INFO)
    else:
        end_point = run_till + 1
    for e_id in range(start_from,end_point):
        e_var = ENEMY_INFO[e_id][ui.e.variant_id]
        if e_var > 0: #variants should only be above 0
            if str(e_var) not in variant_dict:
                variant_dict[str(e_var)] = []
            variant_dict[str(e_var)].append(e_id)
    return variant_dict


""" parts of completing a swap array """

def _get_unit_look_order(swap):
    """ gets a randomized order of indexes that still need to be filled """
    #get the list of indexes that need filling
    missing_units = []
    for x in range(0,len(swap)):
        if swap[x] == -1:
            missing_units.append(x)
    #now randomize its order
    randomized_order = []
    r = rand.randinst(87)
    while len(missing_units) > 0:
        randomized_order.append(missing_units.pop(r.randrange(0,len(missing_units))))
    #all set
    return randomized_order

def _get_inital_absent_dict(swap):
    """ gets a dictionary of all currently unused unit ids at each power """
    absent_dict = {}
    #first get all the unused units
    units = []
    for x in range(0,len(swap)):
        if x not in swap:
            units.append(x)
    #now add each of those unit to arrays in their respective powers
    for each in units:
        this_strength = str(ENEMY_INFO[each][ui.e.swap_strength])
        if this_strength not in absent_dict:
            absent_dict[this_strength] = []
        absent_dict[this_strength].append(each)
    #now kill all outliers that shouldnt be
    if "-1" in absent_dict:
        absent_dict.pop("-1")
    #should be all good
    return absent_dict

def _get_this_units_new_strength(unit_id,absent_dict,initial_chance_dict,random_number=0,debug=False):
    """ determines what strength this unit is swapping to
    \n takes a random number between 0 and 100,000 """
    """ 
    works by setting each allowed grouping as (groupings size)*(grouping difference in balance scalor)
    then these chances are adjusted to sum to 100k and where random number falls in that range determines the strength
     """
    #first step is determining what groups it can even swap to
    this_unit_strength = ENEMY_INFO[unit_id][ui.e.swap_strength]
    chance_dict = copy.deepcopy(initial_chance_dict[str(this_unit_strength)])
    #get a dict with identical keys where the values are the number of swappable units in each strength
    count_dict = copy.deepcopy(chance_dict)
    for each in count_dict:
        number_of_units = len(absent_dict[each])
        if unit_id in absent_dict[each]: #dont count self
            number_of_units -= 1
        count_dict[each] = number_of_units
    #now multiply those by the number of units to scale the chance of each group linearly by its size
    for each in chance_dict:
        chance_dict[each] *= count_dict[each]
    #now get the sum of chances, and multiply each chance by 100/sum in order to scale it to 100
    sum = 0
    for each in chance_dict:
        sum += chance_dict[each]
    if sum == 0:
        if debug:
            print("there were no units for " + str(unit_id) + " to swap to")
        return -1
    for each in chance_dict:
        chance_dict[each] *= (100000/sum)
    #now get a random number between 0-100000 and loop through chance dict until its in that range and return it
    for each in chance_dict:
        if random_number <= chance_dict[each]:
            return int(each)
        else:
            random_number -= chance_dict[each]
    if debug:
        print("failed to properly reduce random number")
        print("remainder: " + str(random_number))
    return -1

def _populate_swap(swaps,balance_scalor=_get_initial_balance_scalor(),initial_chance_dict=_get_initial_chance_dict(),maintain_grouping=True,debug=False):
    """ fills out all remaining entries in the swap and returns """
    #fuck pythong
    swap = copy.deepcopy(swaps)
    #get the order of indexes to fill
    unit_order = _get_unit_look_order(swap)
    #get the absent dict
    absent_dict = _get_inital_absent_dict(swap)
    #ok so from here on out I assume that all the units available for swapping to are also the units needing swapping from
    #I think this is a fine assumption because no matter how I do this it literally cant work if that isnt the case
    for unit_id in unit_order:
        r = rand.randinst(unit_id+100) #this is prolly fine
        #first step is getting the strength to swap to
        new_strength = _get_this_units_new_strength(unit_id,absent_dict,balance_scalor,initial_chance_dict,maintain_grouping,r.randrange(0,100000),debug=debug)
        #what do I do when it fails? just set it to itself I guess
        if new_strength == -1:
            if debug:
                print("forced to set " + str(unit_id) + " to self")
            swap[unit_id] = unit_id
        else:
            #now I should be good to duplicate the strength array and remove self from it
            available_at_strength = copy.deepcopy(absent_dict[str(new_strength)])
            if unit_id in available_at_strength:
                available_at_strength.remove(unit_id)
            #now its all fine and dandy to choose a unit and remove it from absent dict
            second_r = rand.randinst(unit_id+300)
            new_id = available_at_strength[second_r.randrange(0,len(available_at_strength))]
            swap[unit_id] = new_id
            absent_dict[str(new_strength)].remove(new_id)
    #all good
    return swap

def _populate_variants(swaps,variant_dict,shift_index=0):
    """ populates a swap by completing the variants
    \n shift index is the amount to reduce the index by, so for swap2 this should be the length of swap1 """
    r = rand.randinst(104)
    for each in variant_dict:
        this_vswap = _process_variant(variant_dict[each],r.randrange(0,1000))
        #now actually set those values in swap
        for x in range(0,len(this_vswap[0])):
            swaps[this_vswap[0][x]-shift_index] = this_vswap[1][x]
    #should be all good
    return swaps

def _process_variant(variant,random_number):
    """ turns an array of variants [x,y,z] int an array [[x,y,z],[y,z,x]] """
    #first randomly order the array
    r = rand.randinst(random_number)
    new_order = []
    to_add = copy.deepcopy(variant)
    for x in range(0,len(to_add)):
        new_order.append(to_add.pop(r.randrange(0,len(to_add))))
    #now create a new array and rotate that by a random number less than the length of the array
    to_become = copy.deepcopy(new_order)
    for x in range(0,r.randrange(0,len(new_order))):
        to_become.append(to_become.pop(0)) #this will prolly die if theres an empty array on variant for some reason
    #should be all good
    return [new_order,to_become]





""" parts for calculating stats """

def _turn_swap_into_applyable_swap(swap,balance_mag=True,config=defaults.DEFAULT_CONFIG,post_attack_anims=[]):
    """ takes a swap array and turns it into an equal length array
    \n each index contains [id to swap to,amount to multiply mag by] """
    #first step is getting the correct stat array to use
    estat = early_rebalance(config)
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
        #now loop through each line from there till the end attempting to edit it
        for enemy_line in range(number_starting_lines,len(stage_sche)):
            enemy_id = enemy_line[d.enemy_id]
            #check if real then, if enemy doesnt route to self
            if enemy_id != 0 and enemy_id != app_swap[enemy_id][0]:
                edited = True
                enemy_line[d.enemy_id] = app_swap[enemy_id][0]
                new_mag = enemy_line[d.magnification]*app_swap[enemy_id][1]
                enemy_line[d.magnification] = math.ceil(new_mag) #not a clue how slow this is but it should prevent any 0 mags
        if edited:
            gf.file_writer(stage_name,stage_sche)
    









""" full parts """

def _do_id_swap(debug=False,balance_mag=True,maintain_grouping=True,split_id=-1,swap_eoc=False,variant_swap=False,config=defaults.DEFAULT_CONFIG,post_attack_anims=[],chaos=False):
    """ does all the id swap things """
    #first get the swap array and split it into its respective parts
    swap = _get_initial_swaps()
    if split_id == -1:
        swap1 = copy.deepcopy(swap)
        swap2 = []
    else:
        swap1 = []
        swap2 = []
        for x in range(0,len(swap)):
            if x <= split_id: #this means it goes up to and including split id
                swap1.append(swap[x])
            else:
                swap2.append(swap[x])
    #I dont think variant swap will use any of the chance stuff
    if variant_swap:
        #first get variant dict
        varianct_dict = _get_initial_variant_dict(0,split_id)
        swap1 = _populate_variants(swap1,varianct_dict)
        varianct_dict = _get_initial_variant_dict(split_id)
        swap2 = _populate_variants(swap2,varianct_dict,shift_index=len(swap1))
    #now get balance scalor and init chance dict
    balance_scalor = _get_initial_balance_scalor(chaos)
    init_chance_dict = _get_initial_chance_dict(balance_scalor,maintain_grouping,chaos)

    #now complete the rest of the swaps and recombine
    swap1 = _populate_swap(swap1,balance_scalor,init_chance_dict,maintain_grouping,debug)
    swap2 = _populate_swap(swap2,balance_scalor,init_chance_dict,maintain_grouping,debug)
    swap = swap1 + swap2
    #and now get the applyable version
    app_swap = _turn_swap_into_applyable_swap(swap,balance_mag,config,post_attack_anims)
    #and now apply it to nearly every stage in the game!
    _apply_app_swap_to_stages(app_swap,swap_eoc)
















