import tadbcmc.core.game_files as gf
import tadbcmc.data.enums.enemy as e
import tadbcmc.core.simple_funcs as simp




































""" applying specific abilities to stats 
the way these work is inputs are almost always relative to 10, usually within the bounds of 0-20 (outside that rarely does anything different)"""
def _give_ability_weaken(stats,strength=10,time=10,weak_to=50,post_attack_time=-1,scale_by_strength_of_weakness=True):
    """ gives a weaken of specified strength time and % to a unit and returns the stat array
    \n 10 means what I consider to be average strength and time (dont ask what that means) """
    #first figure out the attack cycle
    attack_cycle = _get_stats_attack_cycle(stats,post_attack_time)
    #reduce strength and time if its a strong weakness
    if scale_by_strength_of_weakness:
        if weak_to <= 25:
            strength -= 1
            time -= 1
        if weak_to <= 10:
            strength -= 2
            time -= 2
        if weak_to <= 1:
            strength -= 2
            time -= 2
    strength = simp.clamp(strength)
    time = simp.clamp(time)
    #now use attack cycle and the determiners to get the correct chance and duration
    chance = int(simp.clamp(strength + (attack_cycle*(5+strength))/75))
    duration = int(3*time + attack_cycle*(time/15+((attack_cycle/300)**1.1)/5)) #I have zero clue what this looks like lmao (now that Ive looked it looks ok)
    #apply it
    stats[e.s.weakenPercent] = weak_to
    stats[e.s.weakenChance] = chance
    stats[e.s.weakenTime] = duration
    return stats

def _give_ability_freeze(stats,strength=10,time=10,post_attack_time=-1):
    """ gives a freeze of a calculated chance and duration to a unit and returns the stat array
    \n 10 means what I consider to be average strength and time (dont ask what that means) """
    attack_cycle = _get_stats_attack_cycle(stats,post_attack_time)
    #now use that strength and time to get correct chance and duration
    chance = (5+strength+attack_cycle/3) #get the base chance before I do any math on it
    chance = simp.clamp(int(chance),ub=10*(strength-2)) #clamp it to say 80% if its level 10 strength and lower each unit after that, must be strength 12 to get gauranteed freeze
    chance = simp.clamp(chance) #now properly clamp it for if its above 12 strength
    duration = int(time*3 + attack_cycle*(0.6+time/5)*(0.9+strength/20))
    #apply it
    stats[e.s.freezeChance] = chance
    stats[e.s.freezeTime] = duration
    return stats

def _give_ability_slow(stats,strength=10,time=10,post_attack_time=-1):
    """ gives a slow of a calculated chance and duration to a unit and returns the stat array
    \n 10 means what I consider to be average strength and time (dont ask what that means) """
    attack_cycle = _get_stats_attack_cycle(stats,post_attack_time)
    #now use that strength and time to get correct chance and duration
    chance = (10+strength+attack_cycle/3) #get the base chance before I do any math on it
    chance = simp.clamp(int(chance),ub=10*(strength-1)) #clamp it to say 90% if its level 10 strength and lower each unit after that, must be strength 11 to get gauranteed slow
    chance = simp.clamp(chance) #now properly clamp it for if its above 11 strength
    duration = int(time*3 + attack_cycle*((0.8+time/5)**1.5)*(1+strength/20))
    #apply it
    stats[e.s.freezeChance] = chance
    stats[e.s.freezeTime] = duration
    return stats

def _give_ability_kb(stats,strength=10,post_attack_time=-1):
    """ gives a kb of a calculated chance to a unit and returns the stat array
    \n 10 means what I consider to be average strength (dont ask what that means) """
    attack_cycle = _get_stats_attack_cycle(stats,post_attack_time)
    chance = int(simp.clamp(5+strength+(attack_cycle/3)*(0.5+strength/20)))
    stats[e.s.kbChance] = chance
    return stats

