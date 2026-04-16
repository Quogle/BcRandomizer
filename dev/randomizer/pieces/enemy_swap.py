import dev.randomizer.enums.enemy as e
import dev.randomizer.func.game_files as f
import dev.randomizer.enums.unit_info as ui
from dev.randomizer.func.random import randinst
from dev.randomizer.data.filepaths import *
from dev.randomizer.func.misc import *
from dev.randomizer.parse_config import settings


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
    r = randinst(3004)
    swapped_to = []
    for x in range(0,len(info_array)):
        swapped_to.append(-1)
    #set collabs and unsetables in swapped
    for unit_id in range(0,len(info_array)):
        if info_array[unit_id][1] < 0 or info_array[unit_id][2] == 1:
            swapped_to[unit_id] = unit_id
    #now randomize remaining units
    for unit_id in range(0,len(info_array)):
        #call random on every single unit
        random1 = r.randrange(0,1000)
        if unit_id not in swapped_to: #ignore already done units
            swapped_to = the_while(swapped_to,info_array,unit_id,random1)
    #now create the swap array
    swap_info = []
    #do vanilla first
    for unit_id in range(0,len(vstats)):

    
            


            



















def the_while(swapped_to=list,info_array=list,unit_id=0,random_number=0):
    """
    the while loop for finding a units new id
    """
    #fix specifically for if unit id is the last remaining thing not in swapped to
    if unit_id+1 == len(swapped_to):
        swapped_to[unit_id] = unit_id
        return swapped_to
    #things to intialize
    r = randinst(random_number)
    granuality = 10000
    remaining_units = swapped_to.count(-1)
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



