import dev.randomizer.enums.cats as c
import dev.randomizer.func.game_files as f
from dev.randomizer.func.random import randinst
from dev.randomizer.func.misc import *
from dev.randomizer.parse_config import settings
from dev.randomizer.data.filepaths import *
import copy

"""
rebalancers
"""
def make_base_cat(cstat):
    new_stats = copy.deepcopy(cstat)
    new_stats = early_reworks(new_stats)
    return new_stats


def early_reworks(cstats):
    """
    applies the reworks from congif
    """
    changes = settings["game"]["gameplay"]["unit_reworks"]
    if changes["rework_units"]:
        courier = changes["courier"]
        jurassic = changes["jurassic"]
        space = changes["space"]
        jumprope = changes["jumprope"]
        hurricat = changes["hurricat"]
        waitress = changes["waitress"]
        researcher = changes["aku_researcher"]
        backhoe = changes["backhoe"]
        mint = changes["mint"]
        punt = changes["punt"]
        merc = changes["merc"]
        capsule = changes["capsule"]
        racism_cow = changes["racism_cow"]
        reaper = changes["reaper"]
        million_dollar = changes["million_dollar"]
        cop = changes["cop"]
        paladin = changes["paladin"]
        cat_clan = changes["cat_clan"]
        verbena = changes["verbena"]
        hayabusa = changes["hayabusa"]
        moneko = changes["moneko"]
        neneko = changes["neneko"]
        summer_neneko = changes["summer_neneko"]
        new_year_neneko = changes["new_year_neneko"]
        valentine_neneko = changes["valentine_neneko"]
        easter_neneko = changes["easter_neneko"]
        cmoneko = changes["cmoneko"]

        #all 3 form changes
        for x in range(0,3):
            if courier:
                cstats[658][x][c.t.red] = 0
                cstats[658][x][c.s.massive] = 0
            if jurassic:
                cstats[46][x][c.s.savage_by] = 200
                cstats[46][x][c.s.savage_chance] = 5
                cstats[46][x][c.s.cost] = 500
            if space:
                cstats[48][x][c.s.crit_chance] = 20
            if jumprope:
                cstats[88][x][c.s.hp] = 600
            if hurricat:
                cstats[267][x][c.s.savage_by] = 200
                cstats[267][x][c.s.savage_chance] = 5
                cstats[267][x][c.s.multi_damage_2] = 30
                cstats[267][x][c.s.multi_damage_3] = 30
                cstats[267][x][c.s.multi_has_ability_2] = 1
                cstats[267][x][c.s.multi_has_ability_3] = 1
                cstats[267][x][c.s.multi_preatk_2] = 3
                cstats[267][x][c.s.multi_preatk_3] = 5
            if waitress:
                cstats[273][x][c.s.savage_by] = 300
                cstats[273][x][c.s.savage_chance] = 100
                cstats[273][x][c.t.metal] = 1
                cstats[273][x][c.s.strong] = 1
            if researcher:
                cstats[621][x][c.s.massive] = 1
                cstats[621][x][c.t.metal] = 1
            if backhoe:
                cstats[446][x][c.s.attack] = 100
                cstats[446][x][c.s.multi_damage_2] = 100
                cstats[446][x][c.s.multi_damage_3] = 100
                cstats[446][x][c.s.multi_preatk_2] = 61
                cstats[446][x][c.s.multi_preatk_3] = 62
                cstats[446][x][c.s.multi_has_ability_2] = 1
                cstats[446][x][c.s.multi_has_ability_3] = 1
                cstats[446][x][c.s.curse_chance] = 50
                cstats[446][x][c.s.curse_time] = 100
                cstats[446][x][c.s.explode_chance] = 50
                cstats[446][x][c.s.explode_at] = 1000
                cstats[446][x][c.s.explode_variation_x4] = 3000
            if mint and x<2:
                cstats[184][x][c.s.attack] = 140
                cstats[184][x][c.s.cost] = 350
                cstats[184][x][c.s.recharge] = 400
                cstats[184][x][c.s.hp] = 500
                cstats[184][x][c.s.kbs] = 4
            if punt:
                cstats[26][x][c.s.metal] = 1
                cstats[26][x][c.s.hp] = 1000
                cstats[26][x][c.s.attack] = 1000
                cstats[26][x][c.s.weaken_chance] = 100
                cstats[26][x][c.s.weaken_duration] = 150
                cstats[26][x][c.s.weaken_to] = 50
            if merc:
                cstats[121][x][c.s.hp] = 800
                cstats[121][x][c.s.kbs] = 4
                cstats[121][x][c.s.attack] = 100
                cstats[121][x][c.s.multi_damage_2] = 100
                cstats[121][x][c.s.multi_damage_3] = 100
                cstats[121][x][c.s.ld_minimum] = 155
                cstats[121][x][c.s.ld_width] = -475
                cstats[121][x][c.s.multi_ld_2_start] = -320
                cstats[121][x][c.s.multi_ld_3_start] = -320
                cstats[121][x][c.s.multi_ld_2_width] = 550
                cstats[121][x][c.s.multi_ld_3_width] = 625
                cstats[121][x][c.s.multi_ld_2_exists] = 1
                cstats[121][x][c.s.multi_ld_3_exists] = 1
                cstats[121][x][c.s.multi_preatk_2] = 3
                cstats[121][x][c.s.multi_preatk_3] = 5
                cstats[121][x][c.s.multi_has_ability_2] = 1
                cstats[121][x][c.s.multi_has_ability_3] = 1
                cstats[121][x][c.s.savage_by] = 200
                cstats[121][x][c.s.crit_chance] = 0 #was 20
                cstats[121][x][c.s.savage_chance] = 20
            if capsule and x<2:
                cstats[28][x][c.t.metal] = 1
                cstats[28][x][c.s.attack] = 500
                cstats[28][x][c.s.massive] = 1
            if racism_cow and x<2:
                cstats[65][x][c.s.hp] = 1300        #normally 500hp
                cstats[65][x][c.s.attack] = 80      #normally 30 damage
            if reaper:
                cstats[68][x][c.s.slow_chance] = 60 #normally 40%
                cstats[68][x][c.s.slow_duration] = 120 #normally 120
                cstats[68][x][c.s.cost] = 750       #normally 500
                cstats[68][x][c.s.attack] = 470     #does 7990 at lvl30
                cstats[68][x][c.s.hp] = 700         #normally 700 2nd form
            if million_dollar and x<2:
                cstats[635][x][c.s.savage_by] = 500
                cstats[635][x][c.s.savage_chance] = 100
                cstats[635][x][c.s.eva_killer] = 1
            if cop and x>0:
                cstats[716][x][c.t.white] = 0
                cstats[716][x][c.t.black] = 1
                cstats[716][x][c.t.red] = 1
                cstats[716][x][c.t.alien] = 1
            if paladin:
                cstats[57][x][c.s.savage_by] = 200
                cstats[57][x][c.s.tba] = 100        #normally 60
            if cat_clan:
                cstats[427][x][c.s.savage_by] = 200
                cstats[427][x][c.s.savage_chance] = 3
            if moneko:
                cstats[16][x][c.s.bounty] = 1
            if neneko:
                cstats[131][x][c.t.metal] = 1
                cstats[131][x][c.s.savage_by] = 200
                cstats[131][x][c.s.savage_chance] = 15
                cstats[131][x][c.s.insane_massive] = 1
            if summer_neneko:
                cstats[276][x][c.s.massive] = 1
                cstats[276][x][c.s.insane_massive] = 1
                cstats[276][x][c.t.metal] = 1
            if new_year_neneko:
                cstats[314][x][c.s.tba] = 0
                cstats[314][x][c.s.savage_by] = 200
                cstats[314][x][c.s.savage_chance] = 15
            if valentine_neneko:
                cstats[589][x][c.s.wave_level] = 4
                cstats[589][x][c.s.range] = 410
            if easter_neneko:
                cstats[332][x][c.s.weaken_chance] = 50
                cstats[332][x][c.s.slow_chance] = 50
                cstats[332][x][c.s.freeze_chance] = 50
                #cstats[332][x][c.s.kb_chance] = 50 #might be too strong
                cstats[332][x][c.s.area] = 1
                cstats[332][x][c.t.metal] = 1
                cstats[332][x][c.s.weaken_duration] = 40
                cstats[332][x][c.s.slow_duration] = 40
                cstats[332][x][c.s.freeze_duration] = 40
                cstats[332][x][c.s.weaken_to] = 50
            if cmoneko and x<2:
                cstats[418][x][c.s.savage_by] = 200
                cstats[418][x][c.s.savage_chance] = 100
            if verbena:
                cstats[358][x][c.s.savage_by] = 200
                cstats[358][x][c.s.savage_chance] = 30
                cstats[358][x][c.s.crit_chance] = 30
        

        #single form changes
        if jurassic:
            cstats[46][0][c.s.hp] = 570
            cstats[46][1][c.s.hp] = 900
            cstats[46][2][c.s.hp] = 1400
            cstats[46][0][c.s.attack] = 200
            cstats[46][1][c.s.attack] = 250
            cstats[46][2][c.s.attack] = 300
            cstats[46][2][c.s.savage_chance] = 12
        if hurricat:
            cstats[267][0][c.s.multi_damage_2] = 24
            cstats[267][0][c.s.multi_damage_3] = 24
        if backhoe:
            cstats[446][2][c.s.curse_chance] = 100
            cstats[446][2][c.s.explode_chance] = 100
        if mint:
            cstats[184][1][c.t.alien] = 0
            cstats[184][1][c.t.metal] = 1
        if punt:
            cstats[26][x][c.s.attack] = 1200
            cstats[26][x][c.s.weaken_to] = 10
        if merc:
            cstats[121][2][c.s.crit_chance] = 100
            cstats[121][2][c.s.savage_chance] = 100
        if reaper:
            cstats[68][2][c.s.attack] = 200     #does 7990 at lvl30
            cstats[68][2][c.s.multi_damage_2] = 400
            cstats[68][2][c.s.multi_damage_3] = 800
            cstats[68][2][c.s.hp] = 1000         #normally 700 2nd form
            cstats[68][2][c.s.multi_has_ability_2] = 1
            cstats[68][2][c.s.multi_has_ability_3] = 1
            cstats[68][2][c.s.preatk] = 16
            cstats[68][2][c.s.multi_preatk_2] = 57
            cstats[68][2][c.s.multi_preatk_3] = 83
        if paladin:
            cstats[57][0][c.s.hp] = 2000
            cstats[57][1][c.s.hp] = 3000
            cstats[57][2][c.s.hp] = 4000
            cstats[57][0][c.s.savage_chance] = 20
            cstats[57][1][c.s.savage_chance] = 40
            cstats[57][2][c.s.savage_chance] = 50
            cstats[57][0][c.s.attack] = 600
            cstats[57][1][c.s.attack] = 1000
            cstats[57][2][c.s.attack] = 1200
            cstats[57][2][c.s.soul_strike] = 1
        if moneko:
            cstats[16][2][c.s.is_miniwave] = 0
        if valentine_neneko:
            cstats[589][2][c.s.shield_pierce_chance] = 50
        if easter_neneko:
            cstats[332][x][c.s.weaken_duration] = 90
            cstats[332][x][c.s.slow_duration] = 90
            cstats[332][x][c.s.freeze_duration] = 90
        if verbena:
            cstats[358][2][c.s.crit_chance] = 50
            cstats[358][2][c.s.savage_chance] = 50
        if hayabusa:
            cstats[261][0][c.s.savage_by] = 200
            cstats[261][0][c.s.savage_chance] = 30
    

    return cstats

         

