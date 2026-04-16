from dev.randomizer.func.random import randinst
from dev.randomizer.parse_config import settings
import dev.randomizer.enums.enemy as e
import dev.randomizer.enums.cats as c
import dev.randomizer.enums.item as item
import dev.randomizer.func.game_files as f
import dev.randomizer.func.random as random
from dev.randomizer.data.filepaths import *
from dev.randomizer.func.misc import *
import os




def early_sol_xp_buff():
    """
    buffs pre ururun stages xp
    conditional
    """
    if not settings["game"]["qol"]["stage_changes"]["sol_xp_buff"]:
        return
    current_map = "000"
    for x in range(0,18):
        mult = int(20-x/1.8)/10
        map_data = f.map_data(MAPSTAGEDATA + SOL_MLETTER + "_" + current_map + ".csv")
        current_map = random.number_string_stepper(current_map,3)
        for each in map_data.stages:
            each[map_data.xp] = int(each[map_data.xp]*mult)
        map_data.submit()

def buff_ticket_farming():
    """
    buffs hate siege and fd
    conditional
    """
    changes = settings["game"]["qol"]["stage_changes"]
    hate = changes["hate_metal_hippoe_buff"]
    siege = changes["siege_buff"]
    fd = changes["facing_danger_buff"]

    if hate: #set to 100% for now
        map_data = f.map_data(MAPSTAGEDATA + EVENT_STAGE_MLETTER + "_006.csv")
        map_data.stages[0][map_data.drop1_rate] = 100
        map_data.submit()
    if siege: #set to 3 tickets for now
        map_data = f.map_data(MAPSTAGEDATA + EVENT_STAGE_MLETTER + "_007.csv")
        map_data.stages[0][map_data.drop1_count] = 3
        map_data.submit()
    if fd: # 50-50 of 10 or 15
        map_data = f.map_data(MAPSTAGEDATA + EVENT_STAGE_MLETTER + "_078.csv")
        map_data.stages[0][map_data.drop1_count] = 15
        map_data.stages[0][map_data.drop2_count] = 10
        map_data.stages[0][map_data.drop1_rate] = 50
        map_data.stages[0][map_data.drop2_rate] = 10
        map_data.submit()

def buff_itf_aliens():
    """
    increases mags of ex aliens, will attempt to read from file to determine what to buff
    conditional, post enemies written to file
    """
    do_a = settings["game"]["gameplay"]["preserve_alien_mags_main_chapters"]
    remove_itf_crystals = settings["game"]["gameplay"]["remove_itf_crystals"]
    if do_a:
        vanilla_enemy_array = f.file_reader(DATA_LOCAL + ENEMY_STATS)
        new_stats = f.file_reader(ENEMY_STATS)
        itf_path_start = STAGE_SCHEM + ITF_SLETTER + "0"
        itf_chapters = ["4","5","6"]
        mag_base = 7
        mag_red_at = 23
        for chapter in range(0,len(itf_chapters)):
            for stage in range(0,48):
                mag_mult = mag_base - (chapter*2) - (int(stage/mag_red_at))
                stage_end = "0" + str(stage) + ".csv"
                this_stage = f.stage_sche(itf_path_start + itf_chapters[chapter] + "_" + stage_end[-6:])
                for each in this_stage.enemies:
                    enemy_id = each[this_stage.enemy_id]
                    if vanilla_enemy_array[enemy_id][e.t.alien] == 1:
                        if new_stats[enemy_id][e.t.alien] != 1 or remove_itf_crystals:
                            mag = int(each[this_stage.magnification]*mag_mult)
                            each[this_stage.magnification] = mag
                this_stage.submit()
    
