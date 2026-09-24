"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def marshmallow(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 176
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #marshmallow, first form is bounty ms, second form is a sp (I dont like this but idk what else to do)
    unit[0][c.s.recharge] = 130 #was 230
    unit[0][c.s.cost] = 60 #was 420
    unit[0][c.s.range] = 140
    unit[0][c.s.attack] = 45 #makes for 765 dph at 30, was 180
    unit[0][c.s.bounty] = 1
    #second form
    unit[1][c.s.shield_pierce_chance] = 20


    return stats