def get_swaps(stats):
    """
    gets cat swaps, conditional
    """
    r = randinst(201)
    remove_metals = settings["game"]["gameplay"]["remove_metals"]
    traits = [c.t.black,c.t.red,c.t.white,c.t.floating,c.t.relic,c.t.zombie,c.t.alien,c.t.angel,c.t.aku,c.t.metal]
    text_traits = ["black","red","white","floating","relic","zombie","alien","angel","aku","metal"]

    specified_swap_texts = settings["cat"]["unit"]["traits"]["specified_swap"]
    user_from = []
    user_to = []
    for each in specified_swap_texts:
        try:
            first = text_traits.index(each[0])
            second = text_traits.index(each[1])
            user_from.append(traits[first])
            user_to.append(traits[second])
        except:
            pass
    
    #get current working trait order
    current_trait_order = []
    temp_tl = copy.deepcopy(traits)
    for x in range(temp_tl):
        current_trait_order.append(temp_tl.pop(r.randrange(0,len(temp_tl))))
    
    #get traits to be added
    missing_from = []
    missing_to = []
    for trait in current_trait_order:
        if trait not in user_from and trait not in user_to:
            missing_from.append(trait)
            missing_to.append(trait)
    dually_missing_count = len(missing_from)
    for trait in current_trait_order:
        if trait not in user_from:
            missing_from.append(trait)
        if trait not in user_to:
            missing_to.append(trait)
    
    current_index = 0
    while len(missing_to) < len(missing_from):
        missing_to.append(missing_to[current_index])
        current_index += 1
    
    #rotate
    for x in range(0,dually_missing_count):
        missing_to.append(missing_to.pop(0))
    
    
    if remove_metals:
        index = 0
        if current_trait_order[0] == c.t.metal:
            index = 1
        for x in range(0,len(missing_to)):
            if missing_to[x] == c.t.metal:
                missing_to[x] = current_trait_order[index]
    
    swaps = [[],[]]
    for x in range(0,len(user_from)):
        swaps[0].append(user_from[x])
        swaps[1].append(user_to[x])
    
    for x in range(0,len(missing_from)):
        swaps[0].append(missing_from[x])
        swaps[1].append(missing_to[x])
    
    map_to_return = []
    for x in range(0,len(stats)):
        unit_map = []
        for y in range(0,stats[x]):
            unit_map.append(swaps)
        map_to_return.append(unit_map)
    
    return map_to_return
    
