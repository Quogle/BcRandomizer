
import dev.randomizer.enums.enemy as e
import dev.randomizer.enums.cats as c
from dev.randomizer.func.core import randinst
from dev.randomizer.parse_config import settings
import dev.randomizer.func.files as f
import copy








ABILITIES = {
    "crit":[e.s.critChance],
    "freeze":[e.s.freezeChance,e.s.freezeTime],
    "slow":[e.s.slowChance,e.s.slowTime],
    "weaken":[e.s.weakenChance,e.s.weakenTime,e.s.weakenPercent],
    "kb":[e.s.kbChance],
    "warp":[e.s.warpChance,e.s.warpDuration,e.s.warpMin4x,e.s.warpMax4x],
    "curse":[e.s.curseChance,e.s.curseDuration],
    "dodge":[e.s.dodgeChance,e.s.dodgeDuration],
    "toxic":[e.s.toxicChance,e.s.toxicAmount],
    "savage":[e.s.savageChance,e.s.savageBoost],
    "wave":[e.s.waveChance,e.s.waveLevel],
    "surge":[e.s.surgeChance,e.s.surgeLevel,e.s.surgeStartPos,e.s.surgeWidth],
    "blast":[e.s.explodeChance,e.s.explodeAt4x,e.s.explodeVariance],
    "strengthen":[e.s.strengthenAt,e.s.strengthenBy],
    "lethal":[e.s.lethal],
    "base destroyer":[e.s.baseDestroyer]
}
CHANCE_ABILITIES = ["crit","freeze","slow","weaken","kb","warp","curse","dodge","toxic","savage","wave","surge","blast"]
BOOL_ABILITIES = ["lethal","base destroyer"]


#Ill finish this later I dont feel like working on it
def randomize_abilities(estat):
    for unit in estat:
        #gather how many abilities current unit has
        ability_number = 0
        for ability in ABILITIES:
            if unit[ABILITIES[ability]] > 0:
                ability_number += 1
        
        if ability_number == 0:
            next #dont do unit if no ability
        

        attack_cycle = unit[e.s.preatk] + unit[e.s.tba] + 1
        # sets chance to average chance or bases it on attack rate if no chance abilities
        chance_sum = 0
        chance_count = 0
        for ability in CHANCE_ABILITIES:
            if unit[ABILITIES[ability]] > 0:
                chance_sum += unit[ABILITIES[ability]]
                chance_count += 1
        chance = int(chance_sum/chance_count)
        if chance == 0:
            chance = int(100*attack_cycle/300)
        if chance > 100:
            chance = 100
        
        
        





def make_base_enemy(estat):
    """
    makes the non vanilla base enemy stats array to work off of
    """
    new_stats = copy.deepcopy(estat)
    new_stats = early_enemy_balance(new_stats)
    return new_stats

def early_enemy_balance(estat):
    """
    buff metal hp if metal removed
    give metals new traits and remove metal trait
    apply metal rework

    remove behemoth
    rebalance behemoths
    """
    remove_metals = settings["game"]["gameplay"]["remove_metals"]
    give_metal_new_trait = settings["game"]["gameplay"]["give_metals_new_trait"]
    metal_rework = settings["game"]["gameplay"]["use_metal_rework"]

    remove_behemoths = settings["game"]["gameplay"]["remove_behemoths"]
    rebalance_behemoths = settings["game"]["gameplay"]["use_behemoth_rebalance"]

    if remove_metals:
        estat = metal_hp_buffer(estat)
    if give_metal_new_trait:
        estat = metal_new_trait(estat)
    if metal_rework:
        estat = metal_rebalance(estat)
    if remove_behemoths:
        estat = behemoth_killer(estat)
    if rebalance_behemoths:
        estat = behemoth_rebalance(estat)
    
    return estat

#buffs the hp of things with metal trait
def metal_hp_buffer(estat):
    metal_hp_tipping = 1000
    low_buff = 400
    high_buff = 20
    for unit in estat:
        if unit[e.t.metal] == 1:
            if unit[e.s.hp] >= metal_hp_tipping:
                unit[e.s.hp] = int(high_buff*unit[e.s.hp])
            else:
                unit[e.s.hp] = int(low_buff*unit[e.s.hp])
    
    return estat

# sets all metals to red and then gives traits to specific ones
def metal_new_trait(estat):
    # default to giving metals red
    for unit in estat:
        if unit[e.t.metal] == 1:
            unit[e.t.metal] = 0
            unit[e.t.red] = 1
    
    # specify certain units
    specif = [
        [47,e.t.white], #metal hippoe
        [54,e.t.relic], #smh
        [56,e.t.angel], #metal one horn
        [58,e.t.black], #face
        [59,e.t.white], #seal
        [71,e.t.angel], #cycle
        [116,e.t.white], #sign
        [147,e.t.angel], #doge
        [338,e.t.angel], #rost
        [358,e.t.relic], #snache
        [359,e.t.white], #sloth
        [449,e.t.relic], #baabaa
        [497,e.t.white], #croc
        [517,e.t.relic], #kory
    ]
    for each in specif: #+2 because these are unit id not indexes
        estat[each[0]+2][e.t.red] = 0
        estat[each[0]+2][each[1]] = 1
    
    return estat

#rebalances metals, croc still needs to be added at the end
def metal_rebalance(estat):

    

    # metal doge 147
    estat[149][e.s.hp] = 20000

    #metal hippoe 47
    estat[49][e.s.hp] = 80000

    #kronium 517
    estat[519][e.s.hp] = 75000
    estat[519][e.s.tba] = 0
    estat[519][e.s.attack] = 25000
    estat[519][e.s.waveBlock] = 1
    estat[519][e.s.surgeImmune] = 1

    #metal face 58
    estat[60][e.s.hp] = 1
    estat[60][e.s.waveChance] = 100
    estat[60][e.s.dodgeChance] = 90
    estat[60][e.s.dodgeDuration] = 1
    estat[60][e.s.ldMinRange] = 240
    estat[60][e.s.ldWidth] = -560

    #metal one horn 56
    estat[58][e.s.sage] = 1
    
    #angel fanboy 116
    estat[118][e.s.speed] = 0
    estat[118][e.s.attack] = 10
    estat[118][e.s.surgeChance] = 100
    estat[118][e.s.surgeLevel] = 15
    estat[118][e.s.surgeStartPos] = 4000
    estat[118][e.s.surgeWidth] = 100
    estat[118][e.s.range] = 8000
    estat[118][e.s.dodgeChance] = 100
    estat[118][e.s.dodgeDuration] = 300
    estat[118][e.s.weakenChance] = 100
    estat[118][e.s.weakenTime] = 900
    estat[118][e.s.weakenPercent] = 50

    #smh 54
    estat[56][e.s.kbs] = 3
    estat[56][e.s.hp] = 300000


    return estat

