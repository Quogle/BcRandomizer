"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def ritual(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 70
    unit = stats[unit_id] #passing things as a reference oh lord help me


    #ritual, loses trait things, gains stats, stronger berserk, little omni, its kinda like a bird but tankier and hits slower
    for x in range(0,3):
        unit[x][c.t.red] = 0
        unit[x][c.s.strong] = 0
        unit[x][c.s.ld_minimum] = 240
        unit[x][c.s.ld_width] = -560
    (unit[0][c.s.hp],unit[1][c.s.hp],unit[2][c.s.hp]) = (1500,1500,2500) #was (700,700,1200)
    (unit[0][c.s.attack],unit[1][c.s.attack],unit[2][c.s.attack]) = (440,440,550) #was (160,160,320) #for note, mflying has 724
    unit[0][c.s.strengthen_by] = 100 #was 100


    return stats









