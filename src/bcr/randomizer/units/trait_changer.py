import tadbcmc.data.enums.cats as c
import tadbcmc.core.seeded_randomization as srand
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn

import tadbcmc.core.file_handler as fh
from ...config.defaults import DEFAULT_CONFIG
import copy
from ..units import trait_randomization_mk3
from ...config.version_config import version_config_keys as vck
from ..units import balancing
from ...config.version_config.get_version_config import DEFAULT_VC_CONFIG
import tadbcmc.core.simple_funcs as simp



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


def change_traits_according_to_config(stats,config=DEFAULT_CONFIG,version_config=DEFAULT_VC_CONFIG,log=None):
    """ changes traits according to the method desired in config """
    change_means = config["trait"]["unit"]["randomize"]["randomization_mode"].lower()
    if change_means == "none":
        return stats #theres just no sense in it dab
    per_form = config["trait"]["unit"]["randomize"]["per_form"]
    avoid_old_traits = config["trait"]["unit"]["randomize"]["avoid_old_traits"]
    if change_means == "randomize":
        _create_randomization_trait_map(
            per_form=per_form,
            avoid_old_traits=avoid_old_traits,
            all_traits=TRAITS, #when they add another trait this may need to be changed
            allowed_traits=TRAITS, #INCORRECT
            config=config,
            version_config=version_config,
            )
    elif change_means == "swap":
        #THIS NEEDS TRAIT SWAP MAP ALREADY MADE, I dont care rn
        _create_trait_swap_map()
    else:
        print("unit randomization mode set to an uninterpretable: " + str(change_means))
        if log:
            log("unit randomization mode set to an uninterpretable: " + str(change_means))
        return stats #what went wrong here
    #now apply the map
    stats = _apply_map_to_stats(stats)
    _apply_map_to_talents()
    return stats











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
    #first get the ones from the sum
    talent_sum = talent_array[c.tpos.trait_sum]
    talent_traits_has = _get_traits_from_traitsum(talent_sum)
    for talent_block_id in range(2,len(talent_array)):
        this_block = talent_array[talent_block_id]
        if this_block[c.tpos.ability_id] in TALENT_TRAITS:
            trait = this_block[c.tpos.ability_id]
            index = TALENT_TRAITS.index(trait)
            talent_traits_has.append(TRAITS[index])
    return talent_traits_has

def _get_units_traits(unit_array:list[list[int]]) -> list[list[int]]:
    """ gets the traits a unit has on each form """
    this_unit = []
    for form_id in range(0,len(unit_array)):
        this_form = []
        for trait in TRAITS:
            if unit_array[form_id][trait] == 1:
                this_form.append(trait)
        this_unit.append(this_form)
    return this_unit
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


#THIS MIGHT NEED AN EDITED VERSION CONFIG DONE IN REBALANCE
def _get_stats_and_talents_to_use_in_map_creation(per_form:bool,config=DEFAULT_CONFIG,version_config:dict=DEFAULT_VC_CONFIG) -> tuple[list[list[list]],list[list]]:
    """ gets the stats to use in creating the map by removing the information that would change it after the specified version """
    #I dont feel like figuring out how the fuck Im gonna do this rn nor do I even have the relevant initial cstat array to do it
    #however, if its per form theres no reason to remove any cats stats
    # if its per whole unit then cat stats added afterwards should be removed
    # always talents added afterwards should be removed


    #first step, get the correct initial cat array
    cat_stats = balancing.early_rebalance(config)
    #if per form remove extra forms from cat stats, else it doesnt need editing
    if per_form:
        for u_id in range(0,len(version_config[vck.unit_trait_rand_forms])):
            while len(cat_stats[u_id]) > version_config[vck.unit_trait_rand_forms][u_id]: #if there are more forms than there are supposed to be remove them
                cat_stats[u_id].pop()

    #now edit talents
    #I think literally all talents afterwards shouldnt be considered
    vc_talent_ids = version_config[vck.unit_trait_rand_talents]
    talents = gf.get_talents() #this should be the current talents right? (actually I kill everything that isnt a vanilla talent so idk)
    for line in talents:
        current_u_id = line[c.tpos.unit_id]
        
        if current_u_id < len(vc_talent_ids): #this should not do anything to talents if the unit wasnt in the locked version

            #should be fine to just set all the trait sums to whatever they were in config
            if vc_talent_ids[current_u_id][0] != -1: #-1 is what it sets the traitsum to if there were no talents
                line[c.tpos.trait_sum] = vc_talent_ids[current_u_id][0]
            else: line[c.tpos.trait_sum] = 0 #just make it no traits

            #now do actual talents
            #first get all the talent ids by just ignoring the traitsum
            this_talent_ids = copy.deepcopy(vc_talent_ids[current_u_id])
            this_talent_ids.pop(0)
            #now we remove all talents not originally in the array, (this does mean talents added in early rebalance, such as paladin, are not considered, how do I fix this? do I need to? it could also impact things I add in the future like monthly talents, but Im not sure I care)
            
            current_talent_pos = 2
            while current_talent_pos < len(line):
                if line[current_talent_pos][c.tpos.ability_id] not in this_talent_ids:
                    line.pop(current_talent_pos)
                else:
                    current_talent_pos += 1
    #that should be everything right?
    return (cat_stats,talents)





