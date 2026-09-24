"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c



def merc(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 121
    unit = stats[unit_id] #passing things as a reference oh lord help me

    for x in range(0,3):
        unit[x][c.s.hp] = 800 #was 100
        unit[x][c.s.recharge] = 500 #was 590(295 in tf), makes for about 24 seconds of respawn
        unit[x][c.s.kbs] = 4 #was 2
        unit[x][c.s.attack] = 300
        unit[x][c.s.multi_damage_2] = 300
        unit[x][c.s.multi_damage_3] = 300
        unit[x][c.s.crit_chance] = 20
        #multihit info dont need no changing for balancing
        unit[x][c.s.preatk] = 1
        unit[x][c.s.multi_preatk_2] = 3
        unit[x][c.s.multi_preatk_3] = 5
        unit[x][c.s.multi_has_ability_1] = 1
        unit[x][c.s.multi_has_ability_2] = 1
        unit[x][c.s.multi_has_ability_3] = 1
        unit[x][c.s.ld_minimum] = 155
        unit[x][c.s.ld_width] = -475
        unit[x][c.s.multi_ld_2_exists] = 1
        unit[x][c.s.multi_ld_2_start] = -320
        unit[x][c.s.multi_ld_2_width] = 550
        unit[x][c.s.multi_ld_3_exists] = 1
        unit[x][c.s.multi_ld_3_start] = -320
        unit[x][c.s.multi_ld_3_width] = 625
    #make first form weaker (why its not like its an eoc unit)
    unit[0][c.s.attack] = 100
    unit[0][c.s.multi_damage_2] = 100
    unit[0][c.s.multi_damage_3] = 100
    #true form gets gauranteed crit
    unit[2][c.s.crit_chance] = 100
    #



    levels = gf.file_reader(fn.LEVEL_STAT_GAIN)
    if levels != None:
        levels[unit_id] = [20,20,20,20,20,20,10,10,10,10,10,10,10,10,10,10,10,10,10,10]
        gf.file_writer(fn.LEVEL_STAT_GAIN,levels)





    return stats












