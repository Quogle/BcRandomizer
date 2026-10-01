""" module for all cat combo randomizations
\n needs establish_working_information to be called after game files exist """
import tadbcmc.core.game_files as gf
import tadbcmc.core.seeded_randomization as srand
import tadbcmc.data.enums.nyancombo as nc
import tadbcmc.pieces.combos as combos
from ...config.defaults import DEFAULT_CONFIG
from tadbcmc.data.collated_info.unit_info import*
import tadbcmc.data.enums.unit_info as ui
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.unitbuy as ub
import copy
from ...config.version_config.get_version_config import DEFAULT_VC_CONFIG
from ...config.version_config import version_config_keys as vck

""" tadbcmc unit_info still needs to be done,
a means of determining how many combo ids are in the current version also needs to be figured out 
also param editing still isnt a thing """



def establish_working_information():
    """ to be called once the game files actually exist """
    UNIT_INFO_extend_w_defaults()



ABNORMAL_EFFECTS = [nc.effect.worker_efficiency,nc.effect.immune_to_waves,nc.effect.deploy_cost_down]
NO_DOWN_EFFECTS = [] #Ill have to document this
KILLER_EFFECTS = [nc.effect.witch_killer,nc.effect.eva_killer,nc.effect.kaijin_slayer]
ACTIVATED_EFFECTS = [
    int(nc.effect.kaijin_slayer),
    int(nc.effect.immune_to_waves),
]
MULTS = [
    int(nc.mult.sm),
    int(nc.mult.m),
    int(nc.mult.l),
    int(nc.mult.xl),
    int(nc.mult.down),
]





def do_combos(config=DEFAULT_CONFIG,version_config=DEFAULT_VC_CONFIG,log=None):
    """ does all the combo randomization stuff from config """
    #first, if either combo rand is on we should wipe invisible vanilla combos
    if config["catcombo"]["randomize"]["enabled"] or config["catcombo"]["all_unit_down_combos"]["enabled"]:
        combos.readd_all_visible_vanilla_combos()
    #randomize needs to run first and it just needs config passed to it anyways
    _do_rand_combos(config=config,version_config=version_config,log=log)
    #now edit param
    _edit_params(config=config)
    #dunno what Im doing with this currently
    #now do down combos
    _do_all_unit_down_combos(config=config,version_config=version_config,log=log)


#max post version combo effect id missing here
def _do_all_unit_down_combos(config=DEFAULT_CONFIG,version_config=DEFAULT_VC_CONFIG,log=None):
    """ makes the all unit down combos according to config
    \n does nothing if all unit down combos are off """
    if not config["catcombo"]["all_unit_down_combos"]["enabled"]:
        return
    include_abnormal_effects = config["catcombo"]["all_unit_down_combos"]
    max_preversion_effect_id = version_config[vck.all_unit_down_max_combo_id]
    max_preversion_unit_id = version_config[vck.all_unit_down_max_unit_id]



    _all_unit_down_combos(
        include_abnormal_effects=include_abnormal_effects,
        include_activate_effects=False, #do down combos even work with this?
        max_preversion_effect_id=max_preversion_effect_id,
        max_postversion_effect_id=0, #Ill deal with this later
        max_preversion_unit_id=max_preversion_unit_id,
        log=log,
    )


def _do_rand_combos(config=DEFAULT_CONFIG,version_config=DEFAULT_VC_CONFIG,log=None):
    """ randomizes all currently existing combos according to catcombo randomize in config
    \n does nothing if randomize is disabled """
    if not config["catcombo"]["randomize"]["enabled"]:
        return #no cash
    #now we get the config options
    (
        rand_units,rand_effects,rand_mult,
        include_collab,include_limited_event,include_abnormal_effects,
        max_ubler_count,keep_unit_count,
        count_weight_array,mult_weight_array,
    ) = _interpret_combo_config(config=config,log=log)


    _rand_combos(
        include_collabs=include_collab,include_limited_events=include_limited_event,include_abnormal_effects=include_abnormal_effects,
        rand_units=rand_units,rand_effects=rand_effects,rand_mult=rand_mult,rand_size=(not keep_unit_count),
        max_ubler_count=max_ubler_count,
        count_weights=count_weight_array,mult_weights=mult_weight_array,
        version_config=version_config,
    )





