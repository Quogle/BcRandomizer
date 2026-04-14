import dev.randomizer.func.game_files as f
import dev.randomizer.enums.cats as c
import dev.randomizer.enums.enemy as e
from dev.randomizer.data.filepaths import *
from dev.randomizer.func.random import randinst
from dev.randomizer.parse_config import settings
from dev.randomizer.func.misc import *
import os
import shutil
from PIL import Image



def get_enemy_traits(stats):
    """
    returns an array of trait names that a unit has
    \n conditional
    """
    witch_swap = settings["game"]["gameplay"]["preserve_old_zombies"]
    #get names and arrays #if need to make this work for cats and enemies you only need to swap between differnt number traits
    number_traits = [e.t.black,e.t.red,e.t.white,e.t.floating,e.t.relic,e.t.zombie,e.t.alien,e.t.angel,e.t.aku,e.t.metal]
    text_traits = ["black","red","white","floating","relic","zombie","alien","angel","aku","metal"]

    #witch swap
    if witch_swap:
        try:
            index = number_traits.index(e.t.zombie)
            number_traits[index] = e.s.witch
        except:
            pass


    trait_array = []
    for unit_id in range(0,len(stats)):
        units_traits = []
        for trait_id in range(0,len(number_traits)):
            if stats[unit_id][number_traits[trait_id]] == 1:
                units_traits.append(text_traits[trait_id])
        trait_array.append(units_traits)
    
    return trait_array

def get_new_enemy_traits(new_stats,old_stats):
    """
    returns an array of all the new traits enemies have
    """
    new_traits = get_enemy_traits(new_stats)
    old_traits = get_enemy_traits(old_stats)

    for unit_id in range(0,len(old_traits)): #assuming old stats is short or the same length
        for trait in old_traits[unit_id]:
            if trait in new_traits[unit_id]:
                new_traits[unit_id].remove(trait)
    
    return new_traits

def dual_sprite_maker(unit_id,trait1,trait2):
    """
    makes sprite, will attempt to make them look like 1 trait if one of the two traits is missing a sprite
    """
    file_ending = "\\" + stringize_number(unit_id,3) + "_e.png"
    internal = ""
    #get part 1
    if os.path.exists(PART_1_SPRITES + trait1 + file_ending):
        part_1 = Image.open(PART_1_SPRITES + trait1 + file_ending)
    elif os.path.exists(PART_2_SPRITES + trait1 + file_ending):
        internal += trait1
        part_1 = Image.open(PART_2_SPRITES + trait1 + file_ending)
    else:
        return
    part_1 = part_1.convert("RGBA")

    #get part 2
    if os.path.exists(PART_2_SPRITES + trait1 + file_ending):
        part_2 = Image.open(PART_2_SPRITES + trait1 + file_ending)
    elif os.path.exists(PART_1_SPRITES + trait1 + file_ending):
        internal += trait2
        part_2 = Image.open(PART_1_SPRITES + trait1 + file_ending)
    else:
        return
    part_2 = part_2.convert("RGBA")
    if len(internal) > 0:
        print(internal + " sprite is missing for unit " + str(unit_id))

    #combine parts
    part_1.alpha_composite(part_2)
    part_1.save(DOWNLOAD_LOCAL + stringize_number(unit_id,3) + "_e.png")
    part_1.close()
    part_2.close()

def single_sprite_getter(unit_id,trait):
    """
    copies enemies with a single trait to downloadlocal
    """
    file_ending = "\\" + stringize_number(unit_id,3) + "_e.png"
    if os.path.exists(SINGLE_TRAIT_SPRITE_PATH + trait + file_ending):
        shutil.copy(SINGLE_TRAIT_SPRITE_PATH + trait + file_ending,DOWNLOAD_LOCAL)

def sprite_exceptions(trait_array):
    """
    copies johnnyleon and poultrio if they have more than 3 traits
    """
    #their unit ids
    johnny = 521
    poultrio = 769
    file_ending = "_e.png"
    if len(trait_array[johnny+2]) > 3:
        if os.path.exists(SPRITE_PATH + str(johnny) + file_ending):
            shutil.copy(SPRITE_PATH + str(johnny) + file_ending,DOWNLOAD_LOCAL)
    
    if len(trait_array[poultrio+2]) > 3:
        if os.path.exists(SPRITE_PATH + str(poultrio) + file_ending):
            shutil.copy(SPRITE_PATH + str(poultrio) + file_ending,DOWNLOAD_LOCAL)

def get_sprites(kill_previous=False):
    """
    gets the new sprites and if designated kills old sprites
    \n conditional and the total function
    """
    r = randinst(106)
    new_stats = f.file_reader(ENEMY_STATS)
    old_stats = f.file_reader(DATA_LOCAL + ENEMY_STATS)
    if kill_previous:
        for x in range(0,len(new_stats)):
            file_name = DOWNLOAD_LOCAL + stringize_number(x,3) + "_e.png"
            if os.path.exists(file_name):
                os.remove(file_name)
    
    current_traits = get_enemy_traits(new_stats)
    new_traits = get_new_enemy_traits(new_stats,old_stats) #I ended up not even using this lmao

    #get images
    for unit_id in range(0,len(current_traits)):
        sprite_rando_dec = r.randrange(0,2)
        if len(current_traits[unit_id]) == 1: #it can actually just try to find it if theres only 1 trait
            single_sprite_getter(unit_id-2,current_traits[unit_id][0])
        elif len(current_traits[unit_id]) == 2: 
            dual_sprite_maker(unit_id-2,current_traits[unit_id][1-sprite_rando_dec],current_traits[unit_id][sprite_rando_dec])
    
    sprite_exceptions(current_traits)















