import dev.randomizer.enums.cats as c
import dev.randomizer.enums.enemy as e
from dev.randomizer.enums.files import *
from dev.randomizer.func.core import randinst
from dev.randomizer.parse_config import settings
import copy



#returns a trait map [0] is enemy [1] is cat ([from,to] if per unit,[[from,to],[from,to]] if per form)
def map_maker(estat,cstat,ctalents):
    #sets map to max length
    map = []
    map_size = len(cstat)
    if len(estat) > map_size:
        map_size = len(estat)
    for x in range(0,map_size):
        map.append([[],[]])
    
    enemy_map = create_enemy_map(estat)
    cat_map = create_cat_map(cstat,ctalents)
    for x in range(0,len(enemy_map)):
        map[x][0] = enemy_map[x]
    for x in range(0,len(cat_map)):
        map[x][1] = cat_map[x]
    
    return map

def create_enemy_map(estat):
    """
    returns a map enemy length long of [[from],[to]] 
    """
    r = randinst(0)
    rando_mode = settings["enemy"]["traits"]["mode"]
    # [unit id][from/to]
    enemy_map = []
    for x in range(0,len(estat)):
        enemy_map.append([[],[]])
    if rando_mode == "swap":
        swap = get_swap(r,True)
        for x in range(0,len(enemy_map)):
            enemy_map[x] = swap
    elif rando_mode == "randomize":
        lists = get_enemy_rando_map(r,estat)
        for x in range(0,len(enemy_map)):
            enemy_map[x] = lists[x]

    return enemy_map

def create_cat_map(cstat,ctalent):
    """
    returns a map enemy length long of [[from],[to]] if per unit and that xform a layer deeper per unit if per form
    """
    r = randinst(1)
    rando_mode = settings["cat"]["unit"]["traits"]["mode"]
    cat_map = []
    if rando_mode == "swap":
        swap = get_swap(r)
        for x in range(0,len(cstat)):
            cat_map.append(swap)
    elif rando_mode == "randomize":
        cat_map = get_cat_rando_map(r,cstat,ctalent)
    
    return cat_map

#gets swap list for cats and enemies, swap is just [[fromlist],[tolist]]
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
        index = r.randrange(0,len(temp_vanilla_traits))
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

def get_enemy_rando_map(r=randinst,estat=[]):
    metals_removed = settings["game"]["gameplay"]["remove_metals"]
    vanilla_trait_index = [e.t.black,e.t.red,e.t.white,e.t.floating,e.t.relic,e.t.zombie,e.t.alien,e.t.angel,e.t.aku,e.t.metal]
    map_list = []
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
        map_list.append([old_traits,new_traits])
    
    return map_list
        
def get_cat_rando_map(r=randinst,cstat=[],ctalent=[]):
    metals_removed = settings["game"]["gameplay"]["remove_metals"]
    per_whole_unit = settings["cat"]["unit"]["traits"]["trait_per_whole_unit"]
    try_new_trait = settings["cat"]["unit"]["traits"]["try_new_trait"]
    vanilla_trait_list = []
    for each in c.t:
        vanilla_trait_list.append(each)
    

    cat_map = []

    for unit in range(0,len(cstat)):
        if per_whole_unit:
            #get unit trait order
            old_traits = []
            current_trait_order = []
            temp_trait_list = copy.deepcopy(vanilla_trait_list)
            for trait in range(0,len(temp_trait_list)):
                index = r.randrange(0,len(temp_trait_list))
                current_trait_order.append(temp_trait_list.pop(index))
            # get old has traits
            for form in range(0,len(unit)):
                for trait in current_trait_order:
                    if cstat[unit][form][trait] == 1 and trait not in old_traits:
                        old_traits.append(trait)
            
            # add talents to old traits
            has_talent = False
            for x in range(0,len(ctalent)):
                pass #I cant properly finish this until I bother to remember what talents are where

            #finish old traits 
            trait_count = len(old_traits)
            for trait in current_trait_order:
                if trait not in old_traits:
                    old_traits.append(trait)
            
            #establish new traits
            new_traits = copy.deepcopy(old_traits)
            if metals_removed:
                index = 0
                if current_trait_order[index] == e.t.metal:
                    index += 1
                metal_index = new_traits.index(e.t.metal)
                new_traits[metal_index] = current_trait_order[index]
            
            #rotate the array
            max_length = trait_count
            if not try_new_trait:
                max_length = len(new_traits)
            for x in range(0,max_length):
                new_traits.append(new_traits[0])
                new_traits.pop(0)
            
            #add array to map
            cat_map.append([old_traits,new_traits])
        else:
            #how tf do I do per form
            unit_map = []
            for form in range(0,len(cstat[unit])):
                #get unit trait order
                old_traits = []
                current_trait_order = []
                temp_trait_list = copy.deepcopy(vanilla_trait_list)
                for trait in range(0,len(temp_trait_list)):
                    index = r.randrange(0,len(temp_trait_list))
                    current_trait_order.append(temp_trait_list.pop(index))
                
                #get old traits
                for trait in current_trait_order:
                    if cstat[unit][form][trait] == 1:
                        old_traits.append(trait)
                # get talents
                if form > 1:
                    pass #still dont know how Im formatting talents

                # finish old traits
                for trait in current_trait_order:
                    if trait not in old_traits:
                        old_traits.append(trait)
                
                # make new traits
                new_traits = copy.deepcopy(old_traits)
                if metals_removed:
                    index = 0
                    if current_trait_order[index] == e.t.metal:
                        index += 1
                    metal_index = new_traits.index(e.t.metal)
                    new_traits[metal_index] = current_trait_order[index]
                
                #rotate the array
                max_length = trait_count
                if not try_new_trait:
                    max_length = len(new_traits)
                for x in range(0,max_length):
                    new_traits.append(new_traits[0])
                    new_traits.pop(0)
                
                unit_map.append([old_traits,new_traits])
            cat_map.append(unit_map)
    
    return cat_map