#THIS FUNCTION IS UNDONE
def _edit_params(config=DEFAULT_CONFIG):
    """ edits param to have the correct strength of down combos """
    base_strength = config["catcombo"]["strength_of_downs"]
    penalty_strength = config["catcombo"]["all_unit_down_combos"]["weaken_down_combos_by"]
    do_all_downs = config["catcombo"]["all_unit_down_combos"]["enabled"]
    param = gf.file_reader(fn.COMBO_PARAM)
    #do something here


    gf.file_writer(fn.COMBO_PARAM,param)











def _get_list_of_allowed_effects(
        include_abnormal_effects:bool,
        include_activated_effects:bool,
        max_preversion_effect_id:int,
        max_postversion_effect_id:int,
        ) -> tuple[list[int],list[int]]:
    """ return (preversion_ids,postversion_ids)
    \n gets a list of the available effects """
    #start by figuring out what effects are disallowed
    disallowed_effects = []
    for each in KILLER_EFFECTS:
        disallowed_effects.append(int(each))
    if not include_abnormal_effects:
        for each in ABNORMAL_EFFECTS:
            disallowed_effects.append(int(each))
    if not include_activated_effects:
        for each in ACTIVATED_EFFECTS:
            disallowed_effects.append(int(each))
    #now we just add each id to the max post version combo id if it isnt disallowed
    preversion_ids = []
    postversion_ids = []
    for x in range(0,max_postversion_effect_id+1):
        if x not in disallowed_effects:
            if x <= max_preversion_effect_id:
                preversion_ids.append(x)
            postversion_ids.append(x)
    #thats it
    return (preversion_ids,postversion_ids)


#This has an en specific filename
def _all_unit_down_combos(
        include_abnormal_effects:bool, # |
        include_activate_effects:bool, # |
        max_preversion_effect_id:int,  # |these four are used to get the lists of combo ids to use for preversion and postversion units
        max_postversion_effect_id:int, # |
        max_preversion_unit_id:int,
        log=None,
    ) -> None:
    #first step get the lists of combo ids and vanilla cat stats for determining how many units there are
    (preversion_ids,postversion_ids) = _get_list_of_allowed_effects(
        include_abnormal_effects=include_abnormal_effects,
        include_activated_effects=include_activate_effects,
        max_preversion_effect_id=max_preversion_effect_id,
        max_postversion_effect_id=max_postversion_effect_id
    )
    vanilla_cat_stats = gf.get_cat_stats(vanilla=True)
    (combo_data,combo_names) = _get_combo_files(log=log)
    #now we can literally just add one for each unit in the game
    for u_id in range(0,len(vanilla_cat_stats)):
        #first get the combo id
        r = srand.randinst(43+19*u_id)
        if u_id <= max_preversion_unit_id:
            index = r.randrange(0,len(preversion_ids))
            effect = preversion_ids[index]
        else:
            index = r.randrange(0,len(postversion_ids))
            effect = postversion_ids[index]
        #now get the name to use
        this_name_file = gf.file_reader(fn.UNIT_EXPLANATION + str(u_id+1) + "_en.csv",vanilla=True,separator="|",force_numerical=False,do_first_line_check=False)
        if this_name_file != None:
            this_name = this_name_file[0][0]
        else:
            this_name = ""
        #now we just set that information over a default combo
        this_combo = [-1]*16
        this_combo[nc.pos.effect_pos] = effect
        this_combo[nc.pos.combo_set] = nc.set.Eoc1
        this_combo[nc.pos.level] = nc.mult.down
        this_combo[nc.pos.u1_id] = u_id
        this_combo[nc.pos.u1_form] = 0
        #add it
        combo_data.append(this_combo)
        combo_names.append([this_name])
    #now save the files
    gf.file_writer(fn.COMBO_FILE,combo_data)
    gf.file_writer(fn.COMBO_NAME_DATA,combo_names)

def _get_combo_files(log=None) -> tuple[list,list]:
    """ return (combo_data,combo_names)
    \n gets the combo files and makes sure theyre the right length """
    combo_data = gf.file_reader(fn.COMBO_FILE)
    combo_names = gf.file_reader(fn.COMBO_NAME_DATA)
    #make sure the name file is the same length as the data file just incase something went wrong elsewhere
    error_to_output = None
    while len(combo_names) < len(combo_data):
        error_to_output = "combo names was smaller than data"
        combo_names.append([""])
    while len(combo_names) > len(combo_data):
        error_to_output = "combo names was larger than data"
        combo_names.pop()
    if error_to_output != None:
        if log != None:
            log(error_to_output)
        else:
            print(error_to_output)
    #ok all good to return them
    return (combo_data,combo_names)


