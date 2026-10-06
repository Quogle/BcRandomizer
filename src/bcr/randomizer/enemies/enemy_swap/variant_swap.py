

import copy
from ..enemy_swap import debug_output
import tadbcmc.core.seeded_randomization as srand
from ..enemy_swap import initialize_information





def process_one_variant_on_swap(variant_list:list[int],incomplete_swap:list[int],random_number):
    """ fills out a swap with one particular variant """
    #first get r
    r = srand.randinst(107+45*random_number)
    #first step is randomly ordering this variant list
    new_order = []
    temp_list = copy.deepcopy(variant_list)
    for x in range(0,len(variant_list)):
        new_order.append(temp_list.pop(r.randrange(0,len(temp_list))))
    #now create a copy and rotate it by one
    shifted = copy.deepcopy(new_order)
    shifted.append(shifted.pop(0))
    #now just set each in new order to the corresponding index in shifted
    for x in range(0,len(new_order)):
        incomplete_swap[new_order[x]] = shifted[x]
    return incomplete_swap

def process_all_variants_in_dict_on_swap(
        variant_dict:dict[int,list[int]], #this is all the variants to do it with
        incomplete_swap:list[int],
        random_number:int, #this is required to shift the second half of making a swap so it isnt similar to the first
    ) -> list[int]:
    """ fills out a swap with all variants in given variant dict """
    for variant in variant_dict:
        var_number = int(variant)
        incomplete_swap = process_one_variant_on_swap(
            variant_dict[variant],
            incomplete_swap,
            random_number=(267+var_number*12+random_number)
        )
    #I think thats all?
    return incomplete_swap















