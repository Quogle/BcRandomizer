
from bcr.gui.main_window import main
#main()
from bcr.randomizer import randomize
import tadbcmc.core.file_handler as fh
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import bcr.randomizer.enemies.ability_randomization as ab_swap
from bcr.config.defaults import DEFAULT_CONFIG
from tadbcmc.data.collated_info.enemy_info import *
import tadbcmc.data.enums.unit_info as ui
import tadbcmc.core.simple_funcs as simp
#main()
import bcr.randomizer.units.trait_changer as trait_changer





"""
estat = gf.file_reader(fn.ENEMY_STATS,vanilla=True)
estat = ab_swap.randomize_abilities(estat)
gf.file_writer(fn.ENEMY_STATS,estat)
"""



talent_array = gf.get_talents()
stats = gf.get_cat_stats(vanilla=True)




