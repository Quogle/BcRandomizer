import tadbcmc.data.enums.enemy as e
from ...config.defaults import DEFAULT_CONFIG
import tadbcmc.core.seeded_randomization as srand
import copy
from ..enemies import ability_altering as abal




#I assumed input validation on the inputs for all these funcs
#maybe thats not a good idea? Ill log when it should be validated just incase
#red: speed and kb are assumed to be positive numbers

#this file makes calls to config["enemy"]["trait_gimmicks"]

#functions needing post attack animation information to work correctly:
#alien
#relic

#functions desiring enemy info peon strength
#lethal and barrier in alien
#maybe zombie balancing?




""" all these functions act on a single enemy and return it """
def white_gimmick(stats:list,config=DEFAULT_CONFIG):
    """ gives all white units sage
    \n does nothing if white is off """
    #the only thing is sage right?
    do_anything = config["enemy"]["trait_gimmicks"]["white"]["enabled"]
    do_sage = config["enemy"]["trait_gimmicks"]["white"]["sage"]
    if do_anything:
        for x in range(0,len(stats)):
            if stats[x][e.t.white] == 1:
                if do_sage:
                    stats[e.s.sage] = 1
    return stats

def red_gimmick(stats:list,config=DEFAULT_CONFIG):
    """ changes kb and speed of red enemies and returns stats 
    \n does nothing if red is off """
    if not config["enemy"]["trait_gimmicks"]["red"]["enabled"]:
        return stats
    speed_mult = config["enemy"]["trait_gimmicks"]["red"]["speed_mult"]
    kb_mult = config["enemy"]["trait_gimmicks"]["red"]["kb_mult"]
    rounding = config["enemy"]["trait_gimmicks"]["red"]["mult_rounding"]
    if rounding == "Up":
        is_up = True
    else:
        is_up = False
    #first create a before array in order to not give 0 speed things more than 0 speed
    before_stats = copy.deepcopy(stats)
    for x in range(0,len(stats)):
        if stats[x][e.t.red] == 1:
            unit_speed = stats[x][e.s.speed]*speed_mult
            unit_speed = _round_directionally(unit_speed,is_up)
            #now kb
            unit_kb = stats[x][e.s.kbs]*kb_mult
            unit_kb = _round_directionally(unit_kb,is_up)
            #now validate the inputs
            if unit_speed == 0:
                unit_speed = 1
            if unit_kb == 0:
                unit_kb = 1
            #now apply
            stats[x][e.s.speed] = unit_speed
            stats[x][e.s.kbs] = unit_kb
            #fix for 0 speed enemies
            if before_stats[x][e.s.speed] == 0:
                stats[x][e.s.speed] = 0
    #should be all good
    return stats

def floating_gimmick(stats:list,config=DEFAULT_CONFIG):
    """ gives floating enemies an immunity based on a weighted list and returns stats
    \n does nothing if floating is off """
    if not config["enemy"]["trait_gimmicks"]["floating"]["enabled"]:
        return stats
    #first get all the info
    waveimm = config["enemy"]["trait_gimmicks"]["floating"]["abilities"]["Wave Immunity"]
    surgeimm = config["enemy"]["trait_gimmicks"]["floating"]["abilities"]["Surge Immunity"]
    expimm = config["enemy"]["trait_gimmicks"]["floating"]["abilities"]["Explosion Immunity"]
    cs = config["enemy"]["trait_gimmicks"]["floating"]["abilities"]["Counter-Surge"]
    waveblock = config["enemy"]["trait_gimmicks"]["floating"]["abilities"]["Wave Block"]
    dual_chance = config["enemy"]["trait_gimmicks"]["floating"]["dual_ability_chance"]
    #now get the weighted list and the indexes of those abilities
    wlist = [waveimm,surgeimm,expimm,cs,waveblock]
    index_list = [e.s.waveImmune,e.s.surgeImmune,e.s.explodeImmune,e.s.counterSurge,e.s.waveBlock]
    #now for each unit thats floating
    for x in range(0,len(stats)):
        if stats[x][e.t.floating] == 1:
            #start by getting this units srand instance
            r = srand.randinst(107+10*x)
            #start by getting a unit specific list
            this_wlist = copy.deepcopy(wlist)
            #now remove possibility of a weight a unit already has
            for y in range(0,len(index_list)):
                if stats[x][index_list[y]] == 1:
                    this_wlist[y] = 0
            #now actually utilize that weight list
            #first check number of abilities to give
            ability_count_check = r.randrange(0,100)
            if ability_count_check <= dual_chance:
                number_of_abilities = 2
            else:
                number_of_abilities = 1
            #calling rand an extra time here incase I need an extra for the future
            r.randrange(0,100)
            #now loop that many times
            for y in range(0,number_of_abilities):
                ability_index = r.weighted_list(this_wlist)
                if ability_index == -1:
                    break #this is because theres no abilities left to give
                this_wlist[ability_index] = 0 #prevent next ability from getting it
                #apply it
                stats[x][index_list[ability_index]] = 1 #this works since theyre all just bools
    #should be all good
    return stats

