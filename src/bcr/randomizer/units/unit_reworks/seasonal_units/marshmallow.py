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
    unit[0][c.s.range] = 150
    unit[0][c.s.attack] = 60 #was 180 # with level gain, (720,1200,2100,3000) dph at 20,30,40,50
    unit[0][c.s.hp] = 260 #was 420 # with level gain, (2470,4160,7150,11050) hp at 20,30,40,50
    unit[0][c.s.bounty] = 1
    #second form
    unit[1][c.s.shield_pierce_chance] = 20


    levels = gf.file_reader(fn.LEVEL_STAT_GAIN)
    if levels != None:
        levels[unit_id] = [20,20,32,60,60,60,10,10,10,10,10,10,10,10,10,10,10,10,10,10]
        gf.file_writer(fn.LEVEL_STAT_GAIN,levels)


    return stats