#max post version combo effect id missing here
def _rand_combos(
        include_collabs:bool,
        include_limited_events:bool,
        include_abnormal_effects:bool,
        rand_units:bool,
        rand_effects:bool,
        rand_mult:bool,
        rand_size:bool,
        max_ubler_count:int,
        count_weights:list[int],
        mult_weights:list[list[int]],
        version_config=DEFAULT_VC_CONFIG,
        log=None,
    ) -> None:
    """  """
    #first initialize the needed information
    (combo_data,combo_names) = _get_combo_files(log=log)
    (included_unit_bools,ubler_bools,preversion_form_counts,postversion_form_counts) = _get_unit_info_for_combo_rand(include_collabs,include_limited_events,version_config)
    (preversion_ids,postversion_ids) = _get_list_of_allowed_effects(
        include_abnormal_effects=include_abnormal_effects,
        include_activated_effects=include_abnormal_effects, #these use the same bool
        max_preversion_effect_id=version_config[vck.combo_rand_max_combo_id],
        max_postversion_effect_id=0, #still working on this
    )
    preversion_combo_count = version_config[vck.combo_rand_combo_count]
    #now get the unit arrays
    (prev_av_all_units,prev_av_non_ublers,postv_av_all_units,postv_av_non_ublers) = _get_available_unit_array(included_unit_bools,ubler_bools,preversion_form_counts)

    #initialize the current working information here
    current_av_all_units = prev_av_all_units
    current_av_non_ublers = prev_av_non_ublers
    current_form_counts = preversion_form_counts
    current_av_combo_ids = preversion_ids

    for combo_id in range(0,len(combo_data)):
        #first is the swap
        if combo_id == preversion_combo_count + 1: #at this combo specifically, swap the current information 
            current_av_all_units = postv_av_all_units
            current_av_non_ublers = postv_av_non_ublers
            current_form_counts = postversion_form_counts
            current_av_combo_ids = postversion_ids
        #now randomize the combo
        new_combo_line = _rand_this_combo(
            combo_data=combo_data[combo_id],
            rand_units=rand_units,rand_effects=rand_effects,rand_mult=rand_mult,rand_size=rand_size,
            max_ubler_count=max_ubler_count,
            count_weights=count_weights,mult_weights=mult_weights,
            r_offset=141+407*combo_data[combo_id][nc.pos.id], #use the combos id to make it unaffected by any reordering that may happen
            available_effects=current_av_combo_ids,
            available_all_units=current_av_all_units,available_non_ubler_units=current_av_non_ublers,
            ubler_bools=ubler_bools,form_list=current_form_counts,
        )
        #just set it
        combo_data[combo_id] = new_combo_line
    #ok should be all good to save
    gf.file_writer(fn.COMBO_FILE,combo_data)
    #theres no reason to save the name file



