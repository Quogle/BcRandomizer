"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def new_years_neneko(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 314
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #new years neneko, the single target multi kber
    for x in range(0,3):
        unit[x][c.s.area] = 0
        unit[x][c.s.kb_chance] = 100
        unit[x][c.s.tba] = 80
        unit[x][c.s.crit_chance] = 0
        for trait in c.t:
            unit[x][trait] = 1
    unit[2][c.s.multi_ld_2_exists] = 1
    unit[2][c.s.multi_ld_3_exists] = 1
    unit[2][c.s.multi_ld_2_start] = 250
    unit[2][c.s.multi_ld_2_width] = 180 #hits up to 430
    unit[2][c.s.multi_ld_3_start] = 410
    unit[2][c.s.multi_ld_3_width] = 230 #hits up to 640



    return stats