def buff_cotc_aliens():
    """
    increases mags of ex aliens, will attempt to read from file to determine what to buff
    conditional, post enemies written to file
    """
    
    do_a = settings["game"]["gameplay"]["preserve_alien_mags_main_chapters"]
    remove_cotc_crystals = settings["game"]["gameplay"]["remove_cotc_crystals"]
    if do_a:
        vanilla_enemy_array = f.file_reader(DATA_LOCAL + ENEMY_STATS)
        new_stats = f.file_reader(ENEMY_STATS)
        cotc_path_start = STAGE_SCHEM + COTC_SLETTER + "0"
        cotc_chapters = ["7","8","9"]
        mag_base = 16
        mag_red_at = [5,14,23,32,41]
        for chapter in range(0,len(cotc_chapters)):
            for stage in range(0,48):
                mag_mult = mag_base - (chapter*5)
                for each in mag_red_at:
                    if stage >= each:
                        mag_mult -= 1
                stage_end = "0" + str(stage) + ".csv"
                this_stage = f.stage_sche(cotc_path_start + cotc_chapters[chapter] + "_" + stage_end[-6:])
                for each in this_stage.enemies:
                    enemy_id = each[this_stage.enemy_id]
                    if vanilla_enemy_array[enemy_id][e.s.starred_god] == 1:
                        if new_stats[enemy_id][e.s.starred_god] != 1 or remove_cotc_crystals:
                            mag = int(each[this_stage.magnification]*mag_mult)
                            each[this_stage.magnification] = mag
                this_stage.submit()

def buff_cotc_aliens_in_sol_ul():
    """
    increases mags of ex starred aliens in sol, ul, and events
    \n conditional
    this func sucks to read
    """
    estats = f.file_reader(ENEMY_STATS)
    cotc1_sol_chapters = [42,43,44,45,47] #area 22 to barking bay not included
    cotc1_ul_chapters = [1,2,3]
    cotc2_chapters = [4,5,6,8,9,10] #barkying bay to cherry isles inclusive of both
    cotc1_events = [157] #the second dimension up to never not summer
    cotc2_events = [190] #never not summer to everything before red sky at night
    do_a = settings["game"]["gameplay"]["preserve_cotc_mags_sol_ul_events"]
    
    if do_a:
        mag_boost = 11
        #sol chapters
        for chapter in cotc1_sol_chapters:
            stage_number = 0
            while True:
                stage_number_string = "0" + str(stage_number) + ".csv"
                chapter_number_end = "00" + str(chapter) + "_" + stage_number_string[-6:]
                stage_name = STAGE_SCHEM + SOL_SLETTER + chapter_number_end[-9:]
                exists = buff_cotc_enemies_in_stage(stage_name,mag_boost,estats)
                if not exists:
                    break
                stage_number += 1
        #ul chapters
        for chapter in cotc1_ul_chapters:
            stage_number = 0
            while True:
                stage_number_string = "0" + str(stage_number) + ".csv"
                chapter_number_end = "00" + str(chapter) + "_" + stage_number_string[-6:]
                stage_name = STAGE_SCHEM + UL_SLETTER + chapter_number_end[-9:]
                exists = buff_cotc_enemies_in_stage(stage_name,mag_boost,estats)
                if not exists:
                    break
                stage_number += 1
        #cotc1 events
        for event in cotc1_events:
            stage_number = 0
            while True:
                stage_number_string = "0" + str(stage_number) + ".csv"
                chapter_number_end = "00" + str(event) + "_" + stage_number_string[-6:]
                stage_name = STAGE_SCHEM + EVENT_STAGE_SLETTER + chapter_number_end[-9:]
                exists = buff_cotc_enemies_in_stage(stage_name,mag_boost,estats)
                if not exists:
                    break
                stage_number += 1
        
        mag_boost = 6
        #cotc2 ul chapters
        for chapter in cotc2_chapters:
            stage_number = 0
            while True:
                stage_number_string = "0" + str(stage_number) + ".csv"
                chapter_number_end = "00" + str(chapter) + "_" + stage_number_string[-6:]
                stage_name = STAGE_SCHEM + UL_SLETTER + chapter_number_end[-9:]
                exists = buff_cotc_enemies_in_stage(stage_name,mag_boost,estats)
                if not exists:
                    break
                stage_number += 1
        
        #cotc2 events
        for event in cotc2_events:
            stage_number = 0
            while True:
                stage_number_string = "0" + str(stage_number) + ".csv"
                chapter_number_end = "00" + str(event) + "_" + stage_number_string[-6:]
                stage_name = STAGE_SCHEM + EVENT_STAGE_SLETTER + chapter_number_end[-9:]
                exists = buff_cotc_enemies_in_stage(stage_name,mag_boost,estats)
                if not exists:
                    break
                stage_number += 1
        