def _give_ability_curse(stats,strength=10,time=10,post_attack_time=-1):
    """ gives a kb of a calculated chance to a unit and returns the stat array
    \n 10 means what I consider to be average strength (dont ask what that means) """
    attack_cycle = _get_stats_attack_cycle(stats,post_attack_time)
    chance = int(simp.clamp(5+strength+(attack_cycle/2)*(0.4+strength/10)))
    duration = int(time*3 + attack_cycle*(0.5+int(time/10))*(0.5+time/10))
    stats[e.s.curseChance] = chance
    stats[e.s.curseDuration] = duration
    return stats

def _give_ability_toxic(stats,strength=10,likelihood=10,post_attack_time=-1):
    """ gives a kb of a calculated chance to a unit and returns the stat array
    \n 10 means what I consider to be average strength (dont ask what that means) """
    attack_cycle = _get_stats_attack_cycle(stats,post_attack_time)
    #this is really gonna be a tough one to figure out
    amount = simp.clamp(int((2*strength)*(1+int(attack_cycle/50)/5)))
    chance = simp.clamp(int(5+(3+likelihood/3)*int((attack_cycle/60)**1.5)))
    stats[e.s.toxicAmount] = amount
    stats[e.s.toxicChance] = chance
    return stats
    """ literally just gives stats counter surge and returns it """
    stats[e.s.counterSurge] = 1
    return stats

def _give_ability_self_destruct(stats,die=True,number_of_attacks=1):
    """ gives the unit self destruct, if not die then will stand still
    \n why would you use this lmao """
    if die:
        stats[e.s.selfDestruct] = 2
    else:
        stats[e.s.selfDestruct] = 1
    stats[e.s.attackThenGiveUpCounter] = number_of_attacks
    return stats

def _give_ability_dodge(stats,chance=10,time=30):
    """ gives stats listed dodge and returns it
    \n chance and time are the actual stats, not used for calculation """
    stats[e.s.dodgeChance] = chance
    stats[e.s.dodgeDuration] = time
    return stats

def _give_ability_strengthen(stats,strength=10,earlyhood=10):
    """ gives stats strengthen and returns it
    \n strength is used to determine the magnitude, earlyhood is used to determine how early something strengthens """
    #I think Im gonna split it based on if theyre 1 kb or not
    if stats[e.s.kbs] == 1:
        if earlyhood >= 25: #stop it from dividing by 0 while still allowing for instant strengthen
            earlyhood = 25
        kb_simulation = 2 + int((20-earlyhood)/5) #for each 5 below 20 it appears earlier (16-20 is 2),(11-15 is 3),(6-10 is 4),(1-5 is 5)
        percent = int(100/kb_simulation)
        increase = 10*(strength+5) - 20*int(percent/10) #reduce the increase by 20% for each 10% earlier it is (this results in 100% increase at 25% hp for default 10 10),(140% increase at 33% for 15 15),(110% increase at 50% for 16),(70% increase at 25% for 6 6)
    else:
        #think Ill do earlyhood on a scale from 0-20 corresponding directly to kb counts
        kb_simulation = stats[e.s.kbs]
        early_ratio = simp.clamp(earlyhood,0,20)/20
        kb_ratio = int(kb_simulation*early_ratio)
        #now fix the boundaries
        if kb_ratio >= kb_simulation:
            kb_ratio -= 1
        if kb_ratio < 1:
            kb_ratio = 1
        percent = int((100/kb_simulation)*kb_ratio)
        #now calculate the increase
        increase = 15*(strength+5) - 20*int(percent/10) #base 75%, increase by 15 for each strength, decrease by 20 for each 10% earlier it is, (3kbs at 33% hp get 165% boost for 10 10)
    #now actually clamp them to make sure theres no monkey business
    percent = simp.clamp(percent)
    if increase <= 0:
        increase = 1 #lmao
    #apply it and return
    stats[e.s.strengthenAt] = int(percent)
    stats[e.s.strengthenBy] = int(increase)
    return stats

