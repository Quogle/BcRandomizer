
import tadbcmc.pieces.qol as qol
from ...config.defaults import DEFAULT_CONFIG
import tadbcmc.data.enums.unitbuy as ub
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn



def _gold_cpu_buff(config=DEFAULT_CONFIG):
    """ buffs gold cpu """
    if config["qol"]["gold_cpu_buff"]:
        qol.set_daily_gold_cpu_limit(30)

def _unit_sell_increase(config=DEFAULT_CONFIG):
    """ triples the xp sell and doubles the np sell of all units """
    if config["qol"]["unit_sell_increase"]:
        unitbuy = gf.file_reader(fn.UNITBUY_FILE)
        for u_id in range(0,len(unitbuy)):
            unitbuy[u_id][ub.ub.selling_xp] = int(3*unitbuy[u_id][ub.ub.selling_xp])
            unitbuy[u_id][ub.ub.np_selling_amount] = int(2*unitbuy[u_id][ub.ub.np_selling_amount])

def _free_orb_removal(config=DEFAULT_CONFIG):
    """ sets all orb removal costs to 0 np """
    if config["qol"]["free_orb_removal"]:
        qol.set_orb_removal_cost() #defaults are free so idc











