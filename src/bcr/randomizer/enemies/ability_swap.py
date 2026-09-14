from ..enemies import ability_altering as abal
import tadbcmc.data.enums.enemy as e
from ...config.defaults import DEFAULT_CONFIG
import copy
import tadbcmc.core.seeded_randomization as srand
from typing import Tuple,Dict,List


"""variable explanation:
check/check_id: a check refers the the position in the stat array used for checking if an ability already exists or not (when the value at check !=0 the ability normally exists (single is an exception))
info_dict: a dictionary of all abilities where the value is a list containing that abilities [weight,check id,bool for applying in first half]
#the next two are half specific
count_array: a list of checks to be used in determining how many abilities a unit already has, must be distinct from the list of abilities to apply to make it able to give immunities/ld/omni without having an immunity/ld/omni block units from getting other abilities
giveable/give: a list where at the shared index x in all 3 arrays,
    name: the string name of the ability
    weight: the weight of the ability
    check: the check for the ability
"""
"""algorithm for randomizing abilities:
gather all information about each abilities, weight, name, check, appliability in first half, include in count for each half
then acting on each half separately
get the position in index of single/area/ld/omni
for each unit
    count the number of abilities a unit has according to the config (single/area are never counted)
    copy the weight list for this unit
    loop through ability checks for all givable units, if that ability already exists set the weight for this unit to 0
        note: single/area are separate from this process, if they are in give abilities then only if the unit actually has single/area are they set to 0
    for x number of times, where x is the difference between the number of abilities a unit needs to have at a minimum
        chose an index from the weight list, get that indexes string name
        using string name give a unit that ability in the ungodly function (this is where the balancing should probably happen)
        set the weight of that index to 0
            note: for ld/omni specifically if both are in giveable and one is chosen the others weight is also set to 0
"""








#Im unsure if the max enemy id in this function is correct
def randomize_abilities(stats:List[List[int]],config=DEFAULT_CONFIG,log=None,post_attack_anims=[]) -> List[List[int]]:
    """ randomizes the abilities of enemies in stats according to config """
    if not config["enemy"]["ability"]["randomize_abilities"]:
        return stats #no sense in running any part of this function if its off
    (info_dict,split_at,minimum_ab_count,count_immunities,count_attack_types) = _process_config_for_rando(config=config,log=log)
    if split_at == -1:
        max_enemy_number = len(stats)
    else:
        max_enemy_number = split_at+1 #or is it +3
    #first half
    (giveable_ability_names,giveable_ability_checks,giveable_ability_weights,count_array) = _create_all_necessary_informations(info_dict,count_immunities,count_attack_types,second_half=False)
    stats = _rand_abilities_of_half(stats,minimum_ab_count,count_array,giveable_ability_names,giveable_ability_checks,giveable_ability_weights,starting_id=2,ending_id=max_enemy_number,post_attack_anims=post_attack_anims) #starting index is 2 because dont give the dummy enemies abilities lmao :sob
    #second half
    (giveable_ability_names,giveable_ability_checks,giveable_ability_weights,count_array) = _create_all_necessary_informations(info_dict,count_immunities,count_attack_types,second_half=True)
    stats = _rand_abilities_of_half(stats,minimum_ab_count,count_array,giveable_ability_names,giveable_ability_checks,giveable_ability_weights,starting_id=max_enemy_number,ending_id=-1,post_attack_anims=post_attack_anims)
    return stats







