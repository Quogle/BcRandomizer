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


DEFAULT_CONFIG["enemy"]["ability"]["randomize_abilities"] = True
DEFAULT_CONFIG["enemy"]["ability"]["min_abilities"] = 4





"""
estat = gf.file_reader(fn.ENEMY_STATS,vanilla=True)
estat = ab_swap.randomize_abilities(estat)
gf.file_writer(fn.ENEMY_STATS,estat)
"""


variants = [[]]
for variant in ui.enemy_variant:
    variants.append([])

for unit in ENEMY_INFO:
    if unit[ui.e.variant_id] > 0:
        print(unit[ui.e.variant_id])
        variants[unit[ui.e.variant_id]].append(unit[ui.e.unit_name])


simp.print_array_one_by_one(variants)




