import dev.randomizer.enums.enemy as e
import dev.randomizer.func.game_files as f
import dev.randomizer.enums.unit_info as ui
from dev.randomizer.func.random import randinst
from dev.randomizer.data.filepaths import *
from dev.randomizer.func.misc import *
from dev.randomizer.parse_config import settings
from configs.internal_config import ENEMY_ID_SWAP_COUNT
import math
import copy


conditions = {}
chance_array = []

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

def set_chance_array():
    """
    sets chance array at the start to optimize
    """
    global chance_array
    chance_array = [1]
    if conditions["balanced"]:
        chance_array = []
        for x in range(0,10):
            diff = x
            new_chance = 1/((0.9+ (conditions["strictness"]*diff/40))**2)
            chance_array.append(new_chance)
        chance_array.append(0)
        # at 10 strict  1.25x 0d    .75x 1d .50x 2d .35x 3d .25x 4d
        # at 20 strict  1.25x 0d    .35x 1d .15x 2d .10x 3d .05x 4d
        # at 5 strict   1.25x 0d    .85x 1d .60x 2d .45x 3d .35x 4d

def total_do_swap(debug=True):
    """
    master function, does all the eswap stuff
    \n conditional
    """
    set_conditions()
    set_chance_array()
    if not conditions["do_swap"]:
        return
    #initialize
    vstat = f.file_reader(DATA_LOCAL + ENEMY_STATS)
    #get swap info
    if debug:
        print("get eswaps")
    swap_info = get_swaps_then_info(vstat)
    if debug:
        print("apply eswap to all stages")
    for x in range(0,len(swap_info)):
        print(x,end="\t")
        print(swap_info[x])
    apply_to_all_stages(swap_info,debug)



def get_swaps_then_info(vstat):
    """
    makes swaps from scratch and then gets swap info
    """
    einfo = settings["enemy_info"]

    strong = []
    collab = []
    #make length first to avoid duplicates
    for x in range(0,len(vstat)):
        strong.append(50)
        collab.append(0)
    for x in range(0,len(einfo)):
        unit_id = einfo[x][ui.e.unit_id]
        if unit_id < len(vstat):
            strong[unit_id] = einfo[x][ui.e.swap_strength]
            collab[unit_id] = einfo[x][ui.e.collab]


    #now get swap
    swap = get_total_swap(strong,collab)
    #now make swap info
    swap_info = get_swap_info(swap,vstat)
    return swap_info



def apply_to_all_stages(swap_info,debug=True):
    """
    applies swap info to all stages
    \n conditional, for eoc and mags
    """
    #vanilla_stages = get_all_vanilla_stages(include_eoc=conditions["do_eoc"])
    vanilla_stages = [STAGE_SCHEM + SOL_SLETTER +"000_00.csv"]
    do_mags = conditions["edit_mags"]
    number_of_stages = len(vanilla_stages)
    current_stage = 0
    for stage in vanilla_stages:
        if debug:
            current_stage += 1
            if current_stage % 1000 == 0:
                print(str(current_stage) + "/" + str(number_of_stages) + " eswapped")
        this_stage = f.stage_sche(stage)
        for enemy in this_stage.enemies:
            enemy_id = enemy[this_stage.enemy_id]
            new_enemy_id = swap_info[enemy_id][0]
            enemy[this_stage.enemy_id] = new_enemy_id
            if do_mags and len(enemy) > this_stage.magnification:
                enemy_mag = enemy[this_stage.magnification]
                new_enemy_mag = int(enemy_mag*swap_info[enemy_id][1])
                if new_enemy_mag <= 0:
                    new_enemy_mag = 1
                enemy[this_stage.magnification] = new_enemy_mag
        this_stage.submit()
    if debug:
        print("eswaps applied to stages")


def get_swap_info(swap,vstat):
    """
    2d array [id,mult]
    """
    swap_info = []
    for x in range(0,len(swap)):
        (dps1,hp1) = calc_enemy_stats(vstat[x])
        (dps2,hp2) = calc_enemy_stats(vstat[swap[x]])
        boost = calc_mag_by(dps1,hp1,dps2,hp2)
        swap_info.append([swap[x],boost])
    return swap_info

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



