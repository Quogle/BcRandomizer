""" module exclusively for the process of randomizating units traits """
import tadbcmc.data.enums.cats as c
import copy



"""
most ungodly thing ever
"""


def create_trait_map(form_traits:list[list[int]],talent_traits:list[int],this_look_order:list[int],all_traits:list[int],allowed_traits:list[int]) -> list[list[int]]:
    """ creates and then returns the trait map for this unit 
    \n form traits is a list of the list of traits a unit has each form
    \n if unit a form on the unit is new than the randomization is supposed to consider, set that forms traits to empty before passing it 
    \n similarly talents which are new should also be removed before being passed as arguments"""
    allowed_traits = copy.deepcopy(allowed_traits) #fuck python
    #first step is deal with this edge case (allowed traits length 0 is taken care of elsewhere)
    if len(allowed_traits) == 1:
        return _only_one_allowed_trait(allowed_traits,all_traits)
    #now I need to compile the information into the way its treated throughout the rest of the unit randomization
    (base_traits,including_talents,talent_traits,except_white,ALL,ALLBASE) = _create_form_trait_variables(form_traits,talent_traits,all_traits)
    if len(ALL) <= (len(allowed_traits)/2):
        (from_traits,to_traits) = _all_is_fine(ALL,allowed_traits,all_traits,this_look_order,except_white)
    elif len(ALLBASE) <= (len(allowed_traits)/2):
        pass

















def _only_one_allowed_trait(allowed_traits:list[int],all_traits:list[int]) -> list[list[int]]:
    """ creates the map if some fuck wants randomization to only one trait """
    to_traits = [allowed_traits[0]]*len(all_traits)
    return [all_traits,to_traits]

def _create_form_trait_variables(form_traits,talent_traits,all_traits):
    """ creates the actually used variables """
    talent_traits = copy.deepcopy(talent_traits) #fuck python
    base_traits = []
    for x in range(0,len(form_traits)):
        this_tl = []
        for trait in all_traits:
            if trait in form_traits[x]: this_tl.append(trait)
        base_traits.append(this_tl)
    including_talents = []
    for x in range(0,len(form_traits)):
        this_tl = []
        for trait in all_traits:
            if trait in form_traits[x]: this_tl.append(trait)
            elif x >= 2 and trait in talent_traits: this_tl.append(trait)
        including_talents.append(this_tl)
    #now remove any form with 9/10 traits and catalog why
    except_white = False
    for x in range(0,len(including_talents)):
        if len(including_talents[x]) >= 9:
            if len(including_talents[x]) == 9:
                if int(c.t.white) not in including_talents[x]:
                    except_white = True
            #now kill it
            including_talents[x] = []
            base_traits[x] = []
            #I guess this means if something reaches all traits through talents while having traits without talents it just dies?
            #not my fuckin problem tho
    ALL = []
    ALLBASE = []
    for x in range(0,len(base_traits)):
        for trait in base_traits[x]:
            if trait not in ALLBASE: ALLBASE.append(trait)
        for trait in including_talents[x]:
            if trait not in ALL: ALL.append(trait)
    return (base_traits,including_talents,talent_traits,except_white,ALL,ALLBASE)

def _all_is_fine(ALL:list[int],allowed_traits:list[int],all_traits:list[int],look_order:list[int],except_white:bool):
    """ does trait randomization if all is less than half the length of allowed """
    (from_traits,to_traits,allowed_traits) = _fill_first_half(ALL,allowed_traits,except_white=except_white,look_order=look_order)
    (from_traits,to_traits) = _fill_end(from_traits,to_traits,allowed_traits,all_traits,look_order)
    return (from_traits,to_traits)

def _allbase_is_fine(ALLBASE:list[int],allowed_traits:list[int],all_traits:list[int],look_order:list[int],except_white:bool,talent_traits:list[int],form_traits:list[list[int]]) -> tuple[list[int]]:
    """ does trait randomization if the number of all traits is more than half the length of allowed but the number of traits excluding talents is less than half """
    #first step is placing all those base traits
    (from_traits,to_traits,allowed_traits) = _fill_first_half(ALLBASE,allowed_traits,except_white,look_order)
    #now attempt to place talents till out of allowed traits (could also run out of talents here but idc)
    (from_traits,to_traits) = _fill_talents_to_allowed(from_traits,to_traits,allowed_traits,talent_traits,look_order)



def _fill_first_half(has_traits:list[int],allowed_traits:list[int],except_white:bool,look_order:list[int]) -> tuple[list[int]]:
    """ return (from_traits,to_traits,allowed_traits)
    \n creates from/to and fills from with has traits and to with non has allowed traits in look order
    \n if except white will hand that here
    \n returns an equal length from/to thus handling all in has traits and potential white but nothing else """
    from_traits = []
    to_traits = []
    for trait in has_traits:
        from_traits.append(trait)
    #first add the traits from traits doesnt have
    for trait in look_order:
        if trait in allowed_traits and trait not in from_traits:
            to_traits.append(trait)
    #now add the traits it does in allowed
    for trait in look_order:
        if trait in allowed_traits and trait not in to_traits:
            to_traits.append(trait)
    if except_white:
        if int(c.t.white) not in from_traits:
            from_traits.append(int(c.t.white))
        #now remove what white is targetting from allowed traits
        white_index = from_traits.index(int(c.t.white))
        target_trait = to_traits[white_index]
        allowed_traits.remove(target_trait)
    return (from_traits,to_traits,allowed_traits)

