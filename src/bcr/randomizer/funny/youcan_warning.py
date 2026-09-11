import tadbcmc.core.game_files as gf
import tadbcmc.core.stnmp as stnmp
import copy







#THIS IS MISSING THE ID OR A WAY TO GET IT FOR YOUCAN WARNING ENEMY
def add_youcan_warning():
    """ adds youcan warning enemy to all stages with a youcan
    \n doesnt consider config """
    youcan_id = 377 #its actually 375
    youcan_warning_id = 0 #dunno what Im doing with this yet
    d = stnmp.stage() #this is just used for its position info, I dont use stnmp for this since its slower and not needed
    #               enemy id          # of spawns  start/2  respawn min/2   respawn max/2   spawn hp%  zmin  zmax boss   mag
    warning_line = [youcan_warning_id,1,            0,      0,              0,              100,       0,    0,   1,     100] #does it matter if I dont continue this?
    #first get all stages
    all_stages = gf.get_names_of_all_stages(include_dl=True,include_modded=True,include_eoc=True)
    for stage_name in all_stages:
        youcan_in_stage = False
        this_stage = gf.file_reader(stage_name)
        #check how many first lines there are
        if this_stage[1][0] > 2000: #this is checking stage length
            number_starting_lines = 2
        else:
            number_starting_lines = 1
        for line in range(number_starting_lines,len(this_stage)):
            if this_stage[line][d.enemy_id] == youcan_id:
                youcan_in_stage = True
                break
        if youcan_in_stage:
            #copy the last line since it should always be blank, if it isnt it aint my problem
            this_stage.append(copy.deepcopy(this_stage[-1]))
            for x in range(0,len(warning_line)):
                this_stage[-1][x] = warning_line[x]
            gf.file_writer(stage_name,this_stage)
    