def _give_ability_survive(stats,likelihood=10):
    """ gives stats survive and returns it
    \n 10 and above likelihood is gauranteed, below falls linearly from 50% at 9 to 5% at 0 """
    if likelihood >= 10:
        stats[e.s.lethal] = 100
    else:
        stats[e.s.lethal] = int(5+5*simp.clamp(likelihood,0,9))
    return stats

def _give_ability_crit(stats,likelihood=10,scale_attack_to_keep_dps=True,post_attack_time=-1):
    """ gives stats crit, changes the attack to leave dps the same if true, returns it """
    #get the max crit rate, scales based on intended likelihood
    max_rate_scale = 1.5
    if scale_attack_to_keep_dps:
        max_rate_scale = 2
    max_crit_rate = simp.clamp(int((20*max_rate_scale)+max_rate_scale*likelihood))
    #get attack cycle
    attack_cycle = _get_stats_attack_cycle(stats,post_attack_time)
    #now calculate the crit rate, my idea is something should max out on crit chance around 300f cycle (using 350 since theres a +5)
    chance = int(5+(attack_cycle/350)*max_crit_rate)
    chance = int(simp.clamp(chance,1,max_crit_rate))
    #now apply it
    stats[e.s.critChance] = chance
    #now fix the scale
    if scale_attack_to_keep_dps: #edit each only if that hit can cit
        crit_scale = 1/(1+chance/100)
        if stats[e.s.attack] > 0 and stats[e.s.multiHasAbility1] == 1:
            stats[e.s.attack] = int(stats[e.s.attack]*crit_scale)
        if stats[e.s.multiDamage2] > 0 and stats[e.s.multiHasAbility2] == 1:
            stats[e.s.multiDamage2] = int(stats[e.s.multiDamage2]*crit_scale)
        if stats[e.s.multiDamage3] > 0 and stats[e.s.multiHasAbility3] == 1:
            stats[e.s.multiDamage3] = int(stats[e.s.multiDamage3]*crit_scale)
    #now return it
    return stats
                    
def _give_ability_savage(stats,likelihood=10,strength=10,scale_attack_to_keep_dps=True,post_attack_time=-1):
    """ gives stats savage, changes the attack to leave dps the same if true, returns it """
    #get the max savage rate, scales based on intended likelihood
    max_rate_scale = 0.8
    if scale_attack_to_keep_dps:
        max_rate_scale = 1.3
    max_savage_rate = simp.clamp(int((20*max_rate_scale)+max_rate_scale*likelihood))
    #get attack cycle
    attack_cycle = _get_stats_attack_cycle(stats,post_attack_time)
    #now calculate the savage rate, my idea is something should max out on savage chance around 400f cycle (using 450 since theres a +5)
    chance = int(5+(attack_cycle/450)*max_savage_rate)
    chance = int(simp.clamp(chance,1,max_savage_rate))
    #now apply it
    stats[e.s.savageChance] = chance
    #now calculate the intended strength
    boost = int(15*(5+strength)-20*int(chance/10)) #default 75, +15 for each strength, -20 for each 10 chance, (max 39% chance, 165% boost at 10 10)
    if boost <= 0:
        boost = 1 #why do I bother
    stats[e.s.savageBoost] = boost
    #now fix the scale
    if scale_attack_to_keep_dps: #edit each only if that hit can cit
        savage_scale = 1/(1+(chance/100)*(boost/100))
        if stats[e.s.attack] > 0 and stats[e.s.multiHasAbility1] == 1:
            stats[e.s.attack] = int(stats[e.s.attack]*savage_scale)
        if stats[e.s.multiDamage2] > 0 and stats[e.s.multiHasAbility2] == 1:
            stats[e.s.multiDamage2] = int(stats[e.s.multiDamage2]*savage_scale)
        if stats[e.s.multiDamage3] > 0 and stats[e.s.multiHasAbility3] == 1:
            stats[e.s.multiDamage3] = int(stats[e.s.multiDamage3]*savage_scale)
    #now return it
    return stats

