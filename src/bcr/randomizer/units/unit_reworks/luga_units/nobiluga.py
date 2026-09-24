"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c


#NOT A CLUE WHAT IM DOING WITH THIS
def nobiluga(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 436
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #nobiluga
    for trait in c.t:
        [unit][0][trait] = 1
    #gonna make it a suicide wave unit, trying out funky berserker on the wave
    unit[0][c.s.attack_state] = 2
    unit[0][c.s.attack_count] = 1
    unit[0][c.s.range] = 300
    unit[0][c.s.hp] = 0 #im just ggiving 0 hp to make them immortal instead of dodge
    unit[0][c.s.speed] = 10
    unit[0][c.s.surge_chance] = 100
    unit[0][c.s.surge_start_four] = 2000 #there will be no surge width generally


    unit[0][c.s.surge_chance] = 0 #im actually not giving this surge currently but it does get all the other things
    unit[0][c.s.wave_chance] = 100
    unit[0][c.s.wave_level] = 6
    unit[0][c.s.multi_damage_2] = 500
    unit[0][c.s.strengthen_at] = 100
    unit[0][c.s.strengthen_by] = 900
    """ temp """
    unit[0][c.s.multi_preatk_2] = 20
    unit[0][c.s.wave_level] = 24
    #unit[0][c.s.lethal_chance] = 100 #this doesnt work :pensive




    return stats












