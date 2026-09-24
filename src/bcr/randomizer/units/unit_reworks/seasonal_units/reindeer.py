"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def reindeer(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 74
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #reindeer, constant attacking zkiller with 1 kb, has a little over 4k dps at 30
    for x in range(0,3):
        unit[x][c.s.tba] = 0
        unit[x][c.s.kbs] = 1
        unit[x][c.s.zombie_killer] = 1


    return stats












