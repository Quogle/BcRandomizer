import tadbcmc.data.enums.enemy as e
from ...config.defaults import DEFAULT_CONFIG
import copy
import tadbcmc.core.seeded_randomization as srand







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

















