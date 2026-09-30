
import tadbcmc.data.enums.cats as c
import tadbcmc.core.seeded_randomization as srand
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn

import tadbcmc.core.file_handler as fh
from ...config.defaults import DEFAULT_CONFIG
import copy
from ..units import trait_randomization_mk3
from ...config.version_config import version_config_keys as vck
from ..units import balancing
from ...config.version_config.get_version_config import DEFAULT_VC_CONFIG
import tadbcmc.core.simple_funcs as simp
from .attack_cycle_information import *


"""
the cost and level scheme for all of these is entirely incorrect because I dont feel like documenting anything rn
"""




def basic_chance_duration_type_ability(ability_id:int,r_offset:int,unit_id:int,form_id:int,rarity:int):
    """ returns a talent block """
    #first get the random numbers to use
    r = srand.randinst(r_offset)
    r1 = r.randrange(0,100)
    r2 = r.randrange(0,100)
    r3 = r.randrange(0,100)
    r4 = r.randrange(0,100)
    r5 = r.randrange(0,100)
    r6 = r.randrange(0,100)
    #now set the chance/duration multiples based on ability
    chance = 1
    duration = 1
    third_param = 0
    dont_consider_cycle = False
    if ability_id == int(c.tv.freeze):
        chance = 0.9
        duration = 0.7
    elif ability_id == int(c.tv.slow):
        chance = 1.1
        duration = 1.1
    elif ability_id == int(c.tv.weaken):
        chance = 1.4
        duration = 1
        third_param = 50 #should I allow a third param other than this?
    elif ability_id == int(c.tv.curse):
        chance = 1.4
        duration = 1.2
    elif ability_id == int(c.tv.dodge):
        chance = 0.77
        duration = 1
        dont_consider_cycle = True
    #now actually create the specific information based on the attack cycle
    chance_variate = 0.8 + r1/25
    duration_variate = 0.7 + r2/17

    attack_cycle = _attack_cycle_getter(unit_id,form_id)
    frame_duration = int((attack_cycle/2)*duration*duration_variate)
    eff_chance = simp.clamp(int(10+chance*((attack_cycle/60*chance_variate)**1.4)*10),0,100)
    #now dodge gets its own shit
    if dont_consider_cycle:
        #first do chance, lower chance dodges last longer proportionally
        #I cant actually access stats information here to reduce it when lower cooldown :pensive: I dont care enough to change that
        #double the distance from 1 of chance variate
        chance_variate = (chance_variate-1)*2 + 1
        eff_chance = int(20+5*int(6*chance*chance_variate))
        #now duration is just kinda set semi linearly based on chance
        frame_duration = int(25+5*int((55-chance)/5*duration*duration_variate))
    #now make the talent block
    cost_type = 4
    if rarity > 3:
        cost_type = 8
    block = [0]*14
    block[c.tpos.ability_id] = ability_id
    block[c.tpos.max_level] = 10 #or should it be 5
    block[c.tpos.stat1_min] = int(eff_chance/2)
    block[c.tpos.stat1_min+1] = int(eff_chance)
    block[c.tpos.stat2_min] = int(frame_duration/2)
    block[c.tpos.stat2_min+1] = int(frame_duration)
    block[c.tpos.stat3_min] = third_param
    block[c.tpos.stat3_min+1] = third_param
    block[c.tpos.text_id] = 0 #ILL DO THIS LATER
    block[c.tpos.cost_scheme] = cost_type
    block[c.tpos.name_id] = -1 #idk why this is sometimes not -1 but thats a later me problem
    block[c.tpos.limit] = 0 #ultra talent status is handled elsewhere
    #ok all good
    return block

def resistance_type_ability(ability_id:int,rarity:int,r_offset:int):
    """ creates a resistant talent block of that id """
    #first get the sole random number to use
    r = srand.randinst(r_offset)
    r1 = r.randrange(0,100)
    #now create the different types of resistances
    higher_resistance = [
        int(c.tv.rfreeze),
        int(c.tv.rslow),
        int(c.tv.rweaken),
        int(c.tv.rkb),
        int(c.tv.rwarp),
    ]
    medium_resistance = [
        int(c.tv.rcurse),
        int(c.tv.rwave),
    ]
    low_resistance = [
        int(c.tv.rtoxic),
        int(c.tv.rsurge), #there is no explosion resist
    ]
    #now get the strength mult based on that
    strength_mult = 1
    if ability_id in higher_resistance:
        strength_mult = 1.5
    elif ability_id in low_resistance:
        strength_mult = 0.6
    #now divide the resistance into 40% 50% and 70%
    strength = r1*strength_mult
    resist_by = 40 #this is the default in case things fail somehow
    if strength < 20: #33% for low, 13% for high
        resist_by = 40
    elif strength < 55: #91% for low, 36% for high (58% and 26% are the proportions it appears)
        resist_by = 50
    else: #idk like 9% for low, 45% for medium
        resist_by = 70
    #now make the block
    cost_type = 4
    if rarity > 3:
        cost_type = 8
    block = [0]*14
    block[c.tpos.ability_id] = ability_id
    block[c.tpos.max_level] = 10 #or should it be 5
    block[c.tpos.stat1_min] = 5
    block[c.tpos.stat1_min+1] = resist_by
    block[c.tpos.text_id] = 0 #ILL DO THIS LATER
    block[c.tpos.cost_scheme] = cost_type
    block[c.tpos.name_id] = -1 #idk why this is sometimes not -1 but thats a later me problem
    block[c.tpos.limit] = 0 #ultra talent status is handled elsewhere
    #ok all good
    return block

