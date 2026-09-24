"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def neneko(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 131
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #neneko, the occasionally savaging insane massive unit
    for x in range(0,2): #only two forms
        unit[x][c.s.savage_by] = 200
        unit[x][c.s.savage_chance] = 15
        unit[x][c.t.metal] = 1
        unit[x][c.s.insane_massive] = 1



    return stats