def dark_gimmick(stats:list,config=DEFAULT_CONFIG):
    """ changes kb and speed of dark enemies in stats and returns it
    \n does nothing if dark is off """
    if not config["enemy"]["trait_gimmicks"]["dark"]["enabled"]:
        return stats
    speed_boost_list = config["enemy"]["trait_gimmicks"]["dark"]["speed_boosts"]
    kb_mult = config["enemy"]["trait_gimmicks"]["dark"]["knockback_mult"]
    rounding = config["enemy"]["trait_gimmicks"]["dark"]["mult_rounding"]
    #first take care of rounding
    if rounding == "Up":
        is_up = True
    else:
        is_up = False
    #now process the speed boost list into an actually usable one
    # for reference the strings are Additive and Multiplicative
    speed_boosts = []
    for each in speed_boost_list: #the order shall be [threshold,boost,is_mult]
        this_boost = []
        this_boost.append(each["threshold"])
        this_boost.append(each["boost"])
        #mult is gonna be the default
        if each["multiplier"] == "Additive":
            this_boost.append(False)
        else:
            this_boost.append(True)
    #ok now actually apply the speed boosts to dark enemies
    #start by creating the before array to make sure 0 speed enemies dont gain speed
    before_stats = copy.deepcopy(stats)
    for e_id in range(0,len(stats)):
        if stats[e_id][e.t.dark] == 1:
            done = False
            unit_speed = stats[e_id][e.s.speed]
            for x in range(0,len(speed_boosts)):
                if not done and unit_speed <= speed_boosts[x][0]:
                    done = True
                    if not speed_boosts[x][2]: #if not multiplicative
                        unit_speed += speed_boosts[x][1] #just add the boost and forget about it
                    else:
                        unit_speed *= speed_boosts[x][1]
                    break #isnt this a lil redundant
            #now do kb
            unit_kb = stats[e_id][e.s.kbs]*kb_mult
            #now handle rounding
            unit_speed = _round_directionally(unit_speed,is_up)
            unit_kb = _round_directionally(unit_kb,is_up)
            #make sure kb isnt 0 somehow
            if unit_kb == 0:
                unit_kb = 1
            #apply and return
            stats[e_id][e.s.speed] = unit_speed
            stats[e_id][e.s.kbs] = unit_kb
            #fix for 0 speed enemies
            if before_stats[e_id][e.s.speed] == 0:
                stats[e_id][e.s.speed] = 0
    #should be all good
    return stats

#not done!!!!!
def angel_gimmick(stats:list,config=DEFAULT_CONFIG):
    """ skipping for now since idk what were doing with angels """
    pass

