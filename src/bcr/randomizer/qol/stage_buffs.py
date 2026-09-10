from ...config.defaults import DEFAULT_CONFIG
import tadbcmc.pieces.qol as qol
import tadbcmc.data.enums.item as item



def _behemoth_stage_buffs(config=DEFAULT_CONFIG):
    """ buffs behemoth culling and enigma according to config """
    do_culling = config["qol"]["drop_buffs"]["behemoth_cube_buff"]
    #there actually only seems to be one option for both of them
    if do_culling:
        qol.behemoth_culling_buff() #just gonna use the default for em
        qol.behemoth_enigma_buff()

#missing a config option for xp bonanza
def _xp_stage_buffs(config=DEFAULT_CONFIG):
    """ buffs all the xp stages requested by config """
    #get all the bools from config
    sol_xp = config["qol"]["drop_buffs"]["sol_xp_buff"]
    weekend_stage = config["qol"]["drop_buffs"]["weekend_stage_buff"]
    megablitz = config["qol"]["drop_buffs"]["megablitz_buff"]
    colo = config["qol"]["drop_buffs"]["colosseum_buff"]
    merciless = config["qol"]["drop_buffs"]["merciless_xp_buff"]
    #bonanza = config["qol"]["drop_buffs"][""]
    if sol_xp: qol.xp_sol_buff(3,0.1)
    if weekend_stage: qol.xp_weekend_buff(1.5)
    if megablitz: qol.xp_megablitz_buff(1.5)
    if colo: qol.xp_colo_buff(1.5)
    if merciless: qol.xp_merciless_buff(1.5)
    #if bonanza: qol.xp_bonanza_buff(1.5)

#unsure if this one does drop rates correcctly
def _ticket_stage_buffs(config=DEFAULT_CONFIG):
    """ buffs the ticket stages requested by config """
    hmh = config["qol"]["drop_buffs"]["hate_metal_hippoe_buff"]
    smh = config["qol"]["drop_buffs"]["siege_buff"]
    fmh = config["qol"]["drop_buffs"]["facing_danger_buff"]
    #face metal hippoe makes no sense lmao
    if hmh: qol.ticket_hate_metal_hippoe_buff([100,1])
    if smh: qol.ticket_siege_buff([50,2],[50,3],[100,1])
    if fmh and smh:
        qol.ticket_fd_buff([80,3,item.drop_id.cat_ticket],[100,1,item.drop_id.rare_ticket])
        qol.ticket_siege_fd_continue(50,50)
        qol.ticket_fd_self_continue(100,80)
    elif fmh:
        qol.ticket_fd_buff([30,4,item.drop_id.cat_ticket],[80,3,item.drop_id.cat_ticket],[100,1,item.drop_id.rare_ticket])

#this still needs to do something about the confusing config options for normal catfruit stages
def _fruit_stage_buffs(config=DEFAULT_CONFIG):
    """ buffs fruit stages according to config """
    #why are these two even split (Im going to pretend they arent because I dont think they should be)
    normal_stage_reaad = config["qol"]["stage_changes"]["buff_normal_catfruit_catamins"]
    config["qol"]["stage_changes"]["split_normal_catfruit_stages"]
    #need to figure out what Im doing for this one
    jubilee_epic = config["qol"]["stage_chances"]["jubilee_always_epic"]
    gstrange = config["qol"]["drop_buffs"]["gstrange_buff"]
    gaku = config["qol"]["drop_buffs"]["growing_aku_buff"]
    gepic = config["qol"]["drop_buffs"]["growing_epic_buff"]
    #is this all?
    if normal_stage_reaad: qol.readd_old_catfruit_stages()
    if jubilee_epic: qol.make_jubilee_always_epicfruit()
    if gstrange: qol.growing_strange_rework()
    if gaku: qol.growing_aku_buff()
    if gepic: qol.growing_epic_buff()

#this is missing both aku/relic in island and non trait ability orbs in island
def _orb_stage_buffs(config=DEFAULT_CONFIG):
    """ does the orb stage buffs from config """
    trait_abilities_in_island = config["qol"]["stage_changes"]["orb_stage_has_strong_massive_resist"]
    other_abilities_in_island = config["qol"]["stage_changes"]["orb_stage_has_ability_orb"]
    relic_aku_in_isle = config["qol"]["stage_changes"]["relic_aku_in_island"]
    buff_orbs = config["qol"]["drop_buffs"]["orb_stage_buff"]
    #do adding relic and aku first
    #I dont currently have the logic for that

    #now find out what the string is gonna be for orb stages
    stage1_string_non_ab = "1Dattack82,1Ddefense82,1Cattack15,1Cdefense15"
    stage1_string_ab = "1Dstrong1,1Dmassive1,1Dresist1"
    stage2_string_non_ab = "1Dattack151,1Ddefense151,1Cattack34,1Cdefense34,1Battack6,1Bdefense6"
    stage2_string_ab = "1Dstrong6,1Dmassive6,1Dresist6"
    stage3_string_non_ab = "1Dattack65,1Ddefense65,1Cattack22,1Cdefense22,1Battack7,1Bdefense7"
    stage3_string_ab = "1Dstrong4,1Dmassive4,1Dresist4"
    #hard overwrite for if buff
    if buff_orbs:
        stage1_string_non_ab = "2Dattack50,2Ddefense50,1Cattack50,1Cdefense50"
        stage2_string_non_ab = "3Dattack50,3Ddefense50,2Cattack50,2Cdefense50"
        stage3_string_non_ab = "2Battack50,2Bdefense50,1Aattack50,1Adefense50"
    if trait_abilities_in_island:
        stage1_string_ab = "1Dstrong50,1Dmassive50,1Dresist50"
        stage2_string_ab = "1Cstrong50,1Cmassive50,1Cresist50"
        stage3_string_ab = "1Bstrong50,1Bmassive50,1Bresist50"
    #ok now its good to do something
    qol.orb_island_drop_buff(stage1_line=(stage1_string_non_ab+stage1_string_ab),stage2_line=(stage2_string_non_ab+stage2_string_ab),stage3_line=(stage3_string_non_ab+stage3_string_ab))
    #I dont currently have the func for adding ability orbs to the metal stages





    qol.orb_island_drop_buff()

def _matt_stage_buffs(config=DEFAULT_CONFIG):
    """ buffs the material stages according to config """
    do_something = config["qol"]["drop_buffs"]["material_stage_buff"]
    if do_something:
        qol.material_stages_buff(3,5,9)







