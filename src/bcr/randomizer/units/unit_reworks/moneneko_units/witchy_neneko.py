"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def witchy_neneko(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 228
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #witchy neneko,
    for x in range(0,3):
        unit[x][c.s.crit_chance] = 0
    #first form is a suicidal counter surger though a dummy first hit
    unit[0][c.s.tba] = 200 #doubling the tba to make it attack less often
    unit[0][c.s.range] = 390
    unit[0][c.s.wave_immune] = 1
    unit[0][c.s.explode_immune] = 1
    unit[0][c.s.multi_damage_2] = 80
    unit[0][c.s.multi_preatk_2] = 28
    unit[0][c.s.multi_has_ability_2] = 0
    unit[0][c.s.multi_has_ability_1] = 1
    unit[0][c.s.preatk] = -1
    unit[0][c.s.attack] = 800 #makes for about 13k damage at 30
    unit[0][c.s.savage_by] = 200
    unit[0][c.s.savage_chance] = 20
    unit[0][c.s.counter_surge] = 1
    #second form I dont even know Im ignoring for now
    #third form doesnt need any changing



    return stats












