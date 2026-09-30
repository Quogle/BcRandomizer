import tadbcmc.data.enums.cats as c
import tadbcmc.core.seeded_randomization as srand
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn

import tadbcmc.core.file_handler as fh
from ...config.defaults import DEFAULT_CONFIG
import copy
from . import trait_randomization_mk3
from ...config.version_config import version_config_keys as vck
from . import balancing
from ...config.version_config.get_version_config import DEFAULT_VC_CONFIG
import tadbcmc.core.simple_funcs as simp


""" algorithm
divide a units current talents by each grouping:
    orb/not
    preversion/postversion
    randomize/not
for a total of 8 groupings
count up the number of orbs/talents

#randomization process
for each orb, roll a % chance to become a talent (0% if orbs not included)
for each talent, roll a % chance to become an orb (0% if orbs not included)
now count the total number of orbs and talents a unit is supposed to get
    make a note of how many additional talents this unit needs to get due to minimum/all unit get requirements
if preversion:
    considering only those talents already placed, or those remaining on the unit due to not randomized,
    randomize each talent within the bounds of the max talent for preversion,
        place the talent id without determining any specific stats for now
if postversion:
    consider all talents already placed and other postversion non rand talents
    randomize each talent within the bounds of max talent for postversion,
        place talent id without determining any specific stats for now








 """








""" necessary functions of information getting
talent traits a unit can currently get
trait sums a unit can currently get
get all allowed traits



"""
#defining other information
STAT_TRAITS = [ #these are in the same order as they are in talents
    c.t.red,
    c.t.floating,
    c.t.dark,
    c.t.metal,
    c.t.angel,
    c.t.alien,
    c.t.zombie,
    c.t.relic,
    c.t.white,
    c.t.aku,
]

#defining talent pools
ATTRIBUTES = [
    c.tv.attack,
    c.tv.health,
]
TRAIT_TALENTS = [
    c.tv.red,
    c.tv.floating,
    c.tv.dark,
    c.tv.metal,
    c.tv.angel,
    c.tv.alien,
    c.tv.zombie,
    c.tv.relic,
    c.tv.white,
    c.tv.aku,
]
REMOVED_TALENTS = [
    c.tv.witch,
    c.tv.eva,
    c.tv.collosus_slayer,
    c.tv.behemother_slayer,
]
ABILITIES = [
    c.tv.weaken,
    c.tv.freeze,
    c.tv.slow,
    c.tv.attack_only,
    c.tv.strong,
    c.tv.resist,
    c.tv.massive,
    c.tv.kb,
    c.tv.warp,
    c.tv.strengthen,
    c.tv.lethal,
    c.tv.base_destroyer,
    c.tv.crit,
    c.tv.zkill,
    c.tv.barrier_break,
    c.tv.bounty,
    c.tv.wave,
    c.tv.rweaken,
    c.tv.rfreeze,
    c.tv.rslow,
    c.tv.rkb,
    c.tv.rwave,
    c.tv.wave_block,
    c.tv.rwarp,
    c.tv.cost_down,
    c.tv.recharge,
    c.tv.speed,
    c.tv.improved_kb,
    c.tv.icurse,
    c.tv.rcurse,
    c.tv.iweaken,
    c.tv.ifreeze,
    c.tv.islow,
    c.tv.ikb,
    c.tv.iwave,
    c.tv.iwarp,
    c.tv.savage,
    c.tv.dodge,
    c.tv.rtoxic,
    c.tv.itoxic,
    c.tv.rsurge,
    c.tv.isurge,
    c.tv.surge,
    c.tv.shield_pierce,
    c.tv.soulstrike,
    c.tv.curse,
    c.tv.tba,
    c.tv.miniwave,
    c.tv.minisurge,
    c.tv.sage_slayer, #should it?
    c.tv.explosion,
    c.tv.counter_surge,
    c.tv.iexplosion,
]
DUPLICATE_TALENTS = [ #talents that actually have effects when duplicated, not in any particular
    c.tv.attack,
    c.tv.health,
    c.tv.weaken,
    c.tv.freeze,
    c.tv.slow,
    c.tv.kb,
    c.tv.warp,
    c.tv.strengthen,
    #c.tv.lethal, #technically this could but 90% of the time it wont
    c.tv.crit, #these should count if the chance is already 100%
    c.tv.barrier_break, #^
    c.tv.wave, #is it?
    c.tv.rweaken,
    c.tv.rfreeze,
    c.tv.rslow,
    c.tv.rkb,
    c.tv.rwave,
    c.tv.rwarp,
    c.tv.cost_down,
    c.tv.recharge,
    c.tv.speed,
    c.tv.improved_kb,
    c.tv.rcurse,
    c.tv.savage,
    c.tv.dodge,
    c.tv.rtoxic,
    c.tv.rsurge,
    c.tv.surge, #is it?
    c.tv.shield_pierce, #also shouldnt count if its 100%
    c.tv.curse,
    c.tv.tba,
    c.tv.miniwave,
    c.tv.minisurge,
    c.tv.explosion, #is it?
]
ATTRIBUTE_WEIGHT = 20
TRAIT_WEIGHT = 7
ABILITY_WEIGHT = 4
STACK_POORLY_WEIGHT = 2
STACK_POORLY = [ #these are talents which kinda stack poorly and should have their chance decreased but not turned off after first obtained
    c.tv.crit,
    c.tv.barrier_break,
    c.tv.shield_pierce,
]
ORB_TO_TALENT_RATE = 20
TALENT_TO_ORB_RATE = 8






