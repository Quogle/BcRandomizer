"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def moneko(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 16
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #moneko, waving bountier (miniwave outside tf)
    for x in range(0,3):
        unit[x][c.s.bounty] = 1
        unit[x][c.s.wave_chance] = 100
        unit[x][c.s.is_miniwave] = 1
        unit[x][c.s.crit_chance] = 0
    (unit[0][c.s.attack],unit[1][c.s.attack],unit[2][c.s.attack]) = (300,500,600)
    (unit[0][c.s.hp],unit[1][c.s.hp],unit[2][c.s.hp]) = (900,1300,1600)
    (unit[0][c.s.wave_level],unit[1][c.s.wave_level],unit[2][c.s.wave_level]) = (2,3,4)
    unit[2][c.s.is_miniwave] = 0



    return stats