def buff_material():
    """
    increases material stage drop counts
    \n conditional
    """
    do_buff = settings["game"]["qol"]["stage_changes"]["material_stage_buff"]
    if not do_buff:
        return
    map_name_start = MAPSTAGEDATA + EVENT_STAGE_MLETTER + "_"
    cavern = f.map_data(map_name_start + stringize_number(150) + ".csv")
    island = f.map_data(map_name_start + stringize_number(151) + ".csv")
    strait = f.map_data(map_name_start + stringize_number(152) + ".csv")
    dummy = f.map_data()

    #shorten all stages to number of drops
    for each in cavern.stages:
        while len(each) > dummy.drop2_count+1:
            each.pop()
    for each in island.stages:
        while len(each) > dummy.drop2_count+1:
            each.pop()
    for each in strait.stages:
        while len(each) > dummy.drop3_count+1:
            each.pop()
    
    #now set all stage drop ids, rate, and count
    for x in range(0,3):
        cavern.stages[x][dummy.drop1_id] = item.drop_id.bricks
        cavern.stages[x][dummy.drop2_id] = item.drop_id.meteorite
        cavern.stages[x][dummy.drop1_rate] = 100
        cavern.stages[x][dummy.drop2_rate] = 100
        cavern.stages[x][dummy.drop_scheme] = -4
        cavern.stages[x][dummy.drop1_count] = int(2*(x+1))
        cavern.stages[x][dummy.drop2_count] = int(2*(x+1))

        island.stages[x][dummy.drop1_id] = item.drop_id.coal
        island.stages[x][dummy.drop2_id] = item.drop_id.beast_bones
        island.stages[x][dummy.drop1_rate] = 100
        island.stages[x][dummy.drop2_rate] = 100
        island.stages[x][dummy.drop_scheme] = -4
        island.stages[x][dummy.drop1_count] = int(2*(x+1))
        island.stages[x][dummy.drop2_count] = int(2*(x+1))

        strait.stages[x][dummy.drop1_id] = item.drop_id.feathers
        strait.stages[x][dummy.drop2_id] = item.drop_id.gold
        strait.stages[x][dummy.drop3_id] = item.drop_id.sprockets
        strait.stages[x][dummy.drop1_rate] = 100
        strait.stages[x][dummy.drop2_rate] = 100
        strait.stages[x][dummy.drop3_rate] = 100
        strait.stages[x][dummy.drop_scheme] = -4
        strait.stages[x][dummy.drop1_count] = int(2*(x+1))
        strait.stages[x][dummy.drop2_count] = int(2*(x+1))
        strait.stages[x][dummy.drop3_count] = int(2*(x+1))
    
    cavern.submit()
    island.submit()
    strait.submit()