def get_cat_randomization_map(stats,talents):
    """
    creates map based on input array, [old trait,new trait] for each form in each unit
    \n conditional
    """
    r = randinst(201)
    remove_metals = settings["game"]["gameplay"]["remove_metals"]
    trait_per_whole_unit = settings["cat"]["unit"]["traits"]["trait_per_whole_unit"]
    try_new_trait = settings["cat"]["unit"]["traits"]["try_new_trait"]
    all_traits = []
    for trait in c.t:
        all_traits.append(int(trait))
    map_to_return = []
    for unit_id in range(0,len(stats)):
        unit_map = []
        for form_id in range(0,5): #establish current trait order 5 times regardless of whether per form or not
            current_trait_order = []
            temp_tl = copy.deepcopy(all_traits)
            for x in range(0,len(temp_tl)):
                current_trait_order.append(temp_tl.pop(r.randrange(0,len(temp_tl))))
            shift = r.randrange(0,len(all_traits)-1)
            #get units talents if there are any
            unit_talents = []
            for each in talents:
                if each[c.tpos.unit_id] == unit_id:
                    unit_talents = each

            if trait_per_whole_unit:
                if form_id == 4: #only run on last form id if whole unit
                    #get has traits
                    has_traits = multi_form_total_has_traits(current_trait_order,stats[unit_id],unit_talents)
                    if try_new_trait: #stop it from needlessly rotating and allow metal to work
                        shift = len(has_traits) % len(all_traits)
                        
                    old_traits = fill_out_trait_list(current_trait_order,has_traits)
                    new_traits = copy.deepcopy(old_traits)
                    #if no metals replace metal with the first trait a unit wont get
                    if remove_metals:
                        index = shift
                        if new_traits[index] == int(c.t.metal):
                            index = (index + 1) % len(all_traits)
                        new_traits[new_traits.index(c.t.metal)] = new_traits(index)
                    
                    #now rotate new traits by shift
                    for x in range(shift):
                        new_traits.append(new_traits.pop(0))
                    
                    #now slap it on unit map a number of times
                    for x in range(0,len(stats[unit_id])):
                        unit_map.append([old_traits,new_traits])

            else: #trait per form
                if len(stats[unit_id]) > form_id:
                    #get whether or not talents count this form
                    form_talents = []
                    if form_id >= 2:
                        form_talents = unit_talents
                    #get has traits
                    has_traits = single_form_total_has_traits(current_trait_order,stats[unit_id][form_id],form_talents)
                    if try_new_trait: #stop it from needlessly rotating and allow metal to work
                        shift = len(has_traits) % len(all_traits)
                    
                    old_traits = fill_out_trait_list(current_trait_order,has_traits)
                    new_traits = copy.deepcopy(old_traits)
                    if remove_metals:
                        index = shift
                        if new_traits[index] == int(c.t.metal):
                            index = (index + 1) % len(all_traits)
                        new_traits[new_traits.index(c.t.metal)] = new_traits(index)
                    
                    #now rotate new traits by shift
                    for x in range(shift):
                        new_traits.append(new_traits.pop(0))
                    
                    #now slap in unit map
                    unit_map.append([old_traits,new_traits])
        #slap unit map into total map
        map_to_return.append(unit_map)
    return map_to_return
                    
