import tadbcmc.data.enums.cats as c
import tadbcmc.core.seeded_randomization as srand
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn

import tadbcmc.core.file_handler as fh
from ...config.defaults import DEFAULT_CONFIG
import copy
from ..units import trait_randomization_mk3

UNIT_TRAIT_MAP_FILE = "unit_trait_map.csv"

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

def _get_stats_and_talents_to_use_in_map_creation(per_form,config=DEFAULT_CONFIG) -> tuple[list[list[list]],list[list]]:
    """ gets the stats to use in creating the map by removing the information that would change it after the specified version """
    #I dont feel like figuring out how the fuck Im gonna do this rn nor do I even have the relevant initial cstat array to do it
    #however, if its per form theres no reason to remove any cats stats
    # if its per whole unit then cat stats added afterwards should be removed
    # always talents added afterwards should be removed

def _create_randomization_trait_map(per_form,avoid_old_traits,all_traits,allowed_traits):
    """ creates the trait map to be used elsewhere, saves it to cache """
    trait_map = []
    (cat_stats,talent_stats) = _get_stats_and_talents_to_use_in_map_creation(per_form)
    #now get the form traits and talent traits arrays for all units
    cat_traits = []
    talent_traits = []
    for u_id in range(0,len(cat_stats)):
        this_base_traits = _get_units_traits(cat_stats[u_id])
        this_talent_traits = _get_trait_from_talents(talent_stats[u_id])
        #theres no reason to edit them right?
        cat_traits.append(this_base_traits)
        talent_traits.append(this_talent_traits)
    #now we just create the trait map one by one
    for u_id in range(0,len(cat_traits)):
        if per_form:
            this_units_map = []
            for form_id in range(0,len(cat_traits)):
                #get the info required to do it
                look_order = _get_trait_look_order(all_traits,13+300*u_id+44*form_id)
                this_talents = []
                if form_id >= 2:
                    this_talents = talent_traits[u_id]
                #now make the map
                (from_traits,to_traits) = trait_randomization_mk3.single_form_trait_randomization(
                    form_traits=cat_traits[u_id][form_id],
                    talent_traits=this_talents,
                    all_traits=all_traits,
                    allowed_traits=allowed_traits,
                    avoid_old_traits=avoid_old_traits,
                    look_order=look_order,
                )
                #slap that thang on
                this_units_map.append([from_traits,to_traits])
            trait_map.append(this_units_map)
        else:
            this_units_map = []
            #get the info required to do this
            look_order = _get_trait_look_order(all_traits,13+300*u_id)
            #now make the map
            (from_traits,to_traits) = trait_randomization_mk3.multiform_trait_randomization(
                form_traits=cat_traits[u_id],
                talent_traits=talent_traits[u_id],
                all_traits=all_traits,
                allowed_traits=allowed_traits,
                avoid_old_traits=avoid_old_traits,
                look_order=look_order,
            )
            #ok since Im doing it so that if the units form is out of the bounds of the array it just calls the last one these can all be just this one size
            this_units_map.append([from_traits,to_traits])
            trait_map.append(this_units_map)
    #now we should be good to just save this map to the cache
    fh.write_file_to_cache(UNIT_TRAIT_MAP_FILE,trait_map,list[list[list[list]]])

def _create_trait_swap_map(trait_swap,config=DEFAULT_CONFIG):
    """ just makes the swap have an entry for each unit and saves map to file """
    (cat_stats,talent_stats) = _get_stats_and_talents_to_use_in_map_creation(True,config) #it doesnt really matter Im just using this to get the length
    trait_map = [trait_swap]*len(cat_stats)
    fh.write_file_to_cache(UNIT_TRAIT_MAP_FILE,trait_map,list[list[list[list]]])
    
def _apply_map_to_stats(stats:list[list[list]]) -> list[list[list]]:
    """ pulls the map from cache and uses it to change the traits of stats """
    trait_map = fh.read_cached_file(UNIT_TRAIT_MAP_FILE,type=list[list[list[list]]])
    before = copy.deepcopy(stats)
    after = copy.deepcopy(stats)
    #first step is removing all traits from after
    for u_id in range(0,len(after)):
        for form in range(0,len(after[u_id])):
            for trait in c.t:
                after[u_id][form][trait] = 0
    #now for each trait in before add the corresponding trait in after
    for u_id in range(0,len(trait_map)):
        for form in range(0,len(after[u_id])):
            #first get the map form
            map_form = form
            if map_form >= len(trait_map[u_id]):
                map_form = len(trait_map[u_id]) - 1 #set it to the last used form if current form is out of index
            for index in range(0,len(trait_map[map_form])):
                if before[u_id][form][trait_map[u_id][map_form][0][index]] == 1:
                    after[u_id][form][trait_map[u_id][map_form][1][index]] = 1
    return after