#removes behemoth from all enemies
def behemoth_killer(estat):
    for unit in estat:
        unit[e.s.behemoth] = 0
    return estat

#rebalances most behemoths
def behemoth_rebalance(s):

    # wild doge 603
    s[605][e.s.hp] = 45000
    s[605][e.s.attack] = 12000
    s[605][e.s.surgeImmune] = 0
    s[605][e.s.lethal] = 0

    # ruck 604
    s[606][e.s.hp] = 600000
    s[606][e.s.attack] = 5000
    s[606][e.s.multiDamage2] = 5000
    s[606][e.s.multiDamage3] = 5000

    # hazuku 605
    s[607][e.s.attack] = 12000
    s[607][e.s.hp] = 1400000
    s[607][e.s.ldMinRange] = 355
    s[607][e.s.ldWidth] = 705

    # crab 606
    s[608][e.s.hp] = 1000000
    s[608][e.s.attack] = 10000
    s[608][e.s.multiDamage2] = 12000
    
    #sloth 610
    s[612][e.s.hp] = 800000
    s[612][e.s.attack] = 8000
    s[612][e.s.multiDamage2] = 10000
    s[612][e.s.multiDamage3] = 120000
    s[612][e.s.multiPreAtk2] = s[612][e.s.preatk]
    s[612][e.s.multiPreAtk3] = s[612][e.s.preatk]
    s[612][e.s.ldMinRange] = 500 #do I wanna give sloth omni tho
    s[612][e.s.ldWidth] = -500

    #bluck 611
    s[613][e.s.hp] = 1000000
    s[613][e.s.attack] = 5000
    s[613][e.s.multiDamage2] = 5000
    s[613][e.s.multiDamage3] = 5000

    #raja 613
    s[615][e.s.hp] = 1200000
    s[615][e.s.attack] = 8000
    s[615][e.s.miniwave] = 1

    #chickful 624
    s[626][e.s.hp] = 1200000
    s[626][e.s.attack] = 18000

    #reluck 627
    s[629][e.s.hp] = 1400000
    s[629][e.s.attack] = 7000
    s[629][e.s.multiDamage2] = 7000
    s[629][e.s.multiDamage3] = 10000

    #aku master a 634
    s[636][e.s.hp] = 800000
    s[636][e.s.attack] = 10000
    s[636][e.s.multiDamage2] = 15000

    #deonil 639
    s[641][e.s.hp] = 800000
    s[641][e.s.attack] = 5000

    #le boin 641
    s[643][e.s.hp] = 1200000
    s[643][e.s.attack] = 8000
    s[643][e.s.tba] = 20

    #relic leon 650
    s[652][e.s.hp] = 2600000
    s[652][e.s.attack] = 10000
    s[652][e.s.tba] = 50

    #zombie henry 652
    s[654][e.s.hp] = 400000
    s[654][e.s.attack] = 10000

    #black croc 655
    s[657][e.s.hp] = 2500000
    s[657][e.s.attack] = 25499
    
    #ganglion 659
    s[661][e.s.hp] = 2500000
    s[661][e.s.tba] = 125

    #bunslios 714 idk what to do with this man
    s[716][e.s.hp] = 2800000
    s[716][e.s.attack] = 36000
    



    return s

#currently just rebalances croc, kronium still unfinished
def late_enemy_balance(estat):
    """
    croc/kronium
    maybe put leave modded unchanged in here
    """
    #croc 497
    estat[499][e.t.metal] = 1
    estat[499][e.s.hp] = 5
    estat[499][e.s.tba] = 0

    #kronium
    #idk what Im gonna do for this mf yet

    return estat

"""
rando or swap traits
"""

def create_enemy_trait_map():
    """
    creates the enemy trait map, conditional, uses base ennemy array for now
    """
    rando_mode = settings["enemy"]["traits"]["mode"]
    enemy_map = []
    if rando_mode == "swap":
        enemy_map = get_swap(base_enemy_array)
    if rando_mode == "randomize":
        enemy_map = get_randomization_map(base_enemy_array)
    
    return enemy_map

def get_swap(stats):
    """
    makes the swap map
    """
    r = randinst(200)
    remove_metals = settings["game"]["gameplay"]["remove_metals"]
    traits = [e.t.black,e.t.red,e.t.white,e.t.floating,e.t.relic,e.t.zombie,e.t.alien,e.t.angel,e.t.aku,e.t.metal]
    text_traits = ["black","red","white","floating","relic","zombie","alien","angel","aku","metal"]
    
    #gets set ones from config
    specified_swap_texts = settings["enemy"]["traits"]["specified_swaps"]
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
    for x in range(0,len(temp_tl)):
        current_trait_order.append(temp_tl.pop(r.randrange(0,len(temp_tl))))
    
    # get missing traits, put dually missing in first
    missing_from = []
    missing_to = []
    for trait in current_trait_order:
        if trait not in user_from and trait not in user_to:
            missing_from.append(trait)
            missing_to.append(trait)
    for trait in current_trait_order:
        if trait not in user_from and trait not in missing_from:
            missing_from.append(trait)
        if trait not in user_to and trait not in missing_to:
            missing_to.append(trait)
    
    #make sure there is a trait per missing from
    while len(missing_to) < len(missing_from):#fill out missing to with matching trait from missing from
        missing_index = len(missing_to)
        missing_to.append(missing_from[missing_index])
    
    try: #set shift
        shift = r.randrange(1,len(missing_from)-1)
    except:
        shift = 1
    
    #now rotate missing to, ifed to prevent breakage if missings are 0 length
    if len(missing_from) > 0:
        for x in range(0,shift):
            missing_to.append(missing_to.pop(0))
    
    #kill metals only if not in specified swap
    if remove_metals:
        index = 0
        if current_trait_order[0] == e.t.metal:
            index = 1
        for x in range(0,len(missing_to)):
            if missing_to[x] == e.t.metal:
                missing_to[x] = current_trait_order[index]
    
    #combine user specified swaps with generated swaps
    total_from = copy.deepcopy(user_from)
    total_to = copy.deepcopy(user_to)
    for x in range(0,len(missing_from)):
        total_from.append(missing_from[x])
        total_to.append(missing_to[x])
    
    map_to_return = [] #create map to return
    for x in range(0,len(stats)):
        map_to_return.append([total_from,total_to])
    return map_to_return
    
