""" module containing the various adjustments to make to cat stats at various stages in the randomization process
\nearly_rebalance() - creates an array of cat stats to be treated as the pseudo vanilla stats """
from ...config.defaults import DEFAULT_CONFIG
import tadbcmc.core.game_files as gf
import tadbcmc.data.enums.cats as c
import tadbcmc.core.simple_funcs as simp
import copy
import tadbcmc.core.seeded_randomization as srand
from .unit_reworks import critters
from .unit_reworks import lugas
from .unit_reworks import monenekos
from .unit_reworks import seasonals
from .unit_reworks import collabs




    
def _courier_massive_removal(stats:list[list[list]]):
    """ literally just removes massive damage and red from courier
    \n nonconditional """
    #courier is 658
    for x in range(0,len(stats[658])):
        stats[658][x][c.s.massive] = 0
        stats[658][x][c.t.red] = 0
    return stats

def _cop_cat_fix(stats:list[list[list]]):
    """ fixes the copaganda that is strong against white with strong against red/alien/black instead
    \n nonconditional """
    #cop cat is u id 716
    for x in range(1,3):
        stats[716][x][c.t.white] = 0
        stats[716][x][c.t.red] = 1
        stats[716][x][c.t.dark] = 1
        stats[716][x][c.t.alien] = 1
    return stats

#STILL MISSING ACTUALLY APPLYING SHIELD PIERCE
#STILL UNDECIDED IF I WANT THESE TO BE PER FORM OR NOT
def _trait_change_abilities(stats:list[list[list]],vstats:list[list[list]],config=DEFAULT_CONFIG):
    """ applies/removes trait abilitis where relevant according to config """
    ability_config = config["trait"]["unit"]["ability"]
    grant_ab = ability_config["grant_trait_abilities"]
    remove_ab = ability_config["remove_trait_abilities"]
    zkill_freq = ability_config["zkill_frequency"]
    curse_imm_freq = ability_config["curse_immune_frequency"]
    sp_freq = ability_config["shield_pierce_frequency"]

    if not grant_ab and not remove_ab:
        return stats #not a single reason here
    for u_id in range(0,len(stats)):
        for form_id in range(0,len(stats[u_id])):
            r = srand.randinst(87+93*u_id+17*form_id)
            r1 = r.randrange(0,100)
            r2 = r.randrange(0,100)
            r3 = r.randrange(0,100)
            r4 = r.randrange(0,100)
            r5 = r.randrange(0,100)
            r6 = r.randrange(0,100)
            r7 = r.randrange(0,100)
            r8 = r.randrange(0,100)
            r9 = r.randrange(0,100)
            zombie_sum = stats[u_id][form_id][c.t.zombie] - vstats[u_id][form_id][c.t.zombie]
            relic_sum = stats[u_id][form_id][c.t.relic] - vstats[u_id][form_id][c.t.relic]
            aku_sum = stats[u_id][form_id][c.t.aku] - vstats[u_id][form_id][c.t.aku]
            #zkill
            if zombie_sum > 0 and grant_ab: #if it gained zombie (talents done elsewhere)
                if r1 < zkill_freq:
                    stats[u_id][form_id][c.s.zombie_killer] = 1
            if zombie_sum < 0 and remove_ab:
                if r1 < zkill_freq:
                    stats[u_id][form_id][c.s.zombie_killer] = 0
            #curse immune
            if relic_sum > 0 and grant_ab:
                if r2 < curse_imm_freq:
                    stats[u_id][form_id][c.s.curse_immune] = 1
            if relic_sum < 0 and remove_ab:
                if r2 < curse_imm_freq:
                    stats[u_id][form_id][c.s.curse_immune] = 0
            #sp
            if aku_sum > 0 and grant_ab:
                if r3 < sp_freq:
                    pass
            if aku_sum < 0 and remove_ab:
                if r3 < sp_freq:
                    stats[u_id][form_id][c.s.shield_pierce_chance] = 0
    return stats
            











""" balance functions """

def early_rebalance(config=DEFAULT_CONFIG,log=None):
    """ pulls the vanilla cat stats and edits them with the intended initial modded rebalances """
    rework_config = config["gameplay"]["unit_reworks"]
    #first get cat stats
    stats = gf.get_cat_stats(vanilla=True)
    if rework_config["lugas"]:
        stats = lugas.lugas(stats)
    if rework_config["courier"]:
        stats = _courier_massive_removal(stats)
    if rework_config["critters"]:
        stats = critters.critters(stats)
    if rework_config["cop"]:
        stats = _cop_cat_fix(stats)
    if rework_config["monenekos"]:
        stats = monenekos.monenekos(stats)
    if rework_config["seasonals"]:
        stats = seasonals.seasonals(stats)
    if rework_config["collabs"]:
        stats = collabs.collabs(stats)




    return stats

def pre_trait_change_rebalance(stats:list[list[list]],config=DEFAULT_CONFIG,log=None):
    """ makes changes to stats intended to be included in trait randomization """
    #not a fuckin clue what goes here but this exists in case theres something
    return stats

def post_trait_change_rebalance(stats:list[list[list]],config=DEFAULT_CONFIG,log=None):
    """ makes the post trait change changes to cat stats """
    #jurassic dark target should go here

    #maybe this should get the pretrait change rebalance instead of early rebalance? idk
    stats = _trait_change_abilities(stats,early_rebalance(config=config,log=log),config=config)
    return stats








