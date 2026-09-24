"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def easter_neneko(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 332
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #easter neneko, the wild multihit debuffer
    for x in range(0,3):
        unit[x][c.s.area] = 1
        unit[x][c.t.metal] = 1
        unit[x][c.s.freeze_chance] = 50
        unit[x][c.s.slow_chance] = 50
        unit[x][c.s.weaken_chance] = 50
        unit[x][c.s.weaken_to] = 50
        unit[x][c.s.kb_chance] = 15
        unit[x][c.s.freeze_duration] = 40
        unit[x][c.s.slow_duration] = 60
        unit[x][c.s.weaken_duration] = 80
    unit[2][c.s.freeze_duration] = 90
    unit[2][c.s.slow_duration] = 140
    unit[2][c.s.weaken_duration] = 180





    return stats