#fuck you python
arrays_to_fix = [STAT_TRAITS,ATTRIBUTES,TRAIT_TALENTS,REMOVED_TALENTS,ABILITIES,DUPLICATE_TALENTS,STACK_POORLY]
for array in arrays_to_fix:
    for x in range(0,len(array)):
        array[x] = int(array[x])










def randomize_talents(config=DEFAULT_CONFIG,version_config=DEFAULT_VC_CONFIG,log=None):
    """  """
    #not assigning specific config values yet
    do_randomization = True
    if not do_randomization:
        return
    hp_attack_talents_included = True
    trait_talents_included = True
    ability_talents_included = True
    orbs_included = True
    allow_duplicate_talents = True
    #all units get talents params
    all_unit_talent_number = 0
    all_unit_talent_is_minimum = True
    #version config
    max_talent_id_number = 0
    cat_forms = [] #this is 1
    #traits enabled
    (allowed_stat_traits,allowed_talent_traits) = _get_allowed_traits(config=config)
    non_unit_specific_pool = _get_allowed_talent_pools(hp_attack_talents_included,trait_talents_included,ability_talents_included,allowed_talent_traits)
    #now get the unit stats according to version config
    cat_stats = gf.get_cat_stats()
    for u_id in range(0,len(cat_stats)):
        if u_id < len(cat_forms):
            while len(cat_stats[u_id]) > cat_forms[u_id]:
                cat_stats[u_id].pop()
    #





def _get_allowed_talent_pools(hpattack:bool,trait_talents:bool,abilities:bool,talent_traits_of_traits_enabled:list):
    """ return (hp_attack_pool,trait_talent_pool,ability_pool)
    \n """
    if hpattack: hp_attack_pool = copy.deepcopy(ATTRIBUTES)
    else: hp_attack_pool = []
    if trait_talents: trait_talent_pool = copy.deepcopy(talent_traits_of_traits_enabled)
    else: trait_talent_pool = []
    if abilities: ability_pool = copy.deepcopy(ABILITIES)
    else: ability_pool = []
    return (hp_attack_pool,trait_talent_pool,ability_pool)

def _get_allowed_traits(config=DEFAULT_CONFIG):
    """ return (allowed_stat_traits, allowed_talent_traits)
    \n gets the allowed stat traits and talent traits based on config """
    inc_traits = config["trait"]["included"]
    #now add the bools in the same order as in talent traits
    trait_bools = [
        inc_traits["red"],
        inc_traits["floating"],
        inc_traits["dark"],
        inc_traits["metal"],
        inc_traits["angel"],
        inc_traits["alien"],
        inc_traits["zombie"],
        inc_traits["relic"],
        inc_traits["white"],
        inc_traits["aku"],
    ]
    allowed_stat_traits = []
    allowed_talent_traits = []
    for x in range(0,len(trait_bools)):
        if trait_bools[x]:
            allowed_stat_traits.append(STAT_TRAITS[x])
            allowed_talent_traits.append(TRAIT_TALENTS[x])
    return (allowed_stat_traits,allowed_talent_traits)