def get_randomization_map(stats):
    """
    creates a map from stats
    """
    remove_metals = settings["game"]["gameplay"]["remove_metals"]
    trait_list = [e.t.black,e.t.red,e.t.white,e.t.floating,e.t.relic,e.t.zombie,e.t.alien,e.t.angel,e.t.aku,e.t.metal]
    r = randinst(200)
    map_to_return = []
    for unit_id in range(0,len(stats)):
        #get units trait order
        current_trait_order = []
        temp_tl = copy.deepcopy(trait_list)
        for x in range(0,len(temp_tl)):
            current_trait_order.append(temp_tl.pop(r.randrange(0,len(temp_tl))))
        #get traits a unit has
        has_traits = []
        for each in current_trait_order:
            if stats[unit_id][each] == 1:
                has_traits.append(each)
        #fill from traits with remaining traits unit doesnt have
        from_traits = copy.deepcopy(has_traits)
        for each in current_trait_order:
            if each not in from_traits:
                from_traits.append(each)
        #rotate to traits by len has traits (blocks duplicates)
        to_traits = copy.deepcopy(from_traits)
        for x in range(0,len(has_traits)):
            to_traits.append(to_traits.pop(0))
        
        if remove_metals: #change metals to the first trait a unit wont receive
            index = len(has_traits)
            if to_traits[index] == e.t.metal:
                index += 1
            if index >= len(to_traits):
                index = 0
            for each in range(0,len(to_traits)):
                if to_traits[each] == e.t.metal:
                    to_traits[each] = to_traits[index]
        
        map_to_return.append([from_traits,to_traits])
    
    return map_to_return
        
def do_traits(stats):
    """
    applies trait map to stats, also applied trait exceptions
    """
    enemy_map = create_enemy_trait_map()
    if len(enemy_map) > 0:
        #create stats devoid of traits
        new_stats = copy.deepcopy(stats)
        for unit in new_stats:
            for trait in e.t:
                unit[trait] = 0
        
        #apply map to stats
        for unit_id in range(0,len(new_stats)):
            for trait in range(0,len(enemy_map[unit_id][0])):
                old_trait = enemy_map[unit_id][0][trait]
                new_trait = enemy_map[unit_id][1][trait]
                if new_stats[unit_id][old_trait] == 1:
                    new_stats[unit_id][new_trait] = 1

        #set new stats as stats
        stats = new_stats
    stats = trait_exceptions(stats) #applies the forced traits
    return stats


"""
trait gimmicks
"""

def black_gimmick(estat):
    """
    does all the black kb speed shit, interprets config and has defaults of +3 and 1.5x
    """
    black_info = settings["game"]["traits"]["gimmicks"]["black"]
    if black_info["enabled"]:
        speed_info = black_info["speed_boost"]
        round_down = black_info["rounds_down"]
        kb_boost = black_info["kb_mult"]
        #first of each entry in speed buff is the speed after which it flips, second is how much to buff
        speed_buff = []
        for each in speed_info:
            try:
                speed_flip = int(each[1])
                speed_by = each[0]
                speed_buff.append([speed_flip,speed_by])
            except:
                pass

        for unit in estat:
            if unit[e.t.black] == 1:
                boosted = False
                current_speed = unit[e.s.speed]
                for each in speed_buff:
                    if current_speed <= each[0] and not boosted:
                        # if mult, get mult and do rounding
                        if "x" in each[1]:
                            speed_mult = each[1].replace("x","")
                            try:
                                speed_mult = float(speed_mult)
                            except:
                                speed_mult = 1.5
                            
                            new_speed = speed_mult*current_speed
                            #round up or down
                            if new_speed != int(new_speed):
                                if not round_down:
                                    new_speed = int(new_speed+1)
                            new_speed = int(new_speed)
                            
                        else: #increase speed additively, default 3 if unreadable
                            try:
                                speed_boost = int(float(each[1]))
                            except:
                                speed_boost = 3
                            new_speed = current_speed + speed_boost
                        
                        #set speed as new seed and stop further boosting
                        unit[e.s.speed] = new_speed
                        boosted = True
                #kb boost
                #get kb boost
                try:
                    kb_boost = float(kb_boost)
                except:
                    kb_boost = 1.5
                
                new_kbs = unit[e.s.kbs]*kb_boost
                if int(new_kbs) != new_kbs:
                    if not round_down:
                        new_kbs = int(new_kbs+1)
                new_kbs = int(new_kbs)
            
                unit[e.s.kbs] = new_kbs
    
    return estat

def red_gimmick(estat):
    """
    applies red speed and kb down, conditional, default x0.8 sp and x0.5 kb
    """
    red_info = settings["game"]["traits"]["gimmicks"]["red"]
    do_red = red_info["enabled"]
    speed_mult = red_info["speed_mult"]
    kb_mult = red_info["kb_mult"]
    round_down = red_info["rounds_down"]

    if do_red:
        for unit in estat:
            if unit[e.t.red] == 1:
                unit_speed = unit[e.s.speed]
                unit_kb = unit[e.s.kbs]

                new_speed = unit_speed*speed_mult
                new_kb = unit_kb*kb_mult

                if not round_down:
                    if new_speed != int(new_speed):
                        new_speed += 1
                    if new_kb != int(new_kb):
                        new_kb += 1
                
                new_speed = int(new_speed)
                new_kb = int(new_kb)

                if new_speed == 0:
                    new_speed = 1
                if new_kb == 0:
                    new_kb = 1

                unit[e.s.speed] = new_speed
                unit[e.s.kbs] = new_kb

    return estat

