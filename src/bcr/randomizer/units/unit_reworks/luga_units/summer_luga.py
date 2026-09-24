"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c


#genuinely what even is the point of this it seems like such a nothing unit
#maybe something that spawns with like 3000 range single target with like 5 attacks and the surges spawn in that huge range would be more inchresting than whatever the fuck this is
def summer_luga(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 564
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #summerluga
    unit[0][c.s.attack_state] = 2
    unit[0][c.s.attack_count] = 1
    unit[0][c.s.range] = 300
    unit[0][c.s.hp] = 0 #im just ggiving 0 hp to make them immortal instead of dodge
    unit[0][c.s.speed] = 10
    unit[0][c.s.surge_chance] = 100
    unit[0][c.s.surge_start_four] = 2000 #there will be no surge width generally

    
    unit[0][c.s.surge_level] = 12
    unit[0][c.s.surge_width_four] = 2400
    #proper stats
    unit[0][c.s.multi_damage_2] = 600


    return stats

