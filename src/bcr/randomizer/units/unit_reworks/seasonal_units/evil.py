"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def evil(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 80
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #evil, better freeze and 0tba (45f cycle), I dont really know what the idea here is but my goal was to make it less abhorrently bad
    for x in range(0,3):
        unit[x][c.s.tba] = 0
        unit[x][c.s.freeze_duration] = 90
        unit[x][c.s.freeze_chance] = 30
        unit[x][c.s.cost] = 1000
        unit[x][c.s.hp] = 999 #was 699
    unit[2][c.s.recharge] = 190 #why this number? (it was originally 200)
    unit[2][c.s.freeze_chance] = 40 #this is what it is normally
    unit[2][c.s.cost] = 500



    return stats