def _fill_end(from_traits:list[int],to_traits:list[int],allowed_traits:list[int],all_traits:list[int],look_order:list[int]) -> tuple[list[int]]:
    """ fills out the swaps with the remaing traits to be placed mapping to non self allowed traits
    \n assumes from/to have equal lengths, still works elsewise but could have self mapping """
    added_to_traits = []
    #first try placing all the allowed traits currently unused
    for trait in look_order:
        if trait in allowed_traits and trait not in to_traits:
            added_to_traits.append(trait)
            to_traits.append(trait)
    #now simply fill it in order
    cur_pos = -1
    while len(to_traits) < len(all_traits):
        cur_pos = (cur_pos+1) % len(look_order)
        if look_order[cur_pos] in allowed_traits:
            added_to_traits.append(look_order[cur_pos])
            to_traits.append(look_order[cur_pos])
    #now get the from traits that could be duplicated
    starting_from_length = len(from_traits)
    not_in_from = []
    for trait in all_traits: #or should this be look order
        if trait not in from_traits:
            not_in_from.append(trait)
    possible_dupes = []
    remaining_traits = []
    for trait in not_in_from:
        if trait in added_to_traits:
            possible_dupes.append(trait)
        else:
            remaining_traits.append(trait)
    #now add the dupes first
    from_traits = from_traits + [-1]*(len(to_traits)-starting_from_length)
    for trait in possible_dupes:
        setting_pos = starting_from_length
        #find the first instance of it
        try:
            while to_traits[setting_pos] != trait:
                setting_pos +=1 
            #now add one to that modulusly and set it
            setting_pos += 1
            if setting_pos == len(to_traits):
                setting_pos = starting_from_length
            from_traits[setting_pos] = trait
        except:
            #if trait not found before end of array
            remaining_traits.append(trait)
    #now set the remaining traits to the first instance of -1 found
    for trait in remaining_traits:
        try:
            from_traits[from_traits.index(-1)] = trait
        except:
            pass #guess this traits being left out if something went wrong
    return (from_traits,to_traits)

def _fill_talents_to_allowed(from_traits:list[int],to_traits:list[int],allowed_traits:list[int],talent_traits:list[int],look_order:list[int]) -> tuple[list[int]]:
    """ puts all currently unplaced talent traits into from until one of every allowed trait is in to or all talents placed """
    #first step is getting all the missing allowed traits and missing talent traits
    missing_allowed = []
    missing_talents = []
    for trait in look_order:
        if trait in allowed_traits and trait not in to_traits: missing_allowed.append(trait)
        if trait in talent_traits and trait not in from_traits: missing_talents.append(trait)
    if len(missing_talents) == 0 or len(missing_allowed) == 0: #this is a really stupid check to need to do but whatever
        return (from_traits,to_traits)
    #now deal with duplicates
    duplicates = []
    for trait in missing_talents:
        if trait in missing_allowed: duplicates.append(trait)
    #if its only duplicates theyll have to be linked
    if len(duplicates) == len(missing_talents):
        set_as = copy.deepcopy(duplicates) #just rotate duplicates by one
        set_as.append(set_as.pop(0))
        for trait in duplicates:
            from_traits.append(trait)
        for trait in set_as:
            to_traits.append(trait)
    else:
        #just get all ya can
        for trait in duplicates:
            non_self_missing_alloweds = []
            for this_trait in missing_allowed:
                if this_trait != trait:
                    non_self_missing_alloweds.append(this_trait)
            if len(non_self_missing_alloweds) > 0:
                from_traits.append(trait)
                to_traits.append(non_self_missing_alloweds[0])
                missing_allowed.remove(non_self_missing_alloweds[0])
                missing_talents.remove(trait)
        #now do the same for non duplicate traits
        for trait in missing_talents:
            non_self_missing_alloweds = []
            for this_trait in missing_allowed:
                if this_trait != trait:
                    non_self_missing_alloweds.append(this_trait)
            if len(non_self_missing_alloweds) > 0:
                from_traits.append(trait)
                to_traits.append(non_self_missing_alloweds[0])
                missing_allowed.remove(non_self_missing_alloweds[0])
                missing_talents.remove(trait)
        #technically this can leave one talent trait in extremely rare circumstances
        #I SHOULD LOG THIS
    return (from_traits,to_traits)

def _fill_talents_to_first_second_form_traits(from_traits:list[int],to_traits:list[int],allowed_traits:list[int],talent_traits:list[int],form_traits:list[list[int]],look_order:list[int]) -> tuple[list[int]]:
    """ attempts to place unplaced talents to allowed traits on first and second form but not third/fourth form """
    missing_talents = []
    talent_form_traits = []
    non_talent_form_traits = []
    for trait in look_order:
        if trait in talent_traits and trait not in form_traits: missing_talents.append(trait)
        for x in range(0,len(form_traits)):
            if trait in form_traits[x] and trait in allowed_traits: #only consider the allowed traits for this
                if x < 2:
                    non_talent_form_traits.append(trait)
                else:
                    talent_form_traits.append(trait)
    #now get the ones exclusive to first and second form
    allowed_low_form_traits = []
    for trait in non_talent_form_traits:
        if trait not in talent_form_traits:
            allowed_low_form_traits.append(trait)
    #a trait should never be able to self map here because that implies it is a base trait and all base traits should be set before this function is ever called
    for x in range(0,len(missing_talents)):
        if x < len(allowed_low_form_traits):#this means its only doing the traits where there is at least an entry in both arrays
            from_traits.append(missing_talents[x])
            to_traits.append(allowed_low_form_traits[x])
    #nothing further can be done here
    return (from_traits,to_traits)




