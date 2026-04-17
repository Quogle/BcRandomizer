import dev.randomizer.enums.enemy as e
import dev.randomizer.func.game_files as f
import dev.randomizer.enums.unit_info as ui
from dev.randomizer.func.random import randinst
from dev.randomizer.data.filepaths import *
from dev.randomizer.func.misc import *
from dev.randomizer.parse_config import settings
from configs.internal_config import ENEMY_ID_SWAP_COUNT
import math

conditions = {}

def do_swap():
    """
    total function for id swap
    \n conditional
    """
    set_conditions()
    if not conditions["do_swap"]:
        return
    #load up needed info
    vstats = f.file_reader(DATA_LOCAL + ENEMY_STATS)
    mstats = f.file_reader(ENEMY_STATS)
    #establish array of info needed for this
    info_array = [] #id,strength,collab
    for x in range(0,len(mstats)):
        info_array.append([x])
    #now read info from settings into it
    for x in range(0,len(settings["enemy_info"])):
        info_array[x].append(settings["enemy_info"][x][ui.e.swap_strength])
        info_array[x].append(settings["enemy_info"][x][ui.e.collab])
    for each in mstats:
        if len(each) < 2: #if enemy info hasnt been manually updated set their strength as 50 (theyll only randomize to other new enemies at default settings)
            each.append(50)
            each.append(0)
    #what else do I have to initialize
    swapped_to = get_total_swapped_list(info_array)
    #now get mag changes, 1 is same strength
    swap_info = []
    for unit_id in range(0,len(swapped_to)):
        this_swap = [unit_id]
        (to_dps,to_hp) = calc_enemy_stats(vstats[swapped_to[unit_id]])
        (this_dps,this_hp) = calc_enemy_stats(vstats[unit_id])
        magboost = calc_mag_by(to_dps,to_hp,this_dps,this_hp)
        this_swap.append(magboost)
        swap_info.append(this_swap)
            


            









def apply_swap_to_all_stages(swap_info):
    """
    is responsible for actually applying swap to all stage
    """

def calc_enemy_stats(stats):
    """
    returns dps and health
    """
    damage = 0
    attack_cycle = stats[e.s.tba]
    if attack_cycle == 0:
        attack_cycle = 10
    if stats[e.s.multiPreAtk3] != 0:
        attack_cycle += stats[e.s.multiPreAtk3]
        damage += stats[e.s.multiDamage3]
    elif stats[e.s.multiPreAtk2] != 0:
        attack_cycle += stats[e.s.multiPreAtk2]
        damage += stats[e.s.multiDamage2]
    else:
        attack_cycle += stats[e.s.preatk]
        damage += stats[e.s.attack]
    dps = damage/attack_cycle
    hp = stats[e.s.hp]
    return (dps,hp)

def calc_mag_by(damage1,hp1,damage2,hp2):
    """
    mag boost for replacing 1 with 2
    \n if 2 is weaker than 1, this will be > 1
    """
    if not conditions["edit_mags"]:
        return 1
    if damage1 == 0:
        damage1 = 1
    if hp1 == 0:
        hp1 = 1
    if damage2 == 0:
        damage2 = 1
    if hp2 == 0:
        hp2 = 1
    attack_ratio = damage1/damage2
    health_ratio = hp1/hp2
    return math.sqrt(attack_ratio*health_ratio)

def get_total_swapped_list(info_array):
    """
    creates swapped to
    """
    r = randinst(3004)
    length = len(info_array)
    if conditions["update_enemy_count"] < length:
        length = conditions["update_enemy_count"]
    #divide units into before update and after update
    swap_part_1 = []
    swap_part_2 = []
    for x in range(0,len(info_array)):
        if x < length:
            swap_part_1.append(-1)
        else:
            swap_part_2.append(-1)
    #fill out arrays with collab/unswappable ids
    for unit_id in range(0,len(info_array)):
        if info_array[unit_id][1] < 0 or info_array[unit_id][2] == 1:
            if unit_id < length:
                swap_part_1[unit_id] = unit_id
            else:
                swap_part_2[unit_id-length] = unit_id
    if conditions["block_update_breakage"]:
        swap_part_1 = fill_out_swapped_list(swap_part_1,info_array,r)
    total_swapped_to = swap_part_1 + swap_part_2
    total_swapped_to = fill_out_swapped_list(total_swapped_to,info_array,r)
    return total_swapped_to
 
