
import tadbcmc.data.enums.cats as c
import copy

"""the start of both multiform algos:
if len(allowed_traits) == 1
    map every trait to that trait and return
log what traits a unit has on each form
    if a trait has all but one or all traits count this as 0 traits
        if it is specifically all but white make a note of such
get ALL - traits a unit has across all forms including talents
get ALLBASE - traits a unit has across all forms (not including talents)
get PERSIST - traits a unit has that persist across all forms (including talents only on third form)

define the base arrays from_traits and to_traits
if target all but white:
    choose the first non white allowed trait in look order to set from[white] to[that trait] and remove that trait from further allowed traits
"""

"""simple algo for avoid old traits:

if len(ALL) <= half len(allowed_traits) - set each in ALLBASE to one in allowed not in ALL
if len(ALLBASE) <= half len(allowed_traits) - set each in ALLBASE to one in allowed not in ALLBASE
if len(PERSIST) <= half len(allowed_traits) - set each in PERSIST to one in allowed not in PERSIST

for all remaining traits a unit has
    map each to an allowed unused nonself trait till there are none left
        #here is where mapping across forms would go but idc
for all remaining traits
    map each to an allowed nonself trait

"""

"""simple algo for not avoiding old traits:

if len(ALL) <= len(allowed_traits) - place each allowed trait into to_traits in look order, place all traits in both allowed and ALL to the right of their position in to_traits, then place all remaining ones (remove those allowed traits that never get an equivalent to trait)
if len(ALLBASE) <= len(allowed_traits) - do the above but only with the base traits of a unit
if len(PERSIST) <= len(allowed_traits) - do the above but only with the persistant traits of a unit

for all remaining traits a unit has, attempt to match each with an unused nonself allowed trait
for all remaining traits, match with a nonself allowed trait

"""

"""simple algo for single form:
get the info:
    ALL - all traits including talents
    ALLBASE - all traits not including talents
    except_white - whether or not it targets all but white

if avoid old
    do <= half length: half_map like in avoid old multiform
else:
    do <= length: early_placement like in not avoid old multiform

for all remaining traits the unit has attempt to match each with an unused non self allowed trait like in multiform
for all remaining traits match with a nonself allowed trait

"""



def _handle_one_allowed_trait(allowed_traits:list,all_traits:list) -> tuple[list,list]:
    """ return (from_traits,to_traits)
    \n maps every trait to that one trait """
    from_traits = copy.deepcopy(all_traits)
    to_traits = [allowed_traits[0]]*len(from_traits)
    return (from_traits,to_traits)

def _multiform_initialize_information(form_traits,talent_traits,all_traits):
    """ return (ALL,ALLBASE,PERSISTANT,except_white)
    \n creates the initial variables for multiform trait randomization """
    base_form_traits = []
    total_form_traits = []
    except_white = False
    for form in range(0,len(form_traits)):
        this_form = []
        for trait in all_traits:
            if trait in form_traits[form]:
                this_form.append(trait)
        base_form_traits.append(copy.deepcopy(this_form)) #fuck you python
        if form >= 2:
            for trait in all_traits:
                if trait in talent_traits and trait not in this_form:
                    this_form.append(trait)
        total_form_traits.append(copy.deepcopy(this_form))
        #now do all traits check
        if len(total_form_traits[form]) >= len(all_traits)-1: #this means if a unit gets all but white from talents it actually just ignores base traits lmao
            if int(c.t.white) not in total_form_traits[form]:
                except_white = True
            #kill both
            base_form_traits[form] = []
            total_form_traits[form] = []
    ALL = []
    ALLBASE = []
    PERSISTANT = []
    for trait in all_traits:
        count = 0
        for form in range(0,len(base_form_traits)):
            if trait in base_form_traits[form] and trait not in ALLBASE:
                ALLBASE.append(trait)
                if form < 2:
                    count += 1
            if trait in total_form_traits[form] and trait not in ALL:
                ALL.append(trait)
                if form == 2:
                    count += 1
        if count > 1:
            PERSISTANT.append(trait)
    
    return (ALL,ALLBASE,PERSISTANT,except_white)

