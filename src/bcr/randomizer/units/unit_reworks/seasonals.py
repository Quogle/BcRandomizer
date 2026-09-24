from .seasonal_units import slug_cat
from .seasonal_units import rampage
from .seasonal_units import ritual
from .seasonal_units import reindeer
from .seasonal_units import prisoner
from .seasonal_units import evil
from .seasonal_units import doll
from .seasonal_units import maiden
from .seasonal_units import koi
from .seasonal_units import madam
from .seasonal_units import vacation
from .seasonal_units import vengeful
from .seasonal_units import kungfux
from .seasonal_units import marshmallow
from .seasonal_units import kart
from .seasonal_units import pumpcat
from .seasonal_units import gift_of_cats
from .seasonal_units import delivery
from .seasonal_units import eggy
from .seasonal_units import tricycle


def seasonals(stats:list[list[list]]):
    """ does the reworks for all seasonals and the things required for them
    \n nonconditional """
    stats = slug_cat.slug_cat(stats)
    stats = rampage.rampage(stats)
    stats = ritual.ritual(stats)
    stats = reindeer.reindeer(stats)
    stats = prisoner.prisoner(stats)
    stats = evil.evil(stats)
    stats = doll.doll(stats)
    stats = maiden.maiden(stats)
    stats = koi.koi(stats)
    stats = madam.madam(stats)
    stats = vacation.vacation(stats)
    stats = vengeful.vengeful(stats)
    stats = kungfux.kungfux(stats)
    stats = marshmallow.marshmallow(stats)
    stats = kart.kart(stats)
    stats = pumpcat.pumpcat(stats)
    stats = gift_of_cats.gift_of_cats(stats)
    stats = delivery.delivery(stats)
    stats = eggy.eggy(stats)
    stats = tricycle.tricycle(stats)
    return stats






