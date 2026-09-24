"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c


#this still might be a little too weak, could also have its stats scale abnormally so it stays usabled late game
def mint(stats:list[list[list]],remove_metals=True):
    """ applies the rework to
    \n nonconditional """
    unit_id = 184
    unit = stats[unit_id] #passing things as a reference oh lord help me

    for x in range(0,2):
        unit[x][c.s.attack] = 140 #was 60
        unit[x][c.s.hp] = 500 #was 350
        unit[x][c.s.cost] = 350 #was 660
        unit[x][c.s.recharge] = 350 #was 650
        unit[x][c.s.kbs] = 4

    unit[0][c.t.alien] = 1
    if remove_metals:
        unit[1][c.t.metal] = 1
    else:
        unit[1][c.t.red] = 1



    return stats



