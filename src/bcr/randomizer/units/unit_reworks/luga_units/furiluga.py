"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c


#this one should mostly be in its final form
def furiluga(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 625
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #furiluga
    #suicide but with higher range than its supposed to have and more attacks to balance out the fact it can actually die
    #theres actually nothing incorrect to give this unit currently
    #proper stats
    unit[0][c.s.range] = 350 #this is intended to smaller
    unit[0][c.s.tba] = 0
    unit[0][c.s.attack_state] = 2
    unit[0][c.s.attack_count] = 5 #this is intended to be 3
    unit[0][c.s.hp] = 1300 #was 500
    unit[0][c.s.surge_width_four] = 2200
    unit[0][c.s.surge_start_four] = 800
    unit[0][c.s.surge_level] = 1
    unit[0][c.s.surge_chance] = 100 #this unit is actually supposed to have surge
    unit[0][c.s.barrier_break_chance] = 100
    unit[0][c.s.shield_pierce_chance] = 100
    #note if I decrease the animation time the pre attack will have to be shifted


    return stats

