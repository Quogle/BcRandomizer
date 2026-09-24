"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def goemon(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 49
    unit = stats[unit_id] #passing things as a reference oh lord help me

    for x in range(0,3):
        unit[x][c.s.multi_preatk_2] = 16
        unit[x][c.s.multi_preatk_3] = 17
    #damage
    unit[0][c.s.attack] = 18 #og was 54 in one hit
    unit[0][c.s.multi_damage_2] = 18
    unit[0][c.s.multi_damage_3] = 18
    unit[1][c.s.attack] = 30 #og was 64 in one hit
    unit[1][c.s.multi_damage_2] = 30
    unit[1][c.s.multi_damage_3] = 30
    unit[2][c.s.attack] = 50 #og was 96 in one hit
    unit[2][c.s.multi_damage_2] = 50
    unit[2][c.s.multi_damage_3] = 50
    #true form Im giving it increased strengthen
    #this should stack additively with talents right?
    unit[2][c.s.strengthen_at] = 33
    unit[2][c.s.strengthen_by] = 150


    return stats












