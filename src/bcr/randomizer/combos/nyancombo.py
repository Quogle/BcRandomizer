import tadbcmc.core.game_files as gf
import tadbcmc.core.seeded_randomization as srand
import tadbcmc.data.enums.nyancombo as nc
import tadbcmc.pieces.combos as combos
from ...config.defaults import DEFAULT_CONFIG
from tadbcmc.data.collated_info.unit_info import*
set_UNIT_INFO_unlogged()
import tadbcmc.data.enums.unit_info as ui
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.unitbuy as ub
import copy

ABNORMAL_EFFECTS = [nc.effect.worker_efficiency,nc.effect.immune_to_waves,nc.effect.deploy_cost_down]
NO_DOWN_EFFECTS = [] #Ill have to document this
KILLER_EFFECTS = [nc.effect.witch_killer,nc.effect.eva_killer,nc.effect.kaijin_slayer]
ACTIVATED_EFFECTS = [nc.effect.kaijin_slayer,nc.effect.immune_to_waves]


def do_combos(config=DEFAULT_CONFIG):
    """ does all the combo randomization stuff from config """
    #randomize needs to run first and it just needs config passed to it anyways
    _randomize_combos(config=config)
    #now edit param
    _edit_params(config=config)
    #dunno what Im doing with this currently
    #now do down combos
    _all_down_central(config=config)



def _randomize_combos(config=DEFAULT_CONFIG):
    """ randomizes vanilla combos according to the config
    \n wipes existing combos in the process so must be done before down/modded combos """
    #start by getting needed info from the config
    do_anything = config["catcombo"]["randomize"]["enabled"]
    if not do_anything:
        return #no sense in it
    (max_number_effects,rando_units,rando_sizes,rando_effects,abnormal_effects,max_ubler_count,blacklist_collab,blacklist_limited_event,keep_unit_count,count_weight_array,mult_weight_array) = _interpret_config_for_randomize_combos(config)
    #get the vanilla combos first and then rewipe them
    (vcombo_data,vcombo_names) = combos.readd_all_visible_vanilla_combos()
    combos.wipe_all_combos()
    unit_info = _get_combo_unit_info(include_collabs=(not blacklist_collab),include_limited_events=(not blacklist_limited_event))
    #start by getting the list of all allowed and allowed non uber/lr units
    allowed_non_uber_lr = []
    allowed_all = []
    allowed_uber = []
    for u_id in range(0,len(unit_info)):
        if unit_info[u_id][0]: #if its allowed
            allowed_all.append(u_id)
            if not unit_info[u_id][0]: #if its not an uber/lr
                allowed_non_uber_lr.append(u_id)
            else:
                allowed_uber.append(u_id)
    #now get the allowed combo effects
    #start by getting allowed/not effects
    allowed_effects = []
    disallowed_effects = []
    for each in KILLER_EFFECTS:
        disallowed_effects.append(int(each))
    if not abnormal_effects:
        for each in ABNORMAL_EFFECTS:
            disallowed_effects.append(int(each))
    total_number_of_effects = 0
    for each in nc.effect:
        total_number_of_effects += 1
    for x in range(0,max_number_effects+1):
        #only do it if the effect really exists
        if x < total_number_of_effects and x not in disallowed_effects:
            allowed_effects.append(x)
    #now open vanilla cat stats THIS SHOULD NOT BE
    vstat = gf.get_cat_stats(vanilla=True)
    #now for each combo in vcombos run on self
    for combo_id in range(0,len(vcombo_data)):
        this_combo_data = vcombo_data[combo_id]
        this_combo_name = vcombo_names[combo_id]
        _randomize_this_combo(
            combo_data=this_combo_data,
            combo_name=this_combo_name,
            r_offset=407*combo_id,
            change_effects=rando_effects,
            change_level=rando_sizes,
            change_counts=(not keep_unit_count),
            change_units=rando_units,
            allowed_effects=allowed_effects,
            count_weights=count_weight_array,
            level_weights=mult_weight_array,
            allowed_all=allowed_all,
            allowed_no_uberlr=allowed_non_uber_lr,
            ubers=allowed_uber,
            max_uber_count=max_ubler_count,
            vanilla_cat_stats=vstat
        )

def _all_down_central(config=DEFAULT_CONFIG):
    """ the main function for controlling all unit down behavior """
    do_anything = config["catcombo"]["all_unit_down_combos"]["enabled"]
    if not do_anything:
        return
    include_abnormals = config["catcombo"]["all_unit_down_combos"]["include_abnormal_effects"]
    max_effect_number = config["catcombo"]["number_of_effects"]

    #for now and maybe ever theres only on form 1
    _all_unit_down_combos_on_form_1(max_effect_number,include_abnormals)

#THIS FUNCTION IS UNDONE
def _edit_params(config=DEFAULT_CONFIG):
    """ edits param to have the correct strength of down combos """
    base_strength = config["catcombo"]["strength_of_downs"]
    penalty_strength = config["catcombo"]["all_unit_down_combos"]["weaken_down_combos_by"]
    do_all_downs = config["catcombo"]["all_unit_down_combos"]["enabled"]
    param = gf.file_reader(fn.COMBO_PARAM)
    #do something here


    gf.file_writer(fn.COMBO_PARAM,param)