def _multiform_white_exception(
        from_traits:list,
        to_traits:list,
        allowed_traits:list,
        look_order:list,
        except_white:bool,
    ):
    """ return (from_traits,to_traits,allowed_traits)
    \n adds white to from and an allowed non white trait to to if except white """
    allowed_traits = copy.deepcopy(allowed_traits) #this is required to stop it from editing outside this function
    #this should do nothing if its not except white
    if except_white:
        for trait in look_order:
            if trait in allowed_traits and trait != int(c.t.white):
                from_traits.append(int(c.t.white))
                to_traits.append(trait)
                allowed_traits.remove(trait)
                break
    return (from_traits,to_traits,allowed_traits)

def _multiform_av_half_map(
        from_traits:list,
        to_traits:list,
        traits_to_map:list,
        allowed_traits:list,
        priority_traits:list,
        look_order:list
    ):
    """ return (from_traits,to_traits)
    \n maps traits from the specified half (or less) to the other half, traits marked as priority are mapped to first
    \n does not do duplicates """
    #remove all the ones in the traits to map that shouldnt be
    for trait in from_traits:
        if trait in traits_to_map:
            traits_to_map.remove(trait)
    #now get the other half
    other_half = []
    for trait in allowed_traits:
        if trait not in traits_to_map and trait not in to_traits:
            other_half.append(trait)
    #first do the priority ones
    queue_to_remove = []
    for trait in traits_to_map:
        found = False
        for new_trait in look_order:
            if not found and new_trait in other_half and new_trait in priority_traits and new_trait != trait:
                found = True
                queue_to_remove.append(trait)
                from_traits.append(trait)
                to_traits.append(new_trait)
                priority_traits.remove(new_trait)
                other_half.remove(new_trait)
    for trait in queue_to_remove:
        traits_to_map.remove(trait)
    #now do the others
    for trait in traits_to_map:
        found = False
        for new_trait in look_order:
            if not found and new_trait in other_half and new_trait != trait:
                found = True
                from_traits.append(trait)
                to_traits.append(new_trait)
                other_half.remove(new_trait)
    return (from_traits,to_traits)

def _multiform_map_traits_to_unused_allowed(
        from_traits:list,
        to_traits:list,
        traits_to_map:list,
        allowed_traits:list,
        look_order:list,
        ):
    """ return (from_traits,to_traits)
    \n maps input traits onto allowed traits not yet used """
    #first get unused allowed traits
    unused_allowed = []
    for trait in allowed_traits:
        if trait not in to_traits:
            unused_allowed.append(trait)
    #now make sure those in both unused_allowed and traits_to_map are at the front of traits_to_map
    for x in range(0,len(traits_to_map)):
        if traits_to_map[x] in unused_allowed:
            traits_to_map.insert(0,traits_to_map.pop(x))
    #now do them until one array runs out
    for trait in traits_to_map:
        found = False
        for new_trait in look_order:
            if not found and new_trait != trait and new_trait in unused_allowed:
                found = True
                from_traits.append(trait)
                to_traits.append(new_trait)
                unused_allowed.remove(new_trait)
    return (from_traits,to_traits)

def _map_all_unmapped_traits(
        from_traits:list,
        to_traits:list,
        allowed_traits:list,
        all_traits:list,
        look_order:list,
    ):
    """ return (from_traits,to_traits)
    \n maps all remaining not mapped traits """
    #start by getting whats missing from both
    missing_to = []
    missing_from = []
    for trait in allowed_traits:
        if trait not in to_traits:
            missing_to.append(trait)
    for trait in all_traits:
        if trait not in from_traits:
            missing_from.append(trait)
    #now order missing from with the duplicates at the front
    for x in range(0,len(missing_from)):
        if missing_from[x] in missing_to:
            missing_from.insert(0,missing_from.pop(x))
    #now add until one of the two runs out
    queue_to_remove = []
    for trait in missing_from:
        found = False
        for new_trait in look_order:
            if not found and new_trait != trait and new_trait in missing_to:
                found = True
                from_traits.append(trait)
                queue_to_remove.append(trait)
                to_traits.append(new_trait)
                missing_to.remove(new_trait)
    for trait in queue_to_remove:
        missing_from.remove(trait)
    #now while loop allowed traits to fill out the remaining missing_from traits
    current_pos = -1
    while len(missing_from) > 0:
        loop_count = 0
        current_trait = missing_from[0]
        while True:
            current_pos = (current_pos + 1) % len(look_order)
            loop_count += 1
            if look_order[current_pos] in allowed_traits and look_order[current_pos] != current_trait:
                from_traits.append(current_trait)
                to_traits.append(look_order[current_pos])
                missing_from.remove(current_trait)
                break
            elif loop_count > 12:
                #if it gets this far just set it equal to self something mustve gone wrong
                from_traits.append(current_trait)
                to_traits.append(current_trait)
                missing_from.remove(current_trait)
                print("forced to set a trait to self, this should not happen")
                break
    return (from_traits,to_traits)

