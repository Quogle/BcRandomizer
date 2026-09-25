"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c
import tadbcmc.data.enums.unitbuy as ub




def schoolgirl_lion(stats:list[list[list]],all_unit_downs=False):
    """ applies the rework to
    \n nonconditional """
    unit_id = 651
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #first form is the one billion lions
    unit[0][c.s.spirit_summon] = unit_id
    unit[0][c.s.range] = 5000
    unit[0][c.s.recharge] = 2400 #this is like a 150 second cooldown
    unit[0][c.s.cost] = 11000 #16.5k
    if all_unit_downs:
        unit[0][c.s.cost] = 9160 #with a 20% cost increase this results in a 16500 cost unit
    unit[0][c.s.hp] = 18000
    unit[0][c.s.kbs] = 100
    unit[0][c.s.strong] = 0
    for trait in c.t:
        unit[0][trait] = 1
    unit[0][c.s.kb_chance] = 100
    unit[0][c.s.freeze_chance] = 100
    unit[0][c.s.freeze_duration] = 13
    unit[0][c.s.slow_chance] = 100
    unit[0][c.s.slow_duration] = 13
    #giving multihit
    unit[0][c.s.attack] = 100
    unit[0][c.s.multi_damage_2] = 100
    unit[0][c.s.multi_damage_3] = 100
    unit[0][c.s.preatk] = 3
    unit[0][c.s.multi_preatk_2] = 6
    unit[0][c.s.multi_preatk_3] = 9
    unit[0][c.s.multi_has_ability_1] = 1
    unit[0][c.s.multi_has_ability_2] = 1
    unit[0][c.s.multi_has_ability_3] = 1
    #this needs to be suicide aint it
    unit[0][c.s.dies_of_cringe] = 450
    unit[0][c.s.attack_count] = 0 #does this work?
    unit[0][c.s.attack_state] = 0 #just gonna stand there
    #I think Im gonna make it explode for now?
    unit[0][c.s.explode_chance] = 100
    unit[0][c.s.explode_at] = 400
    unit[0][c.s.explode_variation_x4] = 13600
    unit[0][c.s.surge_chance] = 100
    unit[0][c.s.surge_level] = 4 #maybe this should be higher?
    unit[0][c.s.surge_start_four] = 400
    unit[0][c.s.surge_width_four] = 13600
    unit[0][c.s.wave_chance] = 100
    unit[0][c.s.wave_level] = 24
    


    #making it have actual levels in unitbuy
    unitbuy = gf.file_reader(fn.UNITBUY_FILE)
    unitbuy[unit_id][ub.ub.max_level] = 30
    unitbuy[unit_id][ub.ub.default_max_level] = 10
    unitbuy[unit_id][ub.ub.max_catseyes_level] = 80
    #unitbuy[unit_id][ub.ub] #was intending to make the level to evolve absurdly high to stop it from getting a second form ever
    gf.file_writer(fn.UNITBUY_FILE,unitbuy)


    levels = gf.file_reader(fn.LEVEL_STAT_GAIN)
    if levels != None:
        levels[unit_id] = [20,20,20,20,20,20,20,20,20,20,20,20,10,10,10,10,10,10,10,10]
        gf.file_writer(fn.LEVEL_STAT_GAIN,levels)

    #so I have the intention to increase its level cap slowly over time but I dont currently know how to do that
    #an idea I have is maybe it gets 1 additional level from each like advent and such type things? is that how that works?






    return stats


