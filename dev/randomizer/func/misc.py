import dev.randomizer.func.files as f
from dev.randomizer.parse_config import settings
from dev.randomizer.data.filepaths import *
import dev.randomizer.enums.treasure as tres
import dev.randomizer.enums.item as item
import copy


def remove_itf_crystals():
    """
    removes itf crystals but doesnt replace them with anything
    \n nonconditional
    """
    treasures = f.file_reader(ITF_TREASURE_DATA)
    for x in range(tres.pos.treasure_effects,tres.pos.treasure_effects+tres.pos.treasure_count):
        if treasures[x][tres.pos.treasure_effect_id] == tres.id.itf_crystal:
            treasures[x][tres.pos.treasure_effect_id] = -1
    f.file_writer(treasures)

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
        f.file_writer(treasures)

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
        f.file_writer(treasures)

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
            gap_map[x] = gap[x]
            ash_map[x] = ash[x]
            jin_map[x] = jin[x]
        gap_map.submit()
        ash_map.submit()
        jin_map.submit()

        #should I edit the in forest type stages and enigma?
        
        
        

        



        


            
            



#need to add eoc2 and 3 killer

# still need zombie witch swap










