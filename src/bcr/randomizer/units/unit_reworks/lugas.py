from .luga_units import nekoluga
from .luga_units import ashiluga
from .luga_units import kubiluga
from .luga_units import tecoluga
from .luga_units import balaluga
from .luga_units import togeluga
from .luga_units import nobiluga
from .luga_units import papaluga
from .luga_units import furiluga
from .luga_units import kaoluga
from .luga_units import mamoluga
from .luga_units import summer_luga
from .luga_units import betrothed_balaluga


def monenekos(stats:list[list[list]]):
    """ does the reworks for all first form lugas and the things required for them
    \n nonconditional """
    stats = nekoluga.nekoluga(stats)
    stats = ashiluga.ashiluga(stats)
    stats = kubiluga.kubiluga(stats)
    stats = tecoluga.tecoluga(stats)
    stats = balaluga.balaluga(stats)
    stats = togeluga.togeluga(stats)
    stats = nobiluga.nobiluga(stats)
    stats = papaluga.papaluga(stats)
    stats = furiluga.furiluga(stats)
    stats = kaoluga.kaoluga(stats)
    stats = mamoluga.mamoluga(stats)
    stats = summer_luga.summer_luga(stats)
    stats = betrothed_balaluga.betrothed_balaluga(stats)
    return stats
    """explanation of what each luga does:
    nekoluga - a sentry once it reaches the front line that freezes and kbs, notes say death surge is lvl4 with kb and 150f freeze (prolly shorter tho since it has sentry mode)
    ashiluga - non suicide unit with single target low range slow, notes say ds is lvl4 with 420f of slow
    kubiluga - non suicide single target, low range, kb unit (prolly long attack cycle to stop it from being generally useful), notes say ds is lvl6 with gauranteed kb
    tecoluga - suicide single target, high damage, low range, crit unit, notes say ds is lvl3 with 50% crit and 1000 base damage?
    balaluga - sentry at the front lines with freeze weaken, notes say ds is lvl4 with 300f freeze and 420f weaken to 50, maybe make them shorter since its sentry?
    togeluga - suicide area, high damage, omni with rel high range, notes say ds is lvl30 with 300 base damage
    nobiluga - non suicide unit with nothing on the base attack, notes say ds is lvl10 with 300 base damage and spawns farther away than most
    papaluga - non suicide, low range, curse unit, note say ds is lvl4 with 300f curse
    furiluga - suicide after 3 rapid attacks, spawns minisurge on each attack in a somewhat wide range, notes say ds is lvl6 with barrier and shield pierce
    kaoluga  - non suicide unit with somewhat frequent low kb chance attacks, notes say ds is lvl12 with 30% kb and minisurge
    mamoluga - sentry unit at the front lines, weak to 25% for 150f, notes say ds is lvl4 with weaken for 300f (sentry would force it shorter)
    sumerluga- non suicide unit with nothing on base attack, notes say ds is lvl8 with 600 damage in a huge spawn range (this seems really weak)
    betr bala- sentry at the front lines with 150f freeze, notes ay ds is lvl6 with 300f of freeze (sentry would force that shorter)

    #notes on how they differ as a result of the current lack of death surge will be written on each
    """