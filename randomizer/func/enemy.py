
import enums.enemy as e
import enums.cats as c
from enums.files import *


ABILITIES = {
    "crit":[e.s.critChance],
    "freeze":[e.s.freezeChance,e.s.freezeTime],
    "slow":[e.s.slowChance,e.s.slowTime],
    "weaken":[e.s.weakenChance,e.s.weakenTime,e.s.weakenPercent],
    "kb":[e.s.kbChance],
    "warp":[e.s.warpChance,e.s.warpDuration,e.s.warpMin4x,e.s.warpMax4x],
    "curse":[e.s.curseChance,e.s.curseDuration],
    "dodge":[e.s.dodgeChance,e.s.dodgeDuration],
    "toxic":[e.s.toxicChance,e.s.toxicAmount],
    "savage":[e.s.savageChance,e.s.savageBoost],
    "wave":[e.s.waveChance,e.s.waveLevel],
    "surge":[e.s.surgeChance,e.s.surgeLevel,e.s.surgeStartPos,e.s.surgeWidth],
    "blast":[e.s.explodeChance,e.s.explodeAt4x,e.s.explodeVariance],
    "strengthen":[e.s.strengthenAt,e.s.strengthenBy],
    "lethal":[e.s.lethal],
    "base destroyer":[e.s.baseDestroyer]
}
CHANCE_ABILITIES = ["crit","freeze","slow","weaken","kb","warp","curse","dodge","toxic","savage","wave","surge","blast"]
BOOL_ABILITIES = ["lethal","base destroyer"]



def randomize_abilities(estat):
    for unit in estat:
        #gather how many abilities current unit has
        ability_number = 0
        for ability in ABILITIES:
            if unit[ABILITIES[ability]] > 0:
                ability_number += 1
        
        if ability_number == 0:
            next #dont do unit if no ability
        

        attack_cycle = unit[e.s.preatk] + unit[e.s.tba] + 1
        # sets chance to average chance or bases it on attack rate if no chance abilities
        chance_sum = 0
        chance_count = 0
        for ability in CHANCE_ABILITIES:
            if unit[ABILITIES[ability]] > 0:
                chance_sum += unit[ABILITIES[ability]]
                chance_count += 1
        chance = int(chance_sum/chance_count)
        if chance == 0:
            chance = int(100*attack_cycle/300)
        if chance > 100:
            chance = 100
        
        
        























"""
needed functions
id swap







"""






