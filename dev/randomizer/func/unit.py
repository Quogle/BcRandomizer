import dev.randomizer.enums.cats as c
import dev.randomizer.func.files as f
from dev.randomizer.func.core import randinst
from dev.randomizer.parse_config import settings
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
                cstats[121][x][c.s.crit_chance] = 20
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
    
def get_cat_randomization_map(stats):
    """
    creates map based on input array
    """
    r = randinst(201)
    remove_metals = settings["game"]["gameplay"]["remove_metals"] #this isnt done here anymore
    trait_per_whole_unit = settings["cat"]["unit"]["traits"]["trait_per_whole_unit"]
    try_new_trait = settings["cat"]["unit"]["traits"]["try_new_trait"] #this can be mimmicked by just not using the shift when applying map
    all_traits = [c.t.black,c.t.red,c.t.white,c.t.floating,c.t.relic,c.t.zombie,c.t.alien,c.t.angel,c.t.aku,c.t.metal]

    map_to_return = [] #maybe initialize it with a bunch of values if theres a file with no forms
    for unit_id in range(0,len(stats)):
        units_map = []
        if trait_per_whole_unit:
            #establish units working trait order
            current_trait_order = []
            temp_tl = copy.deepcopy(all_traits)
            for x in range(0,len(temp_tl)):
                current_trait_order.append(temp_tl.pop(r.randrange(0,len(temp_tl))))
            
            has_traits = []
            for trait in current_trait_order:
                for form_id in stats[unit_id]:
                    if stats[unit_id][form_id][trait] == 1 and trait not in has_traits:
                        has_traits.append(trait)
            
            traits_had = len(has_traits)
            #finish traits
            for trait in current_trait_order:
                if trait not in has_traits:
                    has_traits.append(trait)
            
            shift = r.randrange(1,len(current_trait_order)-1)
            if try_new_trait:
                shift = traits_had
            
            form_map = create_form_map(has_traits,shift,traits_had,remove_metals)
            for form_id in range(0,len(stats[unit_id])):
                units_map.append(form_map)

        else: #trait per form
            #run 5 times for future proof
            for form_id in range(0,5):
                current_trait_order = []
                temp_tl = copy.deepcopy(current_trait_order)
                for x in range(0,len(temp_tl)):
                    current_trait_order.append(temp_tl.pop(r.randrange(0,len(temp_tl))))
                shift = r.randrange(1,len(current_trait_order)-1)
                if len(stats[unit_id]) > form_id:
                    has_traits = []
                    for trait in current_trait_order:
                        if stats[unit_id][form_id][trait] == 1:
                            has_traits.append(trait)
                    
                    traits_had = len(has_traits)
                    #finish hastraits
                    for trait in current_trait_order:
                        if trait not in has_traits:
                            has_traits.append(trait)
                    
                    if try_new_trait:
                        shift = traits_had
                    
                    form_map = create_form_map(has_traits,shift,traits_had,remove_metals)
                    units_map.append(form_map)

        map_to_return.append(units_map)
    return map_to_return
                    
def get_map(stats):
    """
    gets map from stats, conditional
    """
    mode = settings["cat"]["unit"]["traits"]["mode"]
    cat_map = []
    if mode == "swap":
        cat_map = get_swaps(stats)
    if mode == "randomize":
        cat_map = get_cat_randomization_map(stats)
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

def apply_map(stats,map):
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

def do_trait_randomization(stats):
    """
    generates trait map from stats and applies it to stats
    """
    cat_map = get_map(stats)
    new_stats = apply_map(stats,cat_map)
    return new_stats

#need one for giving/taking zkill curse and shield and barrier but idk how I intend to do that rn since talents






#the 3d array straight from the files
vanilla_cat_array = f.read_vanilla_cat_stats()

vanilla_unitbuy_array = f.read_vanilla_unitbuy()

#the 3d array with the before everything reworks applied to it
base_cat_array = make_base_cat(vanilla_cat_array)