def _give_ability_wave(stats,strength=10,levelness=10,likelihood=10,post_attack_time=-1,is_miniwave=False):
    """ gives stats a wave of a calculated level and returns it, default 'average' inputs are 10
    \n higher strength results in a greater wave level and wave chance
    \n higher levelness results in a greater level wave 
    \n higher likelihood makes wave chance go up, wave chance is decreased for higher level waves
    \n miniwave results in higher wave level and chance on average """
    mini_mult = 1
    if is_miniwave:
        stats[e.s.miniwave] = 1
        mini_mult = 1.5
    attack_cycle = _get_stats_attack_cycle(stats,post_attack_time)
    wave_level = int(mini_mult*((levelness/9)**2)*((strength/10)**1.2))
    if wave_level < 1:
        wave_level = 1
    #now use that to get the correct chance
    strength_adjustment = (90+strength)/100 #this is a very weak adjustment maybe it should be more
    likeliness_adjustment = (30+likelihood)/40 #this only allows the chance to vary by 25% of what it would otherwise be maybe it should be more
    adjusted_attack_cycle = attack_cycle*strength_adjustment*likeliness_adjustment*mini_mult
    wave_chance = int((5+(((adjusted_attack_cycle)/300)**1.5)*100)/(wave_level**0.5))
    wave_chance = simp.clamp(wave_chance,1,100)
    #apply it
    stats[e.s.waveChance] = wave_chance
    stats[e.s.waveLevel] = wave_level
    return stats

def _give_ability_surge(stats,levelness=10,likelihood=10,post_attack_time=-1,is_minisurge=False,distanceness=10,spawn_range_width_determiner=10):
    """ gives stats a surge and returns it
    \n levelness is used to determine the level of surge, closer surges have slightly lower level
    \n likelihood is used to determine the chance, farther and higher level surges have lower chance
    \n distanceness determines where it spawns relative to unit range
    \n minisurges spawn significantly more frequently """
    #Im gonna divide the surges into ranges based on closeness
    range_determinant = int(simp.clamp(distanceness,0,30)/3) #ranges can only be in 0 to 10 (based on distanceness between 0 and 30)
    range_ratio = 0.3 #this is the case for 0
    if range_determinant == 1:
        range_ratio = 0.5
    elif range_determinant == 2:
        range_ratio = 0.8
    elif range_determinant == 3:
        range_ratio = 1.0
    elif range_determinant == 4:
        range_ratio = 1.2
    elif range_determinant == 5:
        range_ratio = 1.5
    elif range_determinant == 6:
        range_ratio = 1.8
    elif range_determinant == 7:
        range_ratio = 2.0
    elif range_determinant == 8:
        range_ratio = 2.2
    elif range_determinant == 9:
        range_ratio = 2.5
    elif range_determinant == 10:
        range_ratio = 3.0
    unit_range_shifted = stats[e.s.range] + 20 #shift exists to shift the range slightly higher than the real range
    spawn_range_start = int(range_ratio*unit_range_shifted) #this is what should be mult by 4 and slapped onto the start
    #now get spawn width
    #Im using common units for this
    spawn_width = int(20*((simp.clamp(spawn_range_width_determiner-2,0,40)/3)**2)) #i think this is prolly fine its like 140 variant by default, 720 at 20 and 1740 at 30
    #ok now I have the range and width, I still need chance and level
    #level first since thats part of chance
    level_power = 1.1
    if range_determinant >= 5:
        level_power = 1.3
    elif range_determinant >= 3:
        level_power = 1.2
    level = int((simp.clamp(levelness,0,30)/7)**level_power)
    if level < 1:
        level = 1
    #now use that for chance
    #nows the time to take care of minisurge
    mini_mult = 1
    if is_minisurge:
        stats[e.s.miniSurge] = 1
        mini_mult = 2
    #get attack cycle
    attack_cycle = _get_stats_attack_cycle(stats,post_attack_time)
    likeli_adjust = (20+likelihood)/30
    level_adjust = 1/(level**0.5)
    adjusted_cycle = attack_cycle*likeli_adjust*mini_mult
    #scale quadratically up to 300f cycle
    chance = int(level_adjust*(5+((adjusted_cycle/300)**1.5)*100))
    chance = simp.clamp(chance,1,100)
    #now set all that info
    stats[e.s.surgeChance] = chance
    stats[e.s.surgeLevel] = level
    stats[e.s.surgeStartPos] = int(4*spawn_range_start)
    stats[e.s.surgeWidth] = int(4*spawn_width)
    return stats