def alien_gimmick(stats:list,config=DEFAULT_CONFIG,post_attack_info=[]):
    """ gives stats an alien ability and returns it
    \n starred alien abilities are also done here
    \n does nothing if alien is off
    \n can give: warp,barrier,freeze,slow,kb,weaken,wave,surge,explosion,crit,savage,lethal,base destroyer,multihit """
    if not config["enemy"]["trait_gimmicks"]["alien"]["enabled"]:
        return stats
    #first process the config
    ab_dict = config["enemy"]["trait_gimmicks"]["alien"]["abilities"]
    wfreeze = ab_dict["Freeze"]
    wslow = ab_dict["Slow"]
    wkb = ab_dict["Knockback"]
    wweaken = ab_dict["Weaken"]
    wwave = ab_dict["Wave"]
    wsurge = ab_dict["Surge"]
    wexp = ab_dict["Explosion"]
    wcrit = ab_dict["Critical Hit"]
    wsavage = ab_dict["Savage Blow"]
    wlethal = ab_dict["Lethal"]
    wbasedestroyer = ab_dict["Base Destroyer"]
    wmultihit = ab_dict["Multihit"]
    warp_freq = config["enemy"]["trait_gimmicks"]["alien"]["warp_frequency"]
    barrier_freq = config["enemy"]["trait_gimmicks"]["alien"]["barrier_frequency"]
    #now get the necessary lists
    ability_weight_list =   [wfreeze,                   wslow,                      wkb,                    wweaken,                    wwave,                  wsurge,                     wexp,                           wcrit,                      wsavage,                    wlethal,                    wbasedestroyer,     wmultihit]
    ability_check_list =    [e.s.freezeChance,          e.s.slowChance,             e.s.kbChance,           e.s.weakenChance,           e.s.waveChance,         e.s.surgeChance,            e.s.explodeChance,              e.s.critChance,             e.s.savageChance,           e.s.lethal,                 e.s.baseDestroyer,  e.s.multiDamage2]
    starred_alien_normal_ability_rate = 20 #we arent adding this to the config for reasons
    #now do each enemy
    for e_id in range(0,len(stats)):
        if stats[e_id][e.t.alien] == 1:
            #start by creating and using srand
            r = srand.randinst(65+37*e_id) #since most of the numbers are calling for 6 digits I dont want it to be a mult of 6
            starred_ability_decider = r.randrange(0,100)
            starred_gets_normal_ability_decider = r.randrange(0,100)
            rand1 = r.randrange(0,100) #I shall use rand for warp and brand for barrier so if more are needed in the future they are still understandable
            rand2 = r.randrange(0,100)
            rand3 = r.randrange(0,100)
            rand4 = r.randrange(0,100)
            rand5 = r.randrange(0,100)
            rand6 = r.randrange(0,100)
            rand7 = r.randrange(0,100)
            brand1 = r.randrange(0,100)
            brand2 = r.randrange(0,100)
            brand3 = r.randrange(0,100)
            brand4 = r.randrange(0,100)
            post_attack_time = -1
            if len(post_attack_info) > e_id:
                post_attack_time = post_attack_info[e_id]
            #first give an actual alien ability to this enemy
            #am I just giving all of them abilities? (I used to not give starred one)
            give_alien_ability = True
            #do starred shit
            if stats[e_id][e.s.starred_god] == 1:
                #first do warp
                if starred_ability_decider < warp_freq:
                    give_alien_ability = False
                    #first establish this units inputs
                    distanceness = int(rand1/5)
                    slowness = int(rand2/5)
                    likeliness = int(rand3/5)
                    backwards = False
                    if rand4 < 10:
                        backwards = True
                        slowness -= 2 #is this an ok adjustment?
                        distanceness -= 2
                    #now set it
                    stats[e_id] = abal._give_ability_warp(stats[e_id],post_attack_time=post_attack_time,distanceness=distanceness,slowness=slowness,likeliness=likeliness,is_backwards=backwards)
                    #I dont think theres anything else to consider here?
                if starred_ability_decider >= 100-barrier_freq:
                    give_alien_ability = False
                    #now establish this units inputs using none of the same random numbers as starred
                    this_strength = int(brand1/5)
                    stats[e_id] = abal._give_ability_barrier(stats[e_id],strength=this_strength,balanced=True)
                    #that should be all?
                #I dont think theres anything else to consider for starred
            #now give an alien ability if it didnt get one from starred or if it passes the sub 20% check
            if give_alien_ability or starred_gets_normal_ability_decider < starred_alien_normal_ability_rate:
                #since r is passed to this func there shouldnt be anything to do here
                stats[e_id] = _give_an_alien_ability(stats[e_id],r=r,ability_weight_list=ability_weight_list,ability_check_list=ability_check_list,post_attack_time=post_attack_time)
                #I dont think theres anything else to consider
    return stats

