"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def tricycle(stats:list[list[list]],remove_metals:bool=True):
    """ applies the rework to
    \n nonconditional """
    unit_id = 17
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #tricycle, gets stats based on animation
    #first form, explosion (this seems really weak still)
    unit[0][c.s.recharge] = 350
    unit[0][c.s.tba] = 56 #makes for a 132f cycle
    unit[0][c.s.range] = 250 #was 170
    unit[0][c.s.explode_chance] = 100
    unit[0][c.s.explode_at] = 1000
    unit[0][c.s.attack] = 400 #was 180
    unit[0][c.s.speed] = 7 #was 10
    unit[0][c.s.hp] = 580 #was 400
    #second form, constant attacks with massive against 2 traits, very fragile and expensive but has like 25k dps
    unit[1][c.s.recharge] = 195 #makes for 176f
    unit[1][c.s.range] = 195 #was 170
    unit[1][c.s.tba] = 0 #makes for 46f cycle, was 59f cycle
    unit[1][c.s.kbs] = 1 #was 4
    unit[1][c.s.cost] = 950 #was 700
    unit[1][c.s.hp] = 640 #was 400, makes for about 10880 hp at 30
    if remove_metals:
        unit[1][c.t.metal] = 1
    else:
        unit[1][c.t.aku] = 1
    unit[1][c.t.red] = 1
    unit[1][c.s.massive] = 1
    unit[1][c.s.attack] = 180
    unit[1][c.s.multi_damage_2] = 180
    unit[1][c.s.multi_damage_3] = 180
    unit[1][c.s.preatk] = 16 #already was 16
    unit[1][c.s.multi_preatk_2] = 21
    unit[1][c.s.multi_preatk_3] = 33
    #third form, surge past target
    unit[2][c.s.attack] = 400 #makes for 6800 at 30, was 180
    unit[2][c.s.hp] = 780 #makes for 13260 at 30, was 400
    unit[2][c.s.recharge] = 190 #makes for 116f
    unit[2][c.s.surge_chance] = 100
    unit[2][c.s.surge_level] = 1
    unit[2][c.s.surge_start_four] = 1300
    unit[2][c.s.surge_width_four] = 250


    return stats












