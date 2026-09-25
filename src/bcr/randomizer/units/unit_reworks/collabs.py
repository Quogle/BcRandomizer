from .collab_units import capsule
from .collab_units import merc
from .collab_units import mint
from .collab_units import punt
from .collab_units import racism_cow
from .collab_units import reaper




def collabs(stats:list[list[list]],remove_metals=True):
    """ does the reworks for all crit units and the things required for them
    \n nonconditional """
    stats = capsule.capsule(stats)
    stats = merc.merc(stats)
    stats = mint.mint(stats,remove_metals)
    stats = punt.punt(stats,remove_metals)
    stats = racism_cow.racism_cow(stats)
    stats = reaper.reaper(stats)
    return stats














