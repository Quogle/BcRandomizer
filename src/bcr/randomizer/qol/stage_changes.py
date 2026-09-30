
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.core.stnmp as stnmp
from ...config.defaults import DEFAULT_CONFIG
import tadbcmc.pieces.units as units
import tadbcmc.data.enums.unitbuy as ub
import tadbcmc.data.enums.stage_conditions as stage_conditions
import tadbcmc.pieces.stages as stages


"""config options to be added here:
weekday specials
weekend_lils
xp stage item farming? - idk if this should be here
seasonals in sol
collabs in sol/advents




"""





#This is still missing any changes I want to make to their spawn locations and how they are obtained
def _seasonals_in_sol(config=DEFAULT_CONFIG):
    """ adds seasonals as drops to certain stages in sol
    \n also adds their true forms in various ways """
    if not config["qol"]["stage_changes"]["seasonals_in_sol"]:
        return  #not a light of reason in any star in the sky

    #for each of them Im going to specify unit id, chapter, stage for both main drop and tf drop
    unit_drops = []
    tf_drops = []

    #sportsday 63
    unit_drops.append([63,24,7]) #sportsday in winning back
    tf_drops.append([63,35,0]) #rampage tf in greeter at the gates
    #salaryman 70
    unit_drops.append([70,17,1]) #salaryman in prison sentence
    tf_drops.append([70,33,1]) #ritual tf in swap of sacrifice
    #reindeer 74
    unit_drops.append([74,7,7]) #reindeer in frontier spirit
    tf_drops.append([74,12,7]) #xmas pudding tf in shrimp frontier
    #adult 79
    unit_drops.append([79,39,2]) #unit in drunked backrub (there really isnt an early stage to give it from)
    tf_drops.append([79,8,4]) #tf in juvenile killer (maybe 18 2 prison destruction)
    #gentlemen bros 80
    unit_drops.append([80,5,2]) #evil in wanted night (maybe 8 2 mural of the devil)
    tf_drops.append([80,18,4]) #gentlemen tf in liars fate (actually wanted to make this an extra stage)
    #doll 81
    unit_drops.append([81,4,4]) #doll in twin peaks
    tf_drops.append([81,28,4]) #doll tf in darkweb
    #maiden 100
    unit_drops.append([100,14,4]) #maiden in gates of aphrodite
    tf_drops.append([100,28,0]) #maiden tf in renewed conflict (maybe 29 1 overachiever central)
    #koi 104
    unit_drops.append([104,3,6]) #koi in seaweed shallows
    tf_drops.append([104,39,0]) #koi tf in narrow docks
    #madam bride 109
    unit_drops.append([109,21,0]) #madam bride in the red carpet (maybe 20 3 pitfalls of life)
    tf_drops.append([109,43,5]) #madam bride tf in heavens oasis (maybe 43 4 electro safari or some other savannah stage)
    #vacation queen 122
    unit_drops.append([122,15,3]) #vacation queen in apple bobbing ocean
    tf_drops.append([122,40,1]) #call center tf in dial up dreams
    #bomber 127
    tf_drops.append([127,32,5]) #bomber tf in the spy who pet me, maybe this should be moved to a later razor stage
    #vengeful 128
    unit_drops.append([128,28,3]) #vengeful in thorny dialogue (maybe 23 3 trap of cowards)
    tf_drops.append([128,37,1]) #kite tf in seabreeze salon (maybe 47 1 thirst for vengeance)
    #kungfux 132
    unit_drops.append([132,23,1]) #kung fu in angry fighting
    tf_drops.append([132,26,2]) #kung fu tf in warriors dawn
    #marshmallow 176
    unit_drops.append([176,22,0]) #marshmallow in feast of betrayal (maybe 8 7 chubby b goode)
    #gift of cats 224
    unit_drops.append([224,22,3]) #unit in broken mask
    #pumpcat 227
    unit_drops.append([227,35,5]) #pumpcat in the haunted 1ldk
    #awa odori 282
    unit_drops.append([282,40,4]) #awa odori in the holy exploit
    #delivery 303
    unit_drops.append([303,23,5]) #delivery in scent of gore fish
    #eggy 329
    unit_drops.append([329,29,5]) #eggy in lord of the abyss
    #slug 343
    unit_drops.append([343,27,0]) #slug cat in at least Im a cat
    #million dollar 635
    unit_drops.append([635,41,2]) #million dollar in gouache ghouls
    #schoolgirl lion 651
    unit_drops.append([651,0,7]) #schoolgirl lion in sleeping lion

    #now Im doing the nenekos here
    #neneko 131
    unit_drops.append([131,20,4]) #neneko in subtle curfew
    #witchy neneko 228
    unit_drops.append([228,35,1]) #witchy neneko in rickety coaster
    #summer neneko 276 
    unit_drops.append([276,37,2]) #summer neneko in deep sea dying
    #new years neneko 314
    unit_drops.append([314,27,3]) #new years neneko in beautiful finale
    #easter neneko 332
    unit_drops.append([332,35,4]) #easter neneko in seductive chicken room
    #valentine neneko 589
    unit_drops.append([589,43,0]) #valentine neneko in eat the weak


    for unit in unit_drops:
        this_map = stnmp.MapStageData(fn.SOL_MLETTER,unit[1])
        drop_info = units.get_unit_drop_info(unit[0],set=True)
        this_map.set_stage_drop_id(unit[2],1,drop_info[0])
        this_map.set_stage_drop_rate(unit[2],1,100)
        this_map.set_stage_drop_count(unit[2],1,1)
        this_map.submit()
    for unit in tf_drops:
        #these are all gonna be just uid +10001
        drop_id = unit[0] + 10001
        this_map = stnmp.MapStageData(fn.SOL_MLETTER,unit[1])
        this_map.set_stage_drop_id(unit[2],1,drop_id)
        this_map.set_stage_drop_rate(unit[2],1,100)
        this_map.set_stage_drop_count(unit[2],1,1)
        this_map.submit()

