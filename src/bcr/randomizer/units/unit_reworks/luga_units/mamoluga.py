"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c
import tadbcmc.core.simple_funcs as simp
import copy


def mamoluga(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 781
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #mamoluga
    for trait in c.t:
        unit[0][trait] = 1
    #still a sentry with more or less the same stats
    #honestly I think these are pretty much the intended stats
    unit[0][c.s.attack_state] = 1
    unit[0][c.s.attack_count] = 1
    unit[0][c.s.kbs] = 1 #these two are needed to make sure it only gets kbed when its gonna die cause its buggy otherwise
    unit[0][c.s.boss_wave_immune] = 1

    unit[0][c.s.area] = 1
    mamoluga_attack_rate = 320
    unit[0][c.s.weaken_duration] = 160
    unit[0][c.s.weaken_chance] = 100
    unit[0][c.s.weaken_to] = 25
    unit[0][c.s.range] = 800
    unit[0][c.s.recharge] = 2000
    unit[0][c.s.spirit_summon] = 237 #summons cat jobs



    #editing the post attack anim time
    mamoluga_anim_name = simp.uinfo_to_anim(mamoluga,enemy=False,form=0,file_end="maanim",anim_num=2)
    mamoluga_anim = gf.file_reader(mamoluga_anim_name,vanilla=True)#Im assuming its fine to pull the vanilla version of the animations since this is early on
    if mamoluga_anim != None:
        mamoluga_copy = copy.deepcopy(mamoluga_anim[6])
        mamoluga_copy[0] = mamoluga_attack_rate #give mamoluga an attack cycle of 400f
        mamoluga_anim.insert(7,mamoluga_copy)
        mamoluga_anim[3][0] = 4 #change the first block to having 4 lines
        gf.file_writer(mamoluga_anim_name,mamoluga_anim)
    else:
        #if it cant edit the post attack anim its just gonna have to give it a really shitty weaken
        unit[0][c.s.weaken_to] = 50
        unit[0][c.s.weaken_duration] = 15 #has a cycle of 22f


    return stats












