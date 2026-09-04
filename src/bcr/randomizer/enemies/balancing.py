import tadbcmc.data.enums.enemy as e
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import copy


#idk what else to do here but Im gonna put all the making of base arrays in here

def _hp_buff_metals(stats):
    """ buffs the hp of current metals
    \n 400x if hp < 1000, 20x otherwise """
    #I hate python references
    stats = copy.deepcopy(stats)
    for each in stats:
        if each[e.t.metal] == 1:
            this_hp = each[e.s.hp]
            if this_hp < 1000:
                each[e.s.hp] = int(400*this_hp)
            else:
                each[e.s.hp] = int(20*this_hp)
    return stats

def _metal_new_trait(stats):
    """ gives metals a new trait and removes their metal
    \n default trait is red but most used metals get their own """
    #I hate python references
    stats = copy.deepcopy(stats)
    for unit in stats:
        if unit[e.t.metal] == 1:
            unit[e.t.metal] = 0
            unit[e.t.red] = 1
    #now do specific units
    specif = [
        [47,e.t.white], #metal hippoe
        [54,e.t.relic], #smh
        [56,e.t.angel], #metal one horn
        [58,e.t.dark], #face
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
        stats[each[0]+2][e.t.red] = 0
        stats[each[0]+2][each[1]] = 1   
    return stats

def _ex_metal_rebalance(stats):
    """ rebalances some of the vanilla metal enemies, does not remove metal trait
    \n this should be run after buffing metal hp (otherwise you get 3 mill hp smh) """
    #I hate python references
    stats = copy.deepcopy(stats)
    # metal doge 147
    stats[149][e.s.hp] = 20000

    #metal hippoe 47
    stats[49][e.s.hp] = 80000

    #kronium 517
    stats[519][e.s.hp] = 75000
    stats[519][e.s.tba] = 0
    stats[519][e.s.attack] = 25000
    stats[519][e.s.waveBlock] = 1
    stats[519][e.s.surgeImmune] = 1

    #metal face 58
    stats[60][e.s.hp] = 1
    stats[60][e.s.waveChance] = 100
    stats[60][e.s.dodgeChance] = 90
    stats[60][e.s.dodgeDuration] = 1
    stats[60][e.s.ldMinRange] = 240
    stats[60][e.s.ldWidth] = -560

    #metal one horn 56
    stats[58][e.s.sage] = 1
    
    #angel fanboy 116
    stats[118][e.s.speed] = 0
    stats[118][e.s.attack] = 10
    stats[118][e.s.surgeChance] = 100
    stats[118][e.s.surgeLevel] = 15
    stats[118][e.s.surgeStartPos] = 4000
    stats[118][e.s.surgeWidth] = 100
    stats[118][e.s.range] = 8000
    stats[118][e.s.dodgeChance] = 100
    stats[118][e.s.dodgeDuration] = 300
    stats[118][e.s.weakenChance] = 100
    stats[118][e.s.weakenTime] = 900
    stats[118][e.s.weakenPercent] = 50

    #smh 54
    stats[56][e.s.kbs] = 3
    stats[56][e.s.hp] = 300000

    #cybear 57
    stats[59][e.s.waveImmune] = 1

    #croc 497 (only tba is done here hp and metal trait are done after literally everything else)
    stats[499][e.s.tba] = 0


    return stats

def _behemoth_killer(stats):
    """ removes behemoth and returns, thats it """
    #I hate python references
    stats = copy.deepcopy(stats)
    for each in stats:
        each[e.s.behemoth] = 0
    return each

def _ex_behemoth_rebalance(stats):
    """ rebalances the vanilla behemoths """
    #I hate python references
    stats = copy.deepcopy(stats)
    # wild doge 603
    stats[605][e.s.hp] = 45000
    stats[605][e.s.attack] = 12000
    stats[605][e.s.surgeImmune] = 0
    stats[605][e.s.lethal] = 0

    # ruck 604
    stats[606][e.s.hp] = 600000
    stats[606][e.s.attack] = 5000
    stats[606][e.s.multiDamage2] = 5000
    stats[606][e.s.multiDamage3] = 5000

    # hazuku 605
    stats[607][e.s.attack] = 12000
    stats[607][e.s.hp] = 1400000
    stats[607][e.s.ldMinRange] = 355
    stats[607][e.s.ldWidth] = 705

    # crab 606
    stats[608][e.s.hp] = 1000000
    stats[608][e.s.attack] = 10000
    stats[608][e.s.multiDamage2] = 12000
    
    #sloth 610
    stats[612][e.s.hp] = 800000
    stats[612][e.s.attack] = 8000
    stats[612][e.s.multiDamage2] = 10000
    stats[612][e.s.multiDamage3] = 120000
    stats[612][e.s.multiPreAtk2] = stats[612][e.s.preatk]
    stats[612][e.s.multiPreAtk3] = stats[612][e.s.preatk]
    stats[612][e.s.ldMinRange] = 500 #do I wanna give sloth omni tho
    stats[612][e.s.ldWidth] = -500

    #bluck 611
    stats[613][e.s.hp] = 1000000
    stats[613][e.s.attack] = 5000
    stats[613][e.s.multiDamage2] = 5000
    stats[613][e.s.multiDamage3] = 5000

    #raja 613
    stats[615][e.s.hp] = 1200000
    stats[615][e.s.attack] = 8000
    stats[615][e.s.miniwave] = 1

    #chickful 624
    stats[626][e.s.hp] = 1200000
    stats[626][e.s.attack] = 18000

    #reluck 627
    stats[629][e.s.hp] = 1400000
    stats[629][e.s.attack] = 7000
    stats[629][e.s.multiDamage2] = 7000
    stats[629][e.s.multiDamage3] = 10000

    #aku master a 634
    stats[636][e.s.hp] = 800000
    stats[636][e.s.attack] = 10000
    stats[636][e.s.multiDamage2] = 15000

    #deonil 639
    stats[641][e.s.hp] = 800000
    stats[641][e.s.attack] = 5000

    #le boin 641
    stats[643][e.s.hp] = 1200000
    stats[643][e.s.attack] = 8000
    stats[643][e.s.tba] = 20

    #relic leon 650
    stats[652][e.s.hp] = 2600000
    stats[652][e.s.attack] = 10000
    stats[652][e.s.tba] = 50

    #zombie henry 652
    stats[654][e.s.hp] = 400000
    stats[654][e.s.attack] = 10000

    #black croc 655
    stats[657][e.s.hp] = 2500000
    stats[657][e.s.attack] = 25499
    
    #ganglion 659
    stats[661][e.s.hp] = 2500000
    stats[661][e.s.tba] = 125

    #bunslios 714 idk what to do with this man
    stats[716][e.s.hp] = 2800000
    stats[716][e.s.attack] = 36000
    

    return stats

def _literally_just_metal_croc(stats):
    """ literally just gives croc metal with 5 hp
    \n this has to be done after sprites because I didnt account for croc as dual trait """
    #I hate python references
    stats = copy.deepcopy(stats)
    #croc 497
    stats[499][e.t.metal] = 1
    stats[499][e.s.hp] = 5
    return stats



from ...config import defaults

""" actual total functions 
\n this functions do not save to file """
def early_rebalance(config=defaults.DEFAULT_CONFIG):
    """ pulls vanilla enemy array and applys the proper rebalances to make the before anything array """
    vanilla_stats = gf.file_reader(fn.ENEMY_STATS,vanilla=True)
    modded_array = copy.deepcopy(vanilla_stats)
    #gonna specify all the bools here because I dont like calling config in an if
    remove_metals = True
    give_metals_new_trait = True
    rebalance_metals = True
    remove_behemoths = True
    rebalance_behemoths = True
    #now actually edit the arrays
    if remove_metals:
        modded_array = _hp_buff_metals(modded_array)
    if give_metals_new_trait:
        modded_array = _metal_new_trait(modded_array) #as long as this is after hp buff it doesnt matter where in this func it is
    if rebalance_metals:
        modded_array = _ex_metal_rebalance(modded_array) #as long as this is after hp buff location doesnt matter
    if remove_behemoths:
        modded_array = _behemoth_killer(modded_array)
    if rebalance_behemoths:
        modded_array = _ex_behemoth_rebalance(modded_array)
    #is there anything else that needs to be done before this array can be used
    return modded_array

def middle_rebalance(stats,config=defaults.DEFAULT_CONFIG):
    """ modded enemies intended to be affected by randomization should go in here """ #this shouldnt be the method desc lmao
    #dunno what yet so this is basically empty
    stats = copy.deepcopy(stats)


    return stats

def late_rebalance(stats,config=defaults.DEFAULT_CONFIG):
    """ modded enemies that arent intended to be affected by randomization should go in here """ #this shouldnt be the method desc lmao
    #I dont currently know what to do so this is empty for now
    stats = copy.deepcopy(stats)


    return stats

def end_rebalance(stats,config=defaults.DEFAULT_CONFIG):
    """ this function should run at the very end of the program """
    stats = copy.deepcopy(stats)
    rebalance_metal = True
    if rebalance_metal:
        stats = _literally_just_metal_croc(stats)
    return stats