def zombie_gimmick(stats:list,config=DEFAULT_CONFIG):
    """ gives all zombies in stats burrow and revive at specified rates
    \n does nothing if zombie is off """
    if not config["enemy"]["trait_gimmicks"]["zombie"]["enabled"]:
        return stats
    #establish all the config info
    (balanced,grant_revive,grant_burrow,revive_freq,burrow_freq,revive_types,burrow_types,revive_weights,burrow_weights) = _process_zombie_config(config)
    #input validation
    if len(revive_types) == 0:
        (dummy,dummy,dummy,dummy,dummy,revive_types,dummy,revive_weights,dummy) = _process_zombie_config(DEFAULT_CONFIG)
    if len(burrow_types) == 0:
        (dummy,dummy,dummy,dummy,dummy,dummy,burrow_types,dummy,burrow_weights) = _process_zombie_config(DEFAULT_CONFIG)
    #now actually do something with it
    for e_id in range(0,len(stats)):
        if stats[e_id][e.t.zombie] == 1:
            #first get all the random numbers
            r = srand.randinst(87+29*e_id)
            burr_dec = r.randrange(0,100)
            rev_dec = r.randrange(0,100)
            burr_offset = r.randrange(0,100)
            rev_offset = r.randrange(0,100)
            burr_r = srand.randinst(1300+burr_offset) #I have to do this as its the only way to gaurantee they arent influenced by eachother when using weight list
            rev_r = srand.randinst(1400+rev_offset)
            #now create copies of weight lists for this unit
            this_rev_weights = copy.deepcopy(revive_weights)
            this_burr_weights = copy.deepcopy(burrow_weights)
            #now handle the balance info
            if balanced:
                (this_rev_weights,this_burr_weights) = _balance_zombie_weight_lists(this_rev_weights,this_burr_weights,stats[e_id])
            #now grant based on it

            if grant_revive and rev_dec < revive_freq and stats[e_id][e.s.revive] == 0: #dont attempt to give revive to something that already has it
                #rev array is [count,hp,delay]
                rev_to_give = rev_r.weighted_list(this_rev_weights)
                #now set it
                stats[e_id][e.s.revive] = revive_types[rev_to_give][0]
                stats[e_id][e.s.reviveHp] = revive_types[rev_to_give][1]
                stats[e_id][e.s.reviveTime] = revive_types[rev_to_give][2] #are these in normal game time? yes they are
            if grant_burrow and burr_dec < burrow_freq and stats[e_id][e.s.burrow] == 0: #dont attempt to give burrow to something that already has it
                #burr array is [count,distance]
                burr_to_give = burr_r.weighted_list(this_burr_weights)
                #now set it
                stats[e_id][e.s.burrow] = burrow_types[burr_to_give][0]
                stats[e_id][e.s.burrowLength] = int(4*burrow_types[burr_to_give][1])
            #should be all set
    return stats
    
def relic_gimmick(stats:list,config=DEFAULT_CONFIG,post_attack_info=[]):
    """ gives a unit curse and a same frame ld pierce if it can
    \n does nothing if relic is off
    \n\t wont give pierce if already ld/multi or has wave/surge/explosion/crit/savage"""
    #for reference the reason its if not 100% is because theres no difference if the damage is split between two wave/surge/explosion
    if not config["enemy"]["trait_gimmicks"]["relic"]["enabled"]:
        return stats
    #first get config info
    give_curse = config["enemy"]["trait_gimmicks"]["relic"]["curse"]
    give_pierce = config["enemy"]["trait_gimmicks"]["relic"]["pierce"]
    pierce_atk_rate = config["enemy"]["trait_gimmicks"]["relic"]["pierce_attack"]
    pierce_range_rate = config["enemy"]["trait_gimmicks"]["relic"]["pierce_range"]
    #now apply it
    for e_id in range(0,len(stats)):
        if stats[e_id][e.t.relic] == 1:
            #first get the rand for this unit
            r = srand.randinst(76+15*e_id)
            rand1 = r.randrange(0,100)
            rand2 = r.randrange(0,100)
            post_attack_time = -1
            if len(post_attack_info) > e_id:
                post_attack_time = post_attack_info[e_id]
            if give_curse and stats[e_id][e.s.curseChance] == 0: #no sense if giving it to something that already does
                stats[e_id] = abal._give_ability_curse(stats,post_attack_time=post_attack_time,strength=7+int(rand1/15),time=8+int(rand2/15))
            if give_pierce:
                do_pierce = True
                if stats[e_id][e.s.ldWidth] != 0:
                    do_pierce = False
                if stats[e_id][e.s.multiDamage2] != 0 or stats[e_id][e.s.multiDamage3] != 0:
                    do_pierce = False
                if stats[e_id][e.s.waveChance] > 0:
                    do_pierce = False
                if stats[e_id][e.s.surgeChance] > 0:
                    do_pierce = False
                if stats[e_id][e.s.explodeChance] > 0:
                    do_pierce = False
                if stats[e_id][e.s.critChance] > 0:
                    do_pierce = False
                if stats[e_id][e.s.savageChance] > 0:
                    do_pierce = False
                #should be all set?
                if do_pierce:
                    unit_range = stats[e_id][e.s.range]
                    unit_attack = stats[e_id][e.s.attack]
                    piercing_range = int(unit_range*pierce_range_rate/100)
                    piercing_attack = int(unit_attack*pierce_atk_rate/100)
                    #now set allat information
                    stats[e.s.attack] = int(unit_attack-piercing_attack)
                    stats[e.s.multiDamage2] = piercing_attack
                    stats[e.s.multiPreAtk2] = stats[e.s.preatk]
                    stats[e.s.multiHasLdRange2] = 1
                    stats[e.s.multiLdStart2] = int(unit_range+piercing_range)
                    stats[e.s.multiLdWidth2] = -int(320+unit_range+piercing_range)
                    stats[e.s.multiHasAbility1] = 0
                    stats[e.s.multiHasAbility2] = 1
            #should be all?
    return stats
                    