#THIS FUNCTION HAS AN EN SPECIFIC FILE NAME
def _all_unit_down_combos_on_form_1(max_effect_number,include_abnormal_effects):
    """ adds a down combo to all units on the first form """
    #first step is getting all allowed effects
    disallowed_effects = []
    for each in KILLER_EFFECTS:
        disallowed_effects.append(int(each))
    if not include_abnormal_effects:
        for each in ABNORMAL_EFFECTS:
            disallowed_effects.append(int(each))
    allowed_effects = []
    for x in range(0,max_effect_number+1):
        if x not in disallowed_effects:
            allowed_effects.append(x)
    #now add one for each unit
    vanilla_stats = gf.get_cat_stats(vanilla=True)
    for u_id in range(0,len(vanilla_stats)):
        #first step is getting the name
        this_name_file = gf.file_reader(fn.UNIT_EXPLANATION + str(u_id+1) + "_en.csv",vanilla=True,separator="|",force_numerical=False,do_first_line_check=False)
        if this_name_file != None:
            this_name = this_name_file[0][0]
        else:
            this_name = ""
        #now choose an ability
        r = srand.randinst(43+19*u_id)
        this_effect = allowed_effects[r.randrange(0,len(allowed_effects))]
        combos.add_combo(
            u1id=u_id,
            u1form=0,
            comboset=nc.set.Eoc1,
            effect=this_effect,
            level=nc.mult.down,
            name=this_name
        )





def _interpret_config_for_randomize_combos(config=DEFAULT_CONFIG):
    """ gets all the information from config, processes it and returns the tuple:
    \n(max_number_effects,rando_units,rando_sizes,rando_effects,abnormal_effects,max_ubler_count,blacklist_collab,blacklist_limited_event,keep_unit_count,count_weight_array,mult_weight_array)
    \n count weight array is 1D in order [1,2,3,4,5]
    \n mult weight array is 2D in order [1,2,3,4,5] with inner array order [sm,m,l,xl,down] """
    max_number_effects = config["catcombo"]["number_of_effects"]
    rando_units = config["catcombo"]["randomize"]["units"]
    rando_sizes = config["catcombo"]["randomize"]["size"]
    rando_effects = config["catcombo"]["randomize"]["effects"]
    abnormal_effects = config["catcombo"]["randomize"]["allowed_abnormal_effects"]
    max_ubler_count = config["catcombo"]["randomize"]["max_uber_count"]
    blacklist_collab =  config["catcombo"]["blacklist"]["collab"]
    #blacklist_version_exclusive = config["catcombo"]["blacklist"]["version_exclusive"] #also prolly shouldnt exist
    #blacklist_unobtainable = config["catcombo"]["blacklist"]["enabled"] #literally this just shouldnt exist
    blacklist_limited_event = config["catcombo"]["blacklist"]["limited_event"]
    keep_unit_count = config["catcombo"]["size"]["keep_unit_count"]
    count_weights_dict = config["catcombo"]["size"]["custom_count_weights"]
    mult_weights_dict = config["catcombo"]["size"]["custom_mult_weights"]
    #first process count weights into an array
    count_weight_array = []
    for x in range(1,6):
        count_weight_array.append(count_weights_dict[str(x)])
    #now process the mult weights 2d array
    order = ["sm","m","l","xl","down"]
    mult_weight_array = []
    for x in range(1,6):
        this_mult_array = []
        for y in range(0,len(order)):
            this_mult_array.append(mult_weights_dict[str(x)][order[y]])
        mult_weight_array.append(this_mult_array)
    #should be all good!
    return (max_number_effects,rando_units,rando_sizes,rando_effects,abnormal_effects,max_ubler_count,blacklist_collab,blacklist_limited_event,keep_unit_count,count_weight_array,mult_weight_array)

#THIS IS TECHNICALLY INCORRECT BECAUSE WHAT IS UNOBTAINABLE IS NOT YET ACCURATE DUE TO LACK OF FUNCTION SETTING SUMMONS/STATIONARIES EXCEPT BIRD
def _get_combo_unit_info(include_collabs=False,include_limited_events=False) -> list[bool,bool]:
    """ returns unit info array with bools [included,uber/lr] at each index """
    #first make the array of proper length
    unit_info = []
    vanilla_stats = gf.get_cat_stats(vanilla=True)
    for x in range(0,len(vanilla_stats)):
        unit_info.append([True,False])
    unitbuy = gf.file_reader(fn.UNITBUY_FILE,vanilla=True)
    #now go through and disable units and mark them as ubers
    for u_id in range(0,len(unit_info)):
        this_included = True
        is_uber_lr = False
        #first check uber/lr
        if unitbuy[u_id][ub.ub.rarity] > 3:
            is_uber_lr = True
        #now check if its restricted
        if UNIT_INFO[u_id][ui.c.unobtainable]:
            this_included = False
        #I dont actually have a flag for version exclusives in unit info that is simply in unit buy
        if unitbuy[u_id][ub.ub.available_in_game] < 0:
            this_included = False
        #collabs
        if not include_collabs and UNIT_INFO[u_id][ui.c.collab] > 0:
            this_included = False
        #limited events
        if not include_limited_events and UNIT_INFO[u_id][ui.c.limited_event] > 0:
            this_included = False

        #now we should be good to set those bools
        unit_info[u_id][0] = this_included
        unit_info[u_id][1] = is_uber_lr
    return unit_info