def _process_config_for_rando(config=DEFAULT_CONFIG,log=None) -> Tuple[Dict[str,List[int]],int,int,bool,bool]:
    """ processes the config to return the necessary initial information
    \n returns (info_dict, split_at, minimum_ab_count, count_immunities, count_attack_types)
    \n\tinfo_dict["name"]: [weight,check,apply in first half] """
    split_at = config["mod"]["max_enemy_id"]
    minimum_ab_count = config["enemy"]["ability"]["min_abilities"]
    count_immunities = config["enemy"]["ability"]["count_immunities"]
    count_attack_types = config["enemy"]["ability"]["count_attack_types"]
    w = config["enemy"]["ability"]["weights"]
    bools = config["enemy"]["ability"]["apply_before_split"]
    #start by getting the check id for each ability
    check = { #PLEASE dont change the order of these, that would change the randomization, only add new abilities to the end
        "weaken":e.s.weakenChance,
        "freeze":e.s.freezeChance,
        "slow":e.s.slowChance,
        "knockback":e.s.kbChance,
        "warp":e.s.warpChance,
        "curse":e.s.curseChance,
        "dodge":e.s.dodgeChance,
        "strengthen":e.s.strengthenBy,
        "survive":e.s.lethal,
        "base_destroyer":e.s.baseDestroyer,
        "crit":e.s.critChance,
        "savage":e.s.savageChance,
        "wave":e.s.waveChance,
        "mini_wave":e.s.miniwave,
        "surge":e.s.surgeChance,
        "mini_surge":e.s.miniSurge,
        "explosion":e.s.explodeChance,
        "counter_surge":e.s.counterSurge,
        "wave_block":e.s.waveBlock,
        "single_atk":e.s.area,
        "area_atk":e.s.area,
        "long_distance":e.s.ldWidth,
        "omni_strike":e.s.ldWidth,
        "weaken_immune":e.s.weakImmune,
        "freeze_immune":e.s.freezeImmune,
        "slow_immune":e.s.slowImmune,
        "kb_immune":e.s.kbImmune,
        "wave_immune":e.s.waveImmune,
        "surge_immune":e.s.surgeImmune,
        "explosion_immune":e.s.explodeImmune,
        "warp_immune":e.s.warpImmune,
        "curse_immune":e.s.curseImmune,
        "toxic":e.s.toxicChance,
        "drain":e.s.drainChance,
    }
    #create a dict where each value is [weight,check,apply in first half]
    info_dict = {}
    for ability in check:
        this_info = []
        if ability in w:
            this_info.append(w[ability])
        else:
            this_info.append(0)#0 weight if it isnt in it, it should yell at you for this tho
            if log != None:
                log(ability + " not found during ab swap process config weights, this should not happen and ability will not appear")
        this_info.append(check[ability])
        if ability in bools:
            this_info.append(bools[ability])
        else:
            this_info.append(False)
            if log != None:
                log(ability + " not found during ab swap process config bools, this should not happen and ability will not appear")
        info_dict[ability] = this_info
    return (info_dict,split_at,minimum_ab_count,count_immunities,count_attack_types)

def _create_all_necessary_informations(info_dict,count_immunities,count_attack_types,second_half=False) -> Tuple[List[str],List[int],List[int],List[int]]:
    """ creates all the necessary information for this half of randomization 
    \n returns (giveable_ability_names,giveable_ability_checks,giveable_ability_weights,count_array) """
    attack_types = ["long_distance","omni_strike","multihit"]
    never_count = ["single_atk","area_atk"]
    count_array = [] #the array for all check ids involved in getting the count
    giveable_ability_weights = [] #the weights for abilities allowed to be given in this half
    giveable_ability_checks = [] #the check ids for abilities allowed to be given in this half
    giveable_ability_names = [] #the names for abilities allowed to be given in this half
    for ability in info_dict:
        #first do count since that is separate
        count_it = True
        if not second_half and not info_dict[ability][2]: #if its first half and this ability is not considered in first half 
            count_it = False
        if not count_immunities and "immune" in ability: #if its an immunity and they arent supposed to be counted
            count_it = False
        if not count_attack_types and ability in attack_types: #if its an attack type and they arent supposed to be counter
            count_it = False
        if ability in never_count: #never count single/area
            count_it = False
        if count_it:
            count_array.append(info_dict[ability][1])
        #now do all giveable abilities
        giveable = True
        if not second_half and not info_dict[ability][2]: #if its first half and not allowed in first half
            giveable = False
        #that should be the only condition right? (im putting even things with 0 weight in this)
        if giveable:
            giveable_ability_names.append(ability)
            giveable_ability_checks.append(info_dict[ability][1])
            giveable_ability_weights.append(info_dict[ability][0])
    #is there anything else to consider
    return (giveable_ability_names,giveable_ability_checks,giveable_ability_weights,count_array)

