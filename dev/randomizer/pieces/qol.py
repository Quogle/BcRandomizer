import dev.randomizer.func.game_files as f
from dev.randomizer.parse_config import settings
from dev.randomizer.data.filepaths import *
import dev.randomizer.enums.treasure as tres
import dev.randomizer.enums.item as item
import dev.randomizer.enums.unitbuy as ub
from dev.randomizer.func.random import randinst
from dev.randomizer.func.misc import *
import copy
import os


def remove_itf_crystals():
    """
    removes itf crystals but doesnt replace them with anything
    \n nonconditional
    """
    treasures = f.file_reader(ITF_TREASURE_DATA)
    for x in range(tres.pos.treasure_effects,tres.pos.treasure_effects+tres.pos.treasure_count):
        if treasures[x][tres.pos.treasure_effect_id] == tres.id.itf_crystal:
            treasures[x][tres.pos.treasure_effect_id] = -1
    f.file_writer(ITF_TREASURE_DATA,treasures)

def remove_cotc_crystals():
    """
    removes cotc crystals but doesnt replace them with anything
    \n nonconditional
    """
    chapters = [COTC1_TREASURE_DATA,COTC2_TREASURE_DATA,COTC3_TREASURE_DATA]
    for each in chapters:
        treasures = f.file_reader(each)
        for x in range(tres.pos.treasure_effects,tres.pos.treasure_effects+tres.pos.treasure_count):
            if treasures[x][tres.pos.treasure_effect_id] == tres.id.cotc_crystal:
                treasures[x][tres.pos.treasure_effect_id] = -1
        f.file_writer(each,treasures)

def condense_god():
    """
    makes all gods use the same treasure id
    \n nonconditional
    """
    chapters = [COTC1_TREASURE_DATA,COTC2_TREASURE_DATA,COTC3_TREASURE_DATA]
    god_ids = [tres.id.god1_mask,tres.id.god2_mask,tres.id.god3_mask]
    for chapter in chapters:
        treasures = f.file_reader(chapter)
        for line_id in range(tres.pos.treasure_effects,tres.pos.treasure_effects+tres.pos.treasure_count):
            if treasures[line_id][tres.pos.treasure_effect_id] in god_ids:
                treasures[line_id][tres.pos.treasure_effect_id] = tres.id.god1_mask
                treasures[line_id][tres.pos.apply_only_this_chapter] = 1
        f.file_writer(chapter,treasures)

def buff_shop():
    """
    makes shop less shit
    \n conditional
    """
    shop = f.file_reader(SHOP_FILE)
    qol = settings["game"]["qol"]
    shop_buff = qol["shop_buff"] #does this even do anything
    cheaper = qol["cheaper_items"]
    leadership = qol["leadership_in_shop"]
    ototo_helper = qol["ototo_helper_in_shop"]
    cheaper_catamin = qol["cheap_catamin"]
    new_line = [15,0,1000,1,0,"shop_category1",6]
    #buff shop
    if shop_buff:
        for entry in shop:
            if entry[item.shop.item_id_pos] == item.drop_id.speed_up:
                entry[item.shop.item_count_pos] = 1000
                entry[item.shop.price_pos] = 30
            if entry[item.shop.item_id_pos] == item.drop_id.radar:
                entry[item.shop.item_count_pos] = 4
                entry[item.shop.price_pos] = 80
            if entry[item.shop.item_id_pos] == item.drop_id.rich:
                entry[item.shop.item_count_pos] = 15
                entry[item.shop.price_pos] = 150
            if entry[item.shop.item_id_pos] == item.drop_id.cpu:
                entry[item.shop.item_count_pos] = 20
                entry[item.shop.price_pos] = 100
            if entry[item.shop.item_id_pos] == item.drop_id.cat_jobs:
                entry[item.shop.item_count_pos] = 10
                entry[item.shop.price_pos] = 100
            if entry[item.shop.item_id_pos] == item.drop_id.sniper:
                entry[item.shop.item_count_pos] = 6
                entry[item.shop.price_pos] = 90
            if entry[item.shop.item_id_pos] == item.drop_id.catamin_a:
                entry[item.shop.item_count_pos] = 6
                entry[item.shop.price_pos] = 30
            if entry[item.shop.item_id_pos] == item.drop_id.catamin_b:
                entry[item.shop.item_count_pos] = 6
                entry[item.shop.price_pos] = 60
            if entry[item.shop.item_id_pos] == item.drop_id.catamin_c:
                entry[item.shop.item_count_pos] = 6
                entry[item.shop.price_pos] = 90
    
    if leadership:
        new_index = 15
        leadership_not_in_shop = True
        for entry in shop:
            if entry[item.shop.shop_id_pos] >= new_index:
                new_index += 1
            if entry[item.shop.item_id_pos] == item.drop_id.leadership:
                leadership_not_in_shop = False
        if leadership_not_in_shop:
            this_new_line = copy.deepcopy(new_line)
            this_new_line[item.shop.shop_id_pos] = new_index
            this_new_line[item.shop.item_id_pos] = item.drop_id.leadership
            this_new_line[item.shop.item_count_pos] = 100
            this_new_line[item.shop.price_pos] = 30
            #something about image cut for leadership
            shop.append(this_new_line)
    
    if ototo_helper:
        new_index = 15
        ototo_helper_not_in_shop = True
        for entry in shop:
            if entry[item.shop.shop_id_pos] >= new_index:
                new_index = entry[item.shop.shop_id_pos] + 1
            if entry[item.shop.item_id_pos] == item.drop_id.engineer:
                ototo_helper_not_in_shop = False
        if ototo_helper_not_in_shop:
            this_new_line = copy.deepcopy(new_line)
            this_new_line[item.shop.shop_id_pos] = new_index
            this_new_line[item.shop.item_id_pos] = item.drop_id.engineer
            this_new_line[item.shop.item_count_pos] = 5
            this_new_line[item.shop.price_pos] = 30
            #something about image cut for ototo helpers
            shop.append(this_new_line)
    
    if cheaper:
        for entry in shop:
            if entry[item.shop.item_id_pos] == item.drop_id.speed_up:
                entry[item.shop.item_count_pos] = 1000
                entry[item.shop.price_pos] = 1
            if entry[item.shop.item_id_pos] == item.drop_id.radar:
                entry[item.shop.item_count_pos] = 4
                entry[item.shop.price_pos] = 20
            if entry[item.shop.item_id_pos] == item.drop_id.rich:
                entry[item.shop.item_count_pos] = 15
                entry[item.shop.price_pos] = 60
            if entry[item.shop.item_id_pos] == item.drop_id.cpu:
                entry[item.shop.item_count_pos] = 20
                entry[item.shop.price_pos] = 20
            if entry[item.shop.item_id_pos] == item.drop_id.cat_jobs:
                entry[item.shop.item_count_pos] = 10
                entry[item.shop.price_pos] = 20
            if entry[item.shop.item_id_pos] == item.drop_id.sniper:
                entry[item.shop.item_count_pos] = 6
                entry[item.shop.price_pos] = 18

    if cheaper_catamin:
        for entry in shop:
            if entry[item.shop.item_id_pos] == item.drop_id.catamin_a:
                entry[item.shop.item_count_pos] = 20
                entry[item.shop.price_pos] = 20
            if entry[item.shop.item_id_pos] == item.drop_id.catamin_b:
                entry[item.shop.item_count_pos] = 20
                entry[item.shop.price_pos] = 50
            if entry[item.shop.item_id_pos] == item.drop_id.catamin_c:
                entry[item.shop.item_count_pos] = 20
                entry[item.shop.price_pos] = 80


    f.file_writer(SHOP_FILE,shop)