def _give_ability_explosion(stats,likelihood=10,distanceness=10,post_attack_time=-1,spawn_range_width_determiner=10):
    """ gives a unit explosion
    \n likelihood affect chance, explosions near the units range reduce the chance, explosions with more variant increase it
    \n distanceness affects how far it spawns
    \n only spawn ranges above 10 will have variation """
    attack_cycle = _get_stats_attack_cycle(stats,post_attack_time)
    #Im gonna divide the explosions into ranges based on distanceness
    range_determinant = int(simp.clamp(distanceness,0,30)/3) #ranges can only be in 0 to 10 (based on distanceness between 0 and 30)
    range_ratio = 0.5 #this is the case for 0
    if range_determinant == 1:
        range_ratio = 0.6
    elif range_determinant == 2:
        range_ratio = 0.7
    elif range_determinant == 3:
        range_ratio = 0.8
    elif range_determinant == 4:
        range_ratio = 0.9
    elif range_determinant == 5:
        range_ratio = 1.0
    elif range_determinant == 6:
        range_ratio = 1.2
    elif range_determinant == 7:
        range_ratio = 1.5
    elif range_determinant == 8:
        range_ratio = 1.8
    elif range_determinant == 9:
        range_ratio = 2.1
    elif range_determinant == 10:
        range_ratio = 2.5
    #Im adding a bunch to the range beforehand in order to make explosion not spawn super close on lower range units
    unit_range_shifted = stats[e.s.range] + 200 #is this good? (Im using common units)
    spawn_start = int(unit_range_shifted*range_ratio)
    difference_from_range = abs(spawn_start-stats[e.s.range])
    distance_adjustment = simp.clamp(0.5 + (difference_from_range/150)**1.5,1,3) #the distance adjustment is a multiple between 1 and 3 (its pretty much 1 so long as the diff is less than 100)
    #now get the variation
    spawn_variation = 0
    if spawn_range_width_determiner > 10:
        spawn_variation = 10*int((spawn_range_width_determiner-5)**1.5)
    variant_adjustment = simp.clamp(1+(spawn_variation/400)**1.3,1,2) 
    #now do chance
    adjusted_cycle = attack_cycle*(distance_adjustment+variant_adjustment)/4
    chance = int(5+((adjusted_cycle/300)**1.5)*100*(10+likelihood)/20)
    chance = simp.clamp(chance,1,100)
    #now set all that info
    stats[e.s.explodeChance] = chance
    stats[e.s.explodeAt4x] = int(4*spawn_start)
    stats[e.s.explodeVariance] = int(4*spawn_variation)
    return stats

