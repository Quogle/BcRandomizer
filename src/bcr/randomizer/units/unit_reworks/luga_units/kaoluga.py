"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c


#this one should generally be fine?
def kaoluga(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 712
    unit = stats[unit_id] #passing things as a reference oh lord help me

    for trait in c.t:
        unit[0][trait] = 1
    #kaoluga
    #suicide unit with relatively correct stats otherwise
    unit[0][c.s.attack_state] = 2
    unit[0][c.s.attack_count] = 1
    unit[0][c.s.range] = 300
    unit[0][c.s.hp] = 0 #im just giving 0 hp to make them immortal instead of dodge
    unit[0][c.s.speed] = 10
    unit[0][c.s.surge_chance] = 100
    unit[0][c.s.surge_start_four] = 2000 #there will be no surge width generally

    
    unit[0][c.s.surge_level] = 12
    #proper stats
    unit[0][c.s.is_miniwave] = 1 #I forget do cats share this bool across miniwave and minisurge
    unit[0][c.s.kb_chance] = 30


    return stats

