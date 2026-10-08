""" module responsible for executing all qol modules """
from ..qol import misc_qol
from ..qol import shop_maker
from ..qol import stage_buffs
from ..qol import stage_changes
from ...config.defaults import DEFAULT_CONFIG







def qol_total(config=DEFAULT_CONFIG,log=None):
    """ does all the quality of life things from config """
    misc_qol.misc_total(config=config)
    shop_maker.make_shop(config=config)
    stage_buffs.stage_total(config=config,log=log)
    stage_changes.stage_changes_total(config=config)
















