"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def togeluga(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 240
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #togeluga
    unit[0][c.s.attack_state] = 2
    unit[0][c.s.attack_count] = 1
    unit[0][c.s.range] = 300
    unit[0][c.s.hp] = 0 #im just ggiving 0 hp to make them immortal instead of dodge
    unit[0][c.s.speed] = 10
    unit[0][c.s.surge_chance] = 100
    unit[0][c.s.surge_start_four] = 2000 #there will be no surge width generally
    #gonna make it have two back to back hits, one spawns the high surge the other does a lotta damage
    unit[0][c.s.multi_preatk_2] = int(unit[0][c.s.preatk])
    unit[0][c.s.preatk] = unit[0][c.s.multi_preatk_2]-1 #since this has already been set to the pre attack (make it start the surge one frame earlier)
    unit[0][c.s.surge_level] = 30
    #proper stats
    unit[0][c.s.area] = 1
    unit[0][c.s.ld_width] = -920
    unit[0][c.s.ld_minimum] = 600
    unit[0][c.s.range] = 450
    unit[0][c.s.multi_has_ability_2] = 0
    unit[0][c.s.multi_damage_2] = 1500
    unit[0][c.s.attack] = 300
    #only thing to note is the pre attack of both hits should be changed once the animation is added

    return stats