#THIS FUNCTION HAS AN INCORRECT METHOD FOR DETERMINING NUMBER OF FORMS A UNIT HAS
def _randomize_this_combo(combo_data:list,combo_name:str,r_offset:int,change_effects:bool,allowed_effects:list,change_counts,count_weights:list,change_level:bool,level_weights:list,change_units:bool,ubers:list,allowed_all:list,allowed_no_uberlr:list,max_uber_count:int,vanilla_cat_stats:list):
    """ randomizes the data of this combo according to the inputs and saves it with specified name """
    #first step is get this intended effect
    if change_effects:
        r = srand.randinst(r_offset)
        this_effect = allowed_effects[r.randrange(0,len(allowed_effects))]
    else:
        this_effect = combo_data[nc.pos.effect_pos]
    #now handle the number of units a combo should have
    if change_counts:
        r = srand.randinst(r_offset+100)
        this_number_of_units = 1+r.weighted_list(count_weights)
    else:
        this_number_of_units = 0
        for x in range(0,5):
            if combo_data[nc.pos.u1_id+2*x] != -1: #if unit id is not -1 count it
                this_number_of_units += 1
    if this_number_of_units == 0:
        this_number_of_units = 2 #if either method fails for some reason default to a 2 unit combo
    #now get the size/level of the combo based on the number of units
    if change_level:
        r = srand.randinst(r_offset + 200)
        new_level = r.weighted_list(level_weights[this_number_of_units-1])
    else:
        new_level = combo_data[nc.pos.level]
    #fix it for if its an activated type effect
    for each in ACTIVATED_EFFECTS:
        if int(each) == this_effect:
            new_level = nc.mult.activated
    #now we can start the process of adding units to the combo
    #start by creating the [id,form] array
    combo_units = []
    for x in range(0,this_number_of_units):
        combo_units.append([])
    if not change_units:
        for x in range(0,5):
            if x < len(combo_units): #you can only keep what the number of units allows
                this_unit_id = combo_data[nc.pos.u1_id+2*x]
                this_unit_form = combo_data[nc.pos.u1_form+2*x]
                if this_unit_id != -1: #so if theres actually a unit here
                    combo_units[x] = [this_unit_id,this_unit_form]
    #now we can fill out all the remaining units in the array!
    current_position = 0
    while current_position < len(combo_units):
        if combo_units[current_position] != []:
            current_position += 1
        else:
            #start by counting how many ubers have been used so far
            cur_uber_count = 0
            for x in range(0,current_position):
                if combo_units[x][0] in ubers:
                    cur_uber_count += 1
            #use that to determine what array to use
            if cur_uber_count < max_uber_count:
                available_units = copy.deepcopy(allowed_all)
            else:
                available_units = copy.deepcopy(allowed_no_uberlr)
            #now remove all currently used units from that list
            for x in range(0,current_position):
                if combo_units[x][0] in available_units:
                    available_units.remove(combo_units[x][0])
            #now we are free to choose
            r = srand.randinst(r_offset+12+14*current_position)
            new_unit = available_units[r.randrange(0,len(available_units))]
            #now we get the form to use
            #THIS IS BAD I SHOULD HAVE A DIFFERENT METHOD FOR DOING THIS
            new_form = r.randrange(0,len(vanilla_cat_stats[new_unit]))
            combo_units[current_position] = [new_unit,new_form]
    #now we are good to set the combo as such
    #now just loop through setting the units and forms
    for x in range(0,5):
        if x < len(combo_units):
            combo_data[nc.pos.u1_id+2*x] = combo_units[x][0]
            combo_data[nc.pos.u1_form+2*x] = combo_units[x][1]
        else:
            combo_data[nc.pos.u1_id+2*x] = -1
            combo_data[nc.pos.u1_form+2*x] = -1
    #we are all good to save this
    combos.add_combo(
        comboset=combo_data[nc.pos.combo_set],
        effect=this_effect,
        level=new_level,
        name=combo_name,
        u1id=combo_data[nc.pos.u1_id],
        u1form=combo_data[nc.pos.u1_form],
        u2id=combo_data[nc.pos.u2_id],
        u2form=combo_data[nc.pos.u2_form],
        u3id=combo_data[nc.pos.u3_id],
        u3form=combo_data[nc.pos.u3_form],
        u4id=combo_data[nc.pos.u4_id],
        u4form=combo_data[nc.pos.u4_form],
        u5id=combo_data[nc.pos.u5_id],
        u5form=combo_data[nc.pos.u5_form],
        ) #lmao so uggy






