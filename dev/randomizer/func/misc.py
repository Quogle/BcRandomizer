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



#need to add eoc2 and 3 killer

# still need zombie witch swap










