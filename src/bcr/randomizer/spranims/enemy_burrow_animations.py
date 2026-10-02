""" creates a burrow animation for every now burrowing unit without burrow animations
\n if needing to make anim for a specific unit,
\n\t call _make_burrow_anims_for_unit() """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.core.simple_funcs as simp
import tadbcmc.data.enums.enemy as e
import tadbcmc.core.file_handler as fh
import copy




def make_burrow_anims():
    """ makes burrow animations, needs server files to work well
    \n nonconditional, shouldnt be run if not changing traits and animations not extracted """
    units_needing_burrow = _get_unit_ids_of_new_burrowers()
    for each in units_needing_burrow:
        _make_burrow_anims_for_unit(each)










def _get_unit_ids_of_new_burrowers() -> list[int]:
    """ gets a list with the unit id of everything with a burrow but no burrow anim
    \n means it requires server files but it should already """
    cur_stats = gf.file_reader(fn.ENEMY_STATS)
    new_burrowers = []
    for u_id in range(0,len(cur_stats)):
        #Ive decided to check if the burrow file exists or not to make it so if I add enemies past the length of vanilla stats in the future I can give them actually burrow animations should I so choose
        if cur_stats[u_id][e.s.burrow] != 0:
            #now check if theres a file with this units burrow animation name anywhere
            burrow_anim = simp.uinfo_to_anim(id=u_id,enemy=True,file_end="maanim",anim_num=11) #technically 10 11 or 12 would all work since theres no reason for any unit to have one but not the other
            filepath = fh.file_search(burrow_anim,debug=False)
            if filepath == None:
                new_burrowers.append(u_id)
    return new_burrowers

def _make_burrow_anims_for_unit(unit_id:int) -> None:
    """ makes all three burrow anims for the given unit
    \n makes them even if it cant access the idle animation
    \n could result in messed up animations if no server files """
    #file names
    down_anim_name = simp.uinfo_to_anim(unit_id,enemy=True,file_end="maanim",anim_num=10)
    walk_anim_name = simp.uinfo_to_anim(unit_id,enemy=True,file_end="maanim",anim_num=11)
    up_anim_name = simp.uinfo_to_anim(unit_id,enemy=True,file_end="maanim",anim_num=12)
    idle_anim_name = simp.uinfo_to_anim(unit_id,enemy=True,file_end="maanim",anim_num=1)
    #get da file
    idle_anim = gf.file_reader(idle_anim_name)
    if idle_anim == None:
        down_anim = []
        up_anim = []
    else:
        down_anim = copy.deepcopy(idle_anim)
        up_anim = copy.deepcopy(idle_anim)
    #for down and up just slap a fade on the end
    base_fade = [
        [0,12,-1,0,0,"fade"],
        [2],
        [0,0,0,0,"start"],
        [30,0,0,0,"end"],
    ]
    down_fade = copy.deepcopy(base_fade)
    up_fade = copy.deepcopy(base_fade)
    down_fade[2][1] = 1000
    up_fade[3][1] = 1000
    down_anim.extend(down_fade)
    up_anim.extend(up_fade)
    #walk is always just invisible
    walk_anim = [
        [1],
        [1],
        [0,12,-1,0,0,"invisible"],
        [1],
        [0,0,0,0,"empty"],
    ]
    #now save them all
    gf.file_writer(down_anim_name,down_anim)
    gf.file_writer(up_anim_name,up_anim)
    gf.file_writer(walk_anim_name,walk_anim)















