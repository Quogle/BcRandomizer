import dev.randomizer.enums.cats as c
import dev.randomizer.func.files as f
from dev.randomizer.parse_config import settings
import copy

"""
rebalancers
"""
def make_base_cat(cstat):
    new_stats = copy.deepcopy(cstat)
    new_stats = early_reworks(new_stats)
    return new_stats


def early_reworks(cstats):
    """
    applies the reworks from congif
    """
    changes = settings["game"]["gameplay"]["unit_reworks"]
    if changes["rework_units"]:
        courier = changes["courier"]
        jurassic = changes["jurassic"]
        space = changes["space"]
        jumprope = changes["jumprope"]
        hurricat = changes["hurricat"]
        waitress = changes["waitress"]
        researcher = changes["aku_researcher"]
        backhoe = changes["backhoe"]
        mint = changes["mint"]
        punt = changes["punt"]
        merc = changes["merc"]
        capsule = changes["capsule"]
        racism_cow = changes["racism_cow"]
        reaper = changes["reaper"]
        million_dollar = changes["million_dollar"]
        cop = changes["cop"]
        paladin = changes["paladin"]
        cat_clan = changes["cat_clan"]
        verbena = changes["verbena"]
        hayabusa = changes["hayabusa"]
        moneko = changes["moneko"]
        neneko = changes["neneko"]
        summer_neneko = changes["summer_neneko"]
        new_year_neneko = changes["new_year_neneko"]
        valentine_neneko = changes["valentine_neneko"]
        easter_neneko = changes["easter_neneko"]
        cmoneko = changes["cmoneko"]

        #all 3 form changes
        for x in range(0,3):
            if courier:
                cstats[658][x][c.t.red] = 0
                cstats[658][x][c.s.massive] = 0
            if jurassic:
                cstats[46][x][c.s.savage_by] = 200
                cstats[46][x][c.s.savage_chance] = 5
                cstats[46][x][c.s.cost] = 500
            if space:
                cstats[48][x][c.s.crit_chance] = 20
            if jumprope:
                cstats[88][x][c.s.hp] = 600
            if hurricat:
                cstats[267][x][c.s.savage_by] = 200
                cstats[267][x][c.s.savage_chance] = 5
                cstats[267][x][c.s.multi_damage_2] = 30
                cstats[267][x][c.s.multi_damage_3] = 30
                cstats[267][x][c.s.multi_has_ability_2] = 1
                cstats[267][x][c.s.multi_has_ability_3] = 1
                cstats[267][x][c.s.multi_preatk_2] = 3
                cstats[267][x][c.s.multi_preatk_3] = 5
            if waitress:
                cstats[273][x][c.s.savage_by] = 300
                cstats[273][x][c.s.savage_chance] = 100
                cstats[273][x][c.t.metal] = 1
                cstats[273][x][c.s.strong] = 1
            if researcher:
                cstats[621][x][c.s.massive] = 1
                cstats[621][x][c.t.metal] = 1
            if backhoe:
                cstats[446][x][c.s.attack] = 100
                cstats[446][x][c.s.multi_damage_2] = 100
                cstats[446][x][c.s.multi_damage_3] = 100
                cstats[446][x][c.s.multi_preatk_2] = 61
                cstats[446][x][c.s.multi_preatk_3] = 62
                cstats[446][x][c.s.multi_has_ability_2] = 1
                cstats[446][x][c.s.multi_has_ability_3] = 1
                cstats[446][x][c.s.curse_chance] = 50
                cstats[446][x][c.s.curse_time] = 100
                cstats[446][x][c.s.explode_chance] = 50
                cstats[446][x][c.s.explode_at] = 1000
                cstats[446][x][c.s.explode_variation_x4] = 3000
            if mint and x<2:
                cstats[184][x][c.s.attack] = 140
                cstats[184][x][c.s.cost] = 350
                cstats[184][x][c.s.recharge] = 400
                cstats[184][x][c.s.hp] = 500
                cstats[184][x][c.s.kbs] = 4
            if punt:
                cstats[26][x][c.s.metal] = 1
                cstats[26][x][c.s.hp] = 1000
                cstats[26][x][c.s.attack] = 1000
                cstats[26][x][c.s.weaken_chance] = 100
                cstats[26][x][c.s.weaken_duration] = 150
                cstats[26][x][c.s.weaken_to] = 50
            if merc:
                cstats[121][x][c.s.hp] = 800
                cstats[121][x][c.s.kbs] = 4
                cstats[121][x][c.s.attack] = 100
                cstats[121][x][c.s.multi_damage_2] = 100
                cstats[121][x][c.s.multi_damage_3] = 100
                cstats[121][x][c.s.ld_minimum] = 155
                cstats[121][x][c.s.ld_width] = -475
                cstats[121][x][c.s.multi_ld_2_start] = -320
                cstats[121][x][c.s.multi_ld_3_start] = -320
                cstats[121][x][c.s.multi_ld_2_width] = 550
                cstats[121][x][c.s.multi_ld_3_width] = 625
                cstats[121][x][c.s.multi_ld_2_exists] = 1
                cstats[121][x][c.s.multi_ld_3_exists] = 1
                cstats[121][x][c.s.multi_preatk_2] = 3
                cstats[121][x][c.s.multi_preatk_3] = 5
                cstats[121][x][c.s.multi_has_ability_2] = 1
                cstats[121][x][c.s.multi_has_ability_3] = 1
                cstats[121][x][c.s.savage_by] = 200
                cstats[121][x][c.s.crit_chance] = 20
                cstats[121][x][c.s.savage_chance] = 20
            if capsule and x<2:
                cstats[28][x][c.t.metal] = 1
                cstats[28][x][c.s.attack] = 500
                cstats[28][x][c.s.massive] = 1
            if racism_cow and x<2:
                cstats[65][x][c.s.hp] = 1300        #normally 500hp
                cstats[65][x][c.s.attack] = 80      #normally 30 damage
            if reaper:
                cstats[68][x][c.s.slow_chance] = 60 #normally 40%
                cstats[68][x][c.s.slow_duration] = 120 #normally 120
                cstats[68][x][c.s.cost] = 750       #normally 500
                cstats[68][x][c.s.attack] = 470     #does 7990 at lvl30
                cstats[68][x][c.s.hp] = 700         #normally 700 2nd form
            if million_dollar and x<2:
                cstats[635][x][c.s.savage_by] = 500
                cstats[635][x][c.s.savage_chance] = 100
                cstats[635][x][c.s.eva_killer] = 1
            if cop and x>0:
                cstats[716][x][c.t.white] = 0
                cstats[716][x][c.t.black] = 1
                cstats[716][x][c.t.red] = 1
                cstats[716][x][c.t.alien] = 1
            if paladin:
                cstats[57][x][c.s.savage_by] = 200
                cstats[57][x][c.s.tba] = 100        #normally 60
            if cat_clan:
                cstats[427][x][c.s.savage_by] = 200
                cstats[427][x][c.s.savage_chance] = 3
            if moneko:
                cstats[16][x][c.s.bounty] = 1
            if neneko:
                cstats[131][x][c.t.metal] = 1
                cstats[131][x][c.s.savage_by] = 200
                cstats[131][x][c.s.savage_chance] = 15
                cstats[131][x][c.s.insane_massive] = 1
            if summer_neneko:
                cstats[276][x][c.s.massive] = 1
                cstats[276][x][c.s.insane_massive] = 1
                cstats[276][x][c.t.metal] = 1
            if new_year_neneko:
                cstats[314][x][c.s.tba] = 0
                cstats[314][x][c.s.savage_by] = 200
                cstats[314][x][c.s.savage_chance] = 15
            if valentine_neneko:
                cstats[589][x][c.s.wave_level] = 4
                cstats[589][x][c.s.range] = 410
            if easter_neneko:
                cstats[332][x][c.s.weaken_chance] = 50
                cstats[332][x][c.s.slow_chance] = 50
                cstats[332][x][c.s.freeze_chance] = 50
                #cstats[332][x][c.s.kb_chance] = 50 #might be too strong
                cstats[332][x][c.s.area] = 1
                cstats[332][x][c.t.metal] = 1
                cstats[332][x][c.s.weaken_duration] = 40
                cstats[332][x][c.s.slow_duration] = 40
                cstats[332][x][c.s.freeze_duration] = 40
                cstats[332][x][c.s.weaken_to] = 50
            if cmoneko and x<2:
                cstats[418][x][c.s.savage_by] = 200
                cstats[418][x][c.s.savage_chance] = 100
            if verbena:
                cstats[358][x][c.s.savage_by] = 200
                cstats[358][x][c.s.savage_chance] = 30
                cstats[358][x][c.s.crit_chance] = 30
        

        #single form changes
        if jurassic:
            cstats[46][0][c.s.hp] = 570
            cstats[46][1][c.s.hp] = 900
            cstats[46][2][c.s.hp] = 1400
            cstats[46][0][c.s.attack] = 200
            cstats[46][1][c.s.attack] = 250
            cstats[46][2][c.s.attack] = 300
            cstats[46][2][c.s.savage_chance] = 12
        if hurricat:
            cstats[267][0][c.s.multi_damage_2] = 24
            cstats[267][0][c.s.multi_damage_3] = 24
        if backhoe:
            cstats[446][2][c.s.curse_chance] = 100
            cstats[446][2][c.s.explode_chance] = 100
        if mint:
            cstats[184][1][c.t.alien] = 0
            cstats[184][1][c.t.metal] = 1
        if punt:
            cstats[26][x][c.s.attack] = 1200
            cstats[26][x][c.s.weaken_to] = 10
        if merc:
            cstats[121][2][c.s.crit_chance] = 100
            cstats[121][2][c.s.savage_chance] = 100
        if reaper:
            cstats[68][2][c.s.attack] = 200     #does 7990 at lvl30
            cstats[68][2][c.s.multi_damage_2] = 400
            cstats[68][2][c.s.multi_damage_3] = 800
            cstats[68][2][c.s.hp] = 1000         #normally 700 2nd form
            cstats[68][2][c.s.multi_has_ability_2] = 1
            cstats[68][2][c.s.multi_has_ability_3] = 1
            cstats[68][2][c.s.preatk] = 16
            cstats[68][2][c.s.multi_preatk_2] = 57
            cstats[68][2][c.s.multi_preatk_3] = 83
        if paladin:
            cstats[57][0][c.s.hp] = 2000
            cstats[57][1][c.s.hp] = 3000
            cstats[57][2][c.s.hp] = 4000
            cstats[57][0][c.s.savage_chance] = 20
            cstats[57][1][c.s.savage_chance] = 40
            cstats[57][2][c.s.savage_chance] = 50
            cstats[57][0][c.s.attack] = 600
            cstats[57][1][c.s.attack] = 1000
            cstats[57][2][c.s.attack] = 1200
            cstats[57][2][c.s.soul_strike] = 1
        if moneko:
            cstats[16][2][c.s.is_miniwave] = 0
        if valentine_neneko:
            cstats[589][2][c.s.shield_pierce_chance] = 50
        if easter_neneko:
            cstats[332][x][c.s.weaken_duration] = 90
            cstats[332][x][c.s.slow_duration] = 90
            cstats[332][x][c.s.freeze_duration] = 90
        if verbena:
            cstats[358][2][c.s.crit_chance] = 50
            cstats[358][2][c.s.savage_chance] = 50
        if hayabusa:
            cstats[261][0][c.s.savage_by] = 200
            cstats[261][0][c.s.savage_chance] = 30
    

    return cstats

         










#the 3d array straight from the files
vanilla_cat_array = f.read_vanilla_cat_stats()

vanilla_unitbuy_array = f.read_vanilla_unitbuy()

#the 3d array with the before everything reworks applied to it
base_cat_array = make_base_cat(vanilla_cat_array)