def set_with_no_params(ability_id:int,rarity:int):
    """ makes the talent block for those talents with no parameters """
    #technically I should determine the cost here but thats a later thing
    cost_type = 4
    if rarity > 3:
        cost_type = 8
    block = [0]*14
    block[c.tpos.ability_id] = ability_id
    block[c.tpos.max_level] = 1
    block[c.tpos.text_id] = 0 #ILL DO THIS LATER
    block[c.tpos.cost_scheme] = cost_type
    block[c.tpos.name_id] = -1 #idk why this is sometimes not -1 but thats a later me problem
    block[c.tpos.limit] = 0 #ultra talent status is handled elsewhere
    #ok all good
    return block

def wave_surge_explosion_type_ability(ability_id:int,r_offset:int,rarity:int,unit_id:int,form_id:int,form_stats:list):
    """ makes talent block """
    #first make the random numbers to use
    r = srand.randinst(r_offset)
    r1 = r.randrange(0,100)
    r2 = r.randrange(0,100)
    r3 = r.randrange(0,100)
    r4 = r.randrange(0,100)
    r5 = r.randrange(0,100)
    r6 = r.randrange(0,100)
    #now get the 'strength'
    strength = 10
    if form_stats[c.s.range] >= 400:
        strength += 2
    if form_stats[c.s.range] >= 600:
        strength += 2
    strength *= (50+r1)/100
    #now get the level
    chance_boost = 0
    param2 = 0
    if ability_id == int(c.tv.wave):
        param2 = simp.clamp(int((strength/6)**1.7),1,30) #nothings gonna reach a level 30 wave anyways
        chance_boost = 2
    if ability_id == int(c.tv.miniwave):
        param2 = simp.clamp(int((strength/5)**1.7),1,30) #nothings gonna reach a level 30 wave anyways
        chance_boost = 5
    if ability_id == int(c.tv.surge):
        param2 = simp.clamp(int(0.6+(strength/10)**1.7),1,30) #nothings gonna reach a level 30 surge anyways
    if ability_id == int(c.tv.minisurge):
        param2 = simp.clamp(int(1+(strength/8)**1.7),1,30) #nothings gonna reach a level 30 surge anyways
        chance_boost = 3
    #now get the chance
    attack_cycle = _attack_cycle_getter(unit_id,form_id)
    chance = simp.clamp(int(10+((attack_cycle/60)**(1.5+chance_boost/10-param2/10)*(5+r2/33))),1,100) #I have zero clue what this is lmao
    param1 = chance #this is always the case
    #now get the range for surge and explosion
    param3 = 0
    param4 = 0
    if ability_id == int(c.tv.surge) or ability_id == int(c.tv.minisurge):
        #just divide into two groups for each
        if r3 < 50:
            param3 = int(form_stats[c.s.range]*0.7-50)*4
        else:
            param3 = int(form_stats[c.s.range]*0.9+50)*4
        if r4 < 50:
            param4 = 225*4
        else:
            param4 = 450*4
    elif ability_id == int(c.tv.explosion):
        #divide into two groups
        if r3 < 50:
            param2 = int(form_stats[c.s.range])*4
        else:
            param2 = int(form_stats[c.s.range]*0.5+100)
            param3 = int(100)*4
    #now just set allat
    cost_type = 4
    if rarity > 3:
        cost_type = 8
    block = [0]*14
    block[c.tpos.ability_id] = ability_id
    block[c.tpos.max_level] = 10
    block[c.tpos.stat1_min] = int(param1/2)
    block[c.tpos.stat1_min+1] = int(param1)
    block[c.tpos.stat2_min] = int(param2) #I think I dont want the level to be lowered (also this is explosion start)
    block[c.tpos.stat2_min+1] = int(param2)
    block[c.tpos.stat3_min] = int(param3)
    block[c.tpos.stat3_min+1] = int(param3)
    block[c.tpos.stat4_min] = int(param4)
    block[c.tpos.stat4_min+1] = int(param4)
    block[c.tpos.text_id] = 0 #ILL DO THIS LATER
    block[c.tpos.cost_scheme] = cost_type
    block[c.tpos.name_id] = -1 #idk why this is sometimes not -1 but thats a later me problem
    block[c.tpos.limit] = 0 #ultra talent status is handled elsewhere
    #ok all good
    return block































def _attack_cycle_getter(unit_id:int,form_id:int):
    """ gets the attack cycle for the unit specified
    \n assumes attack cycles has been updated """
    global ATTACK_CYCLE_ARRAY
    return ATTACK_CYCLE_ARRAY[unit_id][form_id]

