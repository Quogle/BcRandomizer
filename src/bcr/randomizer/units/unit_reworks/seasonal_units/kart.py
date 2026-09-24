"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def kart(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 183
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #kart_cat
    #first form mario themed, increased attack/hp reduced kbs
    unit[0][c.s.hp] = 760 #12920 at 30, was 390
    unit[0][c.s.attack] = 300 #5100 at 30, was 60
    unit[0][c.s.kbs] = 2 #was 4
    #second form luigi themed, increased attack and range, savage
    unit[1][c.s.attack] = 180 #2550 at 30, was 60
    unit[1][c.s.range] = 465 #was 320
    unit[1][c.s.savage_chance] = 12
    unit[1][c.s.savage_by] = 200
    #third form peach themed, 0tba (makes for 99f cycle from 179f), hp increased
    unit[2][c.s.tba] = 0 #was 55
    unit[2][c.s.hp] = 580 #makes for 9860 at 30, was 390



    return stats












