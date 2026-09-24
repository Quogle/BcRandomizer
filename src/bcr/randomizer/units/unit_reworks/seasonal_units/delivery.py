"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def delivery(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 303
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #delivery, more damage in first 2 forms
    for x in range(0,2):
        unit[x][c.s.attack] = 300 #was 200


    return stats












