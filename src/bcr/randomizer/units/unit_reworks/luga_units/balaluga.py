"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c
import tadbcmc.core.simple_funcs as simp
import copy

#this is probably as good as its gonna get rn
def balaluga(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 171
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #balaluga
    for trait in c.t:
        unit[0][trait] = 1
    #make it sentry with correct freeze and no surge
    unit[0][c.s.attack_state] = 1
    unit[0][c.s.attack_count] = 1
    unit[0][c.s.kbs] = 1 #these two are needed to make sure it only gets kbed when its gonna die cause its buggy otherwise
    unit[0][c.s.boss_wave_immune] = 1

    #sentry stats
    unit[0][c.s.range] = 600
    unit[0][c.s.freeze_chance] = 100
    unit[0][c.s.freeze_duration] = 150
    unit[0][c.s.weaken_to] = 50
    unit[0][c.s.weaken_chance] = 100
    unit[0][c.s.weaken_duration] = 300
    unit[0][c.s.area] = 1 
    unit[0][c.s.recharge] = 2000 #honestly I think most of these stats are just its final stats, it really just deserves to get death surge added on aswell
    balaluga_attack_rate = 400
    unit[0][c.s.spirit_summon] = 120 #summons healer



    #editing the post attack animation time
    balaluga_anim_name = simp.uinfo_to_anim(balaluga,enemy=False,form=0,file_end="maanim",anim_num=2)
    balaluga_anim = gf.file_reader(balaluga_anim_name,vanilla=True)#Im assuming its fine to pull the vanilla version of the animations since this is early on
    if balaluga_anim != None:
        balaluga_copy = copy.deepcopy(balaluga_anim[13])
        balaluga_copy[0] = balaluga_attack_rate #give balaluga an attack cycle of 400f
        balaluga_anim.insert(14,balaluga_copy)
        balaluga_anim[3][0] = 11 #change the first block to having 11 lines
        gf.file_writer(balaluga_anim_name,balaluga_anim)
    else:
        #if it cant edit the animation due to a lack of animation files its gonna have to just have a really shitty freeze/weaken
        unit[0][c.s.weaken_duration] = 15 #it has 25f cycle
        unit[0][c.s.freeze_duration] = 9

    return stats