def aku_gimmick(stats:list,config=DEFAULT_CONFIG,post_attack_info=[]):
    """ gives aku units in stats deathsurge/shield and returns stats 
    \n does nothing if aku is off
    \n frequency of ability ds is set in config """
    if not config["enemy"]["trait_gimmicks"]["aku"]["enabled"]:
        return stats
    #first process config
    shield_freq = config["enemy"]["trait_gimmicks"]["aku"]["enabled"]
    ds_freq = config["enemy"]["trait_gimmicks"]["aku"]["enabled"]
    ds_ability_freq = config["enemy"]["trait_gimmicks"]["aku"]["enabled"]
    ds_ability_is_mini = config["enemy"]["trait_gimmicks"]["aku"]["enabled"]
    #if it has any of these abilities it cant get ab ds
    ability_check_list =    [e.s.freezeChance,e.s.slowChance,e.s.kbChance,e.s.weakenChance,e.s.waveChance,e.s.surgeChance,e.s.explodeChance,e.s.critChance,e.s.savageChance,e.s.multiDamage2,e.s.multiDamage3]
    #now do it
    for e_id in range(0,len(stats)):
        if stats[e_id][e.t.aku] == 1:
            #first get the random numbers needed
            r = srand.randinst(184+17*e_id)
            aku_ab_dec = r.randrange(0,100)
            ds_ab_dec = r.randrange(0,100)
            which_ab_dec = r.randrange(0,100)
            wild_dec = r.randrange(0,100)
            rand1 = r.randrange(0,100)
            rand2 = r.randrange(0,100)
            #im not gonna check if they already have shield/ds
            if aku_ab_dec < shield_freq:
                stats[e_id] = abal._give_ability_shield(stats[e_id])
                #thats all
            if aku_ab_dec >= 100-ds_freq:
                #first get if its even eligible for an ability ds
                eligible = True
                for each in ability_check_list:
                    if stats[e_id][each] != 0:
                        eligible = False
                #get is wild
                if wild_dec < 10:
                    is_wild = True
                else:
                    is_wild = False
                if eligible and ds_ab_dec < ds_ability_freq:
                    #first give it a death surge with ds ab in mind
                    stats[e_id] = abal._give_ability_death_surge(stats[e_id],strength=7+int(rand1/12),distanceness=5+int(rand2/10),is_mini=ds_ability_is_mini,is_wild=is_wild)
                    #now make it an ability ds
                    stats[e_id] = abal._aku_ability_ds(stats[e_id],which_ab_dec)
                else: #just a normal death surge
                    stats[e_id] = abal._give_ability_death_surge(stats[e_id],strength=7+int(rand1/10),distanceness=int(rand2/5),is_wild=is_wild)
            #should be all
    return stats

def metal_gimmick(stats:list,config=DEFAULT_CONFIG):
    """ does literally nothing currently """
    return stats