def _create_randomization_trait_map(per_form,avoid_old_traits,all_traits,allowed_traits,config=DEFAULT_CONFIG,version_config:dict=DEFAULT_VC_CONFIG):
    """ creates the trait map to be used elsewhere, saves it to cache """
    trait_map = []
    (cat_stats,talent_stats) = _get_stats_and_talents_to_use_in_map_creation(per_form,config=config,version_config=version_config)
    #now get the form traits and talent traits arrays for all units
    cat_traits = []
    talent_traits = []
    for u_id in range(0,len(cat_stats)):
        this_base_traits = _get_units_traits(cat_stats[u_id])
        #print(this_base_traits)
        if u_id < len(talent_stats): this_talent_traits = _get_trait_from_talents(talent_stats[u_id])
        else: this_talent_traits = []
        #theres no reason to edit them right?
        cat_traits.append(this_base_traits)
        talent_traits.append(this_talent_traits)
    #now we just create the trait map one by one
    for u_id in range(0,len(cat_traits)):
        if per_form:
            this_units_map = []
            for form_id in range(0,len(cat_traits[u_id])):
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

def _apply_map_to_talents():
    """ applies the trait map saved in cache to talents and saves them to file """
    trait_map = fh.read_cached_file(UNIT_TRAIT_MAP_FILE,type=list[list[list[list]]])
    talents = gf.get_talents()
    
    #
    for line in talents:
        unit_id = line[c.tpos.unit_id]
        #first get the trait map to use for talents, 3rd form or last in the list
        if len(trait_map[unit_id]) > 2: this_trait_map = trait_map[unit_id][2]
        else: this_trait_map = trait_map[unit_id][-1]
        #first take care of the trait sum
        traits_in_sum = _get_traits_from_traitsum(line[c.tpos.trait_sum])
        new_trait_sum = 0
        for trait in traits_in_sum:
            #first get its new trait
            pos_in_map = this_trait_map[0].index(trait)
            new_trait = this_trait_map[1][pos_in_map]
            #now get the position in traits
            pos_in_traits = TRAITS.index(new_trait)
            #now add that positions value in traitsum to the sum
            new_trait_sum += TALENT_SUMS[pos_in_traits]
        line[c.tpos.trait_sum] = new_trait_sum
        #now take care of all the actual talent ids
        for block in range(2,len(line)):
            this_ability_id = line[block][c.tpos.ability_id]
            if this_ability_id in TALENT_TRAITS:
                pos_in_traits = TALENT_TRAITS.index(this_ability_id)
                old_trait = TRAITS[pos_in_traits]
                pos_in_map = this_trait_map[0].index(old_trait)
                new_trait = this_trait_map[1][pos_in_map]
                new_pos_in_traits = TRAITS.index(new_trait)
                new_ability_id = TALENT_TRAITS[new_pos_in_traits]
                line[block][c.tpos.ability_id] = new_ability_id
    #all good?
    gf.write_talents(talents)

def _get_traits_from_traitsum(traitsum:int) -> list[int]:
    """ returns the talents in a trait sum """
    output = []
    for x in range(0,len(TALENT_SUMS)):
        if (traitsum%(2*TALENT_SUMS[x])) >= (TALENT_SUMS[x]):
            output.append(TRAITS[x])
    return output






