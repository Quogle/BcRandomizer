"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def waitress(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 273
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #waitress, single target nuker, 100% savage for 5x damage, also gets strong against metal 
    for x in range(0,3):
        unit[x][c.s.savage_chance] = 100
        unit[x][c.s.savage_by] = 400 #in old randomizer this was 300, at 400 it does bahamut damage so for sake of math and also cause it misses so much Im doing 400
        unit[x][c.s.strong] = 1
        unit[x][c.t.metal] = 1



    return stats












