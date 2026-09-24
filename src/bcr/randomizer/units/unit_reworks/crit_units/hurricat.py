"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c


#this feels weak
def hurricat(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 267
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #hurricat, the utterly rapid attacker, literally just gets 2 more attacks, also remove crit
    for x in range(0,3):
        unit[x][c.s.crit_chance] = 0
        unit[x][c.s.multi_preatk_2] = 3
        unit[x][c.s.multi_preatk_3] = 3
        unit[x][c.s.multi_damage_2] = 30
        unit[x][c.s.multi_damage_3] = 30
    unit[0][c.s.multi_damage_2] = 24
    unit[0][c.s.multi_damage_3] = 24



    return stats












