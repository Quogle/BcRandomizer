"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c
import tadbcmc.core.simple_funcs as simp


def prisoner(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 79
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #prisoner, first and second form become 0tba faster animation fragile 435 ranged attackers, cooldown and speed increased 
    for x in range(0,2):
        unit[x][c.s.hp] = 50 #was 550
        unit[x][c.s.range] = 435 #was 120
        unit[x][c.s.tba] = 0 #was 60c
        unit[x][c.s.speed] = 12
        unit[x][c.s.preatk] = 16
        unit[x][c.s.recharge] = 440 #this seems a little high its a 20 second respawn
    #gonna choose to ignore what happens when the sprites arent included (theyre just mediocre af I guess)

    first_form_anim_name = simp.uinfo_to_anim(unit_id,enemy=False,form=0,file_end="maanim",anim_num=2)
    second_form_anim_name = simp.uinfo_to_anim(unit_id,enemy=False,form=1,file_end="maanim",anim_num=2)
    first_form_anim = gf.file_reader(first_form_anim_name,prefer_modded=True)
    second_form_anim = gf.file_reader(second_form_anim_name,prefer_modded=True)
    if first_form_anim != None:
        #just save it p sure
        gf.file_writer(first_form_anim_name,first_form_anim)
    if second_form_anim != None:
        gf.file_writer(second_form_anim_name,second_form_anim)


    return stats












