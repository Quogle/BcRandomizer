"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def pumpcat(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 227
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #pumpcat, increased freeze, for note the attack cycle for pumpcat is 183f
    unit[1][c.s.freeze_chance] = 40 #was 20
    unit[1][c.s.freeze_duration] = 120 #was 60
    #tf
    unit[2][c.s.freeze_chance] = 60 #was 20
    unit[2][c.s.freeze_duration] = 140 #was 60



    return stats












