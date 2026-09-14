from bcr.gui.main_window import main
#main()
from bcr.randomizer import randomize
import tadbcmc.core.file_handler as fh
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import bcr.randomizer.enemies.ability_swap as ab_swap
from bcr.config.defaults import DEFAULT_CONFIG

DEFAULT_CONFIG["enemy"]["ability"]["randomize_abilities"] = True
DEFAULT_CONFIG["enemy"]["ability"]["min_abilities"] = 4






estat = gf.file_reader(fn.ENEMY_STATS,vanilla=True)
estat = ab_swap.randomize_abilities(estat)
gf.file_writer(fn.ENEMY_STATS,estat)









