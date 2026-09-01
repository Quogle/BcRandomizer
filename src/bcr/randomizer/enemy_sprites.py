import os
from PIL import Image
import tadbcmc.core.file_handler as fh
import tadbcmc.core.simple_funcs as simp
import tadbcmc.data.enums.enemy as e
import tadbcmc.core.seeded_randomization as srand
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn




def _dual_sprite_maker(unit_id,trait1,trait2):
    """
    makes sprite, will attempt to make them look like 1 trait if one of the two traits is missing a sprite
    """
    #works by for each part it attempts to get the correct one, if it cant get the incorrect one and log that it failed
    #if neither exist exit, but if one exist alert user only one exists
    file_name = ("000"+str(unit_id))[-3:] + "_e.png"
    internal = ""
    part1_path = simp.path_join(simp.path_join(fh.SINGLE_SPRITE_FILES,trait1),file_name)
    part2_path = simp.path_join(simp.path_join(fh.SINGLE_SPRITE_FILES,trait2),file_name)
    #get part 1
    if os.path.exists(part1_path):
        part_1 = Image.open(part1_path)
    elif os.path.exists(part2_path):
        internal += trait1
        part_1 = Image.open(part2_path)
    else:
        return
    part_1 = part_1.convert("RGBA")

    #get part 2
    if os.path.exists(part2_path):
        part_2 = Image.open(part2_path)
    elif os.path.exists(part1_path):
        internal += trait2
        part_2 = Image.open(part1_path)
    else:
        return
    part_2 = part_2.convert("RGBA")
    if len(internal) > 0:
        print(internal + " sprite is missing for unit " + str(unit_id))

    #combine parts
    part_1.alpha_composite(part_2)
    part_1.save(fh.get_dl_path_for_new_file(file_name))
    part_1.close()
    part_2.close()

def _single_sprite_getter(unit_id,trait):
    """
    copies enemies with a single trait to downloadlocal
    """
    file_name = ("000"+str(unit_id))[-3:] + "_e.png"
    sprite_path = simp.path_join(simp.path_join(fh.SINGLE_SPRITE_FILES,trait),file_name)
    if os.path.exists(sprite_path):
        fh.copy_file_to_dl(sprite_path)

def _get_all_other_sprites(trait_array):
    """
    copies any other sprites in sprites if the conditions following e are met
    """
    #get a list of all the sprites
    all_in_sprites = os.listdir(fh.SPRITE_FILES)
    pngs = []
    for each in all_in_sprites:
        if ".png" in each:
            pngs.append(each)
    #now get the number of traits needed for those enemies
    counts = []
    unit_ids = []
    for each in pngs:
        trait_count = 0
        if "e" in each:
            try: #use the number after e to determine how many traits something needs
                trait_count += int(each[each.find("e")+1])
            except:
                pass
        counts.append(trait_count)
        unit_ids.append(int(each[:3]))
    #now check and do all of them
    for x in range(0,len(pngs)):
        if len(trait_array[unit_ids[x]]) >= counts[x]:
            #remove the condition after e
            file_name = pngs[x]
            epos = file_name.find("e")
            if epos != -1 and file_name[epos+1] != ".":
                file_name = file_name[:epos+1] + file_name[-4:] #this whole operation seems strange hardcoded and may cause problems
            sprite_path = simp.path_join(fh.SPRITE_FILES,file_name)
            fh.copy_file_to_dl(sprite_path,file_name)
            
def _get_enemy_traits(stats):
    """
    returns an array of trait names that a unit has
    \n nonconditional
    """
    #get names and arrays #if need to make this work for cats and enemies you only need to swap between differnt number traits
    number_traits = [e.t.dark,e.t.red,e.t.white,e.t.floating,e.t.relic,e.t.zombie,e.t.alien,e.t.angel,e.t.aku,e.t.metal]
    text_traits = ["dark","red","white","floating","relic","zombie","alien","angel","aku","metal"]


    trait_array = []
    for unit_id in range(0,len(stats)):
        units_traits = []
        for trait_id in range(0,len(number_traits)):
            if stats[unit_id][number_traits[trait_id]] == 1:
                units_traits.append(text_traits[trait_id])
        trait_array.append(units_traits)
    
    return trait_array

#this function is unused and really has no reason to exist       
def _get_new_enemy_traits(new_stats,old_stats):
    """
    returns an array of all the new traits enemies have
    """
    new_traits = _get_enemy_traits(new_stats)
    old_traits = _get_enemy_traits(old_stats)

    for unit_id in range(0,len(old_traits)): #assuming old stats is short or the same length
        for trait in old_traits[unit_id]:
            if trait in new_traits[unit_id]:
                new_traits[unit_id].remove(trait)
    
    return new_traits
    

def get_enemy_sprites(kill_previous=False):
    """
    gets the new sprites and if designated kills old sprites
    \n total, doesnt consider witch
    """
    r = srand.randinst(106)
    new_stats = gf.file_reader(fn.ENEMY_STATS)
    if kill_previous:
        for x in range(0,len(new_stats)):
            file_name = simp.uinfo_to_anim(x,enemy=True,file_end=".png")
            fh.remove_from_dl(file_name)
    
    current_traits = _get_enemy_traits(new_stats)

    #get images
    for unit_id in range(0,len(current_traits)):
        sprite_rando_dec = r.randrange(0,2)
        if len(current_traits[unit_id]) == 1: #it can actually just try to find it if theres only 1 trait
            _single_sprite_getter(unit_id-2,current_traits[unit_id][0])
        elif len(current_traits[unit_id]) == 2: 
            _dual_sprite_maker(unit_id-2,current_traits[unit_id][1-sprite_rando_dec],current_traits[unit_id][sprite_rando_dec])
    _get_all_other_sprites(current_traits)











