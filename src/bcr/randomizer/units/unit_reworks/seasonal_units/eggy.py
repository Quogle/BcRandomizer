"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def eggy(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 329
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #eggy, high slow rate in first 2 forms
    for x in range(0,2):
        unit[x][c.s.slow_chance] = 50 #was 20


    return stats