def _rand_abilities_of_half(stats:list[list[int]],minimum_ab_count:int,count_array:list[int],give_names:list[str],give_checks:list[int],give_weights:list[int],starting_id=2,ending_id=-1,post_attack_anims=[]):
    """ apply the randomized abilities to enemies within the specified range """
    #these stupid abilities are annoying
    if "single_atk" in give_names: single_index = give_names.index("single_atk")
    else: single_index = -1
    if "area_atk" in give_names: area_index = give_names.index("area_atk")
    else: area_index = -1
    if "long_distance" in give_names: ld_index = give_names.index("long_distance")
    else: ld_index = -1
    if "omni_strike" in give_names: omni_index = give_names.index("omni_strike")
    else: omni_index = -1
    #get the ending id
    if ending_id == -1:
        ending_id = len(stats)
    for u_id in range(starting_id,ending_id):
        #start by getting this units post attack time
        if len(post_attack_anims) > u_id:
            post_attack_time = post_attack_anims[u_id]
        else:
            post_attack_time = -1
        #first get the number of abilities a unit has
        count = 0
        for check in count_array:
            if stats[u_id][check] != 0:
                count += 1
        #now get this units weights
        this_w = copy.deepcopy(give_weights)
        for check_index in range(0,len(give_checks)):
            #stupid ass single/area fix
            if give_checks[check_index] == e.s.area:
                single_area_value = stats[u_id][e.s.area]
                if check_index == single_index:
                    if single_area_value == 0:
                        this_w[check_index] = 0
                if check_index == area_index:
                    if single_area_value == 1:
                        this_w[check_index] = 0
            #for all abilities that arent single/area
            elif stats[u_id][give_checks[check_index]] != 0:
                this_w[check_index] = 0 #set weight to 0 if unit already has that ability
        for x in range(0,minimum_ab_count-count): #run however many times less it is
            #now choose the index of next ability to give
            r = srand.randinst(73+34*u_id+14*x)
            chosen_index = r.weighted_list(this_w)
            #now get that name and apply it
            this_ab_name = give_names[chosen_index]
            if chosen_index == -1:
                this_ab_name = None #dont actually give it a name if it failed and it will pass through the func just fine
            stats[u_id] = _apply_ability_to_unit(stats[u_id],this_ab_name,r.randrange(0,10000),post_attack_time)
            #set that weight to 0 to stop future runs from getting it
            this_w[chosen_index] = 0
            #fix for ld/omni
            if chosen_index == ld_index and omni_index != -1:
                this_w[omni_index] = 0
            if chosen_index == omni_index and ld_index != -1:
                this_w[ld_index] = 0
    return stats

