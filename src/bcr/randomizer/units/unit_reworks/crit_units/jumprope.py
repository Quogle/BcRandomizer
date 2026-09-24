"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def jumprope(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 88
    unit = stats[unit_id] #passing things as a reference oh lord help me
    #jumprope, the actually usable meatshield, literally just give it more hp and remove the crit (cause id find crit on an actually usable meatshield to take away from the feeling of crits)
    for x in range(0,3):
        unit[x][c.s.crit_chance] = 0
        unit[x][c.s.hp] = 800 #needs testing, in my opinion it should be an actually decent ms since it costs so much


    return stats












