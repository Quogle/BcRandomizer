"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c


#so this is kinda like freeze sushi against red (and relic in tf), it has worse hp and recharge and higher cost, maybe its too weak still?
def evil(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 80
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #evil, going for like a freeze sushi type thing
    for x in range(0,3):
        unit[x][c.s.tba] = 28 #was 22, makes for 71f cycle (same as sushi)
        unit[x][c.s.freeze_duration] = 60
        unit[x][c.s.freeze_chance] = 30
        unit[x][c.s.kbs] = 2
        unit[x][c.s.cost] = 1000
        unit[x][c.s.hp] = 2000 #was 699
        unit[x][c.s.attack] = 200 #p sure it already was 200
        unit[x][c.s.strong] = 1
        unit[x][c.s.recharge] = 440 #results in about 20 second cooldown
    unit[2][c.t.relic] = 1
    unit[2][c.s.curse_immune] = 1
    unit[2][c.s.recharge] = 400 # was 200
    unit[2][c.s.freeze_chance] = 40 #this is what it is normally
    unit[2][c.s.cost] = 850
    unit[2][c.s.hp] = 3500


    return stats