def get_map(stats,talents):
    """
    gets map from stats, conditional
    """
    mode = settings["cat"]["unit"]["traits"]["mode"]
    cat_map = []
    if mode == "swap":
        cat_map = get_swaps(stats)
    if mode == "randomize":
        cat_map = get_cat_randomization_map(stats,talents)
    return cat_map

def create_form_map(traits,shift,traits_had,remove_metals):
    new_traits = copy.deepcopy(traits)
    for x in range(0,shift): #rotate it
        new_traits.append(new_traits.pop(0))
    
    if remove_metals: #replace metal with first entry cat wont get
        metal_index = new_traits.index(c.t.metal)
        new_index = traits_had%len(new_traits)
        if new_traits[new_traits] == c.t.metal:
            new_index = new_index%len(new_traits)
        new_traits[metal_index] = new_traits[new_index]
    
    form_map = [traits,new_traits]
    return form_map

def apply_map_to_stats(stats,map):
    """
    applies a map to unit array
    """
    if len(map) == 0: #this is used when set to none
        return stats
    #create traitless array
    new_stats = copy.deepcopy(stats)
    for unit_id in range(0,len(new_stats)):
        for form_id in range(0,len(new_stats[unit_id])):
            for trait in c.t:
                new_stats[unit_id][form_id][trait] = 0
    
    for unit_id in range(0,len(stats)):
        for form_id in range(0,len(stats[unit_id])):
            for index in range(0,len(map[unit_id][form_id][0])): #its done this way so if someone puts multiple swaps from the same trait it works
                old_trait = map[unit_id][form_id][0][index]
                new_trait = map[unit_id][form_id][1][index]
                if stats[unit_id][form_id][old_trait] == 1:
                    new_stats[unit_id][form_id][new_trait] = 1
    
    return new_stats

