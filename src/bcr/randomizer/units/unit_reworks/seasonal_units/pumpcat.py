"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c
import tadbcmc.core.simple_funcs as simp


def pumpcat(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 227
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #pumpcat, increased freeze, for note the attack cycle for pumpcat is 183f
    unit[1][c.s.freeze_chance] = 40 #was 20
    unit[1][c.s.freeze_duration] = 120 #was 60
    #tf
    unit[2][c.s.freeze_chance] = 60 #was 20
    unit[2][c.s.freeze_duration] = 140 #was 60



    #now do the first form changes
    pumpcat_anim_name = simp.uinfo_to_anim(unit_id,enemy=False,form=0,file_end="maanim",anim_num=2)
    #just hard code the animation data since it doesnt really need to pull from the og file
    pumpcat_anim = [
        ["[modelanim:animation]"],
        [1],
        [1],
        [2,12,1,0,0,"dies of cringe"],
        [2],
        [0,1000,0,0],
        [1,500,0,0],
    ]
    #now save it
    gf.file_writer(pumpcat_anim_name,pumpcat_anim)
    #now the stats
    unit[0][c.s.attack_state] = 2
    unit[0][c.s.attack_count] = 1
    unit[0][c.s.preatk] = 1
    unit[0][c.s.speed] = 18
    unit[0][c.s.range] = 50
    unit[0][c.s.attack] = 0

    return stats












