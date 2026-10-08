
from ....config.defaults import DEFAULT_CONFIG
from ....config.version_config.get_version_config import DEFAULT_VC_CONFIG
from ....config.version_config import version_config_keys as vck
from ....randomizer import debug_output
from ..enemy_swap import create_swap
from ..enemy_swap import initialize_information
from ..enemy_swap import stat_calcs
from ..enemy_swap import stage_editor
import tadbcmc.core.file_handler as fh


APP_SWAP_CACHE_FILE_NAME = "enemy_app_swap.csv"
DEBUG_APP_SWAP_CACHE_FILE_NAME = "debug_enemy_app_swap.csv"



def do_enemy_swap(config=DEFAULT_CONFIG,version_config=DEFAULT_VC_CONFIG,log=None,debug=False):
    """ does all the enemy swap stuff from config """
    cinfo = config["enemy"]["randomization"]
    rand_type = cinfo["type"].lower()
    do_var_swap = cinfo["variant_swap"]
    do_gen_swap = cinfo["general_swap"]
    #first exit is for neither per game nor per stage
    if not (rand_type == "per game" or rand_type == "per stage"):
        return
    if not (do_var_swap or do_gen_swap):
        debug_output.output_somewhere("enemy swap was on without variant or general swap, enemies will not be swapped",log=log)
        return
    #make sure initialize has the correct information
    initialize_information.establish_working_information()
    #now the rest of config options
    maintain_class = cinfo["keep_class"]
    consider_strength = cinfo["consider_strength"]
    adjust_mags = cinfo["adjust_magnifications"]
    include_eoc = cinfo["include_eoc"]
    breaking_point = version_config[vck.enemy_swap_max_enemy_id]

    #ok time to split into per game and per stage funcs
    if rand_type == "per game":
        _per_game_swap(
            breaking_point=breaking_point,
            do_var_swap=do_var_swap,
            do_gen_swap=do_gen_swap,
            maintain_class=maintain_class,
            consider_strength=consider_strength,
            adjust_mags=adjust_mags,
            include_eoc=include_eoc,
            log=log,debug=debug
        )




def _per_game_swap(
        breaking_point:int,
        do_var_swap:bool,
        do_gen_swap:bool,
        maintain_class:bool,
        consider_strength:bool,
        adjust_mags:bool,
        include_eoc:bool,
        log=None,
        debug:bool=False,
    ) -> None:
    #first create the swap
    swap = create_swap.create_swap(
        breaking_point=breaking_point,
        do_var_swap=do_var_swap,
        do_gen_swap=do_gen_swap,
        maintain_class=maintain_class,
        consider_strength=consider_strength,
        log=log,debug=debug,
    )
    #now make it an app swap
    app_swap = stat_calcs.convert_swap_to_app_swap(swap,balance_mags=adjust_mags)
    #now we cache that for both debug purposes and potential later use
    fh.write_file_to_cache(APP_SWAP_CACHE_FILE_NAME,app_swap,type=list[list])
    if debug:
        _debug_write_app_swap_to_cache(app_swap)
    #stage_editor.apply_app_swap_to_stages(app_swap,include_eoc,log=log,debug=debug)




















def _debug_write_app_swap_to_cache(app_swap):
    """ writes a modified version of app swap to file """
    mod_app_swap = [] #its just slapping the unit id in front of it
    for u_id in range(0,len(app_swap)):
        this_entry = [u_id-2]
        this_entry.extend(app_swap[u_id])
        this_entry[1] -= 2
        mod_app_swap.append(this_entry)
    #now write to file
    fh.write_file_to_cache(DEBUG_APP_SWAP_CACHE_FILE_NAME,mod_app_swap,type=list[list])