def _round_directionally(number,is_up=False):
    """ rounds based on direction
    \n Up and Down are the inputs """
    trunc = int(number)
    if is_up and trunc != number:
        return trunc + 1
    else:
        return trunc



def _give_an_alien_ability(stat:list,r:srand.randinst=srand.randinst(300),ability_weight_list:list=[],ability_check_list:list=[],post_attack_time=-1):
    """ applies a single alien ability to stat and returns it
    \n calls one weighted list and 8 randrange(0,100) on r """
    #remove everything a unit already has from possibility
    this_ability_weight_list = copy.deepcopy(ability_weight_list)
    for x in range(0,len(ability_check_list)):
        if stat[ability_check_list[x]] != 0:
            this_ability_weight_list[x] = 0
    #now use srand to choose one
    new_ab_index = r.weighted_list(this_ability_weight_list)
    #if none just return stat here (since I have no intention of using srand after this function it shouldnt matter?)
    if new_ab_index == -1:
        return stat
    #call all the srand numbers here
    r1 = r.randrange(0,100)
    r2 = r.randrange(0,100)
    r3 = r.randrange(0,100)
    r4 = r.randrange(0,100)
    r5 = r.randrange(0,100)
    r6 = r.randrange(0,100)
    r7 = r.randrange(0,100)
    r8 = r.randrange(0,100)
    #elif textwall
    if new_ab_index == 0:#freeze
        stat = abal._give_ability_freeze(stat,post_attack_time=post_attack_time,strength=8+int(r1/25),time=8+int(r2/25))
    elif new_ab_index == 1:#slow
        stat = abal._give_ability_slow(stat,post_attack_time=post_attack_time,strength=8+int(r1/25),time=10+int(r2/25))
    elif new_ab_index == 2:#kb
        stat = abal._give_ability_kb(stat,post_attack_time=post_attack_time,strength=8+int(r1/15))
    elif new_ab_index == 3:#weaken
        if r1 < 30:
            weak_to = 10
        else:
            weak_to = 50
        stat = abal._give_ability_weaken(stat,post_attack_time=post_attack_time,weak_to=weak_to,scale_by_strength_of_weakness=True,strength=8+int(r2/25),time=8+int(r3/25))
    elif new_ab_index == 4:#wave
        is_miniwave = False
        if r1 < 30:
            is_miniwave = True
        stat = abal._give_ability_wave(stat,post_attack_time=post_attack_time,strength=7+int(r2/15),levelness=7+int(r3/15),likelihood=7+int(r4/15),is_miniwave=is_miniwave)
    elif new_ab_index == 5:#surge
        is_minisurge = False
        if r1 < 50:
            is_minisurge = True
        stat = abal._give_ability_surge(stat,post_attack_time=post_attack_time,levelness=7+int(r2/15),likelihood=7+int(r3/15),distanceness=4+int(r4/8),spawn_range_width_determiner=6+int(r5/12),is_minisurge=is_minisurge)
    elif new_ab_index == 6:#explosion
        stat = abal._give_ability_explosion(stat,post_attack_time=post_attack_time,likelihood=7+int(r1/15),distanceness=5+int(r2/10),spawn_range_width_determiner=8+int(r3/30))
    elif new_ab_index == 7:#crit
        stat = abal._give_ability_crit(stat,post_attack_time=post_attack_time,scale_attack_to_keep_dps=True,likelihood=7+int(r1/15))
    elif new_ab_index == 8:#savage
        stat = abal._give_ability_savage(stat,post_attack_time=post_attack_time,scale_attack_to_keep_dps=True,likelihood=7+int(r1/15),strength=5+int(r2/10))
    elif new_ab_index == 9:#lethal
        stat = abal._alien_lethal(stat)
    elif new_ab_index == 10:#base destroyer
        stat[e.s.baseDestroyer] = 1
    elif new_ab_index == 11:#multihit
        stat = abal._alien_multihit(stat,multihit_decider=int(r1/5),post_attack_time=post_attack_time)

    #should be all set now?
    return stat

