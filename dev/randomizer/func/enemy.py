
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
    gives whitees sage, does nothing else
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

    WARP_TYPE_COUNT = 10
    WARP_RESTRICT = 3
    BARR_TYPE_COUNT = 10
    STAR_SECOND_ABILITY = 20 #this could be added to the config

    if do_a:
        #make weight lists
        abilities = [freeze_weight,slow_weight,kb_weight,weak_weight,wave_weight,surge_weight,explode_weight,crit_weight,savage_weight,lethal_weight,base_des_weight,multihit_weight]
        ability_weight_total = 0
        for each in abilities:
            ability_weight_total += each
        
        for unit in estat:
            #assign random numbers here
            star = r.randrange(0,100)
            warp_barr = r.randrange(0,100)
            starred_ability = r.randrange(0,100)
            ability_strength = r.randrange(0,100)
            duration_mult = r.randrange(6,15)
            barrier_hp_mult = r.randrange(0,11)
            ability = r.weighted_list(abilities)
            warp_dec = r.randrange(0,WARP_TYPE_COUNT)
            barr_dec = r.randrange(0,BARR_TYPE_COUNT)
            strong_barr = r.randrange(0,5)
            






            if unit[e.t.alien] == 1:
                #find unit stats here, maybe add post attack anim here
                attack_cycle = unit[e.s.tba]
                if attack_cycle == 0:
                    attack_cycle += 10
                attack_cycle += unit[e.s.preatk]
                base_chance = attack_cycle/300
                base_duration = attack_cycle*duration_mult/10
                

                done_starred = False
                if star < starred_freq:
                    done_starred = True
                    unit[e.s.starred_god] == 1
                    if warp_barr < warp_freq:
                        #block weak units from getting last 2 warps
                        if unit[e.s.hp] < 50000 and warp_dec >= WARP_TYPE_COUNT-WARP_RESTRICT:
                            warp_dec -= WARP_RESTRICT

                        
                        warp_chance_boost = 15
                        match warp_dec:
                            case 0:
                                distance = 2
                                time = 10
                            case 1:
                                distance = 2
                                time = 20
                            case 2:
                                distance = 1
                                time = 20
                                warp_chance_boost = 20
                            case 3:
                                distance = 3
                                time = 30
                            case 4:
                                distance = 3
                                time = 10
                            case 5:
                                distance = 4
                                time = 10
                            case 6:
                                distance = 6
                                time = 40
                            case 7:
                                distance = -2
                                time = 20
                            case 9:
                                distance = 0.2
                                time = 5
                        
                        unit[e.s.warpChance] = r.clamp_value(warp_chance_boost+base_chance)
                        unit[e.s.warpDuration] = int(attack_cycle*time/10)
                        unit[e.s.warpMin4x] = int(distance*unit[e.s.range])
                        unit[e.s.warpMax4x] = int(distance*unit[e.s.range])

                    if warp_barr >= (100-barrier_freq):
                        if unit[e.s.hp] < 50000 and barr_dec == BARR_TYPE_COUNT-1:
                            barr_dec -= 1
                        if unit[e.s.hp] < 10000:
                            strong_barr = 1

                        #goofy barr at 1/10, strongest bar at 1/10 disallowed for weaks
                        if barr_dec == 0:
                            barr_hp = 10
                        elif barr_dec == BARR_TYPE_COUNT-1:
                            barr_hp = 15000
                        elif barr_hp < 4:
                            barr_hp = 6000
                        else:
                            barr_hp = 3000

                        #multiple by a number between 1-2 and then by 10 if strong (currently 20% chance)
                        barr_hp *= (1+barrier_hp_mult/10)
                        if strong_barr == 0:
                            barr_hp *= 10
                        
                        unit[e.s.barrierHp] = int(barr_hp)
                #untrip marked as starred completed
                if starred_ability < STAR_SECOND_ABILITY:
                    done_starred = False
                


                # normal alien abilities
                if not done_starred:
                    if ability == 0:
                        if unit[e.s.freezeChance] > 0:
                            ability += 1
                        else:
                            unit[e.s.freezeChance] = r.clamp_value(5+base_chance/1.5)
                            unit[e.s.freezeTime] = int(30+base_duration/1.4)
                    if ability == 1:
                        if unit[e.s.slowChance] > 0:
                            ability += 1
                        else:
                            unit[e.s.slowChance] = r.clamp_value(15+base_chance/2)
                            unit[e.s.slowTime] = int(30+base_duration)
                    if ability == 2:
                        if unit[e.s.kbChance] > 0:
                            ability += 1
                        else:
                            unit[e.s.kbChance] = r.clamp_value(15+base_chance/1.2)
                    if ability == 3:
                        if unit[e.s.weakenChance] > 0:
                            ability += 1
                        else:
                            unit[e.s.weakenChance] = r.clamp_value(5+base_duration/1.5)
                            if ability_strength <30:
                                unit[e.s.weakenPercent] = 10
                                unit[e.s.weakenTime] = int(50+base_duration/2)
                            else:
                                unit[e.s.weakenPercent] = 50
                                unit[e.s.weakenTime] = int(20+base_duration*1.5)
                    if ability == 4:
                        if unit[e.s.waveChance] > 0:
                            ability += 1
                        else:
                            unit[e.s.waveChance] = r.clamp_value(2+((base_chance/250)**2)*80)
                            if ability_strength < 60:
                                unit[e.s.waveLevel] = 1
                            elif ability_strength < 80:
                                unit[e.s.waveLevel] = 2
                            elif ability_strength < 90:
                                unit[e.s.waveLevel] = 3
                            else:
                                unit[e.s.waveLevel] = 10
                    if ability == 5:
                        if unit[e.s.surgeChance] > 0:
                            ability += 1
                        else:
                            unit[e.s.surgeChance] = r.clamp_value(5+((base_chance/300)**2)*100)
                            unit[e.s.surgeWidth] = 0
                            if ability_strength < 80:
                                unit[e.s.surgeLevel] = 1
                                unit[e.s.surgeStartPos] = int(3.5*unit[e.s.range])
                            else:
                                unit[e.s.surgeLevel] = 3
                                unit[e.s.surgeStartPos] = int(1.5*unit[e.s.range])
                    if ability == 6:
                        if unit[e.s.explodeChance] > 0:
                            ability += 1
                        else:
                            unit[e.s.explodeChance] = r.clamp_value(5+((base_chance/400)**2)*80)
                            unit[e.s.explodeAt4x] = int(3*unit[e.s.range] - 75)
                    if ability == 7:
                        if unit[e.s.critChance] > 0:
                            ability += 1
                        else:
                            unit[e.s.critChance] = r.clamp_value(10+base_chance)
                    if ability == 8:
                        if unit[e.s.savageChance] > 0:
                            ability += 1
                        else:
                            savage_chance = r.clamp_value(55+base_chance/2) - 50
                            if ability_strength < 50:
                                unit[e.s.savageChance] = int(savage_chance)
                                unit[e.s.savageBoost] = 200
                            else:
                                unit[e.s.savageChance] = int(savage_chance/2)
                                unit[e.s.savageBoost] = 300
                            unit[e.s.attack] = int(unit[e.s.attack]*(100-savage_chance)/100)
                            unit[e.s.multiDamage2] = int(unit[e.s.multiDamage2]*(100-savage_chance)/100)
                            unit[e.s.multiDamage3] = int(unit[e.s.multiDamage3]*(100-savage_chance)/100)
                    if ability == 9:
                        if unit[e.s.lethal] > 0:
                            ability += 1
                        else:
                            unit[e.s.lethal] = 100
                    if ability == 10:
                        if unit[e.s.baseDestroyer] > 0:
                            ability += 1
                        else:
                            unit[e.s.baseDestroyer] = 1
                    if ability == 11:
                        if unit[e.s.multiDamage2] > 0:
                            ability += 1
                        else:
                            damage = unit[e.s.attack]
                            preatk = unit[e.s.preatk]
                            unit[e.s.multiHasAbility2] = 1
                            if ability_strength < 50: #even split
                                unit[e.s.attack] = int(unit[e.s.attack] - damage/2)
                                unit[e.s.multiDamage2] = int(damage/2)
                                unit[e.s.multiPreAtk2] = int(preatk+6)
                            else: #shift 40% of the attack onto the other two hits
                                damage = int(damage/5)
                                unit[e.s.attack] = int(unit[e.s.attack] - damage*2)
                                unit[e.s.multiDamage2] = damage
                                unit[e.s.multiDamage3] = damage
                                unit[e.s.multiHasAbility3] = 1
                                unit[e.s.multiPreAtk2] = int(preatk+3)
                                unit[e.s.multiPreAtk3] = int(preatk+6)
                    if ability == 12: #double ability chances if failed to grant ability
                        ability_chances = [e.s.freezeChance,e.s.slowChance,e.s.kbChance,e.s.weakenChance,e.s.critChance,e.s.lethal,e.s.savageChance]
                        for each in ability_chances:
                            unit[each] = r.clamp_value(unit[each]*2)

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










                    
                    




"""
needed functions
id swap







"""



#the array straight from t_unit
vanilla_enemy_array = f.read_vanilla_enemy_stats()

#stat array with the before everything reworks applied to it
base_enemy_array = make_base_enemy(vanilla_enemy_array)


