"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def madam(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 109
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #madam, expensive af tanky meatshield, faster recharge, more speed in tf, hp increased slightly (might need more since its so expensive)
    for x in range(0,3):
        unit[x][c.s.recharge] = 180 #for 96f, was 240
    (unit[0][c.s.hp],unit[1][c.s.hp],unit[2][c.s.hp]) = (1200,1200,2000) #was (1140,1140,1710)
    unit[2][c.s.speed] = 11


    return stats