def _rand_this_combo(
        combo_data:list[int],
        rand_units:bool,
        rand_effects:bool,
        rand_mult:bool,
        rand_size:bool,
        max_ubler_count:int,
        count_weights:list[int],
        mult_weights:list[list[int]],
        r_offset:int,
        available_effects:list[int],
        available_all_units:list[int],
        available_non_ubler_units:list[int],
        ubler_bools:list[bool],
        form_list:list[int],
    ) -> list[int]:
    """ randomizes this current combo
    \n all version control logic must be done before this function """
    #first step get the intended effect id
    if rand_effects:
        r = srand.randinst(r_offset)
        effect = available_effects[r.randrange(0,len(available_effects))]
    else:
        effect = combo_data[nc.pos.effect_pos]
    #now get the number of units the combo should have
    if rand_size:
        r = srand.randinst(r_offset+9)
        combo_unit_count = 1 + (r.weighted_list(count_weights))
        if combo_unit_count == 0: #this means weight list failed (I need to log this outside this func so it doesnt spam console 400 times)
            combo_unit_count = 2
    else:
        combo_unit_count = 0
        for x in range(0,5):
            if combo_data[nc.pos.u1_id+2*x] != -1:
                combo_unit_count += 1
    #now get the mult of the combo
    if rand_mult:
        r = srand.randinst(r_offset+27)
        mult_index = combo_unit_count-1
        new_mult_index = r.weighted_list(mult_weights[mult_index])
        mult = MULTS[new_mult_index]
        if new_mult_index == -1: #incase it failed somehow
            mult = combo_data[nc.pos.level]
    else:
        mult = combo_data[nc.pos.level]
    #now we can rand the units
    #start by reading the currently existing units
    current_units = []
    if not rand_units:
        for x in range(0,combo_unit_count): #dont read units past the amount the combo is supposed to have
            look_index = nc.pos.u1_id + 2*x
            if combo_data[look_index] != -1: #so if theres actually a unit
                current_units.append([combo_data[look_index:look_index+2]]) #add the array of unit id and form
    #now only do the process of adding more units if theres more to add
    if len(current_units) < combo_unit_count:
        #initialize the needed information
        all_units = copy.deepcopy(available_all_units)
        non_ublers = copy.deepcopy(available_non_ubler_units)
        current_uber_count = 0
        for existing_unit in current_units:
            if existing_unit[0] in all_units:
                all_units.remove(existing_unit[0])
            if existing_unit[0] in non_ublers:
                non_ublers.remove(existing_unit[0])
            if ubler_bools[existing_unit[0]]:
                current_uber_count += 1
        #now we can just add the number of units lower current unit is than it should be
        for x in range(len(current_units),combo_unit_count):
            r = srand.randinst(r_offset+40+x*23)
            #first choose a unit
            if current_uber_count < max_ubler_count:
                unit_id = all_units[r.randrange(0,len(all_units))]
                all_units.remove(unit_id)
                if unit_id in non_ublers:
                    non_ublers.remove(unit_id)
                #might as well do adding uber count here since it wont run for non ublers
                if ubler_bools[unit_id]:
                    current_uber_count += 1
            else:
                unit_id = non_ublers[r.randrange(0,len(non_ublers))]
                #its gonna be in both
                all_units.remove(unit_id)
                non_ublers.remove(unit_id)
            #now get the form
            form_id = r.randrange(0,form_list[unit_id]) #basic cat has a form list of 3 so this works
            current_units.append([unit_id,form_id])
    #now set the whole combo as this
    combo_data[nc.pos.effect_pos] = effect
    #specifically fix mult for activated effects
    if effect in ACTIVATED_EFFECTS:
        mult = int(nc.mult.activated)
    combo_data[nc.pos.level] = mult
    for x in range(0,5):
        if x < len(current_units):
            combo_data[nc.pos.u1_id+2*x] = current_units[x][0]
            combo_data[nc.pos.u1_id+2*x+1] = current_units[x][1]
        else:
            combo_data[nc.pos.u1_id+2*x] = -1
            combo_data[nc.pos.u1_id+2*x+1] = -1
    #should be all, it edits neither set, ending, nor that nyankorangers 10 value (which is honestly really funny)
    return combo_data

def _get_unit_info_for_combo_rand(
        include_collabs:bool,
        include_limited_event:bool,
        version_config=DEFAULT_VC_CONFIG,
    ) -> tuple[list[bool],list[bool],list[int]]:
    """ return (included_unit_bools,ubler_bools,preversion_form_counts,postversion_form_counts)
    \n gets included uber/lr and form counts for randomizing combos
    \n for note: basic cat has a form count of 3 """
    #first open up all the relevant information
    vanilla_cat_stats = gf.get_cat_stats(vanilla=True)
    nyankobook = gf.file_reader(fn.CAT_GUIDE_DATA,vanilla=True) #should this be vanilla? (for note the value for cat in this is at [0][2] and = 3)
    unitbuy = gf.file_reader(fn.UNIT_FILE,vanilla=True)
    #now make the default info arrays
    included_unit_bools = [True]*len(vanilla_cat_stats)
    ubler_bools = [False]*len(vanilla_cat_stats)
    preversion_form_counts = [0]*len(vanilla_cat_stats)
    postversion_form_counts = [0]*len(vanilla_cat_stats)
    #now go through each unit
    for u_id in range(0,len(vanilla_cat_stats)):
        #first handle uber/lr status
        if unitbuy[u_id][ub.ub.rarity] >= 4:
            ubler_bools[u_id] = True
        #now do forms, just dont include it in preversion if its outside the bounds of the array
        if u_id < len(version_config[vck.combo_rand_unit_forms]):
            preversion_form_counts[u_id] = version_config[vck.combo_rand_unit_forms][u_id]
        postversion_form_counts[u_id] = nyankobook[u_id][2]
        #now determine whether or not units are included
        include_this_unit = True
        #these should always be excluded
        if UNIT_INFO[u_id][ui.c.unobtainable] > 0:
            include_this_unit = False
        if unitbuy[ub.ub.available_in_game] < 0:
            include_this_unit = False
        #now the customizable ones
        if not include_collabs and UNIT_INFO[u_id][ui.c.collab] > 0:
            include_this_unit = False
        if not include_limited_event and UNIT_INFO[u_id][ui.c.limited_event] > 0:
            include_this_unit = False
        #set it
        included_unit_bools[u_id] = include_this_unit
    #return those arrays
    return (included_unit_bools,ubler_bools,preversion_form_counts,postversion_form_counts)