def _apply_ability_to_unit(stat:list[int],ab_name:str,random_number:int,post_attack_time=-1) -> list[int]:
    """ applies the ability of the input name to the 1D stat array and returns it
    \n random_number determines the offset to use """
    #UNGODLY FUNCTION lmao
    r = srand.randinst(random_number)
    r1 = r.randrange(0,100)
    r2 = r.randrange(0,100)
    r3 = r.randrange(0,100)
    r4 = r.randrange(0,100)
    r5 = r.randrange(0,100)
    r6 = r.randrange(0,100)
    r7 = r.randrange(0,100)
    r8 = r.randrange(0,100)
    if ab_name == "weaken":
        weak = 50
        if r1 < 10:
            weak = 10
        elif r1 < 25:
            weak = 25
        return abal._give_ability_weaken(stat,strength=5+int(r2/12),time=5+int(r3/12),weak_to=weak,post_attack_time=post_attack_time,scale_by_strength_of_weakness=True)
    elif ab_name == "freeze":
        return abal._give_ability_freeze(stat,strength=5+int(r1/12),time=5+int(r2/12),post_attack_time=post_attack_time)
    elif ab_name == "slow":
        return abal._give_ability_slow(stat,strength=5+int(r1/12),time=5+int(r2/12),post_attack_time=post_attack_time)
    elif ab_name == "knockback":
        return abal._give_ability_kb(stat,strength=5+int(r1/12),post_attack_time=post_attack_time)
    elif ab_name == "warp":
        if r4 < 15:
            backwards = True
        else:
            backwards = False
        return abal._give_ability_warp(stat,distanceness=5+int(r1/12),slowness=5+int(r2/12),likeliness=5+int(r3/12),is_backwards=backwards,post_attack_time=post_attack_time)
    elif ab_name == "curse":
        return abal._give_ability_curse(stat,strength=5+int(r1/12),time=5+int(r2/12),post_attack_time=post_attack_time)
    elif ab_name == "dodge":
        return abal._give_ability_dodge(stat,chance=5+int(r1/10),time=30+10*int(r2/20))
    elif ab_name == "strengthen":
        return abal._give_ability_strengthen(stat,strength=5+int(r1/12),earlyhood=5+int(r2/12))
    elif ab_name == "survive":
        return abal._give_ability_survive(stat,likelihood=5+int(r1/5))
    elif ab_name == "base_destroyer":
        stat[e.s.baseDestroyer] = 1
        return stat
    elif ab_name == "crit":
        return abal._give_ability_crit(stat,likelihood=5+int(r1/12),scale_attack_to_keep_dps=True,post_attack_time=post_attack_time)
    elif ab_name == "savage":
        return abal._give_ability_savage(stat,strength=5+int(r1/12),likelihood=5+int(r2/12),scale_attack_to_keep_dps=True,post_attack_time=post_attack_time)
    elif ab_name == "wave":
        return abal._give_ability_wave(stat,strength=5+int(r1/12),levelness=5+int(r2/12),likelihood=5+int(r3/12),is_miniwave=False,post_attack_time=post_attack_time)
    elif ab_name == "mini_wave":
        return abal._give_ability_wave(stat,strength=5+int(r1/12),levelness=5+int(r2/12),likelihood=5+int(r3/12),is_miniwave=True,post_attack_time=post_attack_time)
    elif ab_name == "surge":
        return abal._give_ability_surge(stat,levelness=5+int(r1/12),likelihood=5+int(r2/12),distanceness=5+int(r3/12),spawn_range_width_determiner=5+int(r4/12),is_minisurge=False,post_attack_time=post_attack_time)
    elif ab_name == "mini_surge":
        return abal._give_ability_surge(stat,levelness=5+int(r1/12),likelihood=5+int(r2/12),distanceness=5+int(r3/12),spawn_range_width_determiner=5+int(r4/12),is_minisurge=True,post_attack_time=post_attack_time)
    elif ab_name == "explosion":
        return abal._give_ability_explosion(stat,likelihood=5+int(r1/12),distanceness=5+int(r2/12),spawn_range_width_determiner=3+int(r3/11),post_attack_time=post_attack_time)
    elif ab_name == "counter_surge":
        stat[e.s.counterSurge] = 1
        return stat
    elif ab_name == "wave_block":
        stat[e.s.waveBlock] = 1
        return stat
    elif ab_name == "single_atk":
        stat[e.s.area] = 0
        return stat
    elif ab_name == "area_atk":
        stat[e.s.area] = 1
        return stat
    elif ab_name == "long_distance":
        return abal._give_ability_ld(stat,relative_size=5+int(r1/10),blindspot_size=2+int(r2/6))
    elif ab_name == "omni_strike":
        return abal._give_ability_omni(stat,relative_size=5+int(r1/10),blindspot_size=2+int(r2/6))
    elif ab_name == "weaken_immune":
        stat[e.s.weakImmune] = 1
        return stat
    elif ab_name == "freeze_immune":
        stat[e.s.freezeImmune] = 1
        return stat
    elif ab_name == "slow_immune":
        stat[e.s.slowImmune] = 1
        return stat
    elif ab_name == "kb_immune":
        stat[e.s.kbImmune] = 1
        return stat
    elif ab_name == "wave_immune":
        stat[e.s.waveImmune] = 1
        return stat
    elif ab_name == "surge_immune":
        stat[e.s.surgeImmune] = 1
        return stat
    elif ab_name == "explosion_immune":
        stat[e.s.explodeImmune] = 1
        return stat
    elif ab_name == "warp_immune":
        stat[e.s.warpImmune] = 1
        return stat
    elif ab_name == "curse_immune":
        stat[e.s.curseImmune] = 1
        return stat
    elif ab_name == "toxic":
        return abal._give_ability_toxic(stat,strength=5+int(r1/12),likelihood=5+int(r2/12),post_attack_time=post_attack_time)
    elif ab_name == "drain":
        return abal._give_ability_drain(stat,strength=5+int(r1/12),likelihood=5+int(r2/12),post_attack_time=post_attack_time)
    elif ab_name == "self_destruct":
        return abal._give_ability_self_destruct(stat,die=True,number_of_attacks=1+int(r2/12),post_attack_time=post_attack_time)
    elif ab_name == "death_surge":
        return abal._give_ability_death_surge(stat,strength=5+int(r1/12),time=5+int(r2/12),post_attack_time=post_attack_time)
    elif ab_name == "barrier":
        return abal._give_ability_barrier(stat,strength=5+int(r1/12),time=5+int(r2/12),post_attack_time=post_attack_time)
    elif ab_name == "shield":
        return abal._give_ability_shield(stat)
    print("gave a unit nothing!")
    return stat