def behemoth_cube_buff():
    """
    increases the drop rates of culling stages
    \n conditional
    """
    do_buff = settings["game"]["qol"]["behemoth_cube_buff"]
    if do_buff:
        empt = f.map_data("null")
        red_rate_pos = empt.drop1_rate
        red_id_pos = empt.drop1_id
        red_count_pos = empt.drop1_count
        purple_rate_pos = empt.drop2_rate
        purple_id_pos = empt.drop2_id
        purple_count_pos = empt.drop2_count
        blue_rate_pos = empt.drop3_rate
        blue_id_pos = empt.drop3_id
        blue_count_pos = empt.drop3_count
        green_rate_pos = empt.drop4_rate
        green_id_pos = empt.drop4_id
        green_count_pos = empt.drop4_count
        yellow_rate_pos = empt.drop5_rate
        yellow_id_pos = empt.drop5_id
        yellow_count_pos = empt.drop5_count
        
        #create default stage
        default_stage = [0,0,0,0,0,0,0,0,-4] #set scheme to -4 by default
        for x in range(0,4):
            for y in range(0,3):
                default_stage.append(0)
        default_stage.append(-1) #this should be the final -1 that stops reading
        #add item ids to all stages
        default_stage[red_id_pos] = item.drop_id.red_stone
        default_stage[purple_id_pos] = item.drop_id.purple_stone
        default_stage[blue_id_pos] = item.drop_id.blue_stone
        default_stage[green_id_pos] = item.drop_id.green_stone
        default_stage[yellow_id_pos] = item.drop_id.yellow_stone
        #default to giving purple and red a rate of 50
        default_stage[red_rate_pos] = 50
        default_stage[purple_rate_pos] = 50

        gap_map = f.map_data(MAPSTAGEDATA + BEHEMOTH_MLETTER + "_000.csv")
        ash_map = f.map_data(MAPSTAGEDATA + BEHEMOTH_MLETTER + "_001.csv")
        jin_map = f.map_data(MAPSTAGEDATA + BEHEMOTH_MLETTER + "_002.csv")

        #create seperate arrays to store all the stages for now
        gap = []
        ash = []
        jin = []
        for x in range(0,len(gap_map.stages)-1):
            gap.append(default_stage)
            ash.append(default_stage)
            jin.append(default_stage)
        for x in range(0,len(gap)): #copy paste xp nrg and music data from stages
            for y in range(0,5):
                gap[x][y] = gap_map.stages[x][y]
                ash[x][y] = ash_map.stages[x][y]
                jin[x][y] = jin_map.stages[x][y]
        
        #gap
        for x in range(0,len(gap)):
            gap[x][red_count_pos] = int(1+x/5)
            gap[x][purple_count_pos] = int(1+x/5)  
        for x in range(10,len(gap)):
            gap[x][blue_rate_pos] = 15
            gap[x][green_rate_pos] = 15
            gap[x][blue_count_pos] = int(1+x/5)
            gap[x][green_count_pos] = int(1+x/5)

        #ash
        for x in range(0,len(ash)):
            ash[x][red_count_pos] = 2
            ash[x][purple_count_pos] = 2
            ash[x][blue_rate_pos] = 250
            ash[x][green_rate_pos] = 250
            ash[x][blue_count_pos] = int(1+x/5)
            ash[x][green_count_pos] = int(1+x/5)
        for x in range(10,len(ash)):
            ash[x][red_count_pos] = 3
            ash[x][purple_count_pos] = 3
            ash[x][yellow_rate_pos] = 25
            ash[x][yellow_count_pos] = 1
        
        #jinfore
        for x in range(0,len(jin)):
            jin[x][blue_rate_pos] = 50
            jin[x][green_rate_pos] = 50
            jin[x][yellow_rate_pos] = 70
            jin[x][red_count_pos] = int(1+x/7)
            jin[x][purple_count_pos] = int(1+x/7)
            jin[x][blue_count_pos] = int(1+x/7)
            jin[x][green_count_pos] = int(1+x/7)
            jin[x][yellow_count_pos] = int(1+x/7)
        for x in range(10,len(jin)):
            jin[x][yellow_rate_pos] = 100
        
        for x in range(0,len(gap)):
            gap_map.stages[x] = gap[x]
            ash_map.stages[x] = ash[x]
            jin_map.stages[x] = jin[x]
        gap_map.submit()
        ash_map.submit()
        jin_map.submit()

        #enigma
        enigma_1 = f.map_data(MAPSTAGEDATA + ENIGMA_MLETTER + "_060.csv")
        enigma_2 = f.map_data(MAPSTAGEDATA + ENIGMA_MLETTER + "_061.csv")
        enigma_3 = f.map_data(MAPSTAGEDATA + ENIGMA_MLETTER + "_062.csv")
        enigma_4 = f.map_data(MAPSTAGEDATA + ENIGMA_MLETTER + "_066.csv")
        
        #edit 1 separate
        enigma_1.stages[0][empt.drop1_count] = 3 #purple from 2
        enigma_1.stages[1][empt.drop1_count] = 3 #red from 2

        for x in range(0,4):
            enigma_2.stages[x][8] = -4
            enigma_3.stages[x][8] = -4
            enigma_4.stages[x][8] = -4
            while len(enigma_2.stages[x]) > 9:
                enigma_2.stages[x].pop()
            while len(enigma_3.stages[x]) > 9:
                enigma_3.stages[x].pop()
            while len(enigma_4.stages[x]) > 9:
                enigma_4.stages[x].pop()

        #now edit them all
        for x in range(0,4):
            enigma_2.stages[x][empt.drop1_count] = 4
            enigma_3.stages[x][empt.drop1_count] = 5
            enigma_4.stages[x][empt.drop1_count] = 6
        enigma_3.stages[4][empt.drop1_count] = 2
        enigma_4.stages[4][empt.drop1_count] = 3
        enigma_4.stages[4][empt.drop2_count] = 3

        enigma_1.submit()
        enigma_2.submit()
        enigma_3.submit()
        enigma_4.submit()
        #should I edit the in forest type stages

def buff_advent_drops():
    """
    makes advents 100% drop
    \n conditional
    """
    do_buff = settings["game"]["qol"]["guarantee_advent_drops"]
    if do_buff:
        file_name_start = MAPSTAGEDATA + EVENT_STAGE_MLETTER + "_"
        current_map = 0
        while True:
            file_name_end = "00" + str(current_map) + ".csv"
            current_map += 1
            this_map = f.map_data(file_name_start + file_name_end[-7:])

            #loop exit condition
            if not this_map.exists:
                break
            
            if len(this_map.stages) == 1:
                drop_id = this_map.stages[0][this_map.drop1_id]
                if drop_id >= 1000 and drop_id < 2000:
                    if this_map.stages[0][this_map.drop1_rate] == 30:
                        this_map.stages[0][this_map.drop1_rate] = 100
                        this_map.submit()
        
def free_orb_removal():
    """
    makes it free to remove orbs
    \n conditional
    """
    do_buff = settings["game"]["qol"]["free_orb_removal"]
    if do_buff:
        #this is a csv with non numerical info
        orb_file = f.file_reader(ORB_NP_AMOUNT_FILE,True)
        for each in orb_file:
            each[2] = 0
        f.file_writer(ORB_NP_AMOUNT_FILE,orb_file)