def apply_map_to_talents(talents,stats,map):
    """
    takes a map and applies it and all talent edits to it
    \n conditional
    """


#need one for giving/taking zkill curse and shield and barrier but idk how I intend to do that rn since talents





"""
minor parts
"""

def get_units_has_talent_traits(units_talents):
    """
    gets the traits a unit has in talents, returns an empty array if no talents
    """
    try:
        len(units_talents)
        traits = []
        trait_sum = units_talents[c.tpos.type_id]
        if trait_sum > 0:
            if trait_sum >= c.tv.sum_aku:
                trait_sum = trait_sum % c.tv.sum_aku
                traits.append(int(c.t.aku))
            if trait_sum >= c.tv.sum_witch: #this is just here to make the math work
                trait_sum = trait_sum % c.tv.sum_witch
                #traits.append(int(c.t.witch))
            if trait_sum >= c.tv.sum_white:
                trait_sum = trait_sum % c.tv.sum_white
                traits.append(int(c.t.white))
            if trait_sum >= c.tv.sum_relic:
                trait_sum = trait_sum % c.tv.sum_relic
                traits.append(int(c.t.relic))
            if trait_sum >= c.tv.sum_zombie:
                trait_sum = trait_sum % c.tv.sum_zombie
                traits.append(int(c.t.zombie))
            if trait_sum >= c.tv.sum_alien:
                trait_sum = trait_sum % c.tv.sum_alien
                traits.append(int(c.t.alien))
            if trait_sum >= c.tv.sum_angel:
                trait_sum = trait_sum % c.tv.sum_angel
                traits.append(int(c.t.angel))
            if trait_sum >= c.tv.sum_metal:
                trait_sum = trait_sum % c.tv.sum_metal
                traits.append(int(c.t.metal))
            if trait_sum >= c.tv.sum_black:
                trait_sum = trait_sum % c.tv.sum_black
                traits.append(int(c.t.black))
            if trait_sum >= c.tv.sum_floating:
                trait_sum = trait_sum % c.tv.sum_floating
                traits.append(int(c.t.floating))
            if trait_sum >= c.tv.sum_red:
                trait_sum = trait_sum % c.tv.sum_red
                traits.append(int(c.t.red))

        #now get arrays of same index same traits for talent ids
        normal_trait_list_objects = [c.t.black,c.t.red,c.t.white,c.t.floating,c.t.relic,c.t.zombie,c.t.alien,c.t.angel,c.t.aku,c.t.metal]
        talent_trait_list_objects = [c.tv.black,c.tv.red,c.tv.white,c.tv.floating,c.tv.relic,c.tv.zombie,c.tv.alien,c.tv.angel,c.tv.aku,c.tv.metal]
        talent_trait_list = []
        normal_trait_list = []
        for trait in talent_trait_list_objects:
            talent_trait_list.append(int(trait))
        for trait in normal_trait_list_objects:
            normal_trait_list.append(int(trait))
        #if talent is a trait get its position and shove the value from normal traits into traits
        for x in range(2,len(units_talents)):
            talent_id = units_talents[x][c.tpos.ability_id]
            if talent_id in talent_trait_list:
                traits.append(normal_trait_list[talent_trait_list.index(talent_id)])
        
        return []
    except:
        return []

