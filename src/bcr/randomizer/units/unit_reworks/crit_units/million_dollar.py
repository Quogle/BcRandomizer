"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c
import tadbcmc.core.seeded_randomization as srand


def million_dollar(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 635
    unit = stats[unit_id] #passing things as a reference oh lord help me
    #million_dollar, wave weakener, also just has sign stats (the level boost must be set to 0 elsewhere to keep it constant)
    r = srand.randinst(146)
    for x in range(0,2):
        unit[x][c.s.recharge] = 13500
        unit[x][c.s.hp] = 10000
        unit[x][c.s.kbs] = 10000
        unit[x][c.s.attack] = 1
        unit[x][c.s.range] = 800
        unit[x][c.s.tba] = 300
        unit[x][c.s.speed] = 4
        unit[x][c.s.crit_chance] = 0
        unit[x][c.s.bounty] = 0
        unit[x][c.s.weaken_chance] = 100
        unit[x][c.s.weaken_duration] = 150
        unit[x][c.s.weaken_to] = 25
        unit[x][c.s.wave_chance] = 100
        unit[x][c.s.wave_level] = int(5+r.randrange(0,10)) #random level wave from 5 to 14
        for trait in c.t:
            unit[x][trait] = 1
        #I would love to give it a higher willpower but that doesnt seem to be a stat (at least not a logged one)




    levels = gf.file_reader(fn.LEVEL_STAT_GAIN)
    levels[unit_id] = [0]*20
    gf.file_writer(fn.LEVEL_STAT_GAIN,levels)





    return stats












