"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def summer_neneko(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 276
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #summer neneko, the massive insane massive unit,
    for x in range(0,3):
        unit[x][c.s.massive] = 1
        unit[x][c.s.insane_massive] = 1
        unit[x][c.t.metal] = 1


    return stats












