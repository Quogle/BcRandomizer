"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def rampage(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 63
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #rampage, hp increases
    for x in range(0,3):
        unit[x][c.s.hp] = 1200 #is og 700


    return stats












