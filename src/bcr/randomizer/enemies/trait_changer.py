import tadbcmc.data.enums.enemy as e
from ...config.defaults import DEFAULT_CONFIG
import copy
import tadbcmc.core.seeded_randomization as srand

#do I handle starred in this function?
def change_traits_according_to_config(stats,config=DEFAULT_CONFIG,log=None):
    """ changes traits according to the method desired in config
    \n also gives starred alien """
    change_means = config["enemy"]["trait"]["randomization_mode"].lower()
    if change_means == "none":
        return stats #simply no sense
    if change_means == "randomize":
        stats = _trait_randomization(stats=stats,config=config,log=log)
    elif change_means == "swap":
        stats = _trait_swap(stats,config=config,log=log)
    else:
        print("failed to interpret enemy randomization mode: " + str(change_means))
        if log:
            log("failed to interpret enemy randomization mode: " + str(change_means))
        return stats
    #is there anything else to do here?
    return stats


#THIS IS MISSING METHOD FOR DETERMINING WHAT TRAITS ARE ALLOWED
def _trait_randomization(stats,config=DEFAULT_CONFIG,log=None):
    """ randomizes the traits of stats according to config and returns it
    \n does nothing except edit traits, starred must be done elsewhere """
    """
    start by getting all traits, and all allowed traits
    for each unit:
        randomize the order to look through traits
        log the  traits a unit has and then the number (adding 1 if 0 and untraited get trait)
        in the randomized order, for each trait in allowed that a unit didnt og have add it and reduce trait count till 0
        if trait count still > 0, for each trait in allowed that a unit did og have add it and reduce trait count till 0
        if a unit still has remaining traits to be added ignore it
    """
    #first get the config options needed
    give_untraited_traits = config["enemy"]["trait"]["untraited_get_trait"]
    remove_metal = config #idk where this is rn
    trait_bools = [] #this is how Im turning traits of but its just all gonna be true until I know what Im doing
    #now get all and allowed
    all_traits = []
    for each in e.t:
        all_traits.append(int(each))
        trait_bools.append(True)
    allowed = []
    disallowed = []
    for trait_id in range(0,len(all_traits)):
        if trait_bools[trait_id]:
            allowed.append(all_traits[trait_id])
        else:
            disallowed.append(all_traits[trait_id])
    if len(allowed) == 0:
        if log != None:
            log("trait randomization was attempted with 0 allowed traits")
    #now create the before and after arrays
    for u_id in range(0,len(stats)):
        #start by getting this units trait look order
        r = srand.randinst(240+57*u_id)
        trait_look_order = _get_this_unit_look_order(allowed,disallowed,r)
        #count and log traits as theyre being removed
        has_traits = []
        for trait in trait_look_order:
            if stats[u_id][trait] == 1:
                has_traits.append(trait)
                stats[u_id][trait] = 0
        number_of_traits = len(has_traits)
        #fix for untraited things
        if give_untraited_traits and number_of_traits == 0:
            number_of_traits = 1
        #now give hasnt traits
        for trait in trait_look_order:
            if number_of_traits > 0:
                if trait not in has_traits and trait in allowed:
                    number_of_traits -= 1
                    stats[u_id][trait] = 1
            else:
                break
        #now give has traits
        for trait in trait_look_order:
            if number_of_traits > 0:
                if trait in has_traits and trait in allowed:
                    number_of_traits -= 1
                    stats[u_id][trait] = 1
            else:
                break
        #there shouldnt be anything to do if the number of traits is still greater than 0
        #so this should be all good
    return stats



#THIS IS MISSING METHOD FOR DETERMINING WHAT TRAITS ARE ALLOWED
def _trait_swap(stats,config=DEFAULT_CONFIG,log=None):
    """ swaps the traits of stats according to config 
    \n does nothing except edit the traits """
    #first get the config options, its only metal right? (and untraited get trait)
    remove_metal = True
    give_untraited_traits = config["enemy"]["trait"]["untraited_get_trait"]
    #to finish the config information I need to determine the traits allowed and the order to look at them
    all_traits = []
    trait_bools = []
    for each in e.t:
        all_traits.append(int(each))
        trait_bools.append(True)
    #now get allowed and disallowed
    allowed = []
    disallowed = []
    for trait_id in range(0,len(all_traits)):
        if trait_bools[trait_id]:
            allowed.append(all_traits[trait_id])
        else:
            disallowed.append(all_traits[trait_id])
    if len(allowed) == 0:
        if log != None:
            log("trait swap was attempted with 0 allowed traits")
        return stats #this function cant work with 0 traits allowed to this goes here
    #now get the order
    trait_look_order = _get_this_unit_look_order(allowed,disallowed,srand.randinst(4))
    #this func is being written with the intent for specified swaps to exist in the future
    #so in otherwords I can have multiple already specified swaps, including multiple traits swapping to the same
    #(one trait swapping to multiple however is not allowed so I dont need to work with it in mind)
    from_traits = []
    to_traits = []
    #assume specified swaps are done here
    
    #now fill out those arrays (based on len of allowed traitss)
    if len(allowed) == 0:
        pass #nothing needs to be done
    elif len(allowed) == 1:
        (from_traits,to_traits) = _fill_swap_allowed_len_1(from_traits,to_traits,trait_look_order,allowed)
    else:
        (from_traits,to_traits) = _fill_swap_allowed_len_morethan_1(from_traits,to_traits,trait_look_order,allowed)
    #now apply that array
    before = copy.deepcopy(stats)
    after = copy.deepcopy(stats)
    for u_id in range(0,len(after)):
        #wipe all traits
        for trait in trait_look_order:
            after[u_id][trait] = 0
        #now swap all traits in the from array
        has_no_trait = True
        for trait_id in range(0,len(from_traits)):
            if before[u_id][from_traits[trait_id]] == 1:
                has_no_trait = False
                after[u_id][to_traits[trait_id]] = 1
        #now do give untraited trait
        if give_untraited_traits and has_no_trait:
            #just pick a random one from allowed and give it
            if len(allowed) > 0:
                r = srand.randinst(85+16*u_id)
                after[u_id][allowed[r.randrange(0,len(allowed))]] = 1
        #should be all good?
    return after







