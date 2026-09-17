import tadbcmc.data.enums.cats as c
import tadbcmc.core.seeded_randomization as srand
import tadbcmc.core.game_files as gf
from ...config.defaults import DEFAULT_CONFIG
import copy

#these are in alphabetical order
TRAITS = [
    int(c.t.aku),
    int(c.t.alien),
    int(c.t.angel),
    int(c.t.dark),
    int(c.t.floating),
    int(c.t.metal),
    int(c.t.red),
    int(c.t.relic),
    int(c.t.white),
    int(c.t.zombie),
]
TALENT_TRAITS = [
    int(c.tv.aku),
    int(c.tv.alien),
    int(c.tv.angel),
    int(c.tv.dark),
    int(c.tv.floating),
    int(c.tv.metal),
    int(c.tv.red),
    int(c.tv.relic),
    int(c.tv.white),
    int(c.tv.zombie),
]
TALENT_SUMS = [
    int(c.tv.sum_aku),
    int(c.tv.sum_alien),
    int(c.tv.sum_angel),
    int(c.tv.sum_dark),
    int(c.tv.sum_floating),
    int(c.tv.sum_metal),
    int(c.tv.sum_red),
    int(c.tv.sum_relic),
    int(c.tv.sum_white),
    int(c.tv.sum_zombie),
]













def _get_trait_look_order(all_traits:list[int],r_offset:int=13) -> list[int]:
    """ randomizes the order of the traits in the array """
    r = srand.randinst(r_offset)
    output = []
    temp_tl = copy.deepcopy(all_traits)
    for x in range(0,len(temp_tl)):
        output.append(temp_tl.pop(r.randrange(0,len(temp_tl))))
    return output

def _get_trait_from_talents(talent_array:list) -> list[int]:
    """ harvests the traits in a talent and returns a list of their c.t values """
    talent_traits_has = []
    #first get the ones from the sum
    talent_sum = talent_array[c.tpos.trait_sum]
    for x in range(0,len(TALENT_SUMS)):
        if (talent_sum%(2*TALENT_SUMS[x])) >= (TALENT_SUMS[x]):
            talent_traits_has.append(TRAITS[x])
    for talent_block_id in range(2,len(talent_array)):
        this_block = talent_array[talent_block_id]
        if this_block[c.tpos.ability_id] in TALENT_TRAITS:
            trait = this_block[c.tpos.ability_id]
            index = TALENT_TRAITS.index(trait)
            talent_traits_has.append(TRAITS[index])
    return talent_traits_has

def _get_units_traits(unit_array:list[list[int]|int]) -> list[int]:
    """ gets the traits a unit/form has, works for both unit and form """
    if type(unit_array[0]) == list:
        #this means its 2d
        has_traits = []
        for form_id in range(0,len(unit_array)):
            for trait in TRAITS:
                if unit_array[form_id][trait] == 1 and trait not in has_traits:
                    has_traits.append(trait)
    else:
        #this means its 1d
        has_traits = []
        for trait in TRAITS:
            if unit_array[trait] == 1 and trait not in has_traits:
                has_traits.append(trait)
    return has_traits

def _order_has_traits_in_look(look_order:list[int],has_raw:list[int],has_talents:list[int]) -> list[int]:
    """ takes the traits from the unit stats and talents and returns has traits in the correct order """
    has_traits = []
    for trait in look_order:
        if trait in has_raw or trait in has_talents:
            has_traits.append(trait)
    return has_traits