#THIS CANNOT BE FINISHED UNTIL MISSION CODE EXISTS
def _add_collabs_to_various_stages(config=DEFAULT_CONFIG):
    """ adds collab units to sol/events and their true forms as missions """
    #sol drop units
    merc = 121          #sol 3 7 salty is seawater      tf:clionel rev 1st stage
    healer = 120        #sol 17 0 sin and punishment    tf:hannya rev 1st stage
    titi = 191          #sol 5 4 wandering traveler     tf:perfect cyclone rev 1st stage
    mint = 184          #sol 1 0 nyandalucia            tf:NONE
    capsule = 28        #sol 27 1 knights of the round  tf:NONE
    punt = 26           #sol 18 3 king of freedom       tf:papuu rev 1st stage
    #group drops units
    lil_gau = 67        #u id 287 (golfer)              tf:queen bee rev 1st stage
    nono = 111          #u id 324 (zamboney)            tf:daboo rev 1st stage
    power_pro1 = 390    #u id 442 (vendor)              tf:
    power_pro2 = 391    #u id 442 (vendor)              tf:
    power_pro3 = 392    #u id 442 (vendor)              tf:
    kyubey = 293        #u id 507 (supercat)            tf:NONE
    madoka = 299        #u id 507 (supercat)            tf:puffer rev 1st stage
    tan = 565           #u id 382 (glass)               tf:
    dango = 566         #u id 382 (glass)               tf:
    yahiko = 751        #u id 531 (bear)                tf:NONE
    mola = 173          #u id 521 (medusa)              tf:okame rev 1st stage
    reaper = 68         #u id 553 (bakery)              tf:doremi rev 1st stage
    racism_cow = 65     #u id 78 (space)                tf:NONE
    #brainwashed will be done later

    #ids of things being attatched to
    golfer = 287
    zamboney = 324
    vendor = 442
    supercat = 207
    glass = 382
    bear = 531
    medusa = 521
    bakery = 553
    space = 78

    #first do the sol ones
    unit_drops = []
    unit_drops.append([healer,17,0]) #sin and punishment
    unit_drops.append([merc,3,7]) #salty is seawater
    unit_drops.append([titi,5,4]) #wandering traveler
    unit_drops.append([mint,1,0]) #nyandalucia? why is it here
    unit_drops.append([capsule,27,1]) #knights of the round
    unit_drops.append([punt,18,3]) #king of freedom
    #set to drop source in unitbuy and then set them
    unitbuy = gf.file_reader(fn.UNITBUY_FILE)
    for unit in unit_drops:
        unitbuy[unit[0]][ub.ub.unlock_type] = 0
        drop_info = units.get_unit_drop_info(unit[0],set=True)
        this_map = stnmp.MapStageData(fn.SOL_MLETTER,unit[1])
        this_map.set_stage_drop_id(unit[2],1,drop_info[0])
        this_map.set_stage_drop_rate(unit[2],1,100)
        this_map.set_stage_drop_count(unit[2],1,1)
        this_map.submit()
    gf.file_writer(fn.UNITBUY_FILE,unitbuy)
    #now do the drop grouped ones
    unit_groups = [] #first is unit id second it what its attached to
    unit_groups.append([lil_gau,golfer])
    unit_groups.append([nono,zamboney])
    unit_groups.append([power_pro1,vendor])
    unit_groups.append([power_pro2,vendor])
    unit_groups.append([power_pro3,vendor])
    unit_groups.append([kyubey,supercat])
    unit_groups.append([madoka,supercat])
    unit_groups.append([tan,glass])
    unit_groups.append([dango,glass])
    unit_groups.append([yahiko,bear])
    unit_groups.append([mola,medusa])
    unit_groups.append([reaper,bakery])
    unit_groups.append([racism_cow,space])
    #now just set the save ids to that of the group
    for unit in unit_groups:
        to_info = units.get_unit_drop_info(unit[1])
        units.get_unit_drop_info(unit[0],set=True,save_id=to_info[1],use_invalid_drop_id=True)
    #I will do the true forms once I have mission code



