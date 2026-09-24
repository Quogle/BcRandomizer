from .moneneko_units import neneko
from .moneneko_units import summer_neneko
from .moneneko_units import new_years_neneko
from .moneneko_units import valentine_neneko
from .moneneko_units import easter_neneko
from .moneneko_units import witchy_neneko
from .moneneko_units import moneko
from .moneneko_units import crazed_moneko



def monenekos(stats:list[list[list]]):
    """ does the reworks for all monenekos and the things required for them
    \n nonconditional """
    stats = neneko.neneko(stats)
    stats = summer_neneko.summer_neneko(stats)
    stats = new_years_neneko.new_years_neneko(stats)
    stats = valentine_neneko.valentine_neneko(stats)
    stats = easter_neneko.easter_neneko(stats)
    stats = witchy_neneko.witchy_neneko(stats)
    stats = moneko.moneko(stats)
    stats = crazed_moneko.crazed_moneko(stats)
    return stats