def _do_single_units_talents(
        existing_talents:list[int|list[int]],
        all_unit_talent_number:int,
        all_unit_talent_minimum:bool,
        full_pool:list,
        highest_preversion_talent_id:int,
        units_stats:list,#technically, the way its done makes talents added after version not consider forms added after version either but I dont give a shit
        version_config:dict,
        unit_id:int,
        orb_file:list,
        include_attributes:bool,
        include_traits:bool,
        include_abilities:bool,
        include_orbs:bool,
        r_offset:int,
        allow_dupes:bool,
        is_uber:bool, #only ubers specifically can have ultra talents after all
    ) -> list[int|list[int]]:
    """ return (output_talents,new_orb_file) """
    #first get the info specific to this unit
    (preversion_pool,postversion_pool) = _get_this_units_pool(
        full_pool=full_pool,
        split_talent_id=highest_preversion_talent_id,
        unit_stats=units_stats
    )
    (preversion_orbs,postversion_orbs) = _get_orb_counts(
        version_config=version_config,
        unit_id=unit_id,
        orb_file=orb_file,
    )
    (do_rand,dont_rand,preversion_talents) = _divide_talents_into_groupings(
        existing_talents=existing_talents,
        version_config=version_config,
        attribute=include_attributes,
        trait=include_traits,
        ability=include_abilities,
    )
    #now get the counts for the number of talents and orbs
    (prev_new_talent_number,postv_new_talent_number,prev_orbs,postv_orbs) = _resolve_orb_and_new_talent_counts(
        preversion_orbs=preversion_orbs,
        postversion_orbs=postversion_orbs,
        do_rand_talents=do_rand,
        dont_rand_talents=dont_rand,
        preversion_talents=preversion_talents,
        include_orbs=include_orbs,
        r_offset=r_offset, #this is the first call of r so its fine to leave it untouched
        all_unit_talent_minimum=all_unit_talent_minimum,
        all_unit_talent_number=all_unit_talent_number,
    )
    #in order to get the new talents we first must get the old talents
    prev_old_talents = []
    postv_old_talents = []
    for each in dont_rand:
        if each in preversion_talents: prev_old_talents.append(each)
        else: postv_old_talents.append(each)
    #now get the new talents
    prev_new_talent_ids = _get_new_talents(
        number_of_new_talents=prev_new_talent_number,
        already_existing_talent_ids=prev_old_talents,
        allow_dupes=allow_dupes,
        r_offset=r_offset+303,#this is the second calling of r offset, this should be fine?
        unit_pool=preversion_pool
    ) 
    postv_new_talent_ids = _get_new_talents(
        number_of_new_talents=postv_new_talent_number,
        already_existing_talent_ids=prev_old_talents+postv_old_talents+prev_new_talent_ids,
        allow_dupes=allow_dupes,
        r_offset=r_offset+967,#really going big on this one
        unit_pool=postversion_pool
    )
    #now we need to get the actual talent blocks for all those
    prev_new_talent_blocks = _create_talent_blocks_from_ids(prev_new_talent_ids,units_stats)
    postv_new_talent_blocks = _create_talent_blocks_from_ids(postv_new_talent_ids,units_stats)
    (non_ultra_talents,ultra_talents) = _get_old_talents(existing_talents,do_rand)
    #now we need order them
    (ordered_talents,orb_ultra_after) = _order_talents(
        old_talents=non_ultra_talents,
        ultra_old_talents=ultra_talents,
        prev_new_talents=prev_new_talent_blocks,
        postv_new_talents=postv_new_talent_blocks,
        is_uber=is_uber,
    )
    #now get the first two integers
    output_talents = [unit_id]
    if len(existing_talents) > 1:
        output_talents.append(existing_talents[1]) #is this right? do I want that to not be changed by anything in here
    else:
        output_talents.append(0)
    output_talents.extend(ordered_talents)
    #now do orbs
    new_orb_file = _edit_orbs(
        orb_file=orb_file,
        total_orb_count=prev_orbs+postv_orbs,
        ultra_after=orb_ultra_after,
        unit_id=unit_id
    )
    return (output_talents,new_orb_file)