#maybe this shouldnt be in here now that its qol
def randomize_whats_boss():
    """
    randomizes what counts as boss in ALL stages
    \n conditional
    """
    do_self = settings["game"]["funny"]["randomize_boss"]
    if do_self:
        #get all stages
        all_files = os.listdir(DATA_LOCAL)
        stage_files = []
        exclude_fifth = [".","_"]
        for file in all_files:
            if STAGE_SCHEM in file and file[5] not in exclude_fifth and MAIN_STORY_MAPSTAGEDATA not in file:
                stage_files.append(file)
        stage_files.sort()

        #create position array
        identifiers = [
            "", #this is eoc stages lmao
            EXTRA_STAGE_SLETTER,
            AKU_REALMS_SLETTER,
            CATCLAW_SLETTER,
            LABYRINTH_SLETTER,
            GAUNTLET_SLETTER,
            CATAMIN_SLETTER,
            COLLAB_SLETTER,
            COLLAB_GAUNTLET_SLETTER,
            ENIGMA_SLETTER,
            CHALLENGE_SLETTER,
            SOL_SLETTER,
            UL_SLETTER,
            ZL_SLETTER,
            BEHEMOTH_SLETTER,
            RANKING_EVENT_SLETTER,
            EVENT_STAGE_SLETTER,
            COLLOSEUM_SLETTER,
            HALL_OF_INITIATES_SLETTER,
            TOWER_SLETTER,
            ITF_SLETTER,
            COTC_SLETTER,
        ]
        indenty_shift = []
        for each in identifiers:
            indenty_shift.append(0)

        numbers_to_remove = [0,1,2,3,4,5,6,7,8,9,"_"]
        for file in stage_files:
            this_file = file.replace(STAGE_SCHEM,"")
            this_file = this_file.replace(".csv","")
            for x in numbers_to_remove:
                this_file = this_file.replace(str(x),"")
            index = 0
            try:
                index = identifiers.index(this_file)
                indenty_shift[index] += 1
            except:
                pass
            change_boss(file,index*1000 + indenty_shift[index])

#one part is not finished below
def add_unit_drops():
    """
    master function for adding units as drops and missions
    \n conditional, still missing missions
    """
    add_units_to_sol()
    add_grouped_units()
    add_collab_tf_drops()

