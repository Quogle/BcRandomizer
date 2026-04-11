from dev.randomizer.func.core import randinst
from dev.randomizer.parse_config import settings
import dev.randomizer.enums.enemy as e
import dev.randomizer.enums.cats as c
import dev.randomizer.func.files as f
import dev.randomizer.func.core as core
from dev.randomizer.data.filepaths import *
from dev.randomizer.func.enemy import vanilla_enemy_array
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
        current_map = core.number_string_stepper(current_map,3)
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
        if os.path.exists(DOWNLOAD_LOCAL + ENEMY_STATS):
            new_stats = f.csv_reader(DOWNLOAD_LOCAL + ENEMY_STATS)
        else:
            new_stats = vanilla_enemy_array
        
        itf_path_start = STAGE_SCHEM + ITF_SLETTER + "0"
        itf_chapters = ["4","5","6"]
        mag_base = 7
        mag_red_at = 23
        for chapter in range(0,len(itf_chapters)):
            for stage in range(0,48):
                mag_mult = mag_base - (chapter*2) - (int(stage/mag_red_at))
                stage_end = "0" + str(stage) + ".csv"
                this_stage = f.stage_sche(itf_path_start + itf_chapters[chapter] + "_" + stage_end[-6:],1)
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
        if os.path.exists(DOWNLOAD_LOCAL + ENEMY_STATS):
            new_stats = f.csv_reader(DOWNLOAD_LOCAL + ENEMY_STATS)
        else:
            new_stats = vanilla_enemy_array
        
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
                this_stage = f.stage_sche(cotc_path_start + cotc_chapters[chapter] + "_" + stage_end[-6:],1)
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


