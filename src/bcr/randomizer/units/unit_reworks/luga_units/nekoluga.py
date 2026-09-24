"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c
import tadbcmc.core.simple_funcs as simp
import copy

#this seems relatively fine but needs testing
def nekoluga(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 34
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #nekoluga 
    for trait in c.t:
        unit[0][trait] = 1
    #due to the lack of death surge it will be a sentry with 350 range and 100% freeze for 45f and 20% kb (cooldown increased greatly)
    unit[0][c.s.attack_state] = 1
    unit[0][c.s.attack_count] = 1
    unit[0][c.s.kbs] = 1 #these two are needed to make sure it only gets kbed when its gonna die cause its buggy otherwise
    unit[0][c.s.boss_wave_immune] = 1

    unit[0][c.s.range] = 350
    unit[0][c.s.freeze_chance] = 100
    unit[0][c.s.freeze_duration] = 60
    unit[0][c.s.kb_chance] = 20
    unit[0][c.s.recharge] = 2000
    unit[0][c.s.area] = 1
    nekoluga_attack_rate = 300
    unit[0][c.s.spirit_summon] = 239 #summons sniper


    #extending the animation
    nekoluga_anim_name = simp.uinfo_to_anim(unit_id,enemy=False,form=0,file_end="maanim",anim_num=2)
    nekoluga_anim = gf.file_reader(nekoluga_anim_name,vanilla=True) #Im assuming its fine to pull the vanilla version of the animations since this is early on
    #Im just hardcoding this, by slapping the final line of the first block onto it again (ill change this once I actually making shit for editing animations)
    if nekoluga_anim != None:
        nekoluga_copy = copy.deepcopy(nekoluga_anim[6])
        nekoluga_copy[0] = nekoluga_attack_rate #give nekoluga an attack cycle of 300f
        nekoluga_anim.insert(7,nekoluga_copy)
        nekoluga_anim[3][0] = 4 #change the first block to having 4 lines
        gf.file_writer(nekoluga_anim_name,nekoluga_anim)
    else:
        #if it cant edit the animation time due to lack of files it just gives a really bad freeze and lower kb
        unit[0][c.s.kb_chance] = 5
        unit[0][c.s.freeze_chance] = 30
        unit[0][c.s.freeze_duration] = 20 #has a 16f cycle

    return stats