def buff_xp_stages():
    """
    buffs xp stage weekend stage blitz collo and merci, youre welcome
    \n conditional
    """
    st_cha = settings["game"]["qol"]["stage_changes"]
    weekend = st_cha["weekend_stage_buff"]
    megablitz = st_cha["megablitz_buff"]
    collo = st_cha["colloseum_buff"]
    merci = st_cha["merciless_xp_buff"]
    event_start = MAPSTAGEDATA + EVENT_STAGE_MLETTER + "_"
    catamin_start = MAPSTAGEDATA + CATAMIN_MLETTER + "_"
    dummy = f.map_data()

    if weekend:
        weekend_stage_e = f.map_data(event_start + stringize_number(27,3) + ".csv")
        xp_stage_e = f.map_data(event_start + stringize_number(28,3) + ".csv")
        xp_stage_c = f.map_data(catamin_start + stringize_number(11,3) + ".csv")
        maps = [weekend_stage_e,xp_stage_e,xp_stage_c]
        #edit on all of them
        for each in maps:
            #reduce it to 2 drops
            for stage in each.stages:
                while len(stage) > dummy.drop2_count+1:
                    stage.pop()
                #set to 4 to 1 ratio
                stage[dummy.drop1_rate] = 20
                stage[dummy.drop2_rate] = 80
                stage[dummy.drop_scheme] = -4
                #do I have to set drop id, prolly not
            #high xp rewards
            each.stages[0][dummy.drop1_count] = 30000
            each.stages[1][dummy.drop1_count] = 40000
            each.stages[2][dummy.drop1_count] = 60000
            each.stages[3][dummy.drop1_count] = 80000
            each.stages[4][dummy.drop1_count] = 100000
            each.stages[5][dummy.drop1_count] = 140000
            #low xp rewards
            each.stages[0][dummy.drop2_count] = 10000
            each.stages[1][dummy.drop2_count] = 15000
            each.stages[2][dummy.drop2_count] = 25000
            each.stages[3][dummy.drop2_count] = 35000
            each.stages[4][dummy.drop2_count] = 45000
            each.stages[5][dummy.drop2_count] = 60000
            #set stage xp drop
            each.stages[0][dummy.xp] = 20000
            each.stages[1][dummy.xp] = 40000
            each.stages[2][dummy.xp] = 60000
            each.stages[3][dummy.xp] = 80000
            each.stages[4][dummy.xp] = 100000
            each.stages[5][dummy.xp] = 120000
            each.submit()
    if megablitz:
        megablitz_e = f.map_data(event_start + stringize_number(59,3) + ".csv")
        megablitz_c = f.map_data(catamin_start + stringize_number(10,3) + ".csv")
        maps = [megablitz_e,megablitz_c]
        #now act on each the same
        for each in maps:
            each.stages[0][dummy.drop1_rate] = 15
            each.stages[0][dummy.drop2_rate] = 40
            each.stages[0][dummy.xp] = 180000
            each.submit()
    if collo:
        collo_e = f.map_data(event_start + stringize_number(124,3) + ".csv")
        collo_c = f.map_data(catamin_start + stringize_number(9,3) + ".csv")
        maps = [collo_e,collo_c]
        #now act on each the same
        for each in maps:
            each.stages[0][dummy.drop1_rate] = 15
            each.stages[0][dummy.drop2_rate] = 40
            each.stages[0][dummy.drop1_count] = 1800000
            each.stages[0][dummy.xp] = 220000
            each.submit()
    if merci:
        merci_e = f.map_data(event_start + stringize_number(155,3) + ".csv")
        merci_c = f.map_data(catamin_start + stringize_number(8,3) + ".csv")
        maps = [merci_e,merci_c]
        #now act on each the same
        for each in maps:
            each.stages[0][dummy.drop1_rate] = 15
            each.stages[0][dummy.drop2_rate] = 50
            each.stages[0][dummy.drop1_count] = 2500000
            each.stages[0][dummy.drop2_count] = 1500000
            each.stages[0][dummy.drop3_count] = 1000000
            each.stages[0][dummy.xp] = 250000
            each.submit()
        


        











"""
parts of funcs above
"""
def buff_cotc_enemies_in_stage(file_path,mag_boost,stats):
    """
    returns false if stage not found
    \n is conditional
    """
    remove_cotc_crystals = settings["game"]["gameplay"]["remove_cotc_crystals"]
    to_buff_ids = [360,361,362,363,364,365,366,375,377,388,417,418]
    stage = f.stage_sche(file_path)
    if not stage.exists: #this is what breaks it out when the stage does exist
        return False
    did_something = False
    for enemy in stage.enemies:
        enemy_id = enemy[stage.enemy_id]
        if enemy_id-2 in to_buff_ids and (stats[enemy_id][e.s.starred_god] != 1 or remove_cotc_crystals):
            did_something = True
            enemy[stage.magnification] = int(mag_boost*enemy[stage.magnification])
    if did_something:
        stage.submit()
    return True


