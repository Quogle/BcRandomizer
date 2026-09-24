"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def vacation(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 122
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #vacation, increased kb
    for x in range(0,2):
        unit[x][c.s.kb_chance] = 40
    unit[2][c.s.kb_chance] = 100
    #gets triple hit in tf
    unit[2][c.s.multi_damage_2] = 120
    unit[2][c.s.multi_has_ability_2] = 1
    unit[2][c.s.multi_preatk_2] = 82
    unit[2][c.s.multi_damage_3] = 120
    unit[2][c.s.multi_has_ability_3] = 1
    unit[2][c.s.multi_preatk_3] = 84

    return stats










