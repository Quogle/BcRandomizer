"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c


#maybe Ill give this unit some love in the future
def verbena(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 358
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #verbena, not a lot to say it just gets savage at crit rates on each form
    for x in range(0,3):
        unit[x][c.s.savage_by] = 200
        unit[x][c.s.savage_chance] = 30
    unit[2][c.s.savage_chance] = 50

    return stats












