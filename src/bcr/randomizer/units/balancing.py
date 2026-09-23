""" module containing the various adjustments to make to cat stats at various stages in the randomization process
\nearly_rebalance() - creates an array of cat stats to be treated as the pseudo vanilla stats """
from ...config.defaults import DEFAULT_CONFIG
import tadbcmc.core.game_files as gf
import tadbcmc.data.enums.cats as c
import tadbcmc.core.simple_funcs as simp
import copy
import tadbcmc.core.seeded_randomization as srand





#these arent really tested for balance purposes nor are they really finished, I lost motivation due to lack of death surge and every interesting idea I had kinda getting ruined by ponoss bad code
def _first_form_lugas(stats:list[list[list]]):
    """ gives things to the first form lugas
    \n nonconditional """
    #first define all the lugas units ids
    nekoluga = 34
    ashiluga = 168
    kubiluga = 169
    tecoluga = 170
    balaluga = 171
    togeluga = 240
    nobiluga = 436
    papaluga = 546
    furiluga = 625
    kaoluga = 712
    mamoluga = 781
    summerluga = 564
    betrothed_balaluga = 711
    #make an array with all of them
    lugas = [nekoluga,ashiluga,kubiluga,tecoluga,balaluga,togeluga,nobiluga,papaluga,furiluga,kaoluga,mamoluga,summerluga,betrothed_balaluga]
    #now determine which ones get target all traits
    lugas_targetting_all = [nekoluga,ashiluga,kubiluga,balaluga,papaluga,kaoluga,mamoluga,betrothed_balaluga]
    #now determine which ones are suicide
    lugas_with_suicide = [tecoluga,togeluga]
    #now determine which ones are sentry
    lugas_with_sentry_behavior = [nekoluga,mamoluga,balaluga]
    """explanation of what each luga does:
    nekoluga - a sentry once it reaches the front line that freezes and kbs, notes say death surge is lvl4 with kb and 150f freeze (prolly shorter tho since it has sentry mode)
    ashiluga - non suicide unit with single target low range slow, notes say ds is lvl4 with 420f of slow
    kubiluga - non suicide single target, low range, kb unit (prolly long attack cycle to stop it from being generally useful), notes say ds is lvl6 with gauranteed kb
    tecoluga - suicide single target, high damage, low range, crit unit, notes say ds is lvl3 with 50% crit and 1000 base damage?
    balaluga - sentry at the front lines with freeze weaken, notes say ds is lvl4 with 300f freeze and 420f weaken to 50, maybe make them shorter since its sentry?
    togeluga - suicide area, high damage, omni with rel high range, notes say ds is lvl30 with 300 base damage
    nobiluga - non suicide unit with nothing on the base attack, notes say ds is lvl10 with 300 base damage and spawns farther away than most
    papaluga - non suicide, low range, curse unit, note say ds is lvl4 with 300f curse
    furiluga - suicide after 3 rapid attacks, spawns minisurge on each attack in a somewhat wide range, notes say ds is lvl6 with barrier and shield pierce
    kaoluga  - non suicide unit with somewhat frequent low kb chance attacks, notes say ds is lvl12 with 30% kb and minisurge
    mamoluga - sentry unit at the front lines, weak to 25% for 150f, notes say ds is lvl4 with weaken for 300f (sentry would force it shorter)
    sumerluga- non suicide unit with nothing on base attack, notes say ds is lvl8 with 600 damage in a huge spawn range (this seems really weak)
    betr bala- sentry at the front lines with 150f freeze, notes ay ds is lvl6 with 300f of freeze (sentry would force that shorter)

    #notes on how they differ as a result of the current lack of death surge will be written on each
    """
    """ existing till they add ds to cats """
    #lugas_targetting_all.extend([summerluga,tecoluga,togeluga,nobiluga]) #these are things with dodge that dont target traits elsewise
    #for all lugas give them an ability using second hit at their current pre attack, then set their first hits pre attack to -1 (and make it trigger ability, 150 damage)
    for luga in lugas:
        #first do preatks
        this_preatk = stats[luga][0][c.s.preatk]
        stats[luga][0][c.s.preatk] = -1
        stats[luga][0][c.s.multi_preatk_2] = this_preatk
        #now make both use abilities
        stats[luga][0][c.s.multi_has_ability_1] = 1
        stats[luga][0][c.s.multi_has_ability_2] = 1
        #now take care of the damage
        stats[luga][0][c.s.multi_damage_2] = 150
        stats[luga][0][c.s.attack] = 150
        """ temp """
        #for testing purposes Im decreasing their cost
        stats[luga][0][c.s.cost] = 100



    #first step, for all lugas getting all traits, give them here
    for luga in lugas_targetting_all:
        for trait in c.t:
            stats[luga][0][trait] = 1

    #now make those sucide lugas indeed suicide
    for luga in lugas_with_suicide:
        stats[luga][0][c.s.attack_state] = 2
        stats[luga][0][c.s.attack_count] = 1
    #now make those sentry lugas into sentries
    for luga in lugas_with_sentry_behavior:
        stats[luga][0][c.s.attack_state] = 3
        stats[luga][0][c.s.attack_count] = 1
        stats[luga][0][c.s.kbs] = 1 #these two are needed to make sure it only gets kbed when its gonna die cause its buggy otherwise
        stats[luga][0][c.s.boss_wave_immune] = 1
    #now edit each of them individually
    


    """ existing till they add ds to cats """
    lugas_with_suicide_dodge_surge = [ashiluga,kubiluga,tecoluga,togeluga,nobiluga,papaluga,kaoluga,summerluga]
    for luga in lugas_with_suicide_dodge_surge:
        stats[luga][0][c.s.attack_state] = 2
        stats[luga][0][c.s.attack_count] = 1
        stats[luga][0][c.s.range] = 300
        #stats[luga][0][c.s.dodge_chance] = 100
        #stats[luga][0][c.s.dodge_time] = 30
        stats[luga][0][c.s.hp] = 0 #im just ggiving 0 hp to make them immortal instead of dodge
        stats[luga][0][c.s.speed] = 10
        stats[luga][0][c.s.surge_chance] = 100
        stats[luga][0][c.s.surge_start_four] = 2000 #there will be no surge width generally




    #nekoluga 
    #due to the lack of death surge it will be a sentry with 350 range and 100% freeze for 45f and 20% kb (cooldown increased greatly)
    stats[nekoluga][0][c.s.attack_state] = 1
    stats[nekoluga][0][c.s.attack_count] = 1
    stats[nekoluga][0][c.s.range] = 350
    stats[nekoluga][0][c.s.freeze_chance] = 100
    stats[nekoluga][0][c.s.freeze_duration] = 45
    stats[nekoluga][0][c.s.kb_chance] = 20
    stats[nekoluga][0][c.s.recharge] = 4000
    stats[nekoluga][0][c.s.area] = 1
    nekoluga_attack_rate = 300
    stats[nekoluga][0][c.s.spirit_summon] = nekoluga 

    #ashiluga
    #making it a suicide unit with correct surge stats but on a normal surge
    stats[ashiluga][0][c.s.surge_level] = 4
    #intended stats
    stats[ashiluga][0][c.s.slow_chance] = 100
    stats[ashiluga][0][c.s.slow_duration] = 420 #maybe this should be shortend, esp once ds added

    #kubiluga
    #make it suicide with the correct surge on a normal surge
    stats[kubiluga][0][c.s.surge_level] = 6
    #proper stats
    stats[kubiluga][0][c.s.kb_chance] = 100

    #tecoluga
    #make it suicide with correct damage and surge n shit
    stats[tecoluga][0][c.s.surge_level] = 3
    #proper stats
    stats[tecoluga][0][c.s.crit_chance] = 50
    stats[tecoluga][0][c.s.multi_damage_2] = 1000

    #balaluga
    #make it sentry with correct freeze and no surge
    stats[balaluga][0][c.s.range] = 600
    stats[balaluga][0][c.s.freeze_chance] = 100
    stats[balaluga][0][c.s.freeze_duration] = 150
    stats[balaluga][0][c.s.weaken_to] = 50
    stats[balaluga][0][c.s.weaken_chance] = 100
    stats[balaluga][0][c.s.weaken_duration] = 300
    stats[balaluga][0][c.s.area] = 1 
    stats[balaluga][0][c.s.recharge] = 4000 #honestly I think most of these stats are just its final stats, it really just deserves to get death surge added on aswell
    balaluga_attack_rate = 400
    stats[balaluga][0][c.s.spirit_summon] = balaluga

    #togeluga
    #gonna make it have two back to back hits, one spawns the high surge the other does a lotta damage
    stats[togeluga][0][c.s.preatk] = stats[togeluga][0][c.s.multi_preatk_2]-1 #since this has already been set to the pre attack (make it start the surge one frame earlier)
    stats[togeluga][0][c.s.surge_level] = 30
    #proper stats
    stats[togeluga][0][c.s.area] = 1
    stats[togeluga][0][c.s.ld_width] = -920
    stats[togeluga][0][c.s.ld_minimum] = 600
    stats[togeluga][0][c.s.range] = 450
    stats[togeluga][0][c.s.multi_has_ability_2] = 0
    stats[togeluga][0][c.s.multi_damage_2] = 1500
    stats[togeluga][0][c.s.attack] = 300
    #only thing to note is the pre attack of both hits should be changed once the animation is added


    #nobiluga
    #gonna make it a suicide wave unit, trying out funky berserker on the wave
    stats[nobiluga][0][c.s.surge_chance] = 0 #im actually not giving this surge currently but it does get all the other things
    stats[nobiluga][0][c.s.wave_chance] = 100
    stats[nobiluga][0][c.s.wave_level] = 6
    stats[nobiluga][0][c.s.multi_damage_2] = 500
    stats[nobiluga][0][c.s.strengthen_at] = 100
    stats[nobiluga][0][c.s.strengthen_by] = 900
    """ temp """
    stats[nobiluga][0][c.s.multi_preatk_2] = 20
    stats[nobiluga][0][c.s.wave_level] = 24
    #stats[nobiluga][0][c.s.lethal_chance] = 100 #this doesnt work :pensive
    
    #papaluga
    #suicide with curse on the surge pretty boring
    stats[papaluga][0][c.s.surge_level] = 4
    #proper stats
    stats[papaluga][0][c.s.curse_chance] = 100
    stats[papaluga][0][c.s.curse_time] = 300

    #furiluga
    #suicide but with higher range than its supposed to have and more attacks to balance out the fact it can actually die
    #theres actually nothing incorrect to give this unit currently
    #proper stats
    stats[furiluga][0][c.s.range] = 350 #this is intended to smaller
    stats[furiluga][0][c.s.tba] = 0
    stats[furiluga][0][c.s.attack_state] = 2
    stats[furiluga][0][c.s.attack_count] = 5 #this is intended to be 3
    stats[furiluga][0][c.s.surge_width_four] = 2200
    stats[furiluga][0][c.s.surge_start_four] = 800
    stats[furiluga][0][c.s.surge_level] = 1
    stats[furiluga][0][c.s.surge_chance] = 100 #this unit is actually supposed to have surge
    stats[furiluga][0][c.s.barrier_break_chance] = 100
    stats[furiluga][0][c.s.shield_pierce_chance] = 100
    #note if I decrease the animation time the pre attack will have to be shifted

    #kaoluga
    #suicide unit with relatively correct stats otherwise
    stats[kaoluga][0][c.s.surge_level] = 12
    #proper stats
    stats[kaoluga][0][c.s.is_miniwave] = 1 #I forget do cats share this bool across miniwave and minisurge
    stats[kaoluga][0][c.s.kb_chance] = 30


    #mamoluga
    #still a sentry with more or less the same stats
    #honestly I think these are pretty much the intended stats
    stats[mamoluga][0][c.s.area] = 1
    stats[mamoluga][0][c.s.attack_count] = 1
    stats[mamoluga][0][c.s.attack_state] = 1
    mamoluga_attack_rate = 320
    stats[mamoluga][0][c.s.weaken_duration] = 160
    stats[mamoluga][0][c.s.weaken_chance] = 100
    stats[mamoluga][0][c.s.weaken_to] = 25
    stats[mamoluga][0][c.s.boss_wave_immune] = 1
    stats[mamoluga][0][c.s.range] = 800
    stats[mamoluga][0][c.s.recharge] = 4000
    stats[mamoluga][0][c.s.spirit_summon] = mamoluga


    #summerluga
    stats[summerluga][0][c.s.surge_level] = 12
    stats[summerluga][0][c.s.surge_width_four] = 2400
    #proper stats
    stats[summerluga][0][c.s.multi_damage_2] = 600


    #betrothed balaluga
    #Im completely disregarding what I wrote for this unit in favour of something really fucky
    stats[betrothed_balaluga][0][c.s.base_destroyer] = 1
    stats[betrothed_balaluga][0][c.s.tba] = 0
    stats[betrothed_balaluga][0][c.s.multi_damage_2] = 100
    stats[betrothed_balaluga][0][c.s.ld_minimum] = 1000
    stats[betrothed_balaluga][0][c.s.ld_width] = 1000
    stats[betrothed_balaluga][0][c.s.soul_strike] = 1
    stats[betrothed_balaluga][0][c.s.range] = -300 #it sits slightly in the zombies respawn range
    #dunno if I want it to sit in place so Im making it not a sentry
    #stats[betrothed_balaluga][0][c.s.kbs] = 5 #I removed it from the sentry list so these arent needed
    #stats[betrothed_balaluga][0][c.s.boss_wave_immune] = 0
    #stats[betrothed_balaluga][0][c.s.attack_state] = 1
    #stats[betrothed_balaluga][0][c.s.attack_count] = -1


    #Im handling the animations of sentries down here
    nekoluga_anim_name = simp.uinfo_to_anim(nekoluga,enemy=False,form=0,file_end="maanim",anim_num=2)
    balaluga_anim_name = simp.uinfo_to_anim(balaluga,enemy=False,form=0,file_end="maanim",anim_num=2)
    mamoluga_anim_name = simp.uinfo_to_anim(mamoluga,enemy=False,form=0,file_end="maanim",anim_num=2)
    nekoluga_anim = gf.file_reader(nekoluga_anim_name,vanilla=True) #Im assuming its fine to pull the vanilla version of the animations since this is early on
    balaluga_anim = gf.file_reader(balaluga_anim_name,vanilla=True)
    mamoluga_anim = gf.file_reader(mamoluga_anim_name,vanilla=True)
    #Im just hardcoding this, by slapping the final line of the first block onto it again (ill change this once I actually making shit for editing animations)
    nekoluga_copy = copy.deepcopy(nekoluga_anim[6])
    nekoluga_copy[0] = nekoluga_attack_rate #give nekoluga an attack cycle of 300f
    nekoluga_anim.insert(7,nekoluga_copy)
    nekoluga_anim[3][0] = 4 #change the first block to having 4 lines
    
    balaluga_copy = copy.deepcopy(balaluga_anim[13])
    balaluga_copy[0] = balaluga_attack_rate #give balaluga an attack cycle of 400f
    balaluga_anim.insert(14,balaluga_copy)
    balaluga_anim[3][0] = 11 #change the first block to having 11 lines

    mamoluga_copy = copy.deepcopy(mamoluga_anim[6])
    mamoluga_copy[0] = mamoluga_attack_rate #give mamoluga an attack cycle of 400f
    mamoluga_anim.insert(7,mamoluga_copy)
    mamoluga_anim[3][0] = 4 #change the first block to having 4 lines

    #now save those three
    gf.file_writer(nekoluga_anim_name,nekoluga_anim)
    gf.file_writer(balaluga_anim_name,balaluga_anim)
    gf.file_writer(mamoluga_anim_name,mamoluga_anim)


    return stats


    #why
    
