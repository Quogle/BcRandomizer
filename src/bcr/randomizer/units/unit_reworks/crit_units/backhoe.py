"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def backhoe(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 446
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #backhoe, the multihit exploding curser, still has attack only, curse and explode are 100% in tf, still has bounty but who cares
    for x in range(0,3):
        unit[x][c.s.multi_preatk_2] = 61 #fuck u ponos why can these not be on the same frame
        unit[x][c.s.multi_preatk_3] = 62
        unit[x][c.s.multi_damage_2] = 100
        unit[x][c.s.multi_damage_3] = 100
        unit[x][c.s.attack] = 100
        unit[x][c.s.multi_has_ability_1] = 1
        unit[x][c.s.multi_has_ability_2] = 1
        unit[x][c.s.multi_has_ability_3] = 1
        unit[x][c.s.curse_time] = 100
        unit[x][c.s.explode_at] = 1000
        unit[x][c.s.explode_variation_x4] = 3000
        unit[x][c.s.crit_chance] = 0
        unit[x][c.s.curse_chance] = 50
        unit[x][c.s.explode_chance] = 50
        unit[x][c.s.attack_only] = 0
    unit[2][c.s.curse_chance] = 100
    unit[2][c.s.explode_chance] = 100
    unit[2][c.s.surge_chance] = 0 #prevent it from being too sloppy, this should hide all the other surge information


    return stats