def orb_stage_buff():
    """
    buffs the drops from orb stages (not barons)
    \n conditional
    """
    qol = settings["game"]["qol"]["stage_changes"]
    buff_isle = qol["orb_stage_buff"]
    add_relic_aku = qol["relic_aku_in_island"]
    trait_ability_orbs = qol["orb_stage_has_strong_massive_resist"]
    ability_orbs = qol["orb_stage_has_ability_orb"]
    did_anything = buff_isle or trait_ability_orbs or ability_orbs or add_relic_aku
    if not did_anything:#block it from opening the maps if its not gonna change anything
        return
    
    island_traits = ["red","floating","black","angel","alien","zombie","metal"]
    total_traits = ["red","floating","black","angel","alien","zombie","metal","aku","relic"]

    #get map location info
    dummy_map = f.map_data()
    m = {}
    location_data = {}
    start_id = 9
    for x in range(0,len(island_traits)):
        location_data[island_traits[x]] = {}
        for y in range(0,3):
            location_data[island_traits[x]][str(y)] = start_id + x + y
    location_data["aku"] = {
        "0":63,
        "1":64,
        "2":65,
    }
    location_data["relic"] = {
        "0":67,
        "1":68,
        "2":69,
    }

    #open all map and stages and put them in dict
    for x in range(0,len(total_traits)):
        m[total_traits[x]] = {}
        for y in range(0,3):
            m[total_traits[x]][str(y)] = {"m":None,"s":None}
    for each in m:
        for x in range(0,3):
            first_file_name = MAPSTAGEDATA + ENIGMA_MLETTER + "_" + stringize_number(location_data[each][str(x)],3) + ".csv"
            second_file_name = STAGE_SCHEM + ENIGMA_SLETTER + stringize_number(location_data[each][str(x)],3) + "_00.csv" #theyre all first stage
            m[each][str(x)]["m"] = f.map_data(first_file_name)
            m[each][str(x)]["s"] = f.stage_sche(second_file_name)
    
    #now theyre ripe for editing
    #set all stages to 8 drops for now
    for each in m:
        for x in range(0,3):
            this_map = m[each][str(x)]["m"]
            while len(this_map.stages[0]) > this_map.music2+1: #kill all drop info
                this_map.stages[0].pop()
            while len(this_map.stages[0]) < this_map.drop8_count: #now extend all to 8 drops
                this_map.stages[0].append(0)
            this_map.stages[0][this_map.drop_scheme] = -4 #set drop scheme to -4
    

    #now to set drop id for all stages
    for x in range(0,len(island_traits)-1): #dont do metal here
        current_shift = 10*x
        current_ab_shift = 15*x
        if x >= 3:
            current_shift += 5
        this_trait = m[island_traits[x]]
        first_stage = this_trait["0"]["m"].stages[0]
        second_stage = this_trait["1"]["m"].stages[0]
        third_stage = this_trait["2"]["m"].stages[0]
        #ive decided not to put ability orbs on these so they actually dont need 8 drop ids
        #maybe in the future with more ability orbs increase # of drops allowed and make these more refined
        #first stage drops
        first_stage[dummy_map.drop1_id] = item.drop_id.orb_red_atk_d + current_shift
        first_stage[dummy_map.drop2_id] = item.drop_id.orb_red_def_d + current_shift
        first_stage[dummy_map.drop3_id] = item.drop_id.orb_red_atk_c + current_shift
        first_stage[dummy_map.drop4_id] = item.drop_id.orb_red_def_c + current_shift
        first_stage[dummy_map.drop5_id] = item.drop_id.orb_red_massive_d + current_ab_shift
        first_stage[dummy_map.drop6_id] = item.drop_id.orb_red_resist_d + current_ab_shift
        first_stage[dummy_map.drop7_id] = item.drop_id.orb_red_strong_d + current_ab_shift

        #second stage drops
        second_stage[dummy_map.drop1_id] = item.drop_id.orb_red_atk_c + current_shift
        second_stage[dummy_map.drop2_id] = item.drop_id.orb_red_def_c + current_shift
        second_stage[dummy_map.drop3_id] = item.drop_id.orb_red_atk_b + current_shift
        second_stage[dummy_map.drop4_id] = item.drop_id.orb_red_def_b + current_shift
        second_stage[dummy_map.drop5_id] = item.drop_id.orb_red_massive_d + current_ab_shift
        second_stage[dummy_map.drop6_id] = item.drop_id.orb_red_resist_d + current_ab_shift
        second_stage[dummy_map.drop7_id] = item.drop_id.orb_red_strong_d + current_ab_shift

        #third stage drops
        third_stage[dummy_map.drop1_id] = item.drop_id.orb_red_atk_c + current_shift
        third_stage[dummy_map.drop2_id] = item.drop_id.orb_red_def_c + current_shift
        third_stage[dummy_map.drop3_id] = item.drop_id.orb_red_atk_b + current_shift
        third_stage[dummy_map.drop4_id] = item.drop_id.orb_red_def_b + current_shift
        third_stage[dummy_map.drop5_id] = item.drop_id.orb_red_massive_c + current_ab_shift
        third_stage[dummy_map.drop6_id] = item.drop_id.orb_red_resist_c + current_ab_shift
        third_stage[dummy_map.drop7_id] = item.drop_id.orb_red_strong_c + current_ab_shift
    #set drop id for aku relic
    last_two = ["aku","relic"]
    for x in range(0,len(last_two)):
        this_trait = m[last_two[x]]
        first_stage = this_trait["0"]["m"].stages[0]
        second_stage = this_trait["1"]["m"].stages[0]
        third_stage = this_trait["2"]["m"].stages[0]

        #current shift
        current_shift = x*25
        #first stage
        first_stage[dummy_map.drop1_id] = item.drop_id.orb_aku_atk_d + current_shift
        first_stage[dummy_map.drop2_id] = item.drop_id.orb_aku_def_d + current_shift
        first_stage[dummy_map.drop3_id] = item.drop_id.orb_aku_atk_c + current_shift
        first_stage[dummy_map.drop4_id] = item.drop_id.orb_aku_def_c + current_shift
        first_stage[dummy_map.drop5_id] = item.drop_id.orb_aku_massive_d + current_shift
        first_stage[dummy_map.drop6_id] = item.drop_id.orb_aku_resist_d + current_shift
        first_stage[dummy_map.drop7_id] = item.drop_id.orb_aku_strong_d + current_shift
        #second stage
        second_stage[dummy_map.drop1_id] = item.drop_id.orb_aku_atk_c + current_shift
        second_stage[dummy_map.drop2_id] = item.drop_id.orb_aku_def_c + current_shift
        second_stage[dummy_map.drop3_id] = item.drop_id.orb_aku_atk_b + current_shift
        second_stage[dummy_map.drop4_id] = item.drop_id.orb_aku_def_b + current_shift
        second_stage[dummy_map.drop5_id] = item.drop_id.orb_aku_massive_d + current_shift
        second_stage[dummy_map.drop6_id] = item.drop_id.orb_aku_resist_d + current_shift
        second_stage[dummy_map.drop7_id] = item.drop_id.orb_aku_strong_d + current_shift
        #third stage
        third_stage[dummy_map.drop1_id] = item.drop_id.orb_aku_atk_c + current_shift
        third_stage[dummy_map.drop2_id] = item.drop_id.orb_aku_def_c + current_shift
        third_stage[dummy_map.drop3_id] = item.drop_id.orb_aku_atk_b + current_shift
        third_stage[dummy_map.drop4_id] = item.drop_id.orb_aku_def_b + current_shift
        third_stage[dummy_map.drop5_id] = item.drop_id.orb_aku_massive_c + current_shift
        third_stage[dummy_map.drop6_id] = item.drop_id.orb_aku_resist_c + current_shift
        third_stage[dummy_map.drop7_id] = item.drop_id.orb_aku_strong_c + current_shift

        
    # now do rates and counts
    metalless = island_traits + last_two
    for each in metalless:
        this_trait = m[each]
        first_stage = this_trait["0"]["m"].stages[0]
        second_stage = this_trait["1"]["m"].stages[0]
        third_stage = this_trait["2"]["m"].stages[0]

        s1_lower = 200
        s1_upper = 200
        s1_a = 30
        s1_lower_count = 2
        s1_upper_count = 1
        s1_a_count = 1

        s2_lower = 350
        s2_upper = 50
        s2_a = 50
        s2_lower_count = 1
        s2_upper_count = 1
        s2_a_count = 1


        s3_lower = 100
        s3_upper = 300
        s3_a = 50
        s3_lower_count = 2
        s3_upper_count = 1
        s3_a_count = 1


        if trait_ability_orbs:
            s1_a_count = 2
            s2_a_count = 2
            s3_a_count = 2

        
        #first stage
        first_stage[dummy_map.drop1_rate] = s1_lower
        first_stage[dummy_map.drop2_rate] = s1_lower
        first_stage[dummy_map.drop3_rate] = s1_upper
        first_stage[dummy_map.drop4_rate] = s1_upper
        first_stage[dummy_map.drop5_rate] = s1_a
        first_stage[dummy_map.drop6_rate] = s1_a
        first_stage[dummy_map.drop7_rate] = s1_a
        first_stage[dummy_map.drop1_count] = s1_lower_count
        first_stage[dummy_map.drop2_count] = s1_lower_count
        first_stage[dummy_map.drop3_count] = s1_upper_count
        first_stage[dummy_map.drop4_count] = s1_upper_count
        first_stage[dummy_map.drop5_count] = s1_a_count
        first_stage[dummy_map.drop6_count] = s1_a_count
        first_stage[dummy_map.drop7_count] = s1_a_count

        #second stage
        second_stage[dummy_map.drop1_rate] = s2_lower
        second_stage[dummy_map.drop2_rate] = s2_lower
        second_stage[dummy_map.drop3_rate] = s2_upper
        second_stage[dummy_map.drop4_rate] = s2_upper
        second_stage[dummy_map.drop5_rate] = s2_a
        second_stage[dummy_map.drop6_rate] = s2_a
        second_stage[dummy_map.drop7_rate] = s2_a
        second_stage[dummy_map.drop1_count] = s2_lower_count
        second_stage[dummy_map.drop2_count] = s2_lower_count
        second_stage[dummy_map.drop3_count] = s2_upper_count
        second_stage[dummy_map.drop4_count] = s2_upper_count
        second_stage[dummy_map.drop5_count] = s2_a_count
        second_stage[dummy_map.drop6_count] = s2_a_count
        second_stage[dummy_map.drop7_count] = s2_a_count

        #third stage
        third_stage[dummy_map.drop1_rate] = s3_lower
        third_stage[dummy_map.drop2_rate] = s3_lower
        third_stage[dummy_map.drop3_rate] = s3_upper
        third_stage[dummy_map.drop4_rate] = s3_upper
        third_stage[dummy_map.drop5_rate] = s3_a
        third_stage[dummy_map.drop6_rate] = s3_a
        third_stage[dummy_map.drop7_rate] = s3_a
        third_stage[dummy_map.drop1_count] = s3_lower_count
        third_stage[dummy_map.drop2_count] = s3_lower_count
        third_stage[dummy_map.drop3_count] = s3_upper_count
        third_stage[dummy_map.drop4_count] = s3_upper_count
        third_stage[dummy_map.drop5_count] = s3_a_count
        third_stage[dummy_map.drop6_count] = s3_a_count
        third_stage[dummy_map.drop7_count] = s3_a_count

    #metal
    first_stage = m["metal"]["0"]["m"].stages[0]
    second_stage = m["metal"]["1"]["m"].stages[0]
    third_stage = m["metal"]["2"]["m"].stages[0]


    first_stage[dummy_map.drop1_id] = item.drop_id.orb_metal_def_d
    first_stage[dummy_map.drop1_rate] = 500
    first_stage[dummy_map.drop1_count] = 2

    second_stage[dummy_map.drop1_id] = item.drop_id.orb_metal_def_c
    second_stage[dummy_map.drop1_rate] = 500
    second_stage[dummy_map.drop1_count] = 2

    third_stage[dummy_map.drop1_id] = item.drop_id.orb_metal_def_b
    third_stage[dummy_map.drop1_rate] = 500
    third_stage[dummy_map.drop1_count] = 2
    
    if ability_orbs: #can have 7 per stage as of now, only uses 6
        first_stage[dummy_map.drop2_id] = item.drop_id.orb_resist_knockback_d
        first_stage[dummy_map.drop3_id] = item.drop_id.orb_resist_slow_d
        first_stage[dummy_map.drop4_id] = item.drop_id.orb_resist_freeze_d
        first_stage[dummy_map.drop5_id] = item.drop_id.orb_resist_weaken_d
        first_stage[dummy_map.drop6_id] = item.drop_id.orb_resist_curse_d
        first_stage[dummy_map.drop7_id] = item.drop_id.orb_counter_surge_d

        second_stage[dummy_map.drop2_id] = item.drop_id.orb_shortened_cooldown_d
        second_stage[dummy_map.drop3_id] = item.drop_id.orb_cost_down_d
        second_stage[dummy_map.drop4_id] = item.drop_id.orb_death_surge_d
        second_stage[dummy_map.drop5_id] = item.drop_id.orb_berserker_d
        second_stage[dummy_map.drop6_id] = item.drop_id.orb_cannon_recharge_d
        second_stage[dummy_map.drop7_id] = item.drop_id.orb_bounty_up_d

        third_stage[dummy_map.drop2_id] = item.drop_id.orb_resist_wave_d
        third_stage[dummy_map.drop3_id] = item.drop_id.orb_resist_toxic_d
        third_stage[dummy_map.drop4_id] = item.drop_id.orb_resist_surge_d
        third_stage[dummy_map.drop5_id] = item.drop_id.orb_resist_explosion_d
        third_stage[dummy_map.drop6_id] = item.drop_id.orb_cash_back_d
        third_stage[dummy_map.drop7_id] = item.drop_id.orb_dodge_attack_d


        #rates
        first_stage[dummy_map.drop2_rate] = 200
        first_stage[dummy_map.drop3_rate] = 200
        first_stage[dummy_map.drop4_rate] = 200
        first_stage[dummy_map.drop5_rate] = 200
        first_stage[dummy_map.drop6_rate] = 200
        first_stage[dummy_map.drop7_rate] = 200

        second_stage[dummy_map.drop2_rate] = 200
        second_stage[dummy_map.drop3_rate] = 200
        second_stage[dummy_map.drop4_rate] = 250
        second_stage[dummy_map.drop5_rate] = 200
        second_stage[dummy_map.drop6_rate] = 200
        second_stage[dummy_map.drop7_rate] = 200

        third_stage[dummy_map.drop2_rate] = 150
        third_stage[dummy_map.drop3_rate] = 150
        third_stage[dummy_map.drop4_rate] = 200
        third_stage[dummy_map.drop5_rate] = 200
        third_stage[dummy_map.drop6_rate] = 200
        third_stage[dummy_map.drop7_rate] = 200

        #counts
        first_stage[dummy_map.drop2_count] = 4
        first_stage[dummy_map.drop3_count] = 4
        first_stage[dummy_map.drop4_count] = 4
        first_stage[dummy_map.drop5_count] = 4
        first_stage[dummy_map.drop6_count] = 4
        first_stage[dummy_map.drop7_count] = 4

        second_stage[dummy_map.drop2_count] = 4
        second_stage[dummy_map.drop3_count] = 4
        second_stage[dummy_map.drop4_count] = 4
        second_stage[dummy_map.drop5_count] = 4
        second_stage[dummy_map.drop6_count] = 4
        second_stage[dummy_map.drop7_count] = 4

        third_stage[dummy_map.drop2_count] = 4
        third_stage[dummy_map.drop3_count] = 4
        third_stage[dummy_map.drop4_count] = 4
        third_stage[dummy_map.drop5_count] = 4
        third_stage[dummy_map.drop6_count] = 4
        third_stage[dummy_map.drop7_count] = 4

    for each in m:
        for zeach in m[each]:
            m[each][zeach]["m"].submit()
    
    #get new island stages array
    island = []
    traits_to_do = island_traits
    if add_relic_aku:
        traits_to_do = total_traits
    for x in range(0,3):
        for trait in traits_to_do:
            this_map = m[trait][str(x)]["m"]
            island.append(this_map.stages[0])
    
    #set array as new island stages
    island_map = f.map_data(MAPSTAGEDATA + GAUNTLET_MLETTER + "_055.csv")
    island_map.stages = island
    for each in island_map.stages: #fix the reduced xp of enigma vs island
        each[dummy_map.xp] = 5700
    island_map.resolve_stage_count()
    island_map.submit()

    #set new stages
    if add_relic_aku:
        trait_count = len(total_traits)
        for trait_id in range(0,len(total_traits)):
            for x in range(0,3):
                this_stage = m[total_traits[trait_id]][str(x)]["s"]
                stage_name = STAGE_SCHEM + GAUNTLET_SLETTER + stringize_number(55,3) + "_" + stringize_number(x*trait_count+trait_id,2) + ".csv"
                this_stage.submit_as_new_stage(stage_name)
        
        #have to figure out what else is required to submit stages