def _nonview_catamin_unlocks(config=DEFAULT_CONFIG):
    """ makes it so catamins are unlocked not from viewing but from story progress """
    if not config["qol"]["stage_changes"]["nonview_catamin_unlocks"]:
        return
    manic_rework = config["qol"]["stage_changes"]["lil_brainwashed_catamins"]
    eoc1_unlocked = []
    eoc3_unlocked = []
    itf1_unlocked = []
    itf2_unlocked = []
    itf3_unlocked = []
    cotc1_unlocked = []
    cotc2_unlocked = []
    cotc3_unlocked = []
    unleashing_the_cats_unlocked = []
    sol_unlocked = []
    ccat_unlocked = []

    eoc1_viewable = [] #is there any reason for them to not be viewable after eoc1? I dont think it matters for any current catamins


    
    #ticket stages
    ticket1 = [7,6] #hmh and smh
    ticket2 = [5] #fd
    eoc3_unlocked.extend(ticket1)
    itf1_unlocked.extend(ticket2)
    eoc1_viewable.extend(ticket1+ticket2)
    #fruit stages
    fruit1 = [0,1,2,3,4] #og fruits
    fruit2 = [51] #aku fruit
    eoc1_viewable.extend(fruit1+fruit2)
    eoc3_unlocked.extend(fruit1)
    unleashing_the_cats_unlocked.extend(fruit2)
    #xp stages
    xp1 = [9,10,11] #xp stage, megablitz, colo
    xp2 = [8] #merciless xp
    xp3 = [50] #bonanza
    eoc1_viewable.extend(xp1+xp2+xp3)
    eoc3_unlocked.extend(xp1)
    itf3_unlocked.extend(xp2)
    unleashing_the_cats_unlocked.extend(xp3)
    #advents
    advents1 = [12,13,14,15,16,17] #clionel hannya bee daboo wahwah bakuu
    advents2 = [33] #puffer
    advents3 = [39] #kappy
    eoc1_viewable.extend(advents1+advents2+advents3)
    itf1_unlocked.extend(advents1)
    cotc2_unlocked.extend(advents2)
    itf2_unlocked.extend(advents3)
    #cmoneko
    cmoneko = [34]
    eoc1_viewable.extend(cmoneko)
    eoc3_unlocked.extend(cmoneko)
    #cyclone
    cyclone1 = [18,19,20,21,22,23,35,36,49] #red dark white angel metal alien perfect zombie supercosmic
    cyclone2 = [37] #relic
    cyclone3 = [38]
    eoc1_viewable.extend(cyclone1+cyclone2+cyclone3)
    eoc1_unlocked.extend(cyclone1)
    sol_unlocked.extend(cyclone2)
    eoc3_unlocked.extend(cyclone3)
    #crazed cats
    ccats = [24,25,26,27,28,29,30,31,32]
    eoc1_viewable.extend(ccats)
    eoc1_unlocked.extend(ccats)
    #manic
    mcats = [40,41,42,43,44,45,46,47,48]
    eoc1_viewable.extend(mcats)
    if not manic_rework:
        ccat_unlocked.extend(mcats)
    else: #so these are lils
        eoc3_unlocked.extend(mcats)
    #now we must set all these conditions
    conditions = [
        [eoc1_unlocked,stage_conditions.ID.clear_eoc1],
        [eoc3_unlocked,stage_conditions.ID.clear_eoc2],
        [itf1_unlocked,stage_conditions.ID.clear_itf1],
        [itf2_unlocked,stage_conditions.ID.clear_itf2],
        [itf3_unlocked,stage_conditions.ID.clear_itf3],
        [cotc1_unlocked,stage_conditions.ID.clear_cotc1],
        [cotc2_unlocked,stage_conditions.ID.clear_cotc2],
        [cotc3_unlocked,stage_conditions.ID.clear_cotc3],
        [unleashing_the_cats_unlocked,stage_conditions.ID.unleashing_the_cats_cleared],
        [sol_unlocked,stage_conditions.ID.clear_sol],
        [ccat_unlocked,stage_conditions.ID.all_crazed],
    ]
    for each in conditions:
        this_condition = each[1]
        for map_number in each[0]:
            this_map = stnmp.MapStageData(fn.CATAMIN_MLETTER,map_number)
            this_map.unlock_key = this_condition
            if map_number in eoc1_viewable:
                this_map.visible_key = stage_conditions.ID.clear_eoc1
            else:
                print("catamin map number not viewable after eoc 1: " + str(map_number))
            this_map.submit()