def white_gimmick(estat):
    """
    gives whites sage, does nothing else
    """
    white_info = settings["game"]["traits"]["gimmicks"]["white"]
    do_white = white_info["enabled"]
    white_sages = white_info["whites_are_sage"]

    if do_white:
        for unit in estat:
            if unit[e.t.white]:
                unit[e.s.sage] = 1
    
    return estat

def floating_gimmick(estat):
    """
    applies a floating immunity, defaults of 20% extra ability chance and 5,5,5,3 wb as 3
    """
    r = randinst(47)
    floating_info = settings["game"]["traits"]["gimmicks"]["white"]
    do_floating = floating_info["enabled"]
    wi_weight = floating_info["wave_immune_weight"]
    si_weight = floating_info["surge_immune_weight"]
    cs_weight = floating_info["counter_surge_weight"]
    wb_weight = floating_info["wave_block_weight"]
    duo = floating_info["dual_ability_chance"]

    weights = [wi_weight,si_weight,cs_weight,wb_weight]
    
    if do_floating:
        for unit in estat:
            if unit[e.t.floating] == 1:

                #figure out if its duo
                chance = r.randrange(0,100)
                times = 1
                if chance < duo:
                    times = 2
                #this scheme of making it duo doesnt actually make it have the correct chance since it fails to block repeats but idc
                for x in range(0,times):
                    choice = r.weighted_list(weights)

                    if choice == 0:
                        unit[e.s.waveImmune] = 1
                    elif choice == 1:
                        unit[e.s.surgeImmune] = 1
                    elif choice == 2:
                        unit[e.s.counterSurge] = 1
                    elif choice == 3:
                        unit[e.s.waveBlock] = 1
    
    return estat

def relic_gimmick(estat):
    """
    gives relics curse and pierce if able
    """
    r = randinst(46)
    relic_info = settings["game"]["traits"]["gimmicks"]["relic"]
    do_relic = relic_info["enabled"]
    get_curse = relic_info["get_curse"]
    get_pierce = relic_info["get_weak_pierce"]
    pierce_damage = relic_info["pierce_atk_percent"]
    pierce_rate = relic_info["pierce_range_percent"]

    if do_relic:
        for unit in estat:
            #shitty future proofing
            rand1 = r.randrange(80,120)
            rand2 = r.randrange(80,120)
            if unit[e.t.relic] == 1:

                if get_curse:
                    attack_rate = unit[e.s.tba] + unit[e.s.preatk]
                    if attack_rate < 10:
                        attack_rate += 20
                    #maybe I could get the post attack animations from somewhere

                    curse_chance = 15+attack_rate/3
                    curse_duration = 30+attack_rate
                    #adjust them by an amount
                    curse_chance = int(curse_chance*rand1)
                    curse_duration = int(curse_duration*rand2)

                    if curse_chance > 100:
                        curse_chance = 100
                    
                    unit[e.s.curseChance] = curse_chance
                    unit[e.s.curseDuration] = curse_duration
                
                if get_pierce: #only do it to single attack non ld units
                    if unit[e.s.multiDamage2] == 0 and unit[e.s.ldWidth] == 0:
                        #damage portion
                        attack = unit[e.s.attack]
                        second_damage = int(attack*pierce_damage/100)
                        first_damage = int(attack-second_damage)
                        unit[e.s.attack] = first_damage
                        unit[e.s.multiDamage2] = second_damage
                        unit[e.s.multiPreAtk2] = unit[e.s.preatk]

                        #range portion
                        base_range = unit[e.s.range]
                        second_range = int(base_range*(1+pierce_rate/100))
                        first_range = -320 - base_range
                        second_range += 320
                        #set
                        unit[e.s.multiHasLdRange2] = 1
                        unit[e.s.multiLdStart2] = -320
                        unit[e.s.multiLdWidth2] = second_range


                        unit[e.s.ldMinRange] = base_range
                        unit[e.s.ldWidth] = first_range

                        unit[e.s.multiHasAbility1] = 1
                        unit[e.s.multiHasAbility2] = 2
    
    return estat

def zombie_gimmick(estat):
    """
    gives zombies without revive burrow/revive, does not use a normal weight system
    """               
    r = randinst(49)
    z_info = settings["game"]["traits"]["gimmicks"]["zombie"]
    do_z = z_info["enabled"]
    z_balance = z_info["balanced"]
    grant_rev = z_info["grant_revive"]
    rev_freq = z_info["revive_frequency"]
    rev_types = z_info["revive_types"]
    grant_burrow = z_info["grant_burrow"]
    burrow_freq = z_info["burrow_frequency"]
    burrow_types = z_info["burrow_types"]

    if do_z:
        #get weight list totals
        rev_total = 0
        for each in rev_types:
            rev_total += each[3]
        burrow_total = 0
        for each in burrow_types:
            burrow_total += each[2]
        
        for unit in estat:
            #get the values first to make it unaffected if what is or isnt a zombie changes
            rev_decider = r.randrange(0,rev_total)
            burrow_decider = r.randrange(0,burrow_total)
            has_rev = r.randrange(0,100)
            has_burrow = r.randrange(0,100)
            time_mult = r.randrange(7,14)
            if unit[e.t.zombie] == 1 and unit[e.s.revive] == 0:
                #calc zombie strength
                strength = 0
                if unit[e.s.hp] >= 200000:
                    strength += 1
                if unit[e.s.hp] >= 800000:
                    strength += 1
                if unit[e.s.range] >= 600:
                    strength += 1
                if strength == 0 and unit[e.s.range] >= 400:
                    strength += 1
                if strength == 0:
                    strength = -3
                if not z_balance: #this is what stops rebalance from doing anything
                    strength = 0
                
                #shift that thang!!!!, made burrow weaker for both super strong and weak enemies, supposedly
                BURROW_SHIFT = 20
                REVIVE_SHIFT = -20
                rev_decider += int(REVIVE_SHIFT/100 * rev_total * strength/3)
                burrow_decider += int(BURROW_SHIFT/100 * burrow_total * abs(strength/3))

                if has_rev < rev_freq and grant_rev:
                    #default to last rev, loop through decreasing revdec till its less than current weight
                    index = -1
                    for each in range(0,len(rev_types)):
                        if rev_decider < rev_types[each][-1]:
                            index = each
                            break
                        else:
                            rev_decider -= rev_types[each][-1]
                    
                    revive = rev_types[index]
                    unit[e.s.revive] = revive[0]
                    unit[e.s.reviveHp] = revive[1]
                    unit[e.s.reviveTime] = int(revive[2]*time_mult/10)
                
                if has_burrow < burrow_freq and grant_burrow:
                    index = -1
                    for each in range(0,len(burrow_types)):
                        if burrow_decider < burrow_types[each][-1]:
                            index = each
                            break
                        else:
                            burrow_decider -= burrow_types[each][-1]
                    
                    burrow = burrow_types[index]
                    unit[e.s.burrow] = burrow[0]
                    unit[e.s.burrowLength] = burrow[1]
    
    return estat
                    
