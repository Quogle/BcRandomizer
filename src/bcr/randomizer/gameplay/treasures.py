""" module for editing treasures and buffing enemies as a result based on config """
from ...config.defaults import DEFAULT_CONFIG
import tadbcmc.pieces.treasure as treasure
import tadbcmc.data.enums.treasure as tres
import tadbcmc.core.game_files as gf
import tadbcmc.data.enums.enemy as e
import tadbcmc.data.filenames as fn

def do_all_treasure_editing(config=DEFAULT_CONFIG):
    """ does all the things treasure related in config """
    _condense_god() #this just always runs idc
    _remove_itf_crystals(config)
    _remove_cotc_crystals(config)
    _buff_ex_aliens(config)
    _buff_aliens_in_eoc(config)








def _remove_itf_crystals(config=DEFAULT_CONFIG):
    """ removes the crystals from itf, replaces them with weak energy treasures """
    if not config["gameplay"]["modifications"]["remove_itf_crystals"]:
        return #dont do anything if its off
    for x in range(0,2): #run twice since theres two of em
        treasure.set_treasure(
            chapter_number=4,
            target_effect=tres.id.itf_crystal,
            which_target_effect=0,
            overwrite_existing=True,
            new_effect=tres.id.energy_recharge,
            new_strength=40, #if I did 50 then it would result in /0, this should be fine tho
            only_this_chapter=0 #not only thing chapter tho I do wonder how thatd work
            )

def _remove_cotc_crystals(config=DEFAULT_CONFIG):
    """ removes the crystals from cotc, replaces them with weak study treasures """
    if not config["gameplay"]["modifications"]["remove_cotc_crystals"]:
        return #dont do anything if its off
    for x in range(0,5): #run fivce since theres 5 of em
        treasure.set_treasure(
            chapter_number=6,
            target_effect=tres.id.cotc_crystal,
            which_target_effect=0,
            overwrite_existing=True,
            new_effect=tres.id.study,
            new_strength=10, #dont want it to be absurdly strong since theres 15 total
            only_this_chapter=0 #not only thing chapter tho I do wonder how thatd work
            )

def _condense_god():
    """ condenses god down to only the first mask
    \n also edits the flags of the enemies to have it
    \n non configurable this just always runs and theres 0 consequence """
    treasure.condense_god_treasures()
    #now edit the gods themselves
    estat = gf.file_reader(fn.ENEMY_STATS)
    gods = [367,419,446]
    for u_id in gods:
        if estat[u_id+2][e.s.starred_god] > 1:
            estat[u_id+2][e.s.starred_god] = 2
    gf.file_writer(fn.ENEMY_STATS,estat)

def _buff_ex_aliens(config=DEFAULT_CONFIG):
    """ buffs alien enemies in itf/cotc/sol/ul/events which have been made weaker because of alterations """
    if not config["gameplay"]["modifications"]["buff_weak_aliens"]:
        return #no sense going further if thats off
    #if crystals are still on, only no longer aliens should be buffed
    #if crystals are off, all that were alien should be buffed
    if config["gameplay"]["modifications"]["remove_itf_crystals"]:
        treasure.buff_aliens_in_itf(only_do_no_longer_alien=False)
    else:
        treasure.buff_aliens_in_itf(only_do_no_longer_alien=True)
    if config["gameplay"]["modifications"]["remove_cotc_crystals"]:
        treasure.buff_aliens_in_cotc(only_do_no_longer_starred=False)
        treasure.buff_cotc_aliens_outside_cotc(only_do_no_longer_starred=False)
    else:
        treasure.buff_aliens_in_cotc(only_do_no_longer_starred=True)
        treasure.buff_cotc_aliens_outside_cotc(only_do_no_longer_starred=True)

def _buff_aliens_in_eoc(config=DEFAULT_CONFIG):
    """ buffs the aliens in eoc when crystals are off by adding treasures effecting only this chapter to moon """
    itf_treasure_removal = config["gameplay"]["modifications"]["remove_itf_crystals"]
    do_eoc_buff = config["gameplay"]["modifications"]["leave_strong_aliens_in_eoc"]
    if itf_treasure_removal and do_eoc_buff:
        treasure.set_treasure(
            chapter_number=1,
            new_effect=tres.id.itf_crystal,
            new_strength=600,
            new_stages=[48],
            new_number_of_stages=1,
            only_this_chapter=1)