def unit_buy_triple():
    """
    triples the xp sell value of units, doubles np
    \n conditional
    """
    do_self = settings["game"]["qol"]["unit_sell_increase"]
    if not do_self: #this is good enough
        return
    unitbuy = f.file_reader(UNITBUY_FILE)
    for each in unitbuy:
        each[ub.ub.selling_xp] = int(3*each[ub.ub.selling_xp])
        each[ub.ub.np_selling_amount] = int(2*each[ub.ub.np_selling_amount])
    f.file_writer(UNITBUY_FILE,unitbuy)

#not sure where else to put this, I think this is done?
def param_editor():
    """
    applies all changes needed for configs settings
    \n conditional
    \n currently only behemoth and sage
    """
    remove_behemoth = settings["game"]["gameplay"]["remove_behemoths"]
    preserve_zombies = settings["game"]["gameplay"]["preserve_old_zombies"] #apparently collosus slayer isnt in this file
    rework_sage = settings["enemy"]["traits"]["gimmicks"]["white"]["sage_rework"]
    BEHEMOTH_STAT_NAME = "battle_super_beast_hunter" #works for both atk and def
    BEHEMOTH_STAT_NEW_VALUE = 1000 #not sure what to do, its 20k on old randomize
    SAGE_NAME = "battle_super_sage"
    SAGE_KB_NAME = "battle_super_sage_knockback"
    SAGE_SLAYER_NAME = "battle_super_sage_hunter"
    SAGE_SLAYER_KB_NAME = "battle_super_sage_hunter_knockback"
    SAGE_SLAYER_DAMAGE_NAME = "battle_super_sage_hunter_damage"
    SAGE_ALL_STAT = 30
    SAGE_KB_STAT = 150
    SAGE_SLAYER_ALL_STAT = SAGE_ALL_STAT
    SAGE_SLAYER_KB_STAT = SAGE_SLAYER_ALL_STAT
    SAGE_SLAYER_DAMAGE_STAT = 1000

    param = f.file_reader(PARAM_FILE)
    for each in param:
        if remove_behemoth:
            if BEHEMOTH_STAT_NAME in each[0]:
                each[1] = BEHEMOTH_STAT_NEW_VALUE
        if rework_sage:
            if SAGE_SLAYER_DAMAGE_NAME in each[0]: #this is the most specific name
                each[1] = SAGE_SLAYER_DAMAGE_STAT
            elif SAGE_SLAYER_KB_NAME in each[0]:
                each[1] = SAGE_SLAYER_KB_STAT
            elif SAGE_SLAYER_NAME in each[0]:
                each[1] = SAGE_SLAYER_ALL_STAT
            elif SAGE_KB_NAME in each[0]:
                each[1] = SAGE_KB_STAT
            elif SAGE_NAME in each[0]:
                each[1] = SAGE_ALL_STAT
    f.file_writer(PARAM_FILE,param)