def alien_gimmick(estat):
    """
    does the alien shit yo, does give starred aliens the flag
    """               
    r = randinst(63)
    a_info = settings["game"]["traits"]["gimmicks"]["alien"]
    do_a = a_info["enabled"]
    freeze_weight = a_info["freeze_weight"]
    slow_weight = a_info["slow_weight"]
    kb_weight = a_info["kb_weight"]
    weak_weight = a_info["weak_weight"]
    wave_weight = a_info["wave_weight"]
    surge_weight = a_info["surge_weight"]
    explode_weight = a_info["explode_weight"]
    crit_weight = a_info["crit_weight"]
    savage_weight = a_info["savage_weight"]
    lethal_weight = a_info["lethal_weight"]
    base_des_weight = a_info["base_des_weight"]
    multihit_weight = a_info["multihit_weight"]
    
    starred_freq = a_info["starred_frequency"]
    warp_freq = a_info["warp_frequency"]
    barrier_freq = a_info["barrier_frequency"]


    STAR_SECOND_ABILITY = 20 #this could be added to the config

    if do_a:
        #make weight lists
        abilities = [freeze_weight,slow_weight,kb_weight,weak_weight,wave_weight,surge_weight,explode_weight,crit_weight,savage_weight,lethal_weight,base_des_weight,multihit_weight]
        ability_weight_total = 0
        for each in abilities:
            ability_weight_total += each
        
        for unit_id in range(0,len(estat)):
            #assign random numbers here
            star = r.randrange(0,100)
            warp_barr = r.randrange(0,100)
            starred_ability = r.randrange(0,100)
            ability_strength = r.randrange(0,100)
            duration_mult = r.randrange(6,15)
            barrier_hp_mult = r.randrange(0,11)
            ability = r.weighted_list(abilities)
            warp_dec = r.randrange(0,100)
            barr_dec = r.randrange(0,100)
            strong_barr = r.randrange(0,5)
            


            if estat[unit_id][e.t.alien] == 1:
                #find unit stats here, maybe add post attack anim here
                attack_cycle = estat[unit_id][e.s.tba]
                if attack_cycle == 0:
                    attack_cycle += 10
                attack_cycle += estat[unit_id][e.s.preatk]
                base_chance = attack_cycle/300
                base_duration = attack_cycle*duration_mult/10
                

                done_starred = False
                if star < starred_freq:
                    done_starred = True
                    estat[unit_id][e.s.starred_god] == 1
                    if warp_barr < warp_freq:
                        estat[unit_id] = apply_warp(estat[unit_id],warp_dec,attack_cycle)

                    if warp_barr >= (100-barrier_freq):
                        estat[unit_id] = apply_barrier(estat[unit_id],barr_dec,strong_barr,barrier_hp_mult)

                #untrip marked as starred completed
                if starred_ability < STAR_SECOND_ABILITY:
                    done_starred = False
                
                # normal alien abilities
                if not done_starred:
                    estat[unit_id] = apply_ability(estat[unit_id],base_chance,base_duration,ability,ability_strength)

    return estat

def angel_gimmick(estat):
    """
    increases angel speed and hp, reduces attack
    """
    a_info = settings["game"]["traits"]["gimmicks"]["angel"]
    do_a = a_info["enabled"]
    balance = a_info["balanced"]
    speed_mult = a_info["speed_mult"]
    attack_mult = a_info["attack_mult"]
    health_mult = a_info["health_mult"]
    round_up = a_info["round_up"]
    BALANCE_AT = 2000000

    if do_a:
        for unit in estat:
            speed_by = speed_mult-1
            health_by = health_mult-1
            if unit[e.s.hp] >= BALANCE_AT and balance:
                speed_by /= 2
                health_by /= 2
            
            speed = unit[e.s.speed] * (1+speed_by)
            health = unit[e.s.hp] * (1+health_by)
            attack = unit[e.s.attack] * attack_mult
            second = unit[e.s.multiDamage2] * attack_mult
            third = unit[e.s.multiDamage3] * attack_mult
            if round_up:
                if speed != int(speed):
                    speed += 1
                if health != int(health):
                    health + 1
                if attack != int(attack):
                    attack += 1
                if second != int(second):
                    second += 1
                if third != int(third):
                    third += 1
            
            unit[e.s.speed] = int(speed)
            unit[e.s.hp] = int(health)
            unit[e.s.attack] = int(attack)
            unit[e.s.multiDamage2] = int(second)
            unit[e.s.multiDamage3] = int(third)


    return estat

def aku_gimmick(estat):
    """
    gives shield and ds
    """
    r= randinst(93)
    a_info = settings["game"]["traits"]["gimmicks"]["aku"]
    do_a = a_info["enabled"]
    shield_freq = a_info["shield_frequency"]
    death_freq = a_info["death_frequency"]
    ds_ability_freq = a_info["ds_ability_frequency"]
    ds_mini = a_info["ds_ability_is_mini"]

    if do_a:
        for unit in range(0,len(estat)):
            aku_ability_dec = r.randrange(0,100)
            ds_ab_dec = r.randrange(0,100)
            ds_ab_type = r.randrange(0,100)
            ds_lvl = r.randrange(0,100)
            ds_range = r.randrange(0,100)
            if estat[unit][e.t.aku] == 1:
                give_ability = False
                if ds_ab_dec < ds_ability_freq:
                    give_ability = True
                
                if aku_ability_dec < shield_freq:
                    estat[unit] = apply_shield(estat[unit])
                if aku_ability_dec > (100-death_freq):
                    estat[unit] = apply_death_surge(estat[unit],ds_lvl,give_ability,ds_ab_type,ds_mini,ds_range)
    return estat

