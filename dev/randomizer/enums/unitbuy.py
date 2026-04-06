from enum import IntEnum

#eoc_stage_unlock,cost_value,xp_lvl_1,xp_lvl_2,xp_lvl_3,xp_lvl_4,xp_lvl_5,xp_lvl_6,xp_lvl_7,xp_lvl_8,xp_lvl_9,xp_lvl_10,unlock_type,rarity,display_order,unlock_chapter_eoc,selling_xp,unknown_1,default_max_level,default_plus_level,basic_unlock_level,unknown_2,unknown_3,true_form_id,ultra_form_id,level_to_true_form,level_to_ultra_form,xp_for_true_form,material_1_id,material_1_amount,material_2_id,material_2_amount,material_3_id,material_3_amount,material_4_id,material_4_amount,material_5_id,material_5_amount,xp_for_ultra_form,material_1_id_ultra,material_1_amount_ultra,material_2_id_ultra,material_2_amount_ultra,material_3_id_ultra,material_3_amount_ultra,material_4_id_ultra,material_4_amount_ultra,material_5_id_ultra,material_5_amount_ultra,max_level,max_catseyes_level,max_plus_level,unknown_4,unknown_5,unknown_6,unknown_7,unknown_8,available_in_game,np_selling_amount,true_form_availability_unlock,unknown_9,unevolved_sprite_eggs,evolved_sprite_eggs

class ub(IntEnum):
    eoc_stage_unlock = 0
    cost_value = 1
    xp_lvl_1 = 2
    xp_lvl_2 = 3
    xp_lvl_3 = 4
    xp_lvl_4 = 5
    xp_lvl_5 = 6
    xp_lvl_6 = 7
    xp_lvl_7 = 8
    xp_lvl_8 = 9
    xp_lvl_9 = 10
    xp_lvl_10 = 11
    unlock_type = 12
    rarity = 13                     # 0 = basic, 1 = special, 2 = rare, 3 = sr, 4 = uber, 5 = lr
    display_order = 14
    unlock_chapter_eoc = 15
    selling_xp = 16
    unknown_1 = 17
    default_max_level = 18
    default_plus_level = 19
    basic_unlock_level = 20
    unknown_2 = 21
    unknown_3 = 22
    true_form_id = 23
    ultra_form_id = 24
    level_to_true_form = 25
    level_to_ultra_form = 26
    xp_for_true_form = 27
    material_1_id = 28              # catfruit, etc
    material_1_amount = 29
    material_2_id = 30
    material_2_amount = 31
    material_3_id = 32
    material_3_amount = 33
    material_4_id = 34
    material_4_amount = 35
    material_5_id = 36
    material_5_amount = 37
    xp_for_ultra_form = 38
    material_1_id_ultra = 39
    material_1_amount_ultra = 40
    material_2_id_ultra = 41
    material_2_amount_ultra = 42
    material_3_id_ultra = 43
    material_3_amount_ultra = 44
    material_4_id_ultra = 45
    material_4_amount_ultra = 46
    material_5_id_ultra = 47
    material_5_amount_ultra = 48
    max_level = 49
    max_catseyes_level = 50
    max_plus_level = 51
    unknown_4 = 52
    unknown_5 = 53
    unknown_6 = 54
    unknown_7 = 55
    unknown_8 = 56
    available_in_game = 57
    np_selling_amount = 58
    true_form_availability_unlock = 59
    unknown_9 = 60
    unevolved_sprite_eggs = 61
    evolved_sprite_eggs = 62