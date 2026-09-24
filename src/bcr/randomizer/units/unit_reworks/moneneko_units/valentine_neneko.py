"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def valentine_neneko(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 589
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #valentine neneko, the ranged waver, with sp in tf
    for x in range(0,3):
        unit[x][c.s.range] = 410
        unit[x][c.s.wave_level] = 4
        unit[x][c.s.crit_chance] = 0
        unit[x][c.s.attack] = 200 #double its base damage
        unit[x][c.s.hp] = 1200 #base is 900
    unit[2][c.s.shield_pierce_chance] = 30



    return stats