def gimmick_total(estat):
    """
    applies all gimmicks conditionally from config
    """
    do_gimmicks = settings["enemy"]["traits"]["gimmicks"]["enabled"]
    if do_gimmicks: #aside from black before red there was never an order of op before
        estat = black_gimmick(estat)
        estat = red_gimmick(estat)
        estat = white_gimmick(estat)
        estat = floating_gimmick(estat)
        estat = relic_gimmick(estat)
        estat = zombie_gimmick(estat)
        estat = alien_gimmick(estat)
        estat = angel_gimmick(estat)
        estat = aku_gimmick(estat)
        estat = gimmick_exceptions(estat)
    return estat

"""
parts of gimmick
"""

def apply_shield(stats):
    """
    gives shield, nonconditional
    """
    kb = stats[e.s.kbs]
    hp = stats[e.s.hp]

    #default barrier to 5k for most enemies
    barrier_health = 0
    if hp > 5000:
        barrier_health = 5000
    regen_at = 100
    #1 30%,2 20%,3 15%,>24 15%, else 10%    (2 and else 50%)
    if kb == 1:
        barrier_health += hp*0.3
    elif kb == 2:
        barrier_health += hp*0.2
        regen_at = 50
    elif kb == 3:
        barrier_health += hp*0.15
    elif kb > 24:
        barrier_health += hp*0.15
    else:
        barrier_health += hp*0.1
        regen_at = 50
    
    stats[e.s.shieldHp] = int(barrier_health)
    stats[e.s.shieldRegenPercent] = regen_at

    return stats

def apply_death_surge(stats,ds_lvl,has_ability,ds_ab,mini,ds_range):
    """
    applies aku death surge to stats and returns it, nonconditional
    """
    ds_chance = 100
    if stats[e.s.hp] < 10000:
        ds_chance = 50

    ds_level = 1
    if ds_lvl > 75:
        ds_level = 2
    if ds_lvl > 92:
        ds_level = 3

    #add 50 if range below 120, mult by 3.5, add either ~370 or 600
    ds_start = stats[e.s.range]
    if ds_start < 120:
        ds_start += 50
    ds_start = ds_start*3.5 + 1400
    if ds_range > 60:
        ds_start += 1000
    ds_start = int(ds_start)

    ds_variation = 0
    #wild pattern
    if ds_range > 95:
        ds_variation = 6000
        ds_start = -800
        ds_chance = 100

    
    stats[e.s.deathSurgeChance] = ds_chance
    stats[e.s.deathSurgeLevel] = ds_level
    stats[e.s.deathSurgeStartPos] = ds_start
    stats[e.s.deathSurgeWidth] = ds_variation
    
    #verify unit has no abilities
    abilities = [e.s.freezeChance,e.s.slowChance,e.s.kbChance,e.s.weakenChance,e.s.waveChance,e.s.surgeChance,e.s.explodeChance,e.s.critChance,e.s.savageChance,e.s.warpChance,e.s.curseChance]
    count = 0
    for each in abilities:
        if stats[each] > 0:
            count += 1
    
    if has_ability and count == 0 and stats[e.s.multiDamage2] == 0:
        #give mini or force level 1
        if mini:
            stats[e.s.miniSurge] = 1
        else:
            stats[e.s.deathSurgeLevel] = 1
        
        savage_chance = 0
        savage_boost = 0

        #abilities
        if ds_ab < 10:
            savage_chance = 20
            savage_boost = 300
        elif ds_ab < 25:
            savage_chance = 50
            savage_boost = 100
        elif ds_ab < 45:
            stats[e.s.freezeChance] = 100
            stats[e.s.freezeTime] = 60
        elif ds_ab < 65:
            stats[e.s.slowChance] = 100
            stats[e.s.slowTime] = 120
        elif ds_ab < 85:
            stats[e.s.weakenChance] = 100
            stats[e.s.weakenTime] = 180
            stats[e.s.weakenPercent] = 50
        else:
            stats[e.s.kbChance] = 100
        
        #currently makes it so if mini ds does 1.6x instead of 2x and 4.4x instead of 4x
        if mini:
            savage_boost = savage_boost * 7
        
        stats[e.s.savageBoost] = int(savage_boost)
        stats[e.s.savageChance] = savage_chance

        #all dat shit that gotta be done to make this work
        stats[e.s.multiDamage2] = stats[e.s.attack]
        stats[e.s.multiHasAbility2] = 0
        stats[e.s.multiHasAbility1] = 1
        stats[e.s.multiPreAtk2] = stats[e.s.preatk]
        stats[e.s.preatk] = -1

    return stats

def apply_warp(stats,warp_dec,attack_cycle):
    """
    gives warp, nonconditional
    """
    #block 80 and above from below 50k hp units
    if warp_dec >= 80 and stats[e.s.hp] < 50000:
        warp_dec -= 20

    base_chance = 15
    distance = 2
    time = 20
    if warp_dec < 10:
        distance = 2
        time = 10
    elif warp_dec < 20:
        distance = 2
        time = 20
    elif warp_dec < 35:
        distance = 1
        time = 20
        base_chance = 30
    elif warp_dec < 50:
        distance = 3
        time = 40
    elif warp_dec < 65:
        distance = 3
        time = 10
    elif warp_dec < 80:
        distance = 4
        time = 10
    elif warp_dec < 88:
        distance = 60
        time = 40
    elif warp_dec < 94:
        distance = -2
        time = 20
    elif warp_dec < 100:
        distance = 0.2
        time = 5

    stats[e.s.warpChance] = clamp_value(base_chance+attack_cycle/300)
    stats[e.s.warpDuration] = int(attack_cycle*time/10)
    stats[e.s.warpMin4x] = int(distance*stats[e.s.range])
    stats[e.s.warpMax4x] = int(distance*stats[e.s.range])

    return stats