def _get_this_units_pool(full_pool:list,split_talent_id:int,unit_stats:list):
    """ return (preversion_pool,postversion_pool)
    \n gets the two talent pools allowed for this unit by restricting things the unit has in stats 
    \n assumes full pool is sorted already (it should be)"""
    allowed_unit_pool = copy.deepcopy(full_pool)
    #start by removing everything from this pool blocked by a units actual stats
    for form_id in range(2,len(unit_stats)):
        this_form_blocked = _get_unit_blocked_talents(unit_stats[form_id])
        for each in this_form_blocked:
            if each in allowed_unit_pool:
                allowed_unit_pool.remove(each)
    #now separate into pre and post version
    preversion_pool = copy.deepcopy(allowed_unit_pool)
    postversion_pool = copy.deepcopy(allowed_unit_pool)
    #now remove past the highest allowed thing from the preversion pool
    highest_allowed = int(split_talent_id)
    while highest_allowed not in preversion_pool and highest_allowed > 0:
        highest_allowed -= 1
    if this_index in preversion_pool: #check in case it failed
        this_index = preversion_pool.index(highest_allowed)
        preversion_pool = preversion_pool[:this_index+1]
    else:
        preversion_pool = []
    return (preversion_pool,postversion_pool)
    
def _get_unit_blocked_talents(form_stats:list):
    """ gets the ids of talents to be blocked according to the stats of this form """
    blocked_talents = []
    #start by looping through traits
    for x in range(0,len(STAT_TRAITS)):
        if form_stats[STAT_TRAITS[x]] == 1:
            blocked_talents.append(TRAIT_TALENTS[x])
    #immunities
    if form_stats[c.s.kb_immune] == 1:
        blocked_talents.extend([c.tv.ikb,c.tv.rkb])
    if form_stats[c.s.weaken_immune] == 1:
        blocked_talents.extend([c.tv.iweaken,c.tv.rweaken])
    if form_stats[c.s.slow_immune] == 1:
        blocked_talents.extend([c.tv.islow,c.tv.rslow])
    if form_stats[c.s.freeze_immune] == 1:
        blocked_talents.extend([c.tv.ifreeze,c.tv.rfreeze])
    if form_stats[c.s.warp_immune] == 1:
        blocked_talents.extend([c.tv.iwarp,c.tv.rwarp])
    if form_stats[c.s.wave_immune] == 1 or form_stats[c.s.wave_block] == 1:
        blocked_talents.extend([c.tv.iwave,c.tv.rwave])
    if form_stats[c.s.curse_immune] == 1:
        blocked_talents.extend([c.tv.icurse,c.tv.rcurse])
    if form_stats[c.s.surge_immune] == 1:
        blocked_talents.extend([c.tv.isurge,c.tv.rsurge])
    if form_stats[c.s.toxic_immune] == 1:
        blocked_talents.extend([c.tv.itoxic,c.tv.rtoxic])
    if form_stats[c.s.explode_immune] == 1:
        blocked_talents.extend([c.tv.iexplosion,]) #theres no explosion resist currently
    #ability specific
    if form_stats[c.s.attack_only] == 1:
        blocked_talents.append(c.tv.attack_only)
    if form_stats[c.s.barrier_break_chance] == 100:
        blocked_talents.append(c.tv.barrier_break)
    if form_stats[c.s.shield_pierce_chance] == 100:
        blocked_talents.append(c.tv.shield_pierce)
    if form_stats[c.s.base_destroyer] == 1:
        blocked_talents.append(c.tv.base_destroyer)
    if form_stats[c.s.bounty] == 1:
        blocked_talents.append(c.tv.bounty)
    if form_stats[c.s.strong] == 1:
        blocked_talents.append(c.tv.strong)
    if form_stats[c.s.massive] == 1:
        blocked_talents.append(c.tv.massive)
    if form_stats[c.s.resist] == 1:
        blocked_talents.append(c.tv.resist)
    if form_stats[c.s.crit_chance] == 100:
        blocked_talents.append(c.tv.crit)
    if form_stats[c.s.zombie_killer] == 1:
        blocked_talents.append(c.tv.zkill)
    if form_stats[c.s.soul_strike] == 1:
        blocked_talents.append(c.tv.soulstrike)
    if form_stats[c.s.wave_block] == 1:
        blocked_talents.append(c.tv.wave_block)
    if form_stats[c.s.counter_surge] == 1:
        blocked_talents.append(c.tv.counter_surge)
    #fuck you python
    for x in range(0,len(blocked_talents)):
        blocked_talents[x] = int(blocked_talents[x])
    return blocked_talents






