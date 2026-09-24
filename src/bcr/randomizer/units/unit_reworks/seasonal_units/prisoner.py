"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def prisoner(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 79
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #prisoner, first and second form become 0tba faster animation fragile 435 ranged attackers, cooldown and speed increased 
    for x in range(0,2):
        unit[x][c.s.hp] = 50 #was 550
        unit[x][c.s.range] = 435 #was 120
        unit[x][c.s.tba] = 0 #was 60c
        unit[x][c.s.speed] = 12
        unit[x][c.s.preatk] = 16
        unit[x][c.s.recharge] = 440
    #gonna choose to ignore what happens when the sprites arent included


    return stats












