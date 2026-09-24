"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def slug_cat(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 343
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #slug cat, constant attacker
    for x in range(0,2):
        unit[x][c.s.tba] = 0


    return stats












