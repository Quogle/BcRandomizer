
import tadbcmc.core.stnmp as stnmp
import tadbcmc.core.game_files as gf
from ....randomizer import debug_output



def apply_app_swap_to_stages(app_swap,include_eoc=False,log=None,debug=False):
    """ applies the app swap to all vanilla stages and modded ones already in dl """
    #first step is getting all the stages
    all_stages = gf.get_names_of_all_stages(include_dl=True,include_eoc=include_eoc) #do I want it to apply to modded stages?
    #also get a dummy stage to pull stage variables from
    d = stnmp.stage()
    #now loop through all those stages
    debug_output.output_somewhere("applying swap to " + str(len(all_stages)) + " stages:",log=log)
    stages_done = 0
    stages_actively_edited = 0
    for stage_name in all_stages:     #this does not use stnmp because its slower and this should be as fast as possible
        stage_sche = gf.file_reader(stage_name)
        edited = False
        #number of starting lines check
        if stage_sche[1][0] > 2000: #this is checking stage length (otherwise itd be base id and there arent 2000 of those)
            number_starting_lines = 2
        else:
            number_starting_lines = 1
        #enemy base swapping
        if stage_sche[number_starting_lines-1][d.pos_animated_base] != 0:
            old_base = stage_sche[number_starting_lines-1][d.pos_animated_base]
            new_base = app_swap[old_base][0]
            stage_sche[number_starting_lines-1][d.pos_animated_base] = new_base
            #no need to set it to edited here since it will also trip below
        #now loop through each line from there till the end attempting to edit it
        for enemy_line_id in range(number_starting_lines,len(stage_sche)):
            #print(enemy_line_id)
            enemy_line = stage_sche[enemy_line_id]
            enemy_id = enemy_line[d.enemy_id]
            #check if real then, if enemy doesnt route to self (slightly faster than just checking if it routes to self)
            if enemy_id != 0 and enemy_id != app_swap[enemy_id][0]:
                edited = True
                enemy_line[d.enemy_id] = app_swap[enemy_id][0]
                if len(enemy_line) > d.magnification: #eoc sucks
                    new_mag = max(1,enemy_line[d.magnification]*app_swap[enemy_id][1]) #dont set things to 0 mag
                    enemy_line[d.magnification] = int(new_mag)
                else:
                    if debug:
                        debug_output.output_somewhere(f"stage {stage_name} didnt have magnification",log=log)
        if edited:
            gf.file_writer(stage_name,stage_sche)
            stages_actively_edited += 1
        elif debug:
            debug_output.output_somewhere(f"stage {stage_name} was left unedited",log=log)
        stages_done += 1
        if stages_done % 1000 == 0:
            debug_output.output_somewhere(str(stages_done) + " done being swapped",log=log)
    debug_output.output_somewhere(f"swap resulted in {stages_actively_edited} of {stages_done} being edited",log=log)





































