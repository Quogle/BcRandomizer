
from ....config.defaults import DEFAULT_CONFIG
from ....config.version_config.get_version_config import DEFAULT_VC_CONFIG
from tadbcmc.data.collated_info.enemy_info import *
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
import tadbcmc.data.enums.unit_info as ui
import tadbcmc.data.enums.enemy as e
import tadbcmc.core.simple_funcs as simp

"""
notes on enemy class values
0 unlogged,
all have another stat of 'spammability'
peon,
frontliner, subdivided into (pusher (what does this really mean), rusher (?), sauceless (theyre just low range slop like seal sael hyppoh and so on, theyre largely interchangable), freak (kory))
midranger,
backliner,


peons: no fuckin john clue

frontliners:
a pusher is something that generally has a lot of hp per kb and attacks often 
    rost/bore/otter/some cyclones?/fish/
a rusher is something fast with lots of kbs and fast attacks
    sbk/gories/some bunbuns/
a wall is something with a lot of hp per kb but for some reason it doesnt really push 
    duche/dagshund/wall zdoge/helmut/
a freak is something with an aspect that makes it not cleanly fit into other categories (like kories wave)

midrangers:
a nukers, things with big damage per hit
    owlbrowl/teacher bear/chickfula/face/cappy/rain d
pusher
    sleipnir/fenrir/zombear/ctitan/lemurr?/puffers?(dunno what to do with puffer/tapir/daboo type units)
other idk
    ctank/hnah/caxe/im face/bondage/valk/toucan/cmoneko/

backliners:
a slow backliner is something that attacks relatively slowly
    sloth/clionel/nyandam/le grim/hannya
a fast backliner is something that attacks relatively quickly
    master a/calamary/calamaria?/perfect cyclone/alpacky/ururun?
a pushing backliner is something, generally through omni or something else that makes it hit beyond its own range, that pushes
    okame/wahwah/socrates?/scissorex/luza/clionel wow this is just advents and bosses/othom?/dogu/
sniper is something which isnt really meant to target things close to it or what its targetting but instead things beyond that
    henry/tackey/croakly/chibinel/dolphina/moles/turkey?/eel/





"""









""" ENEMY_INFO functions """
def establish_working_information():
    """ makes ENEMY_INFO the length of vanilla enemy stats
    \n to be called once game files exist to prevent import failure """
    ENEMY_INFO_extend_w_defaults()

#its called in create_swap.create_swap()
def _set_ENEMY_INFO_values():
    """ sets ENEMY_INFO to have the correct values for variants and included """
    global ENEMY_INFO
    vstat = gf.file_reader(fn.ENEMY_STATS,vanilla=True)
    for u_id in range(0,len(ENEMY_INFO)):
        included_in_swap = True
        #things that should disallow it from being included,
        #collab
        #removed/unused
        #non attacking enemy base, (determined by 0 speed and < 140 range if it isnt manually logged)
        #first we need to determine the enemy base status of non manually logged things
        if u_id < len(vstat) and ENEMY_INFO[u_id][ui.e.manually_input] == 0:
            if vstat[u_id][e.s.speed] == 0:
                if vstat[u_id][e.s.range] < 140:
                    ENEMY_INFO[u_id][ui.e.variant_id] = ui.enemy_variant.attackless_base
                else:
                    if vstat[u_id][e.s.dojoBase] != 0: ENEMY_INFO[u_id][ui.e.variant_id] = ui.enemy_variant.dojo_base
                    else: ENEMY_INFO[u_id][ui.e.variant_id] = ui.enemy_variant.attacking_base
                    
        if ENEMY_INFO[u_id][ui.e.manually_input] == 0:
            #all non manually input things get set to swap strength 50
            ENEMY_INFO[u_id][ui.e.swap_strength] = 50
        #now we can actually work with it
        this_ei = ENEMY_INFO[u_id] #passing by reference :scream:
        if this_ei[ui.e.collab] > 0:
            included_in_swap = False
        if this_ei[ui.e.unused] != 0:
            included_in_swap = False
        if this_ei[ui.e.variant_id] == int(ui.enemy_variant.attackless_base):
            included_in_swap = False
        if this_ei[ui.e.variant_id] == int(ui.enemy_variant.cake):
            included_in_swap = False
        #ok now set it
        if included_in_swap:
            ENEMY_INFO[u_id][ui.e.included_in_swap] = 1



""" making the initial swap """

def harvest_unit_info_from_ENEMY_INFO(prefered_ENEMY_INFO:list[list]=None,maintain_class:bool=True) -> tuple[list[bool],list[int],list[int]]:
    """ return (included_in_swap_list, swap_strength_list, variant_id_list)
    \n gets the initial information from ENEMY_INFO, can be requested to use a specific version aside from global """
    #get the correct enemy info 2d list to use
    enemy_info = prefered_ENEMY_INFO
    if enemy_info == None:
        global ENEMY_INFO
        enemy_info = ENEMY_INFO
    #make the lists
    included_in_swap_list = []
    swap_strength_list = []
    variant_id_list = []
    for u_id in range(0,len(enemy_info)):
        included_in_swap_list.append(enemy_info[u_id][ui.e.included_in_swap])
        variant_id_list.append(enemy_info[u_id][ui.e.variant_id])
        this_effective_swap_strength = enemy_info[u_id][ui.e.swap_strength]

        swap_strength_list.append(this_effective_swap_strength)
    #return them
    return (included_in_swap_list,swap_strength_list,variant_id_list)