def buff_normal_catfruit():
    """
    adds third tier catfruit stages on the end of catfruit map
    \n conditional
    """
    do_catamin = settings["game"]["qol"]["stage_changes"]["buff_normal_catfruit_catamins"]
    split_catfruit = settings["game"]["qol"]["stage_changes"]["split_normal_catfruit_stages"]
    always_epic = settings["game"]["qol"]["stage_changes"]["jubilee_always_epic"]
    dummy = f.map_data()
    catfruit_map = f.map_data(MAPSTAGEDATA + EVENT_STAGE_MLETTER + "_" + stringize_number(442,3) + ".csv")
    if always_epic:
        make_all_epic_extra_stage()
    catamaps = []
    for x in range(0,5):
        catamaps.append(f.map_data(MAPSTAGEDATA + CATAMIN_MLETTER + "_" + stringize_number(x,3) + ".csv"))
    #set it so all catamin stages have 1 100% drop
    for each in catamaps:
        for x in range(0,len(each.stages)):
            while len(each.stages[x]) > dummy.drop_scheme + 1:
                each.stages[x].pop()
                each.stages[x][dummy.drop_scheme] = 0
                each.stages[x][dummy.drop1_rate] = 100
                each.stages[x][dummy.drop1_count] = 2
    #set drop id of each catamin stage
    seed = [item.drop_id.yellow_seed,item.drop_id.blue_seed,item.drop_id.red_seed,item.drop_id.purple_seed,item.drop_id.green_seed]
    fruits = [item.drop_id.yellow_fruit,item.drop_id.blue_fruit,item.drop_id.red_fruit,item.drop_id.purple_fruit,item.drop_id.green_fruit,]
    for x in range(0,len(catamaps)):
        catamaps[x].stages[0][dummy.drop1_id] = seed[x]
        catamaps[x].stages[1][dummy.drop1_id] = fruits[x]
        catamaps[x].stages[2][dummy.drop1_id] = fruits[x]
        catamaps[x].stages[1][dummy.drop1_count] = 1
    #now submit them if worthy
    if do_catamin:
        for each in catamaps:
            each.submit()
    if split_catfruit:
        catfruit_map.stages.append(catamaps[4].stages[2])
        catfruit_map.stages.append(catamaps[3].stages[2])
        catfruit_map.stages.append(catamaps[2].stages[2])
        catfruit_map.stages.append(catamaps[1].stages[2])
        catfruit_map.stages.append(catamaps[0].stages[2])
        catfruit_map.resolve_stage_count()
        catfruit_map.submit()
    #now open the catamin stages to edit them
    catastages = []
    for x in range(0,5):
        this_map = []
        for y in range(0,3):
            this_map.append(f.stage_sche(STAGE_SCHEM + CATAMIN_SLETTER + stringize_number(x,3) + "_" + stringize_number(y,2) + ".csv"))
        catastages.append(this_map)
    #now set extra stage info
    for x in range(0,5):
        catastages[x][0].extra_chance = 10
        catastages[x][1].extra_chance = 30
        catastages[x][2].extra_chance = 100
        if always_epic:
            for y in range(0,3):
                catastages[x][y].extra_first_stage = "03"
                catastages[x][y].extra_last_stage = "03"
                catastages[x][y].extra_map = "000"
    #submit them
    if do_catamin:
        for x in range(0,5):
            for y in range(0,3):
                catastages[x][y].submit()
    #now paste them into catfruit
    if split_catfruit:
        for x in range(0,5):
            catastages[x][2].submit_as_new_stage(STAGE_SCHEM + EVENT_STAGE_SLETTER + stringize_number(442,3) + "_" + stringize_number(9-x,2) + ".csv")
    #now fix first stages
    if always_epic:
        for x in range(0,5):
            catastages[x][0].submit_as_new_stage(STAGE_SCHEM + EVENT_STAGE_SLETTER + stringize_number(442,3) + "_" + stringize_number(4-x,2) + ".csv")

def buff_gstange():
    """
    buffs growing strange to give 1 seed and then 4 seeds second stage
    \n conditional
    """
    do_self = settings["game"]["qol"]["stage_changes"]["gstrange_buff"]
    if not do_self:
        return
    gstrange_map = f.map_data(MAPSTAGEDATA + EVENT_STAGE_MLETTER + "_" + stringize_number(162,3) + ".csv")
    gstrange_extra_map = f.map_data(MAPSTAGEDATA + EXTRA_STAGE_MLETTER + "_" + stringize_number(22,3) + ".csv")
    
    gstrange_map.stages[0][gstrange_map.drop1_rate] = 100
    gstrange_map.stages[0][gstrange_map.drop1_id] = item.drop_id.elder_seed
    gstrange_map.stages[0][gstrange_map.drop1_count] = 1

    for each in gstrange_extra_map.stages: #set seed drop to 4
        each[gstrange_extra_map.drop2_count] = 4

    gstrange_map.submit()
    gstrange_extra_map.submit()

def buff_gaku():
    """
    buffs third and fourth stage massive, leaves the pre aku realms stages untouched
    \n conditional
    """
    do_self = settings["game"]["qol"]["stage_changes"]["growing_aku_buff"]
    if not do_self:
        return
    gaku_map = f.map_data(MAPSTAGEDATA + EVENT_STAGE_MLETTER + "_" + stringize_number(274,3) + ".csv")
    gaku_map.stages[2][gaku_map.drop1_count] = 3
    gaku_map.stages[3][gaku_map.drop1_count] = 10
    gaku_map.stages[3][gaku_map.drop2_count] = 5
    gaku_map.submit()

def buff_growing_epic():
    """
    makes extra stage always appear
    \n conditional
    """
    do_self = settings["game"]["qol"]["growing_epic_buff"]
    if not do_self:
        return
    gepic = f.stage_sche(STAGE_SCHEM + EVENT_STAGE_SLETTER + stringize_number(222,3) + "_" + stringize_number(0,2) + ".csv")
    gepic.extra_chance = 100
    gepic.submit()