def _process_zombie_config(config=DEFAULT_CONFIG):
    """ processing for the zombie config done here """
    balanced = config["enemy"]["trait_gimmicks"]["zombie"]["balanced"]
    grant_revive = config["enemy"]["trait_gimmicks"]["zombie"]["grant_revive"]
    revive_freq = config["enemy"]["trait_gimmicks"]["zombie"]["revive_frequency"]
    grant_burrow = config["enemy"]["trait_gimmicks"]["zombie"]["grant_burrow"]
    burrow_freq = config["enemy"]["trait_gimmicks"]["zombie"]["burrow_frequency"]
    revive_types_raw = config["enemy"]["trait_gimmicks"]["zombie"]["revive_types"]
    burrow_types_raw = config["enemy"]["trait_gimmicks"]["zombie"]["burrow_types"]
    #now process the types into an understandable array, each is an array of dicts
    revive_types = []
    burrow_types = []
    # set each to [count,hp,delay,weight]
    for each in revive_types_raw:
        this_type = []
        this_type.append(each["count"])
        this_type.append(each["hp"])
        this_type.append(each["delay"])
        this_type.append(each["weight"])
        revive_types.append(this_type)
    # set each to [count,distance,weight]
    for each in burrow_types_raw:
        this_type = []
        this_type.append(each["count"])
        this_type.append(each["distance"])
        this_type.append(each["weight"])
        burrow_types.append(this_type)
    #now create the weight arrays for each of those
    revive_weights = []
    burrow_weights = []
    for each in revive_types:
        revive_weights.append(each.pop(3))
    for each in burrow_types:
        burrow_weights.append(each.pop(2))
    #should be all good to return allat info
    return (balanced,grant_revive,grant_burrow,revive_freq,burrow_freq,revive_types,burrow_types,revive_weights,burrow_weights)

def _balance_zombie_weight_lists(rev_wlist,burr_wlist,stats):
    """ changes the weights of things based on stats """
    #first get the zombies strength
    strength = 0
    if stats[e.s.hp] >= 200000:
        strength += 1
    if stats[e.s.hp] >= 800000:
        strength += 1
    if stats[e.s.range] >= 600:
        strength += 1
    if strength == 0 and stats[e.s.range] >= 400:
        strength += 1
    if strength == 0 and stats[e.s.range] < 200:
        strength = -1
    if stats[e.s.hp] <= 20000 and stats[e.s.range] < 150: #maybe this could use peon strength
        strength -= 2
    #now edit the weightlists according
    #do it differently if the length of the lists is less than 5
    #edit the last 10% of each list respectively
    if len(rev_wlist) >= 5:
        indexes_to_edit = _round_directionally(len(rev_wlist)/10,is_up=True)
        if strength > 1:
            for x in range(0,indexes_to_edit):
                rev_wlist[x] *= 1.5
                rev_wlist[-x] = 0
        elif strength > 0:
            for x in range(0,indexes_to_edit):
                rev_wlist[x] *= 1.2
                rev_wlist[-x] *= 0.5
        elif strength < -2:
            for x in range(0,indexes_to_edit):
                rev_wlist[x] = 0
                rev_wlist[-x] *= 1.5
        elif strength < 0:
            for x in range(0,indexes_to_edit):
                rev_wlist[x] *= 0.5
                rev_wlist[-x] *= 1.2
    else: #what to do if theres less than 5 rev types
        #just gonna mult the first and last indexes by values according to strength
        first_mult = 1+0.2*strength
        second_mult = 1-0.2*strength
        rev_wlist[0] *= first_mult
        rev_wlist[-1] *= second_mult
    if len(burr_wlist) >= 5:
        indexes_to_edit = _round_directionally(len(rev_wlist)/10,is_up=True)
        if strength > 1:
            for x in range(0,indexes_to_edit):
                burr_wlist[x] *= 1.5
                burr_wlist[-x] = 0
        elif strength > 0:
            for x in range(0,indexes_to_edit):
                burr_wlist[x] *= 1.2
                burr_wlist[-x] *= 0.5
        elif strength < -2:
            for x in range(0,indexes_to_edit):
                burr_wlist[x] = 0
                burr_wlist[-x] *= 1.5
        elif strength < 0:
            for x in range(0,indexes_to_edit):
                burr_wlist[x] *= 0.5
                burr_wlist[-x] *= 1.2
    else:
        first_mult = 1+0.2*strength
        second_mult = 1-0.2*strength
        burr_wlist[0] *= first_mult
        burr_wlist[-1] *= second_mult
    return (rev_wlist,burr_wlist)









