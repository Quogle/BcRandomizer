"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def koi(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 104
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #koi, constant attacking (19f cycle), my notes say increase speed of all forms but idk
    for x in range(0,3):
        unit[x][c.s.tba] = 0


    return stats