def _divide_talents_into_groupings(existing_talents:list,version_config=DEFAULT_VC_CONFIG,attribute:bool=True,trait:bool=True,ability:bool=True) -> tuple[list[int],list[int],list[int]]:
    """ return (do_rand,dont_rand,preversion_talents)
    \n creates arrays containing the talent ids of things """
    #first step, divide them into randomize and not randomize
    do_rand = []
    dont_rand = []
    for x in range(2,len(existing_talents)): #Im assuming it is a talent array
        this_talent_id = existing_talents[x][c.tpos.ability_id]
        #now check which grouping its in
        if this_talent_id in ATTRIBUTES:
            if attribute: do_rand.append(this_talent_id)
            else: dont_rand.append(this_talent_id)
        elif this_talent_id in TRAIT_TALENTS:
            if trait: do_rand.append(this_talent_id)
            else: dont_rand.append(this_talent_id)
        elif this_talent_id in ABILITIES:
            if ability: do_rand.append(this_talent_id)
            else: dont_rand.append(this_talent_id)
        elif this_talent_id in REMOVED_TALENTS:
            do_rand.append(this_talent_id) #Im just gonna always randomize these talents, you dont get a choice
        else:
            #this means its not a logged talent yet
            do_rand.append(this_talent_id) #is this right?
    #now we divide talents into preversion and postversion
    preversion_talents = []
    for x in range(2,len(existing_talents)):
        this_talent_id = existing_talents[x][c.tpos.ability_id]
        unit_id = existing_talents[0]
        if (x-2) <= len(version_config[vck.unit_talent_rand_talent_ids][unit_id])-1: #its -1 because the first entry in version config talents is the traitsum
            preversion_talents.append(this_talent_id)
    #thats actually all for here
    return (do_rand,dont_rand,preversion_talents)

def _get_orb_counts(version_config=DEFAULT_VC_CONFIG,unit_id:int=0,orb_file:list[list]=None) -> tuple[int,int]:
    """ return (preversion_orbs,postversion_orbs)
    \n gets the preversion and postversion orb counts of a unit """
    #Im actually not gonna consider the ultra status of orbs I think, just the raw count
    preversion_orbs = 0
    postversion_orbs = 0
    if len(version_config[vck.unit_talent_rand_orb_counts]) > unit_id: #cant count it if it was past the logged amount
        preversion_array = version_config[vck.unit_talent_rand_orb_counts][unit_id]
        preversion_orbs = (preversion_array[0] + preversion_array[1])
    for line in orb_file:
        if line[0] == unit_id:
            postversion_orbs = line[1]
    #thats all
    return (preversion_orbs,postversion_orbs)

def _get_new_talents(number_of_new_talents:int,already_existing_talent_ids:list,allow_dupes:bool,r_offset:int,unit_pool:list) -> list[int]:
    """ gets a list of the new talent ids to put on a unit """
    pool = copy.deepcopy(unit_pool)
    used_talent_ids = copy.deepcopy(already_existing_talent_ids)
    #first step is creating the weighted list to use for the pool
    pool_weights = [0]*len(pool)
    for x in range(0,len(pool_weights)):
        this_id = pool_weights[x]
        if not allow_dupes and this_id in used_talent_ids:
            pool_weights[x] = 0
        elif this_id in ATTRIBUTES:
            pool_weights[x] = ATTRIBUTE_WEIGHT
        elif this_id in TRAIT_TALENTS: #Im assuming all trait talents that cant be obtained have been removed from pool before this
            pool_weights[x] = TRAIT_WEIGHT
        elif this_id in ABILITIES:
            pool_weights[x] = ABILITY_WEIGHT
        else: #what happened here
            pool_weights[x] = 0 #it actually already is 0
    #now we get the correct number of talents
    new_talent_ids = []
    r = srand.randinst(r_offset)
    for x in range(0,number_of_new_talents):
        #first select the new talent to give
        new_talent_index = r.weighted_list(pool_weights)
        new_talent = pool[new_talent_index]
        #now select that talent and if desired set further weight to 0, or if it stacks poorly just reduce the weight
        new_talent_ids.append(new_talent)
        if not allow_dupes:
            pool_weights[new_talent_index] = 0
        elif new_talent in STACK_POORLY:
            pool_weights[new_talent_index] = STACK_POORLY_WEIGHT
    return new_talent_ids
    
