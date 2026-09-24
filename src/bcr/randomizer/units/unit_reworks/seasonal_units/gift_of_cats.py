"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def gift_of_cats(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 244
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #gift of cats, better freeze and area, for note attack cycle is 96f
    for x in range(0,2):
        unit[x][c.s.area] = 1
        unit[x][c.s.freeze_chance] = 50 #was 30
        unit[x][c.s.freeze_duration] = 75 #was 60


    return stats












