"""  """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.cats as c
import copy


def jurassic(stats:list[list[list]]):
    """ applies the rework to
    \n nonconditional """
    unit_id = 46
    unit = stats[unit_id] #passing things as a reference oh lord help me
    #jurassic, the beloved melee dps
    for x in range(0,3):
        unit[x][c.s.savage_by] = 200
        unit[x][c.s.savage_chance] = 5
        unit[x][c.s.cost] = 500
    (unit[0][c.s.hp],unit[1][c.s.hp],unit[2][c.s.hp]) = (570,900,1400)
    (unit[0][c.s.attack],unit[1][c.s.attack],unit[2][c.s.attack]) = (130,250,300)
    unit[2][c.s.savage_chance] = 10
    unit[2][c.s.crit_chance] = 10
    #getting dark target in tf is a post randomization thing

    talents = gf.get_talents()
    this_talents = []
    for x in range(0,len(talents)):
        if unit_id in talents[x]:
            this_talents = talents[x]
    #first kill cost talents and get the position of crit talent
    for x in range(2,len(this_talents)):
        crit_pos = 2
        cost_pos = -1
        if this_talents[x][c.tpos.ability_id] == int(c.tv.crit):
            crit_pos = x
        if this_talents[x][c.tpos.ability_id] == int(c.tv.cost_down):
            cost_pos = x
    #now kill cost and duplicate crit
    this_talents.pop(cost_pos)
    savage_talent_block = copy.deepcopy(this_talents[crit_pos])
    savage_talent_block[c.tpos.ability_id] = c.tv.savage
    #idk if this is really required, or if its even correct
    savage_talent_block[c.tpos.savage_by] = 200
    savage_talent_block[c.tpos.savage_by+1] = 200
    #now put it back in the array
    this_talents.insert(crit_pos+1,savage_talent_block)
    #should be all good to save?
    gf.write_talents(talents)


    #dont think jurassic actually needs level scaling I just made the first form considerably weaker


    return stats