#needs the stages actually made
def buff_proving_grounds():
    """
    buffs xp gains, makes catseyes an endless stage
    \n conditional
    """
    do_self = settings["game"]["qol"]["stage_changes"]["proving_grounds_buff"]
    if not do_self:
        return
    #normal buffs
    main_prov_map = f.map_data(MAPSTAGEDATA + EVENT_STAGE_MLETTER + "_" + stringize_number(250,3) + ".csv")
    main_prov_map.stages[0][main_prov_map.drop1_count] = 100000
    main_prov_map.stages[1][main_prov_map.drop1_count] = 300000
    main_prov_map.stages[2][main_prov_map.drop1_count] = 3
    main_prov_map.stages[2][main_prov_map.drop2_count] = 3
    main_prov_map.stages[2][main_prov_map.drop3_count] = 3
    main_prov_map.stages[2][main_prov_map.drop4_count] = 3
    main_prov_map.stages[2][main_prov_map.drop5_count] = 3
    main_prov_map.submit()
    for x in range(27,35): #this is all the xp proving grounds
        this_map = f.map_data(MAPSTAGEDATA + EXTRA_STAGE_MLETTER + "_" + stringize_number(x,3) + ".csv")
        for each in this_map.stages:
            each[this_map.drop1_count] = int(2*each[this_map.drop1_count])
        this_map.submit()
    for x in range(35,39): #this is the catseye ones
        this_map = f.map_data(MAPSTAGEDATA + EXTRA_STAGE_MLETTER + "_" + stringize_number(x,3) + ".csv")
        for each in this_map.stages:
            each[this_map.drop1_count] = 3
            each[this_map.drop2_count] = 3
            each[this_map.drop3_count] = 3
            each[this_map.drop4_count] = 3
            each[this_map.drop5_count] = 3
        this_map.submit()
    #now the endless shenanigans
    endless_stage_count = 25
    first_endless_stage = f.stage_sche(STAGE_SCHEM + MODDED_SLETTER + stringize_number(0,3) + "_" + stringize_number(0,2) + ".csv")
    second_endless_stage = f.stage_sche(STAGE_SCHEM + MODDED_SLETTER + stringize_number(0,3) + "_" + stringize_number(1,2) + ".csv")
    first_endless_stage.extra_map = "027"
    second_endless_stage.extra_map = "027"
    endless_map = f.map_data(MAPSTAGEDATA + EXTRA_STAGE_MLETTER + "_" + stringize_number(27,3) + ".csv")
    modded_endless_map = f.map_data(MAPSTAGEDATA + MODDED_MLETTER + "_" + stringize_number(0,3) + ".csv")
    #slap the drops onto map and submit it (I dont intend to make drops increase as time goes on)
    for x in range(0,endless_stage_count):
        endless_map.stages.append(modded_endless_map.stages[0])
        endless_map.stages.append(modded_endless_map.stages[1])
    endless_map.submit()
    # prepare stage names
    stage_name_start = STAGE_SCHEM + EXTRA_STAGE_SLETTER + stringize_number(27,3) + "_"
    # now create the stages and submit them
    print(first_endless_stage.enemies)
    first_stage_enemies = copy.deepcopy(first_endless_stage.enemies)
    second_stage_enemies = copy.deepcopy(second_endless_stage.enemies)
    for x in range(0,endless_stage_count):
        scalar = int(1+x**1.4)
        first_endless_stage.enemies = copy.deepcopy(first_stage_enemies)
        second_endless_stage.enemies = copy.deepcopy(second_stage_enemies)
        print(first_endless_stage.enemies)
        for each in first_endless_stage.enemies:
            each[first_endless_stage.magnification] = int(each[first_endless_stage.magnification]*scalar)
        for each in second_endless_stage.enemies:
            each[second_endless_stage.magnification] = int(each[second_endless_stage.magnification]*scalar)
        if x == endless_stage_count-1:
            first_endless_stage.extra_chance = 0
            second_endless_stage.extra_chance = 0
        else:
            first_endless_stage.extra_chance = 100
            second_endless_stage.extra_chance = 100
            first_endless_stage.extra_first_stage = stringize_number(2*(x+2),2)
            second_endless_stage.extra_first_stage = stringize_number(2*(x+2),2)
            first_endless_stage.extra_last_stage = stringize_number(1+2*(x+2),2)
            second_endless_stage.extra_last_stage = stringize_number(1+2*(x+2),2)
        first_endless_stage.submit_as_new_stage(stage_name_start + stringize_number(2*(x+1),2) + ".csv")
        second_endless_stage.submit_as_new_stage(stage_name_start + stringize_number(1+2*(x+1),2) + ".csv")



#need to add eoc2 and 3 killer

# still need zombie witch swap

def change_boss(stage_name,stepby):
    """
    part of randomize whats boss, takes a stage file name and a randomizer shift and randomizes its boss and submits it
    \n nonconditional
    """
    r = randinst(100)
    r.step(stepby)
    stage = f.stage_sche(stage_name)
    number_of_bosses = 0
    for enemy in stage.enemies:
        try:
            if enemy[stage.boss] == 1:
                number_of_bosses += 1
                enemy[stage.boss] = 0
        except:
            print(enemy,end="\t")
            print(stage_name)
    boss_lines = []
    for x in range(0,number_of_bosses):
        attempt_count = 0
        while attempt_count < 150:
            attempt_count += 1
            new_line = r.randrange(0,len(stage.enemies))
            if new_line not in boss_lines:
                boss_lines.append(new_line)
                break
    for each in boss_lines:
        stage.enemies[each][stage.boss] = 1
    
    if len(boss_lines) > 0:
        stage.submit()

def degacha_given_units():
    """
    degachas in unitbuy all the given units
    \n nonconditional
    """
    unitbuy = f.file_reader(UNITBUY_FILE)
    units = [
        131, #neneko
        228, #witchy neneko
        276, #summer neneko
        314, #new years neneko
        332, #easter neneko
        589, #valentine neneko
        120, #healer
        121, #merc
        191, #titi
        67,  #lil gau
        111, #nono
        390, #aoi
        391, #mizuki
        392, #hijiri
        293, #kyubey
        565, #tan
        566, #dango
        751, #lil yahiko
        26,  #punt
        173, #mola
        65,  #racism cow
        28,  #capsule
        184, #mint
        635, #million dollar
        68,  #judgement
        629, #bcat
        636, #btank
        645, #baxe
        654, #bgross
        662, #bcow
        667, #bbird
        684, #bfish
        688, #bdrag
        694, #btitan
    ]
    for each in units:
        unitbuy[each][ub.ub.unlock_type] = 0
    f.file_writer(UNITBUY_FILE,unitbuy)

def get_drop_id(unit_id,save_id=1000,set_save_id=False,dont_use_valid_drop_id=False):
    """
    gets [drop_id,save_id] from drop chara, will make if doesnt exist
    \n specify save id to make it use it, specify invalidity true to make it not a real drop
    """
    drop_chara = f.file_reader(DROP_CHARA)
    relevant_line = -1
    for line in range(0,len(drop_chara)):
        if drop_chara[line][2] == unit_id:
            relevant_line = line
    
    if relevant_line != -1 and drop_chara[relevant_line][0] != -1: #it already exists
        return [drop_chara[relevant_line][0],drop_chara[relevant_line][1]]
    if relevant_line == -1:
        relevant_line = len(drop_chara)
        drop_chara.append([-1,save_id,unit_id])
    if drop_chara[relevant_line][0] == -1:
        valid_drop_ids = []
        for x in range(1000,1200):
            valid_drop_ids.append(x)
        for line in drop_chara:
            if drop_chara[line][0] in valid_drop_ids:
                valid_drop_ids.remove(drop_chara[line][0])
        drop_chara[relevant_line][0] = valid_drop_ids[0]
    if set_save_id:
        drop_chara[relevant_line][1] = save_id
    
    #kill its id if its supposed to be invalid
    if dont_use_valid_drop_id:
        drop_chara[relevant_line][0] = -1
    
    f.file_writer(DROP_CHARA,drop_chara)
    return [drop_chara[relevant_line][0],drop_chara[relevant_line][1]]

