"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c


#genuinely what am I doing with this one
def betrothed_balaluga(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 711
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #betrothed balaluga
    #Im completely disregarding what I wrote for this unit in favour of something really fucky
    unit[0][c.s.base_destroyer] = 1
    unit[0][c.s.tba] = 0
    unit[0][c.s.multi_damage_2] = 100
    unit[0][c.s.ld_minimum] = 1000
    unit[0][c.s.ld_width] = 1000
    unit[0][c.s.soul_strike] = 1
    unit[0][c.s.range] = -300 #it sits slightly in the zombies respawn range


    return stats

