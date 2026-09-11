import tadbcmc.data.enums.enemy as e
from ...config.defaults import DEFAULT_CONFIG
import copy
import tadbcmc.core.seeded_randomization as srand






#THIS IS MISSING CONFIG FOR REMOVING METALS
def trait_randomization(stats,config=DEFAULT_CONFIG):
    """ randomizes the traits of stats according to config and returns it
    \n does nothing except edit traits, starred must be done elsewhere """
    """ 
    this works by getting all the traits a unit does and doesnt have and then
    measuring the length of has traits to get how many it should have after its all done
    then it recombines hasnt and has traits with hasnt in fronts
    and loops through that array adding traits until the number of traits it should have is reached
    """
    #first get the config options needed
    give_untraited_traits = config["enemy"]["trait"]["untraited_get_trait"]
    remove_metal = config #idk where this is rn
    #initialize the arrays
    all_traits = []
    for trait in e.t:
        all_traits.append(int(trait))
    metal = int(e.t.metal) #this is here cause its easier to have this as a distinct variable since I dont have to worry about accidentally comparing an int to an enum of int type
    for e_id in range(0,len(stats)):
        #first get this units srand
        r = srand.randinst(240+57*e_id)
        #first step is get the order of traits to look in for this unit
        temp_traits = copy.deepcopy(all_traits)
        this_trait_order = []
        for x in range(0,len(temp_traits)):
            this_trait_order.append(temp_traits.pop(r.randrange(0,len(temp_traits))))
        #now in that order get all the traits a unit currently has and hasnt
        has_traits = []
        hasnt_traits = []
        for trait in this_trait_order:
            if stats[e_id][trait] == 1:
                has_traits.append(trait)
            else:
                hasnt_traits.append(trait)
        number_of_traits = len(has_traits) #this is for later
        #now create an array thats a combo of hasnt + has
        new_trait_array = copy.deepcopy(hasnt_traits + has_traits)
        #if removing metals do it here
        if remove_metal and metal in new_trait_array:
            new_trait_array.remove(metal)
        #also give untraited things a trait here
        if give_untraited_traits and number_of_traits == 0:
            number_of_traits = 1
        #now removal all traits
        for trait in this_trait_order:
            stats[e_id][trait] = 0
        #now give a trait according to the amount of traits a unit had before
        for trait in new_trait_array:
            if number_of_traits > 0:
                number_of_traits -= 1
                stats[e_id][trait] = 1
        #should be all good
    return stats


#THIS IS MISSING CONFIG FOR REMOVING METALS
def trait_swap(stats,config=DEFAULT_CONFIG):
    """ swaps the traits of stats according to config 
    \n does nothing except edit the traits """
    #first get the config options, its only metal right? (and untraited get trait)
    remove_metal = True
    give_untraited_traits = config["enemy"]["trait"]["untraited_get_trait"]
    #this func is being written with the intent for specified swaps to exist in the future
    #so in otherwords I can have multiple already specified swaps, including multiple traits swapping to the same
    #(one trait swapping to multiple however is not allowed so I dont need to work with it in mind)
    from_traits = []
    to_traits = []
    #assume specified swaps are done here

    #now generate the new swaps
    #start by getting this trait order
    all_traits = []
    for each in e.t:
        all_traits.append(int(each)) #using int so I get the actual int not the enum type int
    r = srand.randinst(4)
    temp_tl = copy.deepcopy(all_traits)
    this_trait_order = []
    for x in range(0,len(all_traits)):
        this_trait_order.append(temp_tl.pop(r.randrange(0,len(temp_tl))))
    #now get the traits missing from 'from' and 'to' starting by missing from both
    not_in_from = []
    not_in_to = []
    #missing from both
    for trait in this_trait_order:
        if trait not in from_traits and trait not in to_traits:
            not_in_from.append(trait)
            not_in_to.append(trait)
    #now get the ones that are only missing from one of the two
    for trait in this_trait_order:
        if trait not in from_traits and trait not in not_in_from:
            not_in_from.append(trait)
        if trait not in to_traits and trait not in not_in_to:
            not_in_to.append(trait)
    #so now we have all the missing traits with the ones missing from both at the start of each array
    #not_in_from must always be equal length or smaller than not_in_to (its only smaller if specified makes it so)
    #should be good to simply rotate not_in_from traits (metal will be handled later)
    r = srand.randinst(99)
    for x in range(1,r.randrange(1,len(not_in_from)-1)):
        not_in_from.append(not_in_from.pop())
    #now we should be all good to just fill out from and to with all the ones in the length of from
    #however before that we need to log the length filled out by specified swaps for doing metal after this
    user_specified_length = len(from_traits)
    for x in range(0,len(not_in_from)):
        from_traits.append(not_in_from[x])
        to_traits.append(not_in_to[x])
    #now all traits have been accounted for, however metal must be dealt with
    #literally just if swapping to metal hasnt been specified by the user, make whatever swaps to metal swap to the same trait as metal currently swaps to
    if remove_metal:
        if int(e.t.metal) in to_traits and to_traits.index(int(e.t.metal)) >= user_specified_length:
            #metal is always gonna end up in from traits so I dont need to check for that
            index_metal_from = from_traits.index(int(e.t.metal))
            index_metal_to = to_traits.index(int(e.t.metal))
            #set to traits to the value from to traits at the position of metal in from traits
            to_traits[index_metal_to] = to_traits[index_metal_from]
    #all good to apply that to it now
    #start by creating an array with traits and an array without traits
    with_traits = copy.deepcopy(stats)
    without_traits = copy.deepcopy(stats)
    
    for e_id in range(0,len(with_traits)):
        #first step remove all traits and count how many there were in the process
        number_of_traits = 0
        for trait in from_traits: #from traits must have all traits right?
            if without_traits[e_id][trait] == 1:
                number_of_traits += 1
                without_traits[e_id][trait] = 0
        #now compare the two arrays to apply the swap
        for trait_id in range(0,len(from_traits)):
            if with_traits[e_id][from_traits[trait_id]] == 1:
                without_traits[e_id][to_traits[trait_id]] = 1
        #and now do something about untraited units
        if give_untraited_traits and number_of_traits == 0:
            untrait_rand = srand.randinst(304+35*e_id)
            without_traits[e_id][to_traits[untrait_rand.randrange(0,len(to_traits))]] = 1 #this does mean that when multiple traits swap to the same trait untraited are more likely to swap to it, maybe thats good?
    #ok should be all good to just return 'without traits'
    return without_traits















