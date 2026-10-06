
import copy
from ..enemy_swap import debug_output
import tadbcmc.core.seeded_randomization as srand
from ..enemy_swap import initialize_information






def _get_this_units_new_strength(
        unit_id:int, #this is needed to exclude self from the size calculation
        current_strength:int, #this is needed to get the base chance to swap to each other strength 
        available_id_dict:dict[int,list[int]], #this is just the lists of all available ids at each strength
        base_chance_dict:dict[int,dict[int,float]], #this actually contains the base chance to swap to each other strength
        random_number:int, #0-100,000  used to determine which strength to swap to
        log=None,
        debug:bool=False
    ) -> int|None:
    """ gets the strength of the new id to swap to, does not select which at that strength to swap to """
    """
    this works by multiplying the base chance of swapping to each strength by the number of units remaining at that strength
    then the sum of those products is used to scale the total size to 100000 and random number is used to select which strength
    """
    #first get the correct base chance dict to use here
    chance_dict = copy.deepcopy(base_chance_dict[str(current_strength)])
    #now multiply each of those by the length of available ids
    for each_strength in chance_dict:
        mult = 0
        if each_strength in available_id_dict:
            mult += len(available_id_dict[each_strength])
            if unit_id in available_id_dict[each_strength]: mult -= 1
        chance_dict[each_strength] *= mult
    #now get the sum
    count = 0
    for each_strength in chance_dict: count += chance_dict[each_strength]
    if count == 0: #not conditional on debug as this should just always run
        debug_output.output_somewhere(f"failed to find id to swap {unit_id} to, this can happen 1-2 times",log=log)
        return None
    #now scale to 100,000
    for each_strength in chance_dict: chance_dict[each_strength] *= (100000/count)
    #now reduce it until a strength is selected
    for each_strength in chance_dict:
        if random_number < chance_dict[each_strength]: return int(each_strength)
        else: random_number -= chance_dict[each_strength]
    #now catch any errors that somehow happened
    pass_log = None
    if debug: #why is this lmao
        pass_log = log
    debug_output.output_somewhere(f"failed to select a new strength for {unit_id} in filling_swap: _get_this_units_new_strength",log=pass_log)
    debug_output.output_somewhere(f"remainder: {random_number}",log=pass_log)
    return None

#This function is likely to cause catastrophic differences in randomization with the slightest difference, is there any possible way to change that
def _get_unit_look_order(
        incomplete_swap:list[int],
    ) -> list[int]:
    """ gets a list of every id still containing a -1 in a randomized order """
    #first get which ids still need to be done
    #this makes the assumption that things which are themselves -1 are not placed elsewhere, an assumption which must be made in order for anything to work
    missing_ids  = []
    for x in range(0,len(incomplete_swap)):
        if incomplete_swap[x] == -1:
            missing_ids.append(x)
    #now randomize the order
    r = srand.randinst(807)
    output_order = []
    for x in range(0,len(missing_ids)): output_order.append(missing_ids.pop(r.randrange(0,len(missing_ids))))
    return output_order

def _get_available_dict(
        incomplete_swap:list[int],
        swap_strength_list:list[int],
    ) -> dict[int,list[int]]:
    """ looks through the incomplete swap logging the strengths of each unit yet to be filled """
    available_dict = {}
    #Im making the assumption that everything with a swap id of -1 is included, I think this is perfectly fair
    for x in range(0,len(incomplete_swap)):
        if incomplete_swap[x] == -1:
            this_strength = str(swap_strength_list[x])
            if this_strength not in available_dict:
                available_dict[this_strength] = []
            available_dict[this_strength].append(x)
    return available_dict

def fill_general_swap(
        incomplete_swap:list[int],
        swap_strength_list:list[int],
        maintain_class:bool, #these need to be passed to getting the base chance dict
        consider_strength:bool, # ^
        log=None,
        debug:bool=False,
    ) -> list[int]:
    """ fills out a general swap with all remaining units """
    #first step, get the look order for this particular swap
    look_order = _get_unit_look_order(incomplete_swap)
    available_dict = _get_available_dict(incomplete_swap,swap_strength_list)
    base_chance_dict = initialize_information.get_base_chance_mult_dict(incomplete_swap,swap_strength_list,maintain_class,consider_strength)
    #now we can just loop through each unit in look order
    for unit_id in look_order:
        self_strength = swap_strength_list[unit_id]
        r = srand.randinst(unit_id*3+100)
        #first, get this units new strength
        new_strength = _get_this_units_new_strength(
            unit_id=unit_id,
            current_strength=self_strength,
            available_id_dict=available_dict,
            base_chance_dict=base_chance_dict,
            random_number=r.randrange(0,100000),
            log=log,debug=debug,
        )
        #if it fails just set it to itself
        if new_strength == None:
            incomplete_swap[unit_id] = unit_id
            debug_output.output_somewhere(f"unit {unit_id} set to swap to self")
        else:
            #now we just choose a unit except from self at that strength
            units_at_strength = copy.deepcopy(available_dict[str(new_strength)])
            if unit_id in units_at_strength: units_at_strength.remove(unit_id)
            new_id = units_at_strength[r.randrange(0,len(units_at_strength))]
            #set and remove from avail dict
            incomplete_swap[unit_id] = new_id
            available_dict[str(new_strength)].remove(new_id)
    #thats it
    return incomplete_swap


















