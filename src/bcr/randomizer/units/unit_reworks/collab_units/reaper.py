"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def reaper(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 68
    unit = stats[unit_id] #passing things as a reference oh lord help me

    for x in range(0,3):
        unit[x][c.s.range] = 385 #was 360
        unit[x][c.s.cost] = 750 #was 500
        unit[x][c.s.slow_duration] = 150 #was 120 (note its a 184f cycle)
        unit[x][c.s.recharge] = 500 #was 600, makes for 736f recharge
        unit[x][c.s.hp] = 700 #was (400,700,1000)
        unit[x][c.s.attack] = 470 #was (200,300,(450,450))
        unit[x][c.s.slow_chance] = 60
    unit[2][c.s.hp] = 1000
    #multihits
    unit[2][c.s.attack] = 200
    unit[2][c.s.multi_damage_2] = 400
    unit[2][c.s.multi_damage_3] = 800

    unit[2][c.s.preatk] = 16
    unit[2][c.s.multi_preatk_2] = 57
    unit[2][c.s.multi_preatk_3] = 83

    unit[2][c.s.multi_has_ability_1] = 1
    unit[2][c.s.multi_has_ability_2] = 1
    unit[2][c.s.multi_has_ability_3] = 1






    return stats












