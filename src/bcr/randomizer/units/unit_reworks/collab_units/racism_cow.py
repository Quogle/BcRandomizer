"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c


#dunno what to do with this
def racism_cow(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 65
    unit = stats[unit_id] #passing things as a reference oh lord help me

    for x in range(0,2):
        unit[x][c.s.hp] = 2200 #was 500
        unit[x][c.s.attack] = 167 #was 30
        unit[x][c.s.recharge] = 205 #makes for 146f recharge, for note mlion is 126
        unit[x][c.s.cost] = 600 #was 500

    return stats


