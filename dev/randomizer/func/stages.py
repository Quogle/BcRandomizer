from dev.randomizer.func.core import randinst
from dev.randomizer.parse_config import settings
import dev.randomizer.func.files as f
import dev.randomizer.func.core as core
from dev.randomizer.data.filepaths import *


def early_sol_xp_buff():
    """
    buffs pre ururun stages xp, conditional
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
    buffs hate siege and fd, conditional
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