def _interpret_combo_config(config=DEFAULT_CONFIG,log=None):
    """ return (
            rand_units,rand_effects,rand_mult,
            include_collab,include_limited_event,include_abnormal_effects,
            max_ubler_count,keep_unit_count,
            count_weight_array,mult_weight_array,
        )
    \n count_weight_array is a 1D array with values for [1,2,3,4,5] units
    \n mult_weight_array is 2D array with values for [sm,m,l,xl,down] for [1,2,3,4,5] units """
    rand_units = config["catcombo"]["randomize"]["units"]
    rand_effects = config["catcombo"]["randomize"]["effects"]
    rand_mult = config["catcombo"]["randomize"]["mult"]
    include_abnormal_effects = config["catcombo"]["randomize"]["allowed_abnormal_effects"]
    include_collab =  not config["catcombo"]["blacklist"]["collab"]
    include_limited_event = not config["catcombo"]["blacklist"]["limited_event"]
    max_ubler_count = config["catcombo"]["randomize"]["max_uber_count"]
    keep_unit_count = config["catcombo"]["size"]["keep_unit_count"]
    count_weights_dict = config["catcombo"]["size"]["custom_count_weights"]
    mult_weights_dict = config["catcombo"]["size"]["custom_mult_weights"]
    #now we need to process the dicts
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
    #now make sure the arrays actually have real weights, if they dont mention it
    count_sum = 0
    for each in count_weight_array:
        count_sum += each
    if count_sum == 0 and not keep_unit_count: #we only care if unit counts are supposed to be changed
        if log != None:
            log("the weights of numbers of units summed to 0, all combos forced to 2 units")
        else:
            print("the weights of numbers of units summed to 0, all combos forced to 2 units")
    for mult_id in range(0,len(mult_weight_array)):
        mult_sum = 0
        for each in mult_weight_array[mult_id]:
            mult_sum += each
        if mult_sum == 0 and rand_mult: #only care if mults are supposed to be changed
            if log != None:
                log(str(mult_id+1) + " units weights summed to 0, combo strength will not be altered")
            else:
                print(str(mult_id+1) + " units weights summed to 0, combo strength will not be altered")
    #ok thats all

    return (
        rand_units,rand_effects,rand_mult,
        include_collab,include_limited_event,include_abnormal_effects,
        max_ubler_count,keep_unit_count,
        count_weight_array,mult_weight_array,
    )

def _get_available_unit_array(included_unit_bools,uberlr_bools,preversion_form_counts):
    """ return (prev_av_all_units,prev_av_non_ublers,postv_av_all_units,postv_av_non_ublers)
    \n gets the non ubers and all units, allowed in combos, for both preversion and postver """
    prev_av_all_units = []
    prev_av_non_ublers = []
    postv_av_all_units = []
    postv_av_non_ublers = []
    preversion_first_unavailable_u_id = len(preversion_form_counts)
    for u_id in range(0,len(included_unit_bools)):
        #do nothing if not included
        is_uber = uberlr_bools[u_id]
        if included_unit_bools[u_id]:
            if u_id < preversion_first_unavailable_u_id:
                if not is_uber: prev_av_non_ublers.append(u_id)
                prev_av_all_units.append(u_id)
            if not is_uber: postv_av_non_ublers.append(u_id)
            postv_av_all_units.append(u_id)
    return (prev_av_all_units,prev_av_non_ublers,postv_av_all_units,postv_av_non_ublers)






