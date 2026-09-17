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


def _get_single_form_map(form_stats:list[int],talent_array:list[int]=[],all_traits:list[int]=TRAITS,allowed_traits:list[int]=[],avoid_old:bool=True,r_offset:int=13):
    """ gets the map for a single form, considers talents if passed """
    #start by getting the look order
    this_look_order = _get_trait_look_order(all_traits,r_offset) #this is not passed TRAITS for if they add a trait in the future
    #now get traits a unit has in various places
    has_base = _get_units_traits(form_stats)
    if talent_array != []: has_talents = _get_trait_from_talents(talent_array)
    else: has_talents = []
    hasnt_traits = []
    for trait in all_traits:
        if trait not in has_base and trait not in has_talents:
            hasnt_traits.append(trait)
    #now append all the traits a unit has to the start of the map
    map_from = []
    for trait in this_look_order: 
        if trait in has_base: map_from.append(trait)
    for trait in this_look_order:
        if trait in has_talents and trait not in has_base: map_from.append(trait)
    #now create map to as a list of same length with no values
    map_to = [None]*len(map_from)
    #start by placing the values from allowed traits that are also in this list into it shifted right by one
    
    

#DOES NOT HAVETARGET ALL EXCEPT WHITE
def _get_single_form_map_avoid_old(form_stats:list[int],talent_array:list[int]=[],all_traits:list[int]=TRAITS,allowed_traits:list[int]=[],r_offset:int=13) -> list[list[int]]:
    """ gets the map for a single form if not avoiding old traits, considers talents if passed """

            
            
def _get_single_form_map(form_stats:list[int],talent_array:list[int]=[],all_traits:list[int]=TRAITS,allowed_traits:list[int]=[],r_offset:int=13,avoid_old:bool=True) -> list[list[int]]:
    """ gets the map for a single form, considers talents if passed to it """
    #start by getting the look order
    this_look_order = _get_trait_look_order(all_traits,r_offset) #this is not passed TRAITS for if they add a trait in the future
    #now get the traits this unit does and doesnt have
    has_base = _get_units_traits(form_stats)
    if talent_array != []: has_talents = _get_trait_from_talents(talent_array)
    else: has_talents = []
    hasnt_traits = []
    for trait in all_traits:
        if trait not in has_base and trait not in has_talents:
            hasnt_traits.append(trait)
    #need to remove extra traits from talent_array if they arent supposed to be considered rn (this is because talent array does not use all_traits it uses TRAITS)
    for trait in TRAITS:
        if trait in has_talents and trait not in all_traits:
            has_talents.remove(trait)
    #now append all the traits a unit has to the start of the map
    map_from = []
    for trait in this_look_order:
        if trait in has_base: map_from.append(trait)
    for trait in this_look_order:
        if trait in has_talents and trait not in map_from: map_from.append(trait)
    #break off here into avoid old and not avoid old
    if avoid_old:
        pass

def _sf_avoid_old_fill_map(map_from:list[int],look_order:list[int],allowed_traits:list[int],has_base:list[int],has_talent:list[int],hasnt:list[int]) -> tuple[list[int],list[int]]:
    """ fills out map_from and map_to priorizing hasnt traits, then talent traits, then base trait """
    map_to = [None]*len(map_from)
    #add the traits a unit doesnt have first
    should_get = []
    for trait in look_order:
        if trait in hasnt and trait in allowed_traits: should_get.append(trait)
    #now check if thats enough to cover map
    if len(should_get) >= len(map_from):
        #fill it with them
        map_to = []
        for x in range(0,len(map_from)):
            map_to.append(should_get[x])
        #is there any sense in doing more right here?
    else:
        #if that isnt enough then try adding talents
        if len(should_get) + len(has_talent) >= len(map_from):
            #do it in look order
            pos_in_look = -1
            get_from_talents = []
            while len(should_get) + len(get_from_talents) < len(map_from):
                pos_in_look = (pos_in_look+1) % len(look_order)
                if look_order[pos_in_look] in has_talent and look_order[pos_in_look] in allowed_traits:
                    get_from_talents.append(look_order[pos_in_look])
            #now now should get is full, what am I doing now?
        else:
            #add all in allowed until it reaches the proper length
            #give priority to those in has talents
            get_from_base = []
            get_from_talents = []
            for trait in look_order:
                if trait in has_talent and trait in allowed_traits:
                    get_from_talents.append(trait)
            for trait in look_order:
                if trait in allowed_traits and trait not in should_get:
                    if len(should_get) + len(get_from_talents) + len(get_from_base) < len(map_from):
                        get_from_base.append(trait)
            
    



def _sf_not_avoid_old_fill_map(map_from:list[int],look_order:list[int],allowed_traits:list[int]) -> tuple[list[int],list[int]]:
    """ fills out a map for avoid old traits by simply adding those allowed traits in look order """
    #start by filling out map from
    for trait in look_order:
        if trait not in map_from:
            map_from.append(trait)
    #now create map_to as the same length as map_from but with allowed traits
    map_to = []
    pos_in_look = -1
    while len(map_to) < len(map_from):
        pos_in_look = (pos_in_look+1) % len(look_order)
        if look_order[pos_in_look] in allowed_traits:
            map_to.append(look_order[pos_in_look])
    return (map_from,map_to)






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

def _order_array_in_look_order(array:list[int],look_order:list[int]) -> list[int]:
    """ takes an array and rearranges it to be in the proper look order """
    output = []
    for trait in look_order:
        if trait in array:
            output.append(trait)
    return output


def _form_randomize_traits(form_stats:list[int],allowed_traits:list[int],r_offset:int,number_intended_traits:int=None,avoid_old:bool=True,talent_array:list=[]) -> list[int]:
    """ randomizes the traits of this specific form, considers talents if passed to it
    \n if requesting a specific number of traits it will make it have that many, else its just how many it naturally has """
    this_look_order = _get_trait_look_order(TRAITS,r_offset=r_offset)
    if number_intended_traits != None:
        trait_number = number_intended_traits
    else:
        trait_number = 0
        for trait in TRAITS:
            if form_stats[trait] == 1:
                trait_number += 1
    #I dont need a map for this since its only this form
    if avoid_old:
        #didnt have at all is highest priority, then had in talents, then has raw
        had_base = _get_units_traits(form_stats)
        has_talents = _get_trait_from_talents(talent_array)
        hadnt = []
        for trait in TRAITS:
            if trait not in had_base and trait not in has_talents:
                hadnt.append(trait)
        #now order those
        had_base = _order_array_in_look_order(had_base,this_look_order)
        has_talents = _order_array_in_look_order(has_talents,this_look_order)
        hadnt = _order_array_in_look_order(hadnt,this_look_order)
        #now in the proper order put only those in allowed into give traits
        give_traits = []
        for trait in hadnt:
            if trait in allowed_traits:
                give_traits.append(trait)
        for trait in has_talents:
            if trait in allowed_traits and trait not in give_traits:
                give_traits.append(trait)
        for trait in had_base:
            if trait in allowed_traits and trait not in give_traits:
                give_traits.append(trait)
    else:
        #this can literally just choose from allowed traits in correct order
        give_traits = []
        for trait in this_look_order:
            if trait in allowed_traits:
                give_traits.append(trait)
    #first kill all traits
    for trait in this_look_order:
        form_stats[trait] = 0
    #now choose from give traits
    for trait in give_traits:
        if trait_number > 0:
            form_stats[trait] = 1
            trait_number -= 1
    #all good
    return form_stats










