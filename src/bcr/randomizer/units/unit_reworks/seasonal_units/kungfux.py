"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def kungfux(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 132
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #kungfu, all attacks/hp increased, first form has weak berserk at low hp, second form bounty on last hit, true form has wave on first hit to clear peon
    for x in range(0,3):
        unit[x][c.s.hp] = 2132 #makes for 36244 at 30, was 999
    #first form has a desperation mode
    unit[0][c.s.attack] = 1780 #makes for 30260 at 30 was 1280
    unit[0][c.s.strengthen_by] = 200
    unit[0][c.s.strengthen_at] = 10
    #second form has curse on the last hit against red dark and angel
    (unit[1][c.s.attack],unit[1][c.s.multi_damage_2],unit[1][c.s.multi_damage_3]) = (372,214,1746) #makes for (6324,3638,29682) at 30, was (282,140,986)
    unit[1][c.s.multi_has_ability_1] = 0
    unit[1][c.s.multi_has_ability_2] = 0
    unit[1][c.s.multi_has_ability_3] = 1
    unit[1][c.s.curse_chance] = 100
    unit[1][c.s.curse_time] = 300
    unit[1][c.t.red] = 1
    unit[1][c.t.dark] = 1
    unit[1][c.t.angel] = 1
    #third form has wave on the first hit
    (unit[2][c.s.attack],unit[2][c.s.multi_damage_2],unit[2][c.s.multi_damage_3]) = (427,234,1646) #makes for (7259,3978,27982) at 30, was (370,184,1294)
    unit[2][c.s.multi_has_ability_1] = 1
    unit[2][c.s.multi_has_ability_2] = 0
    unit[2][c.s.multi_has_ability_3] = 0
    unit[2][c.s.wave_chance] = 100
    unit[2][c.s.wave_level] = 2



    return stats












