from enum import IntEnum

class drop_id(IntEnum): #im only adding the ones were likely to use here
    speed_up = 0
    radar = 1
    rich  = 2
    cpu = 3
    cat_jobs = 4
    sniper = 5
    xp = 6
    np = 7

    cat_ticket = 11
    rare_ticket = 12
    cat_food = 13
    lucky_ticket = 16
    platinum_ticket = 20
    lucky_ticket_g = 77
    platinum_shard = 157
    shop_cat_ticket = 20
    shop_rare_ticket = 21
    shop_cat_food = 22
    shop_lucky_ticket = 23
    shop_platinum_ticket = 29

    purple_seed = 30
    red_seed = 31
    blue_seed = 32
    green_seed = 33
    yellow_seed = 34
    purple_fruit = 35
    red_fruit = 36
    blue_fruit = 37
    green_fruit = 38
    yellow_fruit = 39
    epic_fruit = 40
    elder_seed = 41
    elder_fruit = 42
    epic_seed = 43
    gold_fruit = 44
    aku_seed = 160
    aku_fruit = 161
    gold_seed = 164

    purple_stone = 167
    red_stone = 168
    blue_stone = 169
    green_stone = 170
    yellow_stone = 171
    purple_gem = 179
    red_gem = 180
    blue_gem = 181
    green_gem = 182
    yellow_gem = 183
    epic_stone = 184


    catseye_special = 50
    catseye_rare = 51
    catseye_superrare = 52
    catseye_uber = 53
    catseye_legend = 54
    catseye_dark = 58

    catamin_a = 55
    catamin_b = 56
    catamin_c = 57

    bricks = 85
    feathers = 86
    coal = 87
    sprockets = 88
    gold = 89
    meteorite = 90
    beast_bones = 91
    engineer = 92
    ammonite = 140
    brick_z = 187
    feather_z = 188
    coal_z = 189
    sprocket_z = 190
    gold_z = 191
    meteorite_z = 192
    beast_bone_z = 193
    ammonite_z = 194

    leadership = 105
    restarter_pack = 123
    endless_rich = 151
    endless_cpu = 152
    endless_sniper = 153

    #orbs
    orb_red_atk_d = 30000
    orb_red_atk_c = 30001
    orb_red_atk_b = 30002
    orb_red_atk_a = 30003
    orb_red_atk_s = 30004
    orb_red_def_d = 30005
    orb_red_def_c = 30006
    orb_red_def_b = 30007
    orb_red_def_a = 30008
    orb_red_def_s = 30009
    
    orb_float_atk_d = 30010
    orb_float_atk_c = 30011
    orb_float_atk_b = 30012
    orb_float_atk_a = 30013
    orb_float_atk_s = 30014
    orb_float_def_d = 30015
    orb_float_def_c = 30016
    orb_float_def_b = 30017
    orb_float_def_a = 30018
    orb_float_def_s = 30019
    
    orb_black_atk_d = 30020
    orb_black_atk_c = 30021
    orb_black_atk_b = 30022
    orb_black_atk_a = 30023
    orb_black_atk_s = 30024
    orb_black_def_d = 30025
    orb_black_def_c = 30026
    orb_black_def_b = 30027
    orb_black_def_a = 30028
    orb_black_def_s = 30029

    orb_metal_def_d = 30030
    orb_metal_def_c = 30031
    orb_metal_def_b = 30032
    orb_metal_def_a = 30033
    orb_metal_def_s = 30034

    orb_angel_atk_d = 30035
    orb_angel_atk_c = 30036
    orb_angel_atk_b = 30037
    orb_angel_atk_a = 30038
    orb_angel_atk_s = 30039
    orb_angel_def_d = 30040
    orb_angel_def_c = 30041
    orb_angel_def_b = 30042
    orb_angel_def_a = 30043
    orb_angel_def_s = 30044

    orb_alien_atk_d = 30045
    orb_alien_atk_c = 30046
    orb_alien_atk_b = 30047
    orb_alien_atk_a = 30048
    orb_alien_atk_s = 30049
    orb_alien_def_d = 30050
    orb_alien_def_c = 30051
    orb_alien_def_b = 30052
    orb_alien_def_a = 30053
    orb_alien_def_s = 30054

    orb_zombie_atk_d = 30055
    orb_zombie_atk_c = 30056
    orb_zombie_atk_b = 30057
    orb_zombie_atk_a = 30058
    orb_zombie_atk_s = 30059
    orb_zombie_def_d = 30060
    orb_zombie_def_c = 30061
    orb_zombie_def_b = 30062
    orb_zombie_def_a = 30063
    orb_zombie_def_s = 30064

    orb_red_strong_d = 30065
    orb_red_strong_c = 30066
    orb_red_strong_b = 30067
    orb_red_strong_a = 30068
    orb_red_strong_s = 30069
    orb_red_massive_d = 30070
    orb_red_massive_c = 30071
    orb_red_massive_b = 30072
    orb_red_massive_a = 30073
    orb_red_massive_s = 30074
    orb_red_resist_d = 30075
    orb_red_resist_c = 30076
    orb_red_resist_b = 30077
    orb_red_resist_a = 30078
    orb_red_resist_s = 30079

    orb_float_strong_d = 30080
    orb_float_strong_c = 30081
    orb_float_strong_b = 30082
    orb_float_strong_a = 30083
    orb_float_strong_s = 30084
    orb_float_massive_d = 30085
    orb_float_massive_c = 30086
    orb_float_massive_b = 30087
    orb_float_massive_a = 30088
    orb_float_massive_s = 30089
    orb_float_resist_d = 30090
    orb_float_resist_c = 30091
    orb_float_resist_b = 30092
    orb_float_resist_a = 30093
    orb_float_resist_s = 30094

    orb_black_strong_d = 30095
    orb_black_strong_c = 30096
    orb_black_strong_b = 30097
    orb_black_strong_a = 30098
    orb_black_strong_s = 30099
    orb_black_massive_d = 30100
    orb_black_massive_c = 30101
    orb_black_massive_b = 30102
    orb_black_massive_a = 30103
    orb_black_massive_s = 30104
    orb_black_resist_d = 30105
    orb_black_resist_c = 30106
    orb_black_resist_b = 30107
    orb_black_resist_a = 30108
    orb_black_resist_s = 30109

    orb_angel_strong_d = 30110
    orb_angel_strong_c = 30111
    orb_angel_strong_b = 30112
    orb_angel_strong_a = 30113
    orb_angel_strong_s = 30114
    orb_angel_massive_d = 30115
    orb_angel_massive_c = 30116
    orb_angel_massive_b = 30117
    orb_angel_massive_a = 30118
    orb_angel_massive_s = 30119
    orb_angel_resist_d = 30120
    orb_angel_resist_c = 30121
    orb_angel_resist_b = 30122
    orb_angel_resist_a = 30123
    orb_angel_resist_s = 30124

    orb_alien_strong_d = 30125
    orb_alien_strong_c = 30126
    orb_alien_strong_b = 30127
    orb_alien_strong_a = 30128
    orb_alien_strong_s = 30129
    orb_alien_massive_d = 30130
    orb_alien_massive_c = 30131
    orb_alien_massive_b = 30132
    orb_alien_massive_a = 30133
    orb_alien_massive_s = 30134
    orb_alien_resist_d = 30135
    orb_alien_resist_c = 30136
    orb_alien_resist_b = 30137
    orb_alien_resist_a = 30138
    orb_alien_resist_s = 30139

    orb_zombie_strong_d = 30140
    orb_zombie_strong_c = 30141
    orb_zombie_strong_b = 30142
    orb_zombie_strong_a = 30143
    orb_zombie_strong_s = 30144
    orb_zombie_massive_d = 30145
    orb_zombie_massive_c = 30146
    orb_zombie_massive_b = 30147
    orb_zombie_massive_a = 30148
    orb_zombie_massive_s = 30149
    orb_zombie_resist_d = 30150
    orb_zombie_resist_c = 30151
    orb_zombie_resist_b = 30152
    orb_zombie_resist_a = 30153
    orb_zombie_resist_s = 30154

    orb_aku_atk_d = 30155
    orb_aku_atk_c = 30156
    orb_aku_atk_b = 30157
    orb_aku_atk_a = 30158
    orb_aku_atk_s = 30159
    orb_aku_def_d = 30160
    orb_aku_def_c = 30161
    orb_aku_def_b = 30162
    orb_aku_def_a = 30163
    orb_aku_def_s = 30164
    orb_aku_strong_d = 30165
    orb_aku_strong_c = 30166
    orb_aku_strong_b = 30167
    orb_aku_strong_a = 30168
    orb_aku_strong_s = 30169
    orb_aku_massive_d = 30170
    orb_aku_massive_c = 30171
    orb_aku_massive_b = 30172
    orb_aku_massive_a = 30173
    orb_aku_massive_s = 30174
    orb_aku_resist_d = 30175
    orb_aku_resist_c = 30176
    orb_aku_resist_b = 30177
    orb_aku_resist_a = 30178
    orb_aku_resist_s = 30179

    #I think these are relic
    orb_relic_atk_d = 30180
    orb_relic_atk_c = 30181
    orb_relic_atk_b = 30182
    orb_relic_atk_a = 30183
    orb_relic_atk_s = 30184
    orb_relic_def_d = 30185
    orb_relic_def_c = 30186
    orb_relic_def_b = 30187
    orb_relic_def_a = 30188
    orb_relic_def_s = 30189
    orb_relic_strong_d = 30190
    orb_relic_strong_c = 30191
    orb_relic_strong_b = 30192
    orb_relic_strong_a = 30193
    orb_relic_strong_s = 30194
    orb_relic_massive_d = 30195
    orb_relic_massive_c = 30196
    orb_relic_massive_b = 30197
    orb_relic_massive_a = 30198
    orb_relic_massive_s = 30199
    orb_relic_resist_d = 30200
    orb_relic_resist_c = 30201
    orb_relic_resist_b = 30202
    orb_relic_resist_a = 30203
    orb_relic_resist_s = 30204

    #ability orbs
    orb_death_surge_d = 30205
    orb_death_surge_c = 30206
    orb_death_surge_b = 30207
    orb_death_surge_a = 30208
    orb_death_surge_s = 30209

    orb_resist_wave_d = 30210
    orb_resist_wave_c = 30211
    orb_resist_wave_b = 30212
    orb_resist_wave_a = 30213
    orb_resist_wave_s = 30214
    orb_cash_back_d = 30215
    orb_cash_back_c = 30216
    orb_cash_back_b = 30217
    orb_cash_back_a = 30218
    orb_cash_back_s = 30219

    orb_resist_knockback_d = 30220
    orb_resist_knockback_c = 30221
    orb_resist_knockback_b = 30222
    orb_resist_knockback_a = 30223
    orb_resist_knockback_s = 30224
    orb_sol_boost_d = 30225
    orb_sol_boost_c = 30226
    orb_sol_boost_b = 30227
    orb_sol_boost_a = 30228
    orb_sol_boost_s = 30229

    orb_colossus_slayer_d = 30230
    orb_colossus_slayer_c = 30231
    orb_colossus_slayer_b = 30232
    orb_colossus_slayer_a = 30233
    orb_colossus_slayer_s = 30234
    orb_cannon_recharge_d = 30235
    orb_cannon_recharge_c = 30236
    orb_cannon_recharge_b = 30237
    orb_cannon_recharge_a = 30238
    orb_cannon_recharge_s = 30239

    orb_resist_toxic_d = 30240
    orb_resist_toxic_c = 30241
    orb_resist_toxic_b = 30242
    orb_resist_toxic_a = 30243
    orb_resist_toxic_s = 30244
    orb_dodge_attack_d = 30245
    orb_dodge_attack_c = 30246
    orb_dodge_attack_b = 30247
    orb_dodge_attack_a = 30248
    orb_dodge_attack_s = 30249

    orb_resist_slow_d = 30250
    orb_resist_slow_c = 30251
    orb_resist_slow_b = 30252
    orb_resist_slow_a = 30253
    orb_resist_slow_s = 30254
    orb_resist_curse_d = 30255
    orb_resist_curse_c = 30256
    orb_resist_curse_b = 30257
    orb_resist_curse_a = 30258
    orb_resist_curse_s = 30259

    orb_ul_boost_d = 30260
    orb_ul_boost_c = 30261
    orb_ul_boost_b = 30262
    orb_ul_boost_a = 30263
    orb_ul_boost_s = 30264
    orb_counter_surge_d = 30265
    orb_counter_surge_c = 30266
    orb_counter_surge_b = 30267
    orb_counter_surge_a = 30268
    orb_counter_surge_s = 30269

    orb_berserker_d = 30270
    orb_berserker_c = 30271
    orb_berserker_b = 30272
    orb_berserker_a = 30273
    orb_berserker_s = 30274
    orb_shortened_cooldown_d = 30275
    orb_shortened_cooldown_c = 30276
    orb_shortened_cooldown_b = 30277
    orb_shortened_cooldown_a = 30278
    orb_shortened_cooldown_s = 30279

    orb_resist_freeze_d = 30280
    orb_resist_freeze_c = 30281
    orb_resist_freeze_b = 30282
    orb_resist_freeze_a = 30283
    orb_resist_freeze_s = 30284
    orb_resist_weaken_d = 30285
    orb_resist_weaken_c = 30286
    orb_resist_weaken_b = 30287
    orb_resist_weaken_a = 30288
    orb_resist_weaken_s = 30289

    orb_cost_down_d = 30290
    orb_cost_down_c = 30291
    orb_cost_down_b = 30292
    orb_cost_down_a = 30293
    orb_cost_down_s = 30294
    orb_resist_surge_d = 30295
    orb_resist_surge_c = 30296
    orb_resist_surge_b = 30297
    orb_resist_surge_a = 30298
    orb_resist_surge_s = 30299

    orb_bounty_up_d = 30300
    orb_bounty_up_c = 30301
    orb_bounty_up_b = 30302
    orb_bounty_up_a = 30303
    orb_bounty_up_s = 30304
    orb_resist_explosion_d = 30305
    orb_resist_explosion_c = 30306
    orb_resist_explosion_b = 30307
    orb_resist_explosion_a = 30308
    orb_resist_explosion_s = 30309
    
    """
    orb__d = 30210
    orb__c = 30211
    orb__b = 30212
    orb__a = 30213
    orb__s = 30214
    orb__d = 30215
    orb__c = 30216
    orb__b = 30217
    orb__a = 30218
    orb__s = 30219
    """

class shop(IntEnum):
    shop_id_pos = 0
    item_id_pos = 1
    item_count_pos = 2
    price_pos = 3
    drawitemvalue_pos = 4
    category_pos = 5
    imgcut_pos = 6
    


