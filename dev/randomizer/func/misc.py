import dev.randomizer.func.files as f
from dev.randomizer.parse_config import settings
from dev.randomizer.data.filepaths import *
import dev.randomizer.enums.treasure as tres




def remove_itf_crystals():
    """
    removes itf crystals but doesnt replace them with anything
    """
    treasures = f.file_reader(ITF_TREASURE_DATA)
    for x in range(tres.pos.treasure_effects,tres.pos.treasure_effects+tres.pos.treasure_count):
        if treasures[x][tres.pos.treasure_effect_id] == tres.id.itf_crystal:
            treasures[x][tres.pos.treasure_effect_id] = -1
    f.file_writer(treasures)

def remove_cotc_crystals():
    """
    removes cotc crystals but doesnt replace them with anything
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
    """
    chapters = [COTC1_TREASURE_DATA,COTC2_TREASURE_DATA,COTC3_TREASURE_DATA]
    god_ids = [tres.id.god1_mask,tres.id.god2_mask,tres.id.god3_mask]
    for chapter in chapters:
        treasures = f.file_reader(chapter)
        for line_id in range(tres.pos.treasure_effects,tres.pos.treasure_effects+tres.pos.treasure_count):
            if chapter[line_id][tres.pos.treasure_effect_id] in god_ids:
                chapter[line_id][tres.pos.treasure_effect_id] = tres.id.god1_mask
                chapter[line_id][tres.pos.apply_only_this_chapter] = 1
        f.file_writer(chapter)


#need to add eoc2 and 3 killer

# still need zombie witch swap