def _courier_massive_removal(stats:list[list[list]]):
    """ literally just removes massive damage and red from courier
    \n nonconditional """
    #courier is 658
    for x in range(0,len(stats[658])):
        stats[658][x][c.s.massive] = 0
        stats[658][x][c.t.red] = 0
    return stats

def _critter_metal_removal_rebalance(stats:list[list[list]]):
    """ rebalances crit units with the intent of having no metals (doesnt have to be the case)
    \n nonconditional """

    #first Im gonna define all the unit ids since I dont feel like using raw numbers
    jurassic = 46
    million_dollar = 635
    space = 78
    jumprope = 88
    hurricat = 267
    waitress = 273
    aku_researcher = 621
    backhoe = 446
    paladin = 57
    verbena = 358
    hayabusa = 261
    #I left out cat clan 427 (its literally just a 3% crit I dont think its needed)
    #also choosing to do nothing with axel it seems fine enough as is

    #jurassic, the beloved melee dps
    for x in range(0,3):
        stats[jurassic][x][c.s.savage_by] = 200
        stats[jurassic][x][c.s.savage_chance] = 5
        stats[jurassic][x][c.s.cost] = 500
    (stats[jurassic][0][c.s.hp],stats[jurassic][1][c.s.hp],stats[jurassic][2][c.s.hp]) = (570,900,1400)
    (stats[jurassic][0][c.s.attack],stats[jurassic][1][c.s.attack],stats[jurassic][2][c.s.attack]) = (200,250,300)
    #getting dark target in tf is a post randomization thing

    #million_dollar, wave weakener, also just has sign stats (the level boost must be set to 0 elsewhere to keep it constant)
    r = srand.randinst(146)
    for x in range(0,2):
        stats[million_dollar][x][c.s.recharge] = 27000
        stats[million_dollar][x][c.s.hp] = 10000
        stats[million_dollar][x][c.s.kbs] = 10000
        stats[million_dollar][x][c.s.attack] = 1
        stats[million_dollar][x][c.s.range] = 800
        stats[million_dollar][x][c.s.tba] = 300
        stats[million_dollar][x][c.s.speed] = 4
        stats[million_dollar][x][c.s.crit_chance] = 0
        stats[million_dollar][x][c.s.bounty] = 0
        stats[million_dollar][x][c.s.weaken_chance] = 100
        stats[million_dollar][x][c.s.weaken_duration] = 150
        stats[million_dollar][x][c.s.weaken_to] = 25
        stats[million_dollar][x][c.s.wave_chance] = 100
        stats[million_dollar][x][c.s.wave_level] = int(5+r.randrange(0,10)) #random level wave from 5 to 14
        for trait in c.t:
            stats[million_dollar][x][trait] = 1
        #I would love to give it a higher willpower but that doesnt seem to be a stat (at least not a logged one)

    #space cat, gets things based on animation, first form surge, second form blast, third form I havent a clue and amph suggested single target paris so third form is just better at that role
    for x in range(0,3):
        stats[space][x][c.s.recharge] = 500
        stats[space][x][c.s.barrier_break_chance] = 0
        stats[space][x][c.s.wave_immune] = 0
        stats[space][x][c.s.crit_chance] = 20
    #my idea for first form is generally the surges shouldnt hit what space is actually targetting (not editing hp/atk for now)
    stats[space][0][c.s.surge_chance] = 40
    stats[space][0][c.s.surge_level] = 2
    stats[space][0][c.s.surge_start_four] = 1700
    stats[space][0][c.s.surge_width_four] = 1300
    #my idea for second form is its a good aoe barrier breaker
    stats[space][1][c.s.crit_chance] = 0
    stats[space][1][c.s.explode_chance] = 50
    stats[space][1][c.s.explode_at] = 1360
    stats[space][1][c.s.barrier_break_chance] = 50
    #my idea for third form is idk a mix between camera and paris I guess
    stats[space][2][c.s.attack] = 100
    stats[space][2][c.s.lethal_chance] = 40
    stats[space][2][c.s.recharge] = 400 


    #jumprope, the actually usable meatshield, literally just give it more hp and remove the crit (cause id find crit on an actually usable meatshield to take away from the feeling of crits)
    for x in range(0,3):
        stats[jumprope][x][c.s.crit_chance] = 0
        stats[jumprope][x][c.s.hp] = 800 #needs testing, in my opinion it should be an actually decent ms since it costs so much


    #hurricat, the utterly rapid attacker, literally just gets 2 more attacks, also remove crit
    for x in range(0,3):
        stats[hurricat][x][c.s.crit_chance] = 0
        stats[hurricat][x][c.s.multi_preatk_2] = 3
        stats[hurricat][x][c.s.multi_preatk_3] = 3
        stats[hurricat][x][c.s.multi_damage_2] = 30
        stats[hurricat][x][c.s.multi_damage_3] = 30
    stats[hurricat][0][c.s.multi_damage_2] = 24
    stats[hurricat][0][c.s.multi_damage_3] = 24


    #waitress, single target nuker, 100% savage for 5x damage, also gets strong against metal 
    for x in range(0,3):
        stats[waitress][x][c.s.savage_chance] = 100
        stats[waitress][x][c.s.savage_by] = 400 #in old randomizer this was 300, at 400 it does bahamut damage so for sake of math and also cause it misses so much Im doing 400
        stats[waitress][x][c.s.strong] = 1
        stats[waitress][x][c.t.metal] = 1

    #aku researcher, massive against a single trait, not much to be said here (I dont feel like making aku researcher target aku if metals are still on)
    for x in range(0,3):
        stats[aku_researcher][x][c.s.massive] = 1
        stats[aku_researcher][x][c.t.metal] = 1
    

    #backhoe, the multihit exploding curser, still has attack only, curse and explode are 100% in tf, still has bounty but who cares
    for x in range(0,3):
        stats[backhoe][x][c.s.multi_preatk_2] = 61 #fuck u ponos why can these not be on the same frame
        stats[backhoe][x][c.s.multi_preatk_3] = 62
        stats[backhoe][x][c.s.multi_damage_2] = 100
        stats[backhoe][x][c.s.multi_damage_3] = 100
        stats[backhoe][x][c.s.attack] = 100
        stats[backhoe][x][c.s.multi_has_ability_1] = 1
        stats[backhoe][x][c.s.multi_has_ability_2] = 1
        stats[backhoe][x][c.s.multi_has_ability_3] = 1
        stats[backhoe][x][c.s.curse_time] = 100
        stats[backhoe][x][c.s.explode_at] = 1000
        stats[backhoe][x][c.s.explode_variation_x4] = 3000
        stats[backhoe][x][c.s.crit_chance] = 0
        stats[backhoe][x][c.s.curse_chance] = 50
        stats[backhoe][x][c.s.explode_chance] = 50
    stats[backhoe][2][c.s.curse_chance] = 100
    stats[backhoe][2][c.s.explode_chance] = 100
    stats[backhoe][2][c.s.surge_chance] = 0 #prevent it from being too sloppy, this should hide all the other surge information


    #paladin, the melee nuker, savage 200% equal to crit rate, first form has higher damage in compensation for its lack of area and lower proc rates
    for x in range(0,3):
        stats[paladin][x][c.s.savage_by] = 200
        stats[paladin][x][c.s.tba] = 140 #makes for about 310f cycle
        stats[paladin][x][c.s.soul_strike] = 1
        stats[paladin][x][c.s.weaken_immune] = 1
        stats[paladin][x][c.s.slow_immune] = 1
        stats[paladin][x][c.s.zombie_killer] = 1
    stats[paladin][0][c.s.crit_chance] = 30
    stats[paladin][0][c.s.tba] = 90 #for a cycle of about 210f
    (stats[paladin][0][c.s.savage_chance],stats[paladin][1][c.s.savage_chance],stats[paladin][2][c.s.savage_chance]) = (30,40,50)
    (stats[paladin][0][c.s.hp],stats[paladin][1][c.s.hp],stats[paladin][2][c.s.hp]) = (3500,3500,4000)
    (stats[paladin][0][c.s.attack],stats[paladin][1][c.s.attack],stats[paladin][2][c.s.attack]) = (1400,1000,1200)


    #verbena, not a lot to say it just gets savage at crit rates on each form
    for x in range(0,3):
        stats[verbena][x][c.s.savage_by] = 200
        stats[verbena][x][c.s.savage_chance] = 30
    stats[verbena][2][c.s.savage_chance] = 50

    #hayabusa, 200% savage at crit rate, makes for same average dps (technically 1.04x) as second form but with higher max dph
    stats[hayabusa][0][c.s.savage_by] = 200
    stats[hayabusa][0][c.s.savage_chance] = 30


    #ok I think thats it
    return stats









""" balance functions """

def early_rebalance(config=DEFAULT_CONFIG,log=None):
    """ pulls the vanilla cat stats and edits them with the intended initial modded rebalances """
    #first get cat stats
    stats = gf.get_cat_stats(vanilla=True)
    if config["gameplay"]["unit_reworks"]["lugas"]:
        stats = _first_form_lugas(stats)




    return stats















