
import dev.randomizer.enums.enemy as e
import dev.randomizer.enums.cats as c
from dev.randomizer.func.core import randinst
from dev.randomizer.parse_config import settings
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

def black_speed(estat):
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

"""
needed functions
id swap







"""