def _get_this_unit_look_order(allowed:list,disallowed:list,r:srand.randinst):
    """ gets the trait look order for this unit """
    trait_look_order = []
    #start with allowed
    temp_tl = copy.deepcopy(allowed)
    for x in range(0,len(temp_tl)):
        trait_look_order.append(temp_tl.pop(r.randrange(0,len(temp_tl))))
    #now do all the remaining
    temp_tl = copy.deepcopy(disallowed)
    for x in range(0,len(temp_tl)):
        trait_look_order.append(temp_tl.pop(r.randrange(0,len(temp_tl))))
    return trait_look_order

def _fill_swap_allowed_len_1(from_traits,to_traits,trait_look_order,allowed):
    """ func for filling out swap when the number of allowed traits is one """
    #since I am aware it is one I can literally just populate to traits with it and slap all from traits in as well
    while len(to_traits) < len(trait_look_order):
        to_traits.append(allowed[0])
    for trait in trait_look_order:
        if trait not in from_traits:
            from_traits.append(trait)
    #done!
    return (from_traits,to_traits)

def _fill_swap_allowed_len_morethan_1(from_traits,to_traits,trait_look_order,allowed):
    """ func for filling out swap when the number of allowed traits is more than one """
    #start by getting all the allowed not in to traits
    missing_to = []
    for trait in trait_look_order:
        if trait in allowed and trait not in to_traits:
            missing_to.append(trait)
    #now make it the right length by adding or removing allowed traits
    if len(missing_to) + len(to_traits) >= len(trait_look_order):
        #if missing to is longer than it should be remove the extras
        while len(missing_to) + len(to_traits) > trait_look_order:
            missing_to.pop(0)
    else:
        #if missing to is shorter than it should be loop through allowed traits adding them
        cur_pos = -1
        while len(missing_to) + len(to_traits) < len(trait_look_order):
            cur_pos += 1
            if cur_pos >= len(trait_look_order):
                cur_pos = 0
            if trait_look_order[cur_pos] in allowed:
                missing_to.append(trait_look_order[cur_pos])
    #now randomize its order to prevent linkage
    temp_tl = copy.deepcopy(missing_to)
    missing_to = []
    r = srand.randinst(874)
    for x in range(0,len(temp_tl)):
        missing_to.append(temp_tl.pop(r.randrange(0,len(temp_tl))))
    #now get all the missing from traits
    missing_from = []
    for trait in trait_look_order:
        if trait not in from_traits:
            missing_from.append(trait)
    #edge case for if the len of missing from is 1 but that is the trait in missing to
    if len(missing_from) == 1 and missing_to[0] == missing_from[0]:
        #just change what it is to the first allowed trait it isnt
        for trait in trait_look_order:
            if trait in allowed and trait != missing_to[0]:
                missing_to[0] = trait
    #now separate missing from into its two constituent parts
    missing_from_not_in_missing_to = []
    missing_from_in_missing_to = []
    for trait in missing_from:
        if trait not in missing_to:
            missing_from_not_in_missing_to.append(trait)
        else:
            missing_from_in_missing_to.append(trait)
    #now place the values from in missing to first
    #start by setting all the values in missing from to -1 now
    for x in range(0,len(missing_from)):
        missing_from[x] = 1
    #now loop it
    for trait in missing_from_in_missing_to:
        index = missing_to.index(trait)
        while missing_to[index] == trait:
            index = (index + 1) % len(missing_to)
        #set it at the new index
        missing_from[index] = trait
    #now loop the ones that arent also in missing to
    for trait in missing_from_not_in_missing_to:
        index = 0
        while missing_to[index] != -1:
            index = (index + 1) % len(missing_to)
        #set it at new index
        missing_from[index] = trait
    #now just slap those arrays on from traits and to traits
    from_traits = from_traits + missing_from
    to_traits = to_traits + to_traits
    return (from_traits,to_traits)