def get_total_swap(strong,collab):
    """
    returns the fully map swap awaay
    """
    (swap1,swap2) = get_initial_swaps(strong,collab)
    swap1 = fill_swap(swap1,strong,0,False)
    swap1 = swap1 + swap2
    swap1 = fill_swap(swap1,strong,1167,False)
    return swap1

def get_initial_swaps(strong,collab):
    """
    returns swaps array initilized with unit ids of unswappables and -1 otherwise
    """
    swap1 = []
    swap2 = []
    length = len(strong)
    if conditions["block_update_breakage"]:
        length = conditions["update_enemy_count"]
    for unit_id in range(0,len(strong)):
        if unit_id < length:
            if strong[unit_id] < 0 or collab[unit_id] == 1:
                swap1.append(unit_id)
            else:
                swap1.append(-1)
        else:
            if strong[unit_id] < 0 or collab[unit_id] == 1:
                swap2.append(unit_id)
            else:
                swap2.append(-1)
    return (swap1,swap2)

def fill_swap(swap,strong,random_number,debug=True):
    """
    fills out a swap and returns it
    """
    r = randinst(random_number)
    count_dict = get_count_dict(swap,strong)
    for x in range(0,len(swap)):
        random_number = r.randrange(0,100000)
        if swap[x] == -1:
            unit_strength = strong[x]
            new_strength = get_unit_new_strength(count_dict,unit_strength,random_number)
            if new_strength == None:
                swap[x] = x
                if debug:
                    print(str(x) + " was the last enemy standing!")
            else:
                count_dict[str(new_strength)] -= 1
                for each in count_dict:
                    if count_dict[each] == -1:
                        pass
                #now get all units at that strength
                available = []
                for y in range(0,len(swap)):
                    if y not in swap and strong[y] == new_strength:
                        if x != y:
                            available.append(y)
                #now set this unit
                r2 = randinst(x*10+random_number)
                swap[x] = available[r2.randrange(0,len(available))]
                if debug:
                    print("set " + str(x) + " as " + str(swap[x]))
    return swap

def get_count_dict(swap,strong):
    """
    gets count dict for a swap
    """
    count_dict = {}
    lower = 0
    upper = 0
    for x in range(0,len(swap)):
        if swap[x] == -1:
            if strong[x] < lower:
                lower = strong[x]
            if strong[x] > upper:
                upper = strong[x]
    for x in range(lower,upper+1):
        count_dict[str(x)] = 0
    #now add all the counts
    for x in range(0,len(swap)):
        if swap[x] == -1:
            count_dict[str(strong[x])] += 1
    return count_dict

def get_unit_new_strength(count_dict,strength,random_number):
    """
    gets a units new strength
    """
    scale = 100000
    this_count = copy.deepcopy(count_dict)
    this_count[str(strength)] -= 1
    if this_count[str(strength)] == -1:
        this_count[str(strength)] = 0
    #set lower and upper
    if conditions["swap_in_class"]:
        lower = 10*int(strength/10)
        upper = lower + 9
    elif conditions["balanced"]:
        lower = strength-10
        upper = strength+10
    else:
        lower = 100
        upper = -1
        for each in this_count:
            n = int(each)
            if n < lower:
                lower = n
            if n > upper:
                upper = n
    #now get number of enemies
    total_number_enemies = 0
    for x in range(lower,upper+1):
        if str(x) in this_count:
            total_number_enemies += this_count[str(x)]
    if total_number_enemies == 0:
        return None
    #now get chance array
    chances = {}
    for x in range(lower,upper+1):
        if str(x) in this_count:
            chances[str(x)] = this_count[str(x)]
    #make them proportions
    for x in chances:
        chances[x] /= total_number_enemies
    #now adjust them for balance
    if conditions["balanced"]:
        total_chances = 0
        for x in chances:
            chances[x] *= get_multiplier_based_on_diff(strength,int(x))
            total_chances += chances[x]
        #reset them back to proportions
        for x in chances:
            chances[x] /= total_chances
    #now get the value
    for x in chances:
        if random_number < chances[x]*scale:
            return int(x)
        else:
            random_number -= chances[x]*scale
    print("wow I failed " +str(random_number))
    return None

def get_multiplier_based_on_diff(value1,value2):
    """
    
    """
    global chance_array
    diff = abs(value1-value2)
    if diff < len(chance_array):
        return chance_array[diff]
    else:
        return chance_array[-1]











