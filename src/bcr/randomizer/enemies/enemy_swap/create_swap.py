
import tadbcmc.data.enums.unit_info as ui
from ..enemy_swap import variant_swap
from ..enemy_swap import filling_swap
from ..enemy_swap import debug_output
from ..enemy_swap import initialize_information

def create_swap(
        breaking_point:int,
        do_var_swap:bool,
        do_gen_swap:bool,
        maintain_class:bool,
        consider_strength:bool,
        log=None,
        debug:bool=False,
    ) -> list[int]:
    """  """
    #first we need to get the total information
    initialize_information._set_ENEMY_INFO_values()
    (included_in_swap_list, swap_strength_list, variant_id_list) = initialize_information.harvest_unit_info_from_ENEMY_INFO()
    (first_half_variants,second_half_variants) = initialize_information.variant_list_dict_maker(variant_id_list,included_in_swap_list,breaking_point)
    #now make the first half
    first_half_included = included_in_swap_list[0:breaking_point]
    first_half_strengths = swap_strength_list[0:breaking_point]
    if breaking_point == -1: #this is if theres no breaking point
        first_half_included = included_in_swap_list
        first_half_strengths = swap_strength_list
        first_half_variants = second_half_variants
    swap = _make_swap_half(
        existing_swap=[],
        included_in_swap_list=first_half_included,
        swap_strength_list=first_half_strengths,
        variant_dict=first_half_variants,
        do_var_swap=do_var_swap,
        do_gen_swap=do_gen_swap,
        maintain_class=maintain_class,
        consider_strength=consider_strength,
        log=log,debug=debug,
    )
    #now do the second half
    swap = _make_swap_half(
        existing_swap=swap,
        included_in_swap_list=included_in_swap_list,
        swap_strength_list=swap_strength_list,
        variant_dict=second_half_variants,
        do_var_swap=do_var_swap,
        do_gen_swap=do_gen_swap,
        maintain_class=maintain_class,
        consider_strength=consider_strength,
        log=log,debug=debug,
    )
    #ok thats all
    return swap





def _extend_swap_with_new_units(
        existing_swap:list[int],
        included_in_swap_list:list[bool],
    ) -> list[int]:
    """ extends the input swap with new units, included units are set to -1 while excluded are set to self 
    \n included in swap list is the full list, not only the new units """
    for u_id in range(len(existing_swap),len(included_in_swap_list)):
        if included_in_swap_list[u_id]: existing_swap.append(-1)
        else: existing_swap.append(u_id)
    return existing_swap

def _prepare_swap_for_vg_swap(
        existing_swap:list[int],
        included_in_swap_list:list[bool],
        variant_dict:list[int],
    ) -> list[int]:
    """ extends an existing swap to the length of included bools and takes care of enemy base swap """
    #first extend
    new_swap = _extend_swap_with_new_units(existing_swap,included_in_swap_list)
    enemy_base_var = str(int(ui.enemy_variant.attacking_base))
    if enemy_base_var in variant_dict:
        new_swap = variant_swap.process_one_variant_on_swap(variant_dict.pop(enemy_base_var),new_swap,len(included_in_swap_list))
    return new_swap

def _make_swap_half(
        existing_swap:list[int], #this is just [] for the first half
        included_in_swap_list:list[bool], 
        swap_strength_list:list[int],
        variant_dict:dict[int,list[int]], # this is required even without variant swap since enemy bases use it
        do_var_swap:bool,
        do_gen_swap:bool,
        maintain_class:bool,
        consider_strength:bool,
        log=None,
        debug:bool=False,
    ) -> list[int]:
    """ makes a swap half based on input information
    \n included and strength should only contain info upto split unit id
    \n variant dict should only be from this half """
    #first just extend it and do enemy base swap, this isnt running if neither var or gen swap are on anyways
    new_swap = _prepare_swap_for_vg_swap(existing_swap,included_in_swap_list,variant_dict)
    #now if variant swap, do the rest of variants
    if do_var_swap:
        new_swap = variant_swap.process_all_variants_in_dict_on_swap(variant_dict,new_swap,random_number=len(included_in_swap_list)+30)
    #now if general swap, do it
    if do_gen_swap:
        new_swap = filling_swap.fill_general_swap(
            incomplete_swap=new_swap,
            swap_strength_list=swap_strength_list,
            maintain_class=maintain_class,
            consider_strength=consider_strength,
            log=log,debug=debug,
        )
    #now set all remaining units to self
    for u_id in range(0,len(new_swap)):
        if new_swap[u_id] == -1:
            debug_output.output_somewhere(f"unit {u_id} not set by v or g swap, setting to self") #this is actually gonna happen a lot if gen swap is off
            new_swap[u_id] = u_id
    #all good
    return new_swap








