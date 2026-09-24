"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def aku_researcher(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 621
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #aku researcher, massive against a single trait, not much to be said here (I dont feel like making aku researcher target aku if metals are still on)
    for x in range(0,3):
        unit[x][c.s.massive] = 1
        unit[x][c.t.metal] = 1
    

    return stats