def _give_ability_warp(stats,post_attack_time=-1,distanceness=10,slowness=10,likeliness=10,is_backwards=False):
    """ gives stats a warp and returns it 
    \ndistanceness determines the distance of the warp, higher means further backwards too
    \nslowness determines how long the warp takes"""
    #first start by getting the units range + say 200
    shifted_range = stats[e.s.range] + 200
    #now determine the warp range ratio by dividing distanceness into chunks
    range_ratio = 0.3  #this is the default ratio
    if is_backwards:
        if distanceness < 3:
            range_ratio = -0.1
        elif distanceness < 5:
            range_ratio = -0.3
        elif distanceness < 7:
            range_ratio = -0.4
        elif distanceness < 10:
            range_ratio = -0.6
        elif distanceness < 14:
            range_ratio = -0.8
        elif distanceness < 16:
            range_ratio = -1.2
        elif distanceness < 18:
            range_ratio = -1.5
        elif distanceness < 21:
            range_ratio = -1.8
        else:
            range_ratio = -2.0
    else:
        if distanceness < 3:
            range_ratio = 0.2
        elif distanceness < 5:
            range_ratio = 0.5
        elif distanceness < 7:
            range_ratio = 0.7
        elif distanceness < 10:
            range_ratio = 0.9
        elif distanceness < 14:
            range_ratio = 1.2
        elif distanceness < 16:
            range_ratio = 1.5
        elif distanceness < 18:
            range_ratio = 1.9
        elif distanceness < 21:
            range_ratio = 2.4
        else:
            range_ratio = 4.0
    #now get the actual warp range resulting from that
    warp_range = shifted_range*range_ratio #common units
    #now determine the warp time
    #Im gonna also just block this (do I even wanna consider attack cycle or just use hard numbers)
    time_scale = 30
    attack_cycle_increase_minimum = 150 #this is the minimum amount before attack cycle will be added to the time scale
    cycle_scalor = 0.2 #this is the % amount thats added to the scale (after minimum)
    attack_cycle = _get_stats_attack_cycle(stats,post_attack_time)
    time_scale += simp.clamp((attack_cycle-attack_cycle_increase_minimum)*cycle_scalor,0,400) #restrict it to not reduce and only increase by 400 max
    #now get the ratios to be mult with time scale and boost
    time_ratio = 1
    time_boost = 0
    if slowness < 3:
        time_ratio = 0.1
    elif slowness < 6:
        time_ratio = 0.5
    elif slowness < 10:
        time_ratio = 1
    elif slowness < 13:
        time_boost = 30
        time_ratio = 1.5
    elif slowness < 15:
        time_boost = 40
        time_ratio = 1.9
    elif slowness < 17:
        time_boost = 60
        time_ratio = 2.5
    elif slowness < 18:
        time_boost = 90
        time_ratio = 3.5
    elif slowness < 19:
        time_boost = 120
        time_ratio = 5.0
    elif slowness < 20:
        time_boost = 130
        time_ratio = 7.0
    else:
        time_ratio = slowness/2 #it can keep increasing beyond 20 but its linear
    warp_time = time_ratio*(time_scale+time_boost)
    #now to do chance (I think for warp Ill actually ignore all other information and just do chance raw)
    #actually no Ill set chance higher on single target things
    chance = 5+((attack_cycle/60)**1.5)*(4+likeliness/10)
    if stats[e.s.area] == 0:
        chance += (20 + attack_cycle/8 + likeliness)
    chance = simp.clamp(int(chance),1,100)
    #set it
    stats[e.s.warpChance] = int(chance)
    stats[e.s.warpDuration] = int(warp_time) #im gonna ignore the possibility it could be negative if something else went wrong
    stats[e.s.warpMin4x] = int(4*warp_range)
    stats[e.s.warpMax4x] = int(4*warp_range)
    return stats

def _give_ability_barrier(stats,strength=10):
    """ gives the unit a barrier, doesnt scale with units hp
    \n strength below 1 results in a shitter barrier """
    #Im literally just gonna separate this into 8 blocks with hardcoded stats
    barrier_hp = 400 #this is prolly a decent shitter hp
    if strength >= 1:
        barrier_hp += 2600 #for 3k
    if strength >= 6:
        barrier_hp += 3000 #for 6k
    if strength >= 9:
        barrier_hp += 4000 #for 10k
    if strength >= 13:
        barrier_hp += 12000 #for 22k
    if strength >= 15:
        barrier_hp += 20000 #for 42k
    if strength >= 17:
        barrier_hp += 40000 #for 82k
    if strength >= 19:
        barrier_hp += 178000 #for 260k
    stats[e.s.barrierHp] = int(barrier_hp)
    return stats

