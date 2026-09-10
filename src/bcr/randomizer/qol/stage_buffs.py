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













