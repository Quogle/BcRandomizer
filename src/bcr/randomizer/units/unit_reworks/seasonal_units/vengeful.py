"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def vengeful(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 128
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #vengeful, bounty soul strike with more damage, hp also increased
    for x in range(0,3):
        unit[x][c.s.bounty] = 1
        unit[x][c.s.soul_strike] = 1
        unit[x][c.s.attack] = 500
        unit[x][c.s.hp] = 900


    return stats