def _adjust_strength_based_on_class(strength,this_class,maintain_class):
    """ because the numbers for class values are not linearly based on strength this must be adjusted semi arbitarily """
    if maintain_class:
        strength += 1000*this_class
    else:
        pass
    return strength



def variant_list_dict_maker(variant_id_list:list[int],included_bool_list:list[bool],split_id:int=0):
    """ makes a dictionary with keys of variant ids, and values of a list of unit ids of that variant included in swap
    \n returns (first_half, second_half) 
    \n if theres no split point (id=-1) it shoves everything in second half """
    first_half = {}
    second_half = {}
    for u_id in range(0,len(variant_id_list)):
        this_variant_id = str(variant_id_list[u_id])
        if this_variant_id != "0" and included_bool_list[u_id]:
            if u_id < split_id:
                if this_variant_id not in first_half:
                    first_half[this_variant_id] = []
                first_half[this_variant_id].append(u_id)
            else:
                if this_variant_id not in second_half:
                    second_half[this_variant_id] = []
                second_half[this_variant_id].append(u_id)
    #now remove all with only one unit in them
    queue_to_remove = []
    for each in first_half:
        if len(first_half[each]) < 2: queue_to_remove.append(each)
    for each in queue_to_remove:
        first_half.pop(each)
    queue_to_remove = []
    for each in second_half:
        if len(second_half[each]) < 2: queue_to_remove.append(each)
    for each in queue_to_remove:
        second_half.pop(each)
    #ok good to return
    return (first_half,second_half)


""" selection arrays """

def _get_difference_scalor_array(consider_strength=True) -> list[float]:
    """ gets the strength difference array to scale the chance of groups by
    \n index in array is the difference between the swap strengths
    \n len(array) = 11 """
    balance_scalor = []
    for x in range(0,10):
        scale = 1/((0.9 + 0.20*x)**2)-0.01*x
        balance_scalor.append(scale)
    balance_scalor.append(0) #this is so anything outside the range can just call to -1 and it nullifies the chance
    if not consider_strength: #set all proportions to 1
        for x in range(0,len(balance_scalor)):
            balance_scalor[x] = 1
    return balance_scalor
    """ relative proportions when considering strength:
    0:1.23x
    1:0.82x
    2:0.57x
    3:0.41x
    4:0.31x
    5:0.23x
    6:0.17x
    7:0.12x
    8:0.08x
    9:0.047x
    10:0x
    """

def get_base_chance_mult_dict(
        incomplete_swap:list[int], #this is used to make it so only strengths that are actually available for using in this half are considered
        swap_strength_list:list[int], #
        maintain_class:bool, #locks chances to groups of 10
        consider_strength:bool #makes it scale based on distance
    ) -> dict[int,dict[int,float]]:
    """ gets the chance mult dict for each swap strength actually used in this swap half """
    #first get the diff scalor
    difference_scalor = _get_difference_scalor_array(consider_strength=consider_strength)
    #now get which swap strengths even exist
    used_swap_strengths = []
    for x in range(0,len(incomplete_swap)):
        if incomplete_swap[x] == -1: #so if it actually matters
            if swap_strength_list[x] not in used_swap_strengths:
                used_swap_strengths.append(swap_strength_list[x])
    used_swap_strengths.sort()
    #now start the process of making the output dict
    base_chance_dict = {}
    for swap_strength in used_swap_strengths:
        if maintain_class: #separate it into only strengths within a range of 30
            lower_bound = 10*int(swap_strength/10)-20
            upper_bound = lower_bound + 30
        else:
            lower_bound = simp.clamp(swap_strength - 9,used_swap_strengths[0],used_swap_strengths[-1])
            upper_bound = lower_bound + 19
            if not consider_strength: #chaos mode
                lower_bound = used_swap_strengths[0]
                upper_bound = used_swap_strengths[-1] + 1
        #now add all in those bounds that actually exist (no sense having any that dont exist)
        this_chance_dict = {}
        for x in range(lower_bound,upper_bound):
            if x in used_swap_strengths:
                diff = abs(x-swap_strength)
                if diff >= 10:
                    diff = 10
                this_chance_dict[str(x)] = difference_scalor[diff]
        #now scale the total sum of this dict to 1 for some reason I cant remember
        sum = 0
        for each in this_chance_dict: sum += this_chance_dict[each]
        if sum != 0:
            for each in this_chance_dict: this_chance_dict[each] *= (1/sum)
        #set it
        base_chance_dict[str(swap_strength)] = this_chance_dict
    #thats it
    return base_chance_dict








