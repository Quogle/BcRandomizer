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
    do_a = settings["game"]["gameplay"]["preserve_alien_magnifications"]
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
    do_a = settings["game"]["gameplay"]["preserve_alien_magnifications"]
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



        







