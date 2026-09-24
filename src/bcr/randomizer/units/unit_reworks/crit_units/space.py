"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def space(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 78
    unit = stats[unit_id] #passing things as a reference oh lord help me
    #space cat, gets things based on animation, first form surge, second form blast, third form I havent a clue and amph suggested single target paris so third form is just better at that role
    for x in range(0,3):
        unit[x][c.s.recharge] = 250
        unit[x][c.s.barrier_break_chance] = 0
        unit[x][c.s.wave_immune] = 1
        unit[x][c.s.crit_chance] = 20
        unit[x][c.s.attack] = 135
    #my idea for first form is generally the surges shouldnt hit what space is actually targetting (not editing hp/atk for now)
    unit[0][c.s.surge_chance] = 40
    unit[0][c.s.surge_level] = 4
    unit[0][c.s.surge_start_four] = 1700
    unit[0][c.s.surge_width_four] = 1300
    #my idea for second form is its a good aoe barrier breaker
    unit[1][c.s.crit_chance] = 0
    unit[1][c.s.explode_chance] = 50
    unit[1][c.s.explode_at] = 1360
    unit[1][c.s.barrier_break_chance] = 50
    #my idea for third form is idk a mix between camera and paris I guess
    unit[2][c.s.attack] = 155
    unit[2][c.s.lethal_chance] = 40
    unit[2][c.s.recharge] = 182
    unit[2][c.s.hp] = 960 #was 720
    unit[2][c.s.kbs] = 4 #was 3, the net effect of these two is just an additional whole kbs worth of hp 


    return stats












