"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def capsule(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 28
    unit = stats[unit_id] #passing things as a reference oh lord help me

    for x in range(0,2):
        unit[x][c.s.attack] = 800
        unit[x][c.s.hp] = 0
        unit[x][c.s.lethal_chance] = 100
        unit[x][c.s.attack_only] = 1
        unit[x][c.t.metal] = x
        unit[x][c.t.white] = x
        unit[x][c.t.aku] = x
        unit[x][c.t.relic] = x
        unit[x][c.t.zombie] = x
        unit[x][c.t.dark] = 1-x
        unit[x][c.t.angel] = 1-x
        unit[x][c.t.red] = 1-x
        unit[x][c.t.alien] = 1-x
        unit[x][c.t.floating] = 1-x


    return stats

