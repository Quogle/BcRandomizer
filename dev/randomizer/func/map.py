import dev.randomizer.enums.cats as c
import dev.randomizer.enums.enemy as e
from dev.randomizer.enums.files import *
from dev.randomizer.func.core import randinst
from dev.randomizer.parse_config import settings
import copy




def map_maker(estat,cstat):
    #sets map to max length
    map = []
    map_size = len(cstat)
    if len(estat) > map_size:
        map_size = len(estat)
    for x in range(0,map_size):
        map.append([])
    
    map = create_enemy_map(map,estat)

def create_enemy_map(map,estat):
    r = randinst(0)
    vanilla_traits = ["black","red","white","floating","relic","zombie","alien","angel","aku","metal"]
    settings["enemy"]
    metals_removed = settings["game"]["gameplay"]["remove_metals"]
    rando_mode = settings["enemy"]["traits"]["mode"]
    
    map = [[],[]]

    if rando_mode == "swap":
        map[0] = get_swap(r,True)
    elif rando_mode == "randomize":
        map[0]
    
    

#gets swap list for cats and enemies
def get_swap(r=randinst,enemy=True):
    swaps = [[],[]]
    #get game settings
    vanilla_traits = ["black","red","white","floating","relic","zombie","alien","angel","aku","metal"]
    metals_removed = settings["game"]["gameplay"]["remove_metals"]
    #get enemy/cat values from their dicts
    if enemy:
        specified_swaps = settings["enemy"]["traits"]["specified_swaps"]
    else:
        specified_swaps = settings["cat"]["unit"]["traits"]["specified_swaps"]

    #make a randomly ordered trait list
    temp_vanilla_traits = copy.deepcopy(vanilla_traits)
    trait_list = []
    while len(temp_vanilla_traits) > 0:
        index = r.randrange(0,len(vanilla_traits))
        trait_list.append(temp_vanilla_traits.pop(index))
        
    
    #adds the swaps specified
    for each in specified_swaps:
        if len(each) == 2:
            if each[0] != "" and each[1] != "":
                swaps[0].append(each[0])
                swaps[1].append(each[1])
    
    #figures out what traits still need to be added
    from_traits = []
    to_traits = []
    for trait in trait_list:
        if trait not in swaps[0]:
            from_traits.append(trait)
        if trait not in swaps[1]:
            to_traits.append(trait)
    if metals_removed:
        if "metal" in to_traits:
            to_traits.remove("metal")
    
    # gets a list of all traits in from with those in both from and to at the start
    traits = []
    extra = []
    for trait in trait_list:
        if trait in from_traits and trait in to_traits:
            traits.append(trait)
        elif trait in from_traits:
            extra.append(trait)
    for each in extra:
        traits.append(each)
    
    #get what metal should be if its removed
    if metals_removed and "metal" in from_traits:
        metal_to = traits[0]
        if "metal" in traits:
            traits.remove("metal")

    #make desti array
    new_traits = copy.deepcopy(traits)
    
    #rotate traits by an amount between 1 and len - 1
    for x in range(1,r.randrange(1,len(new_traits)-1)):
        new_traits.append(new_traits[0])
        new_traits.pop(0)
    
    #add them to swaps
    for x in range(0,len(traits)):
        swaps[0].append(traits[x])
        swaps[1].append(new_traits[x])
    
    #add metal to the end if metals removed
    if metals_removed and "metal" in from_traits:
        swaps[0].append("metal")
        swaps[1].append(metal_to)
    


    return swaps

def get_enemy_randotraits(r=randinst,estat=[]):
    metals_removed = settings["game"]["gameplay"]["remove_metals"]
    vanilla_traits = ["black","red","white","floating","relic","zombie","alien","angel","aku","metal"]
    vanilla_trait_index = [e.t.black,e.t.red,e.t.white,e.t.floating,e.t.relic,e.t.zombie,e.t.alien,e.t.angel,e.t.aku,e.t.metal]
    keep_trait_count = settings["enemy"]["traits"]["keep_trait_amount"]
    always_new_trait = settings["enemy"]["traits"]["always_new_trait"]
    force_dict = settings["enemy"]["force_traits"]

    for unit in estat:

        #make randomized ordered trait list
        unit_trait_list = []
        temp_tl = copy.deepcopy(vanilla_trait_index)
        while len(temp_tl) > 0:
            index = r.randrange(0,len(temp_tl))
            unit_trait_list.append(temp_tl.pop(index))
        
        #get unit info
        has_traits = []
        for trait in unit_trait_list:
            if unit[trait] == 1:
                has_traits.append(trait)
        trait_count = len(has_traits)
        old_traits = copy.deepcopy(has_traits)
        for trait in unit_trait_list:
            if trait not in old_traits:
                old_traits.append(trait)
        new_traits = copy.deepcopy(old_traits)

        #remove metal from new trait and replace it with a trait the unit doesnt have
        if metals_removed:
            new_traits.remove(e.t.metal)
            index_to_add = trait_count
            if old_traits[index_to_add] == e.t.metal:
                index_to_add += 1
            new_traits.append(old_traits[index_to_add])
        
        #rotate new traits
        for x in range(0,trait_count):
            new_traits.append(new_traits[0])
            new_traits.pop(0)
        
        #ready to be returned
        




