#this function requires serve files for moving maps
def _lil_brainwashed_catamins(config=DEFAULT_CONFIG):
    """ moves the manics to crazed maps and uses their maps for lils and brainwasheds """
    if not config["qol"]["stage_changes"]["lil_brainwashed_catamins"]:
        return
    #first get the map ids
    crazeds = [24,25,26,27,28,29,30,31,32] #catamin
    manics = [40,41,42,43,44,45,46,47,48] #catamin
    lils = [130,131,132,133,134,135,136,137,138] #events
    brainwasheds = [350,351,352,353,354,355,356,357,358] #events
    #first deal with the crazeds/manics
    for x in range(0,len(crazeds)):
        this_map = stnmp.MapStageData(fn.CATAMIN_MLETTER,crazeds[x])
        stnmp.copy_stage_onto_map(
            this_map,
            sletter=fn.CATAMIN_SLETTER,
            mnumber=manics[x],
            snumber=0,
            vanilla=True,
            new_snumber=1,
            save_stage=True
        )
        this_map.submit()
        #now make it unplayable until all crazed beaten, does this not work because catamins dont activate it?
        stages.restrict_stage_behind_condition(fn.CATAMIN_MLETTER,crazeds[x],1,stage_conditions.ID.all_crazed)
    #now copy lil maps into the manic map positions and slap brainwashed restricted on them
    for x in range(0,len(crazeds)):
        this_map = stnmp.MapStageData(fn.EVENT_STAGE_MLETTER,lils[x])
        this_map.update_save_info(fn.CATAMIN_MLETTER,manics[x])
        stnmp.copy_stage_onto_map(
            this_map,
            sletter=fn.EVENT_STAGE_SLETTER,
            mnumber=brainwasheds[x],
            snumber=0,
            vanilla=True,
            new_snumber=1,
            save_stage=True
        )
        this_map.submit()
        #now make it playable after mount aku?
        stages.restrict_stage_behind_condition(fn.CATAMIN_MLETTER,manics[x],1,stage_conditions.ID.mount_aku)








