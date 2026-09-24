"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c


#idk what to make of this one it just kinda is
def ashiluga(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 168
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #ashiluga
    for trait in c.t:
        unit[0][trait] = 1
    #making it a suicide unit with correct surge stats but on a normal surge
    unit[0][c.s.attack_state] = 2
    unit[0][c.s.attack_count] = 1
    unit[0][c.s.range] = 300
    unit[0][c.s.hp] = 0 #im just giving 0 hp to make them immortal instead of dodge
    unit[0][c.s.speed] = 10
    unit[0][c.s.surge_chance] = 100
    unit[0][c.s.surge_start_four] = 2000 #there will be no surge width generally


    unit[0][c.s.surge_level] = 4
    #intended stats
    unit[0][c.s.slow_chance] = 100
    unit[0][c.s.slow_duration] = 420 #maybe this should be shortend, esp once ds added

    return stats