def fill_out_swapped_list(swapped_to=list,info_array=list,r=randinst):
    """
    fills out the current swapped to list
    """
    for unit_id in range(0,len(swapped_to)):
        #call random on every single unit
        random1 = r.randrange(0,1000)
        if unit_id not in swapped_to: #ignore already done units
            swapped_to = the_while(swapped_to,info_array,unit_id,random1)
    return swapped_to

#this prolly needs to be redone to better fix config changes having wild efffect
def the_while(swapped_to=list,info_array=list,unit_id=0,random_number=0):
    """
    the while loop for finding a units new id
    """
    #count how many units
    remaining_units = swapped_to.count(-1)
    if conditions["swap_in_class"]:
        remaining_units = 0
        for unit in info_array:
            if int(unit[1]/10) == int(info_array[unit_id][1]/10):
                remaining_units += 1
    #if remaining units = 0 or unitid is the last unit end it
    if unit_id+1 == len(swapped_to)  or remaining_units == 0:
        swapped_to[unit_id] = unit_id
        return swapped_to
    #things to intialize
    r = randinst(random_number)
    granuality = 10000
    base_chance = 1/remaining_units
    current_id = unit_id
    loop_count = 0
    while unit_id not in swapped_to:
        loop_count += 1
        if current_id >= len(info_array):
            current_id = unit_id
        current_id += 1
        chance = base_chance
        if loop_count > 10: #increase base chance past 10
            chance = base_chance*(1+loop_count/10)
        if loop_count > 100: #kill self if continually failed 100 times
            swapped_to[unit_id] = unit_id
            return swapped_to 
        #get current chance
        if current_id in swapped_to: #this covers collabs and unswappables aswell as already swapped
            this_chance = 0
        else:
            this_chance = calc_chance(chance,info_array[unit_id][1],info_array[current_id][1])
        #see if passes chance
        benchmark = this_chance*granuality
        number = r.randrange(0,granuality)
        #return it if it does
        if number < benchmark:
            swapped_to[unit_id] = current_id
            return swapped_to
        #go to next unit if it doesnt

def calc_chance(base_chance,value1,value2):
    """
    calculates the chance adjusted for distance
    \n conditional for some reason
    """
    if conditions["swap_in_class"]: #just straight up 0% chance if theyre different classes
        first_class = int(value1/10)
        second_class = int(value2/10)
        if first_class != second_class:
            return 0
    if conditions["balanced"]:
        diff = abs(value1-value2)
        new_chance = base_chance/((0.9+ (conditions["strictness"]*diff/40))**2)
        # at 10 strict  1.25x 0d    .75x 1d .50x 2d .35x 3d .25x 4d
        # at 20 strict  1.25x 0d    .35x 1d .15x 2d .10x 3d .05x 4d
        # at 5 strict   1.25x 0d    .85x 1d .60x 2d .45x 3d .35x 4d
        return new_chance
    else:
        return base_chance

def set_conditions():
    """
    sets global variable conditions to have values needed
    \n just to make constant processing of settings
    """
    swap_in_class = settings["enemy"]["extras"]["swap_only_in_class"]
    balanced = settings["enemy"]["extras"]["balanced_swap"]
    strictness = settings["enemy"]["extras"]["balance_strictness"]
    id_swap = settings["enemy"]["extras"]["balance_strictness"]
    strictness = settings["enemy"]["extras"]["balance_strictness"]
    update = settings["enemy"]["extras"]["swap_untouched_by_update"]
    enemy_count = ENEMY_ID_SWAP_COUNT
    edit_mags = settings["enemy"]["extras"]["adjust_magnification"]
    do_eoc = settings["enemy"]["extras"]["include_eoc"]
    try:
        strictness = float(strictness)
        if strictness < 0: #prevent negatives from breaking it
            strictness = 0
    except:
        strictness = 10
    global conditions
    conditions["swap_in_class"] = swap_in_class
    conditions["balanced"] = balanced
    conditions["strictness"] = strictness
    conditions["do_swap"] = id_swap
    conditions["block_update_breakage"] = update
    conditions["update_enemy_count"] = enemy_count + 2
    conditions["edit_mags"] = edit_mags
    conditions["do_eoc"] = do_eoc