def _multiform_not_av_early_placement(
        from_traits:list,
        to_traits:list,
        traits_to_map:list,
        allowed_traits:list,
        look_order:list,
    ):
    """ return (from_traits,to_traits) """
    #divide them into duplicates and not
    dupes = []
    not_dupes = []
    for trait in traits_to_map:
        if trait in allowed_traits:
            dupes.append(trait)
        else:
            not_dupes.append(trait)
    #now get the to and from arrays
    new_to = []
    for trait in look_order:
        if trait in allowed_traits:
            new_to.append(trait)
    new_from = [None]*len(new_to)
    #now place each dupe one to the right of its location in allowed traits
    for trait in dupes:
        index = new_to.index(trait)
        new_from[(index+1)%len(new_to)] = trait
    #now place all remaining traits
    for trait in not_dupes:
        index = new_from.index(-1)
        new_from[index] = trait
    #now remove all the entries that didnt get filled
    current_pos = -1
    while current_pos < len(new_from):
        if new_from[current_pos] == None:
            new_from.pop(current_pos)
            new_to.pop(current_pos)
        else: current_pos += 1
    #now attach the new info
    from_traits = from_traits + new_from
    to_traits = to_traits + new_to
    return (from_traits,to_traits)

def _single_form_initialize_information(
        form_traits:list,
        talent_traits:list,
        all_traits:list,
    ):
    """ return (ALL,ALLBASE,except_white)
    \n gets the info ALL, ALLBASE and except_white from the trait arrays
    \n if all is one less or equal to all_traits they are considered as no traits """
    ALL = []
    ALLBASE = []
    for trait in all_traits:
        if trait in form_traits:
            ALL.append(trait)
            ALLBASE.append(trait)
        if trait in talent_traits and trait not in ALL:
            ALL.append(trait)
    #now take care of white
    except_white = False
    if len(ALL) >= len(all_traits)-1:
        if int(c.t.white) not in ALL:
            except_white = True
        ALL = []
        ALLBASE = [] #yeah this kills things which get all traits resulting from talent despite having traits without them, I dont care
    #good to return
    return (ALL,ALLBASE,except_white)

#NOTE doing it this way prevents me from makng it so that traits map to other forms in the future, I do not know if I intend to do that tho
def _form_independent_first_placement(
        from_traits:list,
        to_traits:list,
        ALL:list,
        ALLBASE:list,
        PERSISTANT:list,
        all_traits:list,
        allowed_traits:list,
        avoid_old_traits:bool,
        look_order:list,
    ):
    """ return (from_traits,to_traits)
    \n does either half map or early placement depending on whether or not its avoid old trait """
    #now diverge into avoid or not
    if avoid_old_traits:
        do_half_map = True
        #set preferred traits to those not in all
        prefered = []
        for trait in all_traits: #it looks fine to use all traits and not allowed traits for this as it checks if a trait is allowed or not when applying it
            if trait not in ALL:
                prefered.append(trait)
        #choose the largest grouping not more than half the length of allowed to map to
        if len(ALL) > 0 and len(ALL) <= len(allowed_traits)/2:
            half_mappers = copy.deepcopy(ALL)
        elif len(ALLBASE) > 0 and len(ALLBASE) <= len(allowed_traits)/2:
            half_mappers = copy.deepcopy(ALLBASE)
        elif len(PERSISTANT) > 0 and len(PERSISTANT) <= len(allowed_traits)/2:
            half_mappers = copy.deepcopy(PERSISTANT)
            prefered = []
            for trait in all_traits:
                if trait not in ALLBASE: #is it true that talents should be in preferred?
                    prefered.append(trait)
        else:
            do_half_map = False
        #if any of those groups checked then do it
        if do_half_map:
            (from_traits,to_traits) = _multiform_av_half_map(from_traits,to_traits,half_mappers,allowed_traits,prefered,look_order)
        #theres nothing unique to avoid old traits after this
    else:
        #choose the largest group not bigger than allowed traits to place with first
        do_early_placement = True
        if len(ALL) > 0 and len(ALL) <= len(allowed_traits):
            early_placers = copy.deepcopy(ALL)
        elif len(ALLBASE) > 0 and len(ALLBASE) <= len(allowed_traits):
            early_placers = copy.deepcopy(ALLBASE)
        elif len(PERSISTANT) > 0 and len(PERSISTANT) <= len(allowed_traits):
            early_placers = copy.deepcopy(PERSISTANT)
        else:
            do_early_placement = False
        #if any work do it
        if do_early_placement:
            (from_traits,to_traits) = _multiform_not_av_early_placement(from_traits,to_traits,early_placers,allowed_traits,look_order)
    return (from_traits,to_traits)