def add_units_to_sol():
    """
    adds given units to sol
    \n conditional, minor function
    """
    add_seasonals = settings["game"]["qol"]["stage_change"]["seasonals_in_sol"]
    add_collab = settings["game"]["qol"]["stage_changes"]["collabs_in_sol_advents"]
    collab_advent_tf = settings["game"]["qol"]["stage_changes"]["collab_tf_as_advents"]
    do_mission = settings["game"]["qol"]["stage_changes"]["mission_collab_special_tf_drop"]

    #change unitbuy
    if add_collab:
        degacha_given_units()

    sol_units = []
    if add_seasonals:
        sol_units.append([63,24,7]) #sportsday in winning back
        sol_units.append([63,35,0,1]) #rampage tf in greeter at the gates
        sol_units.append([70,17,1]) #salaryman in prison sentence
        sol_units.append([70,33,1,1]) #ritual tf in swap of sacrifice
        sol_units.append([74,7,7]) #reindeer in frontier spirit
        sol_units.append([74,12,7,1]) #xmas pudding tf in shrimp frontier
        sol_units.append([79,39,2]) #adult in drunken backrub
        sol_units.append([79,8,4,1]) #prisoner tf in juvenile killer
        sol_units.append([80,5,2]) #evil in wanted night
        sol_units.append([80,18,4,1]) #gentlemen tf in liars fate
        sol_units.append([81,4,4]) #doll in twin peaks
        sol_units.append([81,28,4,1]) #doll tf in darkweb
        sol_units.append([100,14,4]) #maiden in gates of aphrodite
        sol_units.append([100,28,0,1]) #maiden tf in renewed conflict
        sol_units.append([104,3,6]) #koi in seaweed shallows
        sol_units.append([104,39,0,1]) #koi tf in narrow docks
        sol_units.append([109,21,0]) #madam bride in the red carpet
        sol_units.append([109,43,5,1]) #madam bride tf in heavens oasis
        sol_units.append([122,15,3]) #vacation queen in apple bobbing ocean
        sol_units.append([122,40,1,1]) #call center tf in dial up dreams
        sol_units.append([128,28,3]) #vengeful in thorny dialogue
        sol_units.append([128,37,1,1]) #kite tf in seabreeze salon
        sol_units.append([132,23,1]) #kung fu in angry fighting
        sol_units.append([132,26,2,1]) #kung fu tf in warriors dawn
        sol_units.append([176,22,0]) #marshmallow in feast of betrayal
        sol_units.append([227,35,5]) #pumpcat in the haunted 1ldk
        sol_units.append([244,22,3]) #gift of cats
        sol_units.append([282,40,4]) #awa odori in the holy exploit
        sol_units.append([303,23,5]) #delivery in scent of gore fish
        sol_units.append([329,29,5]) #eggy in lord of the abyss
        sol_units.append([343,27,0]) #slug cat in at least Im a cat
        sol_units.append([127,32,5,1]) #bomber tf in the spy who pet me, maybe this should be moved to a later razor stage
    if add_collab:
        sol_units.append([184,1,0]) #mint in nyandalucia
        sol_units.append([121,3,7]) #merc in salty is seawater
        sol_units.append([191,5,4]) #titi in wandering traveler
        sol_units.append([28,8,1]) #capsule in fluffy dark weapon
        sol_units.append([120,17,0]) #healer in sin and punishment
        sol_units.append([26,18,3]) #punt in king of freedom
        sol_units.append([131,20,4]) #neneko in subtle curfew
        sol_units.append([228,35,1]) #neneko witchy in rickety coaster
        sol_units.append([276,37,2]) #neneko summer in deep sea dying
        sol_units.append([314,27,3]) #neneko new years in beautiful finale
        sol_units.append([332,35,4]) #neneko easter in seductive chicken room
        sol_units.append([589,43,0]) #neneko valentine in eat the weak
    
    #add units to sol
    current_save_id = 1000
    for unit in sol_units:
        current_save_id -= 1
        drop_id = -1
        if len(unit) == 4:
            drop_id = unit[0] + 10001
        else:
            result = get_drop_id(unit[0],current_save_id)
            drop_id = result[0]
        file_start = MAPSTAGEDATA + SOL_MLETTER + "_"
        file_end = "00" + str(unit[1]) + ".csv"
        this_map = f.map_data(file_start + file_end[-7:])
        this_map.stages[unit[2]] = drop_id
        this_map.submit()

def add_grouped_units():
    """
    clumps grouped units onto the same save id
    \n conditional, minor function
    """
    add_collab = settings["game"]["qol"]["stage_changes"]["collabs_in_sol_advents"]

    #attatch grouped units together
    grouped = []
    if add_collab:
        grouped.append([287,67]) #golfer gives lil gau
        grouped.append([324,111]) #zamboney gives nono
        grouped.append([442,390,391,392]) #vendor gives power pro
        grouped.append([507,293,299]) #supercat gives kyubey and madoka
        grouped.append([382,565,566]) #glass gives tan/dango
        grouped.append([531,751]) #bear gives yahiko
        grouped.append([528,26]) #russian gives punt
        grouped.append([521,173]) #medusa gives mola
        grouped.append([553,68]) #bakery gives judgement
        grouped.append([78,65]) #space gives racism cow
        grouped.append([88,28]) #jump rope gives capsule
        grouped.append([201,635]) #drumpcorps gives million dollar
        grouped.append([636,645,654,662,667,684,688,694]) #bcat gives all brainwashed
        get_drop_id(629,600,True) #set bcat to having a drop id
    
    for each in grouped:
        result = get_drop_id(each[0])
        for x in range(1,len(each)):
            get_drop_id(each[x],result[1],True,True) #add all of them tied to each[0]s save id with no drop id

#not done 
def add_collab_tf_drops():
    """
    adds collab tf as either missions on drops
    \n conditional, minor function
    """
    add_seasonals = settings["game"]["qol"]["stage_change"]["seasonals_in_sol"]
    add_collab = settings["game"]["qol"]["stage_changes"]["collabs_in_sol_advents"]
    collab_advent_tf = settings["game"]["qol"]["stage_changes"]["collab_tf_as_advents"]
    do_mission = settings["game"]["qol"]["stage_changes"]["mission_collab_special_tf_drop"]
    if add_collab: #need to figure out how to make disabling catfruit tfs work
        units = []
        units.append([120,199,0]) #healer tf in river archeon (hannya)
        units.append([121,196,0]) #merc tf in new testament (clionel)
        units.append([191,195,0]) #titi tf in perfect cyclone revenge
        units.append([67,201,0]) #lil gau tf in honey drip (queen bee)
        units.append([111,205,0]) #nono tf in prisoners progress (daboo)
        units.append([26,381,0]) #punt tf in divine daughter (papuu)
        units.append([173,296,0]) #mola tf in heaven and hell (okame)
        units.append([68,375,0]) #judgement tf in babies first (doremi)
        #not adding power pro for now
        if do_mission:
            pass #Ill have to figure out how to do missions
        elif collab_advent_tf:
            for unit in units:
                drop_id = 10001 + unit[0]
                if unit[0] == 120: #literally just healer fix
                    drop_id -= 1
                file_name_start = MAPSTAGEDATA + EVENT_STAGE_MLETTER + "_"
                file_name_end = "00" + str(unit[1]) + ".csv"
                this_map = f.map_data(file_name_start + file_name_end[-7:])
                this_map.stages[unit[2]][this_map.drop1_count] = 1
                this_map.stages[unit[2]][this_map.drop1_id] = drop_id
                this_map.stages[unit[2]][this_map.drop1_rate] = drop_id
                this_map.submit()
    
def make_all_epic_extra_stage():
    """
    makes the all epic extra stage
    """
    epic_green_map = f.map_data(MAPSTAGEDATA + EXTRA_STAGE_MLETTER + "_" + stringize_number(0,3) + ".csv")
    epic_green_stage = f.stage_sche(STAGE_SCHEM + EXTRA_STAGE_SLETTER + stringize_number(0,3) + "_" + stringize_number(2,2) + ".csv")
    #add the only jubilee line to map data
    map_data = []
    for x in range(0,epic_green_map.drop_scheme+1):
        map_data.append(epic_green_map.stages[2][x])
    epic_green_map.stages.append(map_data)
    epic_green_map.stages[3][epic_green_map.drop1_id] = item.drop_id.epic_fruit
    epic_green_map.stages[3][epic_green_map.drop1_rate] = 100
    epic_green_map.stages[3][epic_green_map.drop1_count] = 2
    epic_green_map.resolve_stage_count()
    epic_green_map.submit()
    epic_green_stage.submit_as_new_stage(STAGE_SCHEM + EXTRA_STAGE_SLETTER + stringize_number(0,3) + "_" + stringize_number(3,2) + ".csv")