def _get_old_talents(existing_talents:list,do_rand:list):
    """ return (non_ultra_talents,ultra_talents)
    \n gets the blocks of talents on a unit that are not being changed """
    non_ultra_talents = []
    ultra_talents = []
    for x in range(2,len(existing_talents)):
        this_ability = existing_talents[x][c.tpos.ability_id]
        if this_ability not in do_rand:
            if existing_talents[x][c.tpos.limit] == 0:
                non_ultra_talents.append(copy.deepcopy(existing_talents[x]))
            elif existing_talents[x][c.tpos.limit] == 1:
                ultra_talents.append(copy.deepcopy(existing_talents[x]))
            else:
                print("talent not considered ultra or not?: ")
                print(existing_talents[x])
    return (non_ultra_talents,ultra_talents)


def _resolve_orb_and_new_talent_counts(preversion_orbs:int,postversion_orbs:int,do_rand_talents:list,dont_rand_talents:list,preversion_talents:list,include_orbs:bool,r_offset:int,all_unit_talent_minimum:bool,all_unit_talent_number:int):
    """ return (prev_new_talents,postv_new_talents,prev_orbs,postv_orbs) """
    #now get the number of talents and orb
    old_talent_count = 0
    new_talent_count = 0
    postversion_old_talent_count = 0 #this is never used
    postversion_new_talent_count = 0
    for each in do_rand_talents:
        if each in preversion_talents:
            new_talent_count += 1
        else:
            postversion_new_talent_count += 1
    for each in dont_rand_talents: 
        if each in preversion_talents:
            old_talent_count += 1
        else:
            postversion_old_talent_count += 1
    #nows the time to do all unit talents counts, do it with only preversion talents
    if all_unit_talent_minimum:
        if old_talent_count + new_talent_count < all_unit_talent_number:
            new_talent_count = all_unit_talent_number - old_talent_count #make it so it will end up with the correct number of talents
    else: #so if it isnt a minimum
        new_talent_count += all_unit_talent_number #just raw give it that many new talents
    #now handle orbs becoming talents and talents becoming orbs
    if include_orbs:
        #orb half
        orb_r = srand.randinst(r_offset)
        orb_to_talent_count = 0
        for x in range(0,preversion_orbs):
            if orb_r.randrange(0,100) < ORB_TO_TALENT_RATE:
                orb_to_talent_count += 1
        postversion_orb_to_talent_count = 0
        for x in range(0,postversion_orbs):
            if orb_r.randrange(0,100) < ORB_TO_TALENT_RATE:
                postversion_orb_to_talent_count += 1
        #talent half
        talent_r = srand.randinst(r_offset+99)
        talent_to_orb_count = 0
        for x in range(0,new_talent_count):
            if talent_r.randrange(0,100) < TALENT_TO_ORB_RATE:
                talent_to_orb_count += 1
        postversion_talent_to_orb_count = 0
        for x in range(0,postversion_new_talent_count):
            if talent_r.randrange(0,100) < TALENT_TO_ORB_RATE:
                postversion_talent_to_orb_count += 1
        #now update the counts
        preversion_orbs += (talent_to_orb_count-orb_to_talent_count)
        new_talent_count += (orb_to_talent_count-talent_to_orb_count)
        postversion_orbs += (postversion_talent_to_orb_count-postversion_orb_to_talent_count)
        postversion_new_talent_count += (postversion_orb_to_talent_count-postversion_talent_to_orb_count)
    #now give the variables reasonable names for understanding outside this function
    prev_orbs = preversion_orbs
    postv_orbs = postversion_orbs
    prev_new_talents = new_talent_count
    postv_new_talents = postversion_new_talent_count
    return (prev_new_talents,postv_new_talents,prev_orbs,postv_orbs)

