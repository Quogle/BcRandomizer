"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def crazed_moneko(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 418
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #crazed moneko, suicide after 3 hits, absurd weaken miniwave, (the order of hits is actually reversed to make interrupting burn an attack)
    for x in range(0,2):
        unit[x][c.s.attack_count] = 3
        unit[x][c.s.attack_state] = 2
        unit[x][c.s.preatk] = 139
        unit[x][c.s.multi_has_ability_1] = 1
        unit[x][c.s.multi_preatk_2] = 19
        unit[x][c.s.multi_has_ability_2] = 0
        unit[x][c.s.multi_preatk_3] = 4
        unit[x][c.s.multi_has_ability_3] = 0
        unit[x][c.s.crit_chance] = 0
        unit[x][c.s.weaken_to] = 50
        unit[x][c.s.weaken_chance] = 100
        unit[x][c.s.weaken_duration] = 900
        unit[x][c.s.wave_chance] = 100
        unit[x][c.s.wave_level] = 30
        unit[x][c.s.is_miniwave] = 1
        unit[x][c.s.kbs] = 2000
        unit[x][c.s.recharge] = 1030 #makes for about a minute of recharge
        for trait in c.t:
            unit[x][trait] = 1
    unit[0][c.s.hp] = 2000
    unit[0][c.s.attack] = 200 #the wave hit
    unit[0][c.s.multi_damage_2] = 300
    unit[0][c.s.multi_damage_3] = 300
    unit[1][c.s.hp] = 2500
    unit[1][c.s.attack] = 300 #the wave hit
    unit[1][c.s.multi_damage_2] = 400
    unit[1][c.s.multi_damage_3] = 400



    return stats