def _give_ability_shield(stats):
    """ gives a unit a shield based on kb count """
    #literally just gonna copy this from aku
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

def _give_ability_death_surge(stats,strength=10,distanceness=10,is_mini=False,is_wild=False,force_gauranteed=False):
    """ gives stats death surge, NOT a death surge with an ability
    \n mini ds has a higher level on average
    \n wild means has a high spawn area
    \n things with <5k hp and <200 range get 50% chance, can be forced to 100% for eoc enemies and the like """
    #first get the level
    surge_level = (strength/8)**1.2
    if is_mini:
        stats[e.s.miniSurge] = 1
        surge_level += 0.3
    surge_level = simp.clamp(int(surge_level),1,3)
    #now get the range
    #Im literally just gonna do 3 ratios to add the units range to 345 + 30
    range_ratio = 0.3
    if distanceness > 7:
        range_ratio = 0.5
    if distanceness > 14:
        range_ratio = 0.8
    spawn_start = 345 + 30 + int(range_ratio*stats[e.s.range]) #common units
    spawn_variation = 60
    if is_wild:
        spawn_variation = 1200
    #now do chance
    spawn_chance = 100
    if stats[e.s.hp] < 5000 and stats[e.s.range] < 200: #most peons will only get 50%, unfortunately so will most eoc enemies
        spawn_chance = 50
    if force_gauranteed:
        spawn_chance = 100
    #now set it
    stats[e.s.deathSurgeChance] = simp.clamp(int(spawn_chance),1,100)
    stats[e.s.deathSurgeLevel] = simp.clamp(int(surge_level),1,3)
    stats[e.s.deathSurgeStartPos] = int(spawn_start)
    stats[e.s.deathSurgeWidth] = int(spawn_variation)
    return stats
    
def _give_ability_ld(stats,relative_size=10,blindspot_size=10):
    """ gives a unit ld
    \n inputs clamped to within 0-20
    \n blindspots 18 and above result in a unit that cant hit within its own range """
    #clamp the inputs to array indexes
    relative_size = simp.clamp(int(relative_size),0,20)
    blindspot_size = simp.clamp(int(blindspot_size),0,20)
    unit_range = stats[e.s.range]
    #                    0      1       2       3       4       5       6       7       8       9       10      11      12      13      14      15      16      17      18      19      20
    sizes_array =       [0.2,   0.25,   0.33,   0.40,   0.45,   0.50,   0.58,   0.66,   0.70,   0.78,   0.85,   0.90,   0.95,   1.00,   1.10,   1.20,   1.30,   1.40,   1.60,   1.70,   1.80]
    blindspot_array =   [-1,    0,      0.10,   0.20,   0.25,   0.30,   0.33,   0.35,   0.40,   0.45,   0.50,   0.55,   0.60,   0.66,   0.70,   0.75,   0.80,   0.85,   0.05,   0.05,   0.05]
    width = unit_range*sizes_array[relative_size]
    blindspot_start = unit_range*blindspot_array[blindspot_size]
    #now adjust for 0 and 1 blindspot
    if blindspot_size == 0:
        blindspot_start = -320
    elif blindspot_size == 1:
        blindspot_start = 0
    #now break into pattern for 18+ or not
    if blindspot_size >= 18:
        #18:50, 19:150, 20:250, with chunks of 5 based on the units actual range
        blindspot_increase = 50 + 100*(blindspot_size-18) + 5*int(blindspot_start/5)
        blindspot_start = int(unit_range + blindspot_increase)
        width = int(round(width,0))
        #should be all good to set this one
    else: #now to do if it isnt tackey type enemy
        #adjustment loop for if it doesnt reach its standing range
        while int(blindspot_start) + int(width) < unit_range:
            blindspot_start += 0.01*unit_range
            width += 0.01*unit_range
        #adjustment loop for if a unit with a proportionally large width also has a large pierce
        # first check is if (width-50)/unit range is more than 60%
        # second check is if (piercing width - 50)/unitrange is more than 40%
        #doesnt this prevent anything like clionel where it has a large blindspot but also massive pierce? (do I want that anyways) clionel type enemies could easily be added by simply adding an or that makes this not function on say 15+ blindspot size
        while (int(width)-50)/unit_range >= 0.6 and (int(blindspot_start)+int(width)-unit_range-50)/unit_range >= 0.4:
            blindspot_start -= 1 #Im gonna make this move back way slower
            width -= 0.01*unit_range
        #now floor them to make them flat numbers
        blindspot_start = int(blindspot_start)
        width = int(width)
    #now set it
    stats[e.s.ldMinRange] = blindspot_start
    stats[e.s.ldWidth] = width
    return stats

