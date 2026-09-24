"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def punt(stats:list[list[list]],remove_metals=True):
    """ applies the rework to
    \n nonconditional """
    unit_id = 26
    unit = stats[unit_id] #passing things as a reference oh lord help me


    for x in range(0,3):
        unit[x][c.s.hp] = 1000
        unit[x][c.s.attack] = 1000
        unit[x][c.s.weaken_chance] = 100
        unit[x][c.s.weaken_to] = 50
        unit[x][c.s.weaken_duration] = 150
        if remove_metals:
            unit[x][c.t.metal]
        else:
            unit[x][c.t.red]
    unit[2][c.s.attack] = 1200
    unit[2][c.s.weaken_to] = 10



    return stats

