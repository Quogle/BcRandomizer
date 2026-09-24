"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def doll(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 81
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #doll, increased hp/attack, decreased cost, lvl 1 wave in all forms (lvl5 in tf)
    for x in range(0,3):
        unit[x][c.s.cost] = 500 #was 650 #honestly this might need to be lower
        unit[x][c.s.wave_level] = 1
        unit[x][c.s.wave_chance] = 100
        unit[x][c.s.hp] =  900 #was 300, this still seems very low
        unit[x][c.s.kbs] = 2 #was 4
        unit[x][c.s.attack] = 200 #was 167
    unit[2][c.s.wave_level] = 5


    return stats












