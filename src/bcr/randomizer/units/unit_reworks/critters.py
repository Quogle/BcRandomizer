from .crit_units import jurassic
from .crit_units import million_dollar
from .crit_units import space
from .crit_units import jumprope
from .crit_units import hurricat
from .crit_units import waitress
from .crit_units import aku_researcher
from .crit_units import backhoe
from .crit_units import paladin
from .crit_units import verbena
from .crit_units import hayabusa



def critters(stats:list[list[list]]):
    """ does the reworks for all crit units and the things required for them
    \n nonconditional """
    stats = jurassic.jurassic(stats)
    stats = million_dollar.million_dollar(stats)
    stats = space.space(stats)
    stats = jumprope.jumprope(stats)
    stats = hurricat.hurricat(stats)
    stats = waitress.waitress(stats)
    stats = aku_researcher.aku_researcher(stats)
    stats = backhoe.backhoe(stats)
    stats = paladin.paladin(stats)
    stats = verbena.verbena(stats)
    stats = hayabusa.hayabusa(stats)
    return stats













