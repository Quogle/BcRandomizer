"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c
import copy


def paladin(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 57
    unit = stats[unit_id] #passing things as a reference oh lord help me

    #paladin, the melee nuker, savage 200% and crit at 50%
    for x in range(0,3):
        unit[x][c.s.savage_by] = 200
        unit[x][c.s.tba] = 140 #makes for about 310f cycle
        unit[x][c.s.soul_strike] = 1
        unit[x][c.s.zombie_killer] = 1
        unit[x][c.s.weaken_immune] = 1
        unit[x][c.s.crit_chance] = 50
        unit[x][c.s.savage_chance] = 50
    #first form is a more rapid attacking single target version
    unit[0][c.s.tba] = 90 #for a cycle of about 210f
    unit[0][c.s.barrier_break_chance] = 100
    #second form is a fastier tankier lower damage version
    unit[1][c.s.speed] = 11
    unit[1][c.s.slow_immune] = 1
    unit[1][c.s.freeze_immune] = 1
    unit[1][c.s.kbs] = 2
    unit[1][c.s.lethal_chance] = 100
    #third form is just a midranged semi nuker idrk, I think most of its interesting bits come from talents since it has so many
    unit[2][c.s.range] = 265 #from 245
    #I had this intent to maybe give slow/freeze immune as talents, but also a relatively frequent dodge chance for very short time
    (unit[0][c.s.hp],unit[1][c.s.hp],unit[2][c.s.hp]) = (5000,6000,4000)
    (unit[0][c.s.attack],unit[1][c.s.attack],unit[2][c.s.attack]) = (1800,1200,1400) #took a look at barlog and decided to increase first form damage from 1300 to 1800





    talents = gf.get_talents()
    this_talents = []
    for x in range(0,len(talents)):
        if unit_id in talents[x]:
            this_talents = talents[x]
    #actually just gonna nuke its talents lmao
    while len(this_talents) > 2:
        this_talents.pop(-1)
    #now add each talent                                                will correct later    fix later
    #                   ability id,     maxlvl, s1 min/max,                 ,   text id,        cost,   name,   limit
    slow_talent =       [c.tv.islow,    1,      0,0,    0,0,    0,0,    0,0,    c.tv.islow,     3,      -1,     0]
    freeze_talent =     [c.tv.ifreeze,  1,      0,0,    0,0,    0,0,    0,0,    c.tv.ifreeze,   3,      -1,     0]
    recharge_talent =   [c.tv.recharge, 5,      20,200, 0,0,    0,0,    0,0,    c.tv.recharge,  2,      -1,     0]
    hp_talent =         [c.tv.health,   10,     2,20,   0,0,    0,0,    0,0,    c.tv.health,    8,      -1,     0]
    attack_talent =     [c.tv.attack,   10,     2,20,   0,0,    0,0,    0,0,    c.tv.attack,    8,      -1,     0]
    #ultras
    dodge_talent =      [c.tv.dodge,    1,      30,30,  10,10,  0,0,    0,0,    c.tv.dodge,     3,      -1,     1]
    tba_talent =        [c.tv.tba,      1,      25,25,  0,0,    0,0,    0,0,    c.tv.tba,       3,      -1,     1]
    bounty_talent =     [c.tv.bounty,   1,      0,0,    0,0,    0,0,    0,0,    c.tv.bounty,    3,      -1,     1]

    """ temp """
    for x in range(11,69):
        this_t = copy.deepcopy(slow_talent)
        this_t[0] = x
        if x > 30:
            this_t[-1] = 1
        this_talents.append(this_t)

    """
    #now ad them all
    this_talents.append(slow_talent)
    this_talents.append(freeze_talent)
    this_talents.append(recharge_talent)
    this_talents.append(hp_talent)
    this_talents.append(attack_talent)
    this_talents.append(dodge_talent)
    this_talents.append(tba_talent)
    this_talents.append(bounty_talent)
    """


    gf.write_talents(talents)

    return stats












