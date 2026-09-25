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