def get_trait_ordered_traits(trait_order,traits):
    """
    takes an array with potential duplicates in a set order and gets the non duplicated trait ordered version
    """
    new_traits = []
    for each in trait_order:
        if each in traits:
            new_traits.append(each)
    return new_traits

def fill_out_trait_list(current_trait_order,trait_list):
    """
    fills out trait list with the remaining traits
    """
    for each in current_trait_order:
        if each not in trait_list:
            trait_list.append(each)
    return trait_list

def single_form_has_non_talent_traits(current_trait_order,form_stats):
    """
    returns has traits for a single form
    """
    has_traits = []
    for trait in current_trait_order:
        if form_stats[trait] == 1:
            has_traits.append(trait)
    return has_traits

def all_form_has_traits(current_trait_order,unit_stats):
    """
    returns a potentially duplicated has traits
    """
    has_traits = []
    for form in unit_stats:
        for trait in current_trait_order:
            if form[trait] == 1:
                has_traits.append(trait)
    return has_traits

def single_form_total_has_traits(trait_order,form_stats,talents):
    """
    gets the has traits a single form has including talents
    """
    base_traits = single_form_has_non_talent_traits(trait_order,form_stats)
    talent_traits = get_units_has_talent_traits(talents)
    has_traits = get_trait_ordered_traits(trait_order,base_traits + talent_traits)
    return has_traits

def multi_form_total_has_traits(trait_order,unit_stats,talents):
    """
    returns the multiform has traits that includes talents
    """
    base_traits = all_form_has_traits(trait_order,unit_stats)
    talent_traits = get_units_has_talent_traits(talents)
    has_traits = get_trait_ordered_traits(trait_order,base_traits + talent_traits)
    return has_traits

def give_and_take_trait_abilities(stats,vanilla_stats):
    """
    removes zkill from ex zombie targetters for instance
    """
    r = randinst(106)
    give = settings["unit"]["give_trait_specific_abilities"]
    take = settings["unit"]["take_trait_specific_abilities"]
    zkill = settings["unit"]["zkiller_frequency"]
    curse = settings["unit"]["curse_imm_frequency"]
    shield = settings["unit"]["shield_pierce_frequency"]
    strong_sp_threshold = 20 #as a % of how many units get it, currently changes divisor from 600f to be 100% down to 300f
    for unit_id in range(0,len(stats)):
        for form_id in range(0,5):
            zk = r.randrange(0,100)
            ci = r.randrange(0,100)
            sp = r.randrange(0,100)
            sp_strength = r.randrange(0,100)
            if len(stats[unit_id]) > form_id:
                if give:
                    if zk < zkill: #grant zkill
                        if stats[unit_id][form_id][c.t.zombie] == 1 and vanilla_stats[unit_id][form_id][c.t.zombie] == 0:
                            stats[unit_id][form_id][c.s.zombie_killer] = 1
                    if ci < curse:
                        if stats[unit_id][form_id][c.t.relic] == 1 and vanilla_stats[unit_id][form_id][c.t.relic] == 0:
                            stats[unit_id][form_id][c.s.curse_immune] = 1
                    if sp < shield:
                        if stats[unit_id][form_id][c.t.aku] == 1 and vanilla_stats[unit_id][form_id][c.t.aku] == 0:
                            attack_cycle = stats[unit_id][form_id][c.s.tba] + stats[unit_id][form_id][c.s.preatk] #just realized this way of getting atk cyc fails on multi hit
                            divisor = 600
                            if sp_strength < strong_sp_threshold:
                                divisor = 300
                            stats[unit_id][form_id][c.s.shield_pierce_chance] = clamp_value(1+attack_cycle/divisor)
                if take:
                    if zk < zkill: #grant zkill
                        if stats[unit_id][form_id][c.t.zombie] == 0 and vanilla_stats[unit_id][form_id][c.t.zombie] == 1:
                            stats[unit_id][form_id][c.s.zombie_killer] = 0
                    if ci < curse:
                        if stats[unit_id][form_id][c.t.relic] == 0 and vanilla_stats[unit_id][form_id][c.t.relic] == 1:
                            stats[unit_id][form_id][c.s.curse_immune] = 0
                    if sp < shield:
                        if stats[unit_id][form_id][c.t.aku] == 0 and vanilla_stats[unit_id][form_id][c.t.aku] == 1:
                            stats[unit_id][form_id][c.s.shield_pierce_chance] = 0
    return stats