def apply_barrier(stats,bar_dec,strong_bar,bar_hp_mult):
    """
    gives cat barrier, non conditional
    """
    #block strong barriers from weak enemies
    if stats[e.s.hp] < 50000 and bar_dec > 75:
        bar_dec -= 25
    if stats[e.s.hp] < 10000:
        strong_bar = 0
    
    #10% shitter, 40% 3k, 40% 6k, 10% 15k (these are then mult by 1-2x, 15k locked from weaks)
    barhp = 0
    if bar_dec < 10:
        barhp = 10
    elif bar_dec < 50:
        barhp = 3000
    elif bar_dec < 90:
        barhp = 6000
    else:
        barhp = 15000
    
    barhp *= (1+bar_hp_mult/10)
    if strong_bar > 90: #strong barrier makes it 10x stronger
        barhp *= 10

    stats[e.s.barrierHp] = int(barhp)

    return stats

def apply_ability(stats,chance,duration,ability,ability_strength):
    """
    applies the normal alien abilities to a stat line, nonconditional
    """
    count = 0
    while True:
        count += 1
        if ability == 12: #the loop part
            ability = 0
        
        if count > 1:
            pass #do doubling here
        if ability == 0:
            if stats[e.s.freezeChance] > 0:
                ability += 1
            else:
                stats[e.s.freezeChance] = clamp_value(5+chance/1.5)
                stats[e.s.freezeTime] = int(30+duration/1.4)
        if ability == 1:
            if stats[e.s.slowChance] > 0:
                ability += 1
            else:
                stats[e.s.slowChance] = clamp_value(15+chance/1.5)
                stats[e.s.slowTime] = int(30+duration)
        if ability == 2:
            if stats[e.s.kbChance] > 0:
                ability += 1
            else:
                stats[e.s.kbChance] = clamp_value(15+chance/1.2)
        if ability == 3:
            if stats[e.s.weakenChance] > 0:
                ability += 1
            else:
                stats[e.s.weakenChance] = clamp_value(5+duration/1.5)
                if ability_strength < 30:
                    stats[e.s.weakenPercent] = 10
                    stats[e.s.weakenTime] = int(50+duration/2)
                else:
                    stats[e.s.weakenPercent] = 50
                    stats[e.s.weakenTime] = int(20+duration*1.5)
        if ability == 4:
            if stats[e.s.waveChance] > 0:
                ability += 1
            else:
                wave_level = 10
                if ability_strength < 60:
                    wave_level = 1
                elif ability_strength < 80:
                    wave_level = 2
                elif ability_strength < 90:
                    wave_level = 3
                stats[e.s.waveLevel] = wave_level
                wave_chance = clamp_value(2+((chance/250)**2)*80)
                stats[e.s.waveChance] = wave_chance
                #keep dps the same for all attacks, except reduce it by 5% per wave level
                if stats[e.s.multiHasAbility1] == 1:
                    stats[e.s.attack] = int(stats[e.s.attack] * (100-5*wave_level)/(100+wave_chance))
                if stats[e.s.multiHasAbility2] == 1:
                    stats[e.s.multiDamage2] = int(stats[e.s.multiDamage2] * (100-5*wave_level)/(100+wave_chance))
                if stats[e.s.multiDamage3] == 1:
                    stats[e.s.multiDamage3] = int(stats[e.s.multiDamage3] * (100-5*wave_level)/(100+wave_chance))

        if ability == 5:
            if stats[e.s.surgeChance] > 0:
                ability += 1
            else: #prob needs a dps reducer
                stats[e.s.surgeChance] = clamp_value(5+((chance/300)**2)*100)
                stats[e.s.surgeWidth] = 0
                if ability_strength < 80:
                    stats[e.s.surgeLevel] = 1
                    stats[e.s.surgeStartPos] = int(3.5*stats[e.s.range])
                else:
                    stats[e.s.surgeLevel] = 3
                    stats[e.s.surgeStartPos] = int(1.5*stats[e.s.range])
        if ability == 6:
            if stats[e.s.explodeChance] > 0:
                ability += 1
            else: #prob needs a dps reducer
                stats[e.s.explodeChance] = clamp_value(5+((chance/400)**2)*80)
                stats[e.s.explodeAt4x] = int(3*stats[e.s.range] - 75)
        if ability == 7:
            if stats[e.s.critChance] > 0:
                ability += 1
            else:
                stats[e.s.critChance] = clamp_value(10+chance)
        if ability == 8:
            if stats[e.s.savageChance] > 0:
                ability += 1
            else:
                savage_chance = clamp_value(55+chance/2) - 50
                if ability_strength < 50:
                    stats[e.s.savageChance] = int(savage_chance)
                    stats[e.s.savageBoost] = 200
                else:
                    stats[e.s.savageChance] = int(savage_chance/2)
                    stats[e.s.savageBoost] = 300
                stats[e.s.attack] = int(stats[e.s.attack] * (100-savage_chance)/100)
                stats[e.s.multiDamage2] = int(stats[e.s.multiDamage2] * (100-savage_chance)/100)
                stats[e.s.multiDamage3] = int(stats[e.s.multiDamage3] * (100-savage_chance)/100)
        if ability == 9:
            if stats[e.s.lethal] > 0:
                ability += 1
            else:
                stats[e.s.lethal] = 100
        if ability == 10:
            if stats[e.s.baseDestroyer] > 0:
                ability += 1
            else:
                stats[e.s.baseDestroyer] = 1
        if ability == 11:
            if stats[e.s.multiDamage2] > 0:
                ability += 1
            else:
                damage = stats[e.s.attack]
                preatk = stats[e.s.preatk]
                stats[e.s.multiHasAbility2] = 1
                if ability_strength < 50: #50 50 damage split
                    stats[e.s.attack] = int(stats[e.s.attack] - int(damage/2))
                    stats[e.s.multiDamage2] = int(damage/2)
                    stats[e.s.multiPreAtk2] = int(preatk + 6)
                else: #shift 40% onto other two attacks
                    damage = int(damage/5)
                    stats[e.s.attack] = int(stats[e.s.attack]-2*damage)
                    stats[e.s.multiDamage2] = damage
                    stats[e.s.multiDamage3] = damage
                    stats[e.s.multiHasAbility3] = 1
                    stats[e.s.multiPreAtk2] = int(preatk+3)
                    stats[e.s.multiPreAtk3] = int(preatk+6)
        if ability != 12:
            break
        if count > 1: #double if all else failed
            ability_chances = [e.s.freezeChance,e.s.slowChance,e.s.kbChance,e.s.weakenChance,e.s.critChance,e.s.lethal,e.s.savageChance]
            for each in ability_chances:
                stats[each] = clamp_value(stats[each]*2)
            break

    return stats