def single_form_trait_randomization(
        form_traits:list,
        talent_traits:list,
        all_traits:list,
        allowed_traits:list,
        avoid_old_traits:bool,
        look_order:list,
    ) -> tuple[list[int],list[int]]:
    """ return (from_traits,to_traits)
    \n makes a map utilizing the info in the form traits and talent traits
    \n input must be process into the traits a unit has at base and as talents """
    #dumb exception
    if len(allowed_traits) == 1:
        return _handle_one_allowed_trait(allowed_traits,all_traits)
    #now get the initial info
    (ALL,ALLBASE,except_white) = _single_form_initialize_information(form_traits,talent_traits,all_traits)
    #now make the from and to arrays
    from_traits = []
    to_traits = []
    #white (multiform works for this)
    (from_traits,to_traits,allowed_traits) = _multiform_white_exception(from_traits,to_traits,allowed_traits,look_order,except_white)
    #now do the function for the first initial large post white placement
    (from_traits,to_traits) = _form_independent_first_placement(from_traits,to_traits,ALL,ALLBASE,[],all_traits,allowed_traits,avoid_old_traits,look_order)
    #now do all traits that have yet to be mapped, starting with placing them on unused allowed traits
    still_needs_mapping = []
    for trait in ALL:
        if trait not in from_traits:
            still_needs_mapping.append(trait)
    (from_traits,to_traits) = _multiform_map_traits_to_unused_allowed(from_traits,to_traits,still_needs_mapping,allowed_traits,look_order)
    #now do all missing from from
    (from_traits,to_traits) = _map_all_unmapped_traits(from_traits,to_traits,allowed_traits,all_traits,look_order)
    #that should be the entire map
    return (from_traits,to_traits)




    

def multiform_trait_randomization(
        form_traits:list[list],
        talent_traits:list,
        all_traits:list,
        allowed_traits:list,
        avoid_old_traits:bool,
        look_order:list
    ) -> tuple[list[int],list[int]]:
    """ return (from_traits,to_traits)
    \n makes a map across multiple forms utilizing the info in form traits and talent traits 
    \n input must be processed into a list of lists of traits a unit has on each form and a list of talent traits
    \n make new forms/talents not change map by just setting the arrays to not include those forms/talents """
    #this stupid exception
    if len(allowed_traits) == 1:
        return _handle_one_allowed_trait(allowed_traits,all_traits)
    #now get initial information
    (ALL,ALLBASE,PERSISTANT,except_white) = _multiform_initialize_information(form_traits,talent_traits,all_traits)
    #now make from_traits and to_traits
    from_traits = []
    to_traits = []
    #white
    (from_traits,to_traits,allowed_traits) = _multiform_white_exception(from_traits,to_traits,allowed_traits,look_order,except_white)
    #now do the function for the initial post white large scale placement
    (from_traits,to_traits) = _form_independent_first_placement(from_traits,to_traits,ALL,ALLBASE,PERSISTANT,all_traits,allowed_traits,avoid_old_traits,look_order)
    #now do all traits that have yet to be mapped, starting with placing them on unused allowed traits
    still_needs_mapping = []
    for trait in ALL:
        if trait not in from_traits:
            still_needs_mapping.append(trait)
    (from_traits,to_traits) = _multiform_map_traits_to_unused_allowed(from_traits,to_traits,still_needs_mapping,allowed_traits,look_order)
    #now do all missing from from
    (from_traits,to_traits) = _map_all_unmapped_traits(from_traits,to_traits,allowed_traits,all_traits,look_order)
    #that should be the entire map
    return (from_traits,to_traits)