def _order_talents(
        old_talents:list,
        ultra_old_talents:list,
        prev_new_talents:list, #fully used
        postv_new_talents:list, #fully used
        preversion_old_ids:list,
        is_uber:list,
        include_orbs:bool, #this is here because if orbs arent included the minimum non ultra orb should be 1, while if they are on it should be 0 I feel
    ):
    """ (sorted_talents,ultra_orb_after)
    \n orders and assigns ultra status to talents and returns the array of blocks """
    #I hate this
    #split the old ultra and not into 4
    preversion_old_talents = [] #fully used
    postversion_old_talents = [] #fully used
    preversion_ultra_old_talents = [] #fully used
    postversion_ultra_old_talents = [] #fully used
    for each in old_talents:
        if each[c.tpos.ability_id] in preversion_old_ids:
            preversion_old_talents.append(each)
        else:
            postversion_old_talents.append(each)
    for each in ultra_old_talents:
        if each[c.tpos.ability_id] in preversion_old_ids:
            preversion_ultra_old_talents.append(each)
        else:
            postversion_ultra_old_talents.append(each)
    #separate into ultra and not, keeping prev and postv separate for now
    new_ultra = []
    new_nonultra = []
    postv_new_ultra = []
    postv_new_nonultra = []
    #fill out the arrays with the old preversions first
    new_nonultra.extend(preversion_old_talents)
    new_ultra.extend(preversion_ultra_old_talents)
    #now fill out them with the new talents adding half to ultra talents after 5
    for each in prev_new_talents:
        if len(new_nonultra) - len(new_ultra) >= 5:
            new_ultra.append(each) #add once theres 5 non ultra talents
        else:
            new_nonultra.append(each)
    #now do the same process but for postv talents
    postv_new_nonultra.extend(postversion_old_talents)
    postv_new_ultra.extend(postversion_ultra_old_talents)
    for each in postv_new_talents:
        if len(postv_new_nonultra) - len(postv_new_ultra) >= 5:
            postv_new_ultra.append(each)
        else:
            postv_new_nonultra.append(each)
    #now we actually handle the ultra status of each talent
    non_ultra_value = 0
    ultra_value = 0
    if is_uber:
        ultra_value = 1

    for each in new_nonultra:       each[c.tpos.limit] = non_ultra_value
    for each in new_ultra:          each[c.tpos.limit] = ultra_value
    for each in postv_new_nonultra: each[c.tpos.limit] = non_ultra_value
    for each in postv_new_ultra:    each[c.tpos.limit] = ultra_value
    #now get the orb count
    min_orb_count = 1
    if include_orbs: min_orb_count = 0
    ultra_orb_after = max(6-len(prev_new_talents),min_orb_count) #so basically if theres 5 talents the first orb is fine, second is not, but for each less talent there is the more orbs are free
    if not is_uber:
        ultra_orb_after = -1 #just mog it
    #now the positions have to be set, they cant be changed by version updates (however they are changed wildly by changes to talent configs, that seems problematic)
    sorted_talents = new_nonultra + new_ultra + postv_new_nonultra + postv_new_ultra
    return (sorted_talents,ultra_orb_after)

def _edit_orbs(orb_file:list,total_orb_count:int,ultra_after:int,unit_id:int):
    """ edits the line for this unit to have the correct information and returns it """
    #dont feel like fucking with python
    orb_file = copy.deepcopy(orb_file)
    #start by finding the correct line to work with it one already exist
    relevant_line = -1
    for line in range(0,len(orb_file)):
        if orb_file[line][0] == unit_id:
            relevant_line = line
    #add it if it doesnt exist
    if relevant_line == -1:
        orb_file.append([unit_id,0])
    #now remove the line if orb count is 0
    if total_orb_count == 0:
        orb_file.pop(relevant_line)
    else:
        #now set the orb count
        orb_file[relevant_line][1] = total_orb_count
        #now for each orb set the status of it? is this how the file even works?
        #start by removing any already existing information
        while len(orb_file[relevant_line]) > 2:
            orb_file[relevant_line].pop(-1)
        #now we can just add each orb
        for x in range(0,total_orb_count):
            if ultra_after == -1 or x < ultra_after:
                orb_file[relevant_line].append(0)
            else:
                orb_file[relevant_line].append(1)
    #das all
    return orb_file

def _create_talent_blocks_from_ids(talent_ids:list,unit_stats:list):
    """ creates a block for each talent in talent_ids and returns an array of those blocks """
    #it prefers the third form but if no third form it just uses the last form
    if len(unit_stats) > 2:
        form_stats = unit_stats[2]
    else:
        form_stats = unit_stats[-1]
    #something here



    output_array = []
    return output_array















