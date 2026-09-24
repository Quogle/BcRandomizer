"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def hayabusa(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 261
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #hayabusa, 200% savage at crit rate, makes for same average dps (technically 1.04x) as second form but with higher max dph
    unit[0][c.s.savage_by] = 200
    unit[0][c.s.savage_chance] = 30

    return stats