def _give_ability_omni(stats,relative_size=10,blindspot_size=10):
    """ gives stats an omni and returns it
    \n bounds on inputs limited to 0-20
    \n 20 blindspot results in a unit that cant hit within its range """
    #clamp the inputs to array indexes
    relative_size = simp.clamp(int(relative_size),0,20)
    blindspot_size = simp.clamp(int(blindspot_size),0,20)
    unit_range = stats[e.s.range]
    #                    0      1       2       3       4       5       6       7       8       9       10      11      12      13      14      15      16      17      18      19      20
    sizes_array =       [0.2,   0.25,   0.33,   0.40,   0.45,   0.50,   0.58,   0.66,   0.70,   0.78,   0.85,   0.90,   0.95,   1.00,   1.10,   1.20,   1.30,   1.40,   1.60,   1.70,   1.80]
    blindspot_array =   [-1.0,  -0.70,  -0.50,  -0.30,  -0.20,  0.00,   0.10,   0.20,   0.25,   0.33,   0.40,   0.45,   0.50,   0.55,   0.60,   0.66,   0.70,   0.75,   0.80,   0.85,   0.05]
    width = unit_range*sizes_array[relative_size]
    blindspot_start = unit_range*blindspot_array[blindspot_size]
    #omni blindspot shit
    if blindspot_size <= 4:
        blindspot_start -= 345*(blindspot_start-4)/4
    #now separate into 20 and not
    if blindspot_size == 20:
        #carry over the blindspot start in blocks of 5 starting from 100 past the range
        blindspot_start = int(unit_range + 100 + 5*int(blindspot_start/5))
        width = int(width)
        #that should be all ready
    else: #now what to do for all else
        #adjustment for if the omni doesnt reach the units range
        while int(blindspot_start) + int(width) < unit_range:
            blindspot_start += 0.01*unit_range
            width += 0.01*unit_range
        #now adjustment for if the omni is too huge without also a respectively large blindspot
        #first check is if blindspot-50 is less than 50% of a units range
        #second check is if pierce-50 is greater than 50% of a units range
        while int(blindspot_start-50)/unit_range < 0.5 and (int(blindspot_start)+int(width)-50-unit_range)/unit_range > 0.5:
            blindspot_start += 0.01*unit_range
            width -= 0.01*unit_range
        #now floor them to make them nice numbers
        blindspot_start = int(blindspot_start)
        width = int(width)
    #now set them
    #(just now realizing I didnt even consider that this is omni not ld)
    stats[e.s.ldMinRange] = int(blindspot_start+width)
    stats[e.s.ldWidth] = int(-width)
    return stats









def _get_stats_attack_cycle(stats,post_attack_time=-1):
    """ returns the attack cycle for input unit """
    #first figure out the attack cycle
    attack_cycle = stats[e.s.preatk]
    if stats[e.s.tba] == 0:
        if post_attack_time == -1:
            attack_cycle += 30 #30 is just my default assumed post attack if I dont get it
        else:
            attack_cycle += post_attack_time
    else:
        attack_cycle += stats[e.s.tba]
    return attack_cycle



