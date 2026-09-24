"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def maiden(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 100
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #maiden, increased stats to be roughly on par with jams, also gets slow and weak imm in tf (to add to its base freeze imm)
    #for note jam has 2000hp/560atk
    (unit[0][c.s.hp],unit[1][c.s.hp],unit[2][c.s.hp]) = (1800,1800,2800) #was (994,994,1988), results in (30600,30600,47600)
    (unit[0][c.s.attack],unit[1][c.s.attack],unit[2][c.s.attack]) = (500,500,600) #was (277,277,277), results in (8500,8500,10200)
    unit[2][c.s.slow_immune] = 1
    unit[2][c.s.weaken_immune] = 1
    unit[2][c.s.kb_immune] = 1
    #screw it Im giving it omni
    unit[2][c.s.ld_minimum] = 185
    unit[2][c.s.ld_width] = -505

    return stats