def trait_exceptions(estat):
    """
    applies force traits and exceptions before gimmicks, conditional
    """
    exceptions = settings["enemy"]["exceptions"]
    force = settings["enemy"]["force_traits"]
    johnny = exceptions["johnny"]
    poultrio = exceptions["poultrio"]
    doge = force["tad_type_apk"]
    squirrel = force["dab_type_apk"]
    bluck = force["amph_type_apk"]
    red_face = force["ryelo_type_apk"]
    nu_metal = settings["game"]["gameplay"]["remove_metals"]

    traits = [t for t in e.t]
    if nu_metal:
        try:
            traits.remove(e.t.metal)
        except:
            pass
    
    for trait in traits:
        if johnny:
            estat[523][trait] = 1
        if poultrio:
            estat[771][trait] = 1
        if doge:
            estat[2][trait] = 0
        if squirrel:
            estat[17][trait] = 0
        if bluck:
            estat[38][trait] = 0
        if red_face:
            estat[19][trait] = 0
    
    if doge:
        estat[2][e.t.alien] = 1
    if squirrel:
        estat[17][e.t.angel] = 1
    if bluck:
        estat[38][e.t.aku] = 1
    if red_face:
        estat[19][e.t.alien] = 1
    
    return estat

def gimmick_exceptions(estat):
    """
    applies post gimmick exceptions from config
    """
    exceptions = settings["enemy"]["exceptions"]
    doge = exceptions["doge"]
    brollow = exceptions["brollow"]
    squirrel = exceptions["squirrel"]
    red_face = settings["enemy"]["force_traits"]["ryelo_type_apk"]
    remove_crystals = settings["game"]["gameplay"]["remove_itf_crystals"]

    if doge:
        if not remove_crystals:
            estat[2][e.s.attack] = 1
        estat[2][e.s.area] = 1
        estat[2][e.s.attackOnce] = 1
        estat[2][e.s.selfDestruct] = 2
        estat[2][e.s.ldMinRange] = -320
        estat[2][e.s.ldWidth] = 1320
        estat[2][e.s.freezeChance] = 100
        estat[2][e.s.freezeTime] = 120
    
    if squirrel:
        estat[17][e.s.explodeChance] = 35
        estat[17][e.s.explodeAt4x] = 1400
        estat[17][e.s.explodeVariance] = 800
        estat[17][e.s.explodeImmune] = 1
        estat[17][e.s.kbChance] = 100
    
    if brollow: #set stats based trait, some of these are less interesting
        brol = estat[209]
        r = randinst(10)



        if brol[e.t.black] == 1: #applies double the speed boost
            speed_info = settings["enemy"]["traits"]["gimmicks"]["black"]["speed_boost"]
            last_speed = speed_info[-1]
            mult = False
            if "x" in last_speed:
                last_speed.replace("x","")
                mult = True
            try:
                speed = float(last_speed)
            except:
                speed = 1.5
            
            if mult:
                brol[e.s.speed] = int(99*(1+(speed-1)*2))
            else:
                brol[e.s.speed] = int(99 + 80) #just adds 80 for now
        
        if brol[e.t.red] == 1: #multiplies health by reduced kb ratio
            brol[e.s.hp] = int(19000 * 10/brol[e.s.kbs])
        
        if brol[e.t.white] == 1: #idk
            pass
        
        if brol[e.t.floating] == 1: #immune to wavess and counters surge
            brol[e.s.waveImmune] = 1
            brol[e.s.counterSurge] = 1
        
        if brol[e.t.relic] == 1: # gets 1/5 of second hits damage as pierce additional 100 range, increases curse chance as a result
            brol[e.s.multiHasAbility3] = 1
            brol[e.s.multiDamage3] = int(brol[e.s.multiDamage2]/5)
            brol[e.s.multiDamage2] = int(brol[e.s.multiDamage2] - brol[e.s.multiDamage3])
            brol[e.s.multiLdStart3] = -320
            brol[e.s.multiLdWidth3] = brol[e.s.multiLdWidth2] + 100
            brol[e.s.multiHasLdRange3] = 1
            brol[e.s.multiPreAtk3] = 1
        
        if brol[e.t.zombie] == 1: #current just makes it so brollows burrow count is stronger, idk what to do
            if brol[e.s.revive] > 0:
                brol[e.s.revive] = int(1 + brol[e.s.revive])
            elif brol[e.s.revive] < 0:
                brol[e.s.reviveHp] = 100
            
            if brol[e.s.burrow] > 0:
                pass #really dunno what to do here
            if brol[e.s.burrow] < 0:
                brol[e.s.burrowLength] += 500
        
        if brol[e.t.alien] == 1: #get a second ability, excludes multihit and isnt weighted
            
            brol = apply_ability(brol,50,150,r.randrange(0,10),r.randrange(0,100))
        
        if brol[e.t.angel] == 1: #doubles speed and health boost
            brol[e.s.speed] = int(vanilla_enemy_array[209][e.s.speed] + 2*(brol[e.s.speed]-vanilla_enemy_array[209][e.s.speed]))
            brol[e.s.hp] = int(vanilla_enemy_array[209][e.s.hp] + 2*(brol[e.s.hp]-vanilla_enemy_array[209][e.s.hp]))
     
        if brol[e.t.aku] == 1: #gives both shield and a death surge ability as minisurge
            brol = apply_shield(brol)
            brol = apply_death_surge(brol,1,100,r.randrange(0,100),True,r.randrange(0,100))
        
        #theres still no metal
        estat[209] = brol
    
    if red_face:
        estat[19][e.s.starred_god] = 1
        estat[19][e.s.surgeChance] = 20
        estat[19][e.s.miniSurge] = 1
        estat[19][e.s.surgeLevel] = 1
        estat[19][e.s.surgeStartPos] = 800
        estat[19][e.s.surgeWidth] = 0

    return estat




"""
needed functions
id swap



"""
def clamp_value(value):
        """
        clamps a value as an int between 0-100
        """
        if value<0:
            value = 0
        if value>100:
            value = 100
        return int(value)






#the array straight from t_unit
vanilla_enemy_array = f.read_vanilla_enemy_stats()

#stat array with the before everything reworks applied to it
base_enemy_array = make_base_enemy(vanilla_enemy_array)


