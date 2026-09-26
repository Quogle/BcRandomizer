""" this module is what makes the config files for the current version\n
 """
import bcr.randomizer.file_local as fl
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
from ..config import paths
import tadbcmc.data.enums.cats as c
import tadbcmc.core.file_handler as fh
import tadbcmc.pieces.combos as combos
import bcr.apk.breakdown_apk as breakdown_apk
import tadbcmc.core.simple_funcs as simp
import os
from pathlib import Path


#I have no idea what the version config is going to look like

#putting the file names here for now, they can be moved to paths if needed
TALENT_CONFIG = "talent_ids.csv"
UNIT_FORM_CONFIG = "unit_forms.csv"
MISC_INFO_CONFIG = "misc_info.csv"

NUMBER_OF_COMBOS = "number_of_combos"
NUMBER_OF_COMBO_IDS = "number_of_combo_ids"
NUMBER_OF_ZL_CHAPTERS = "number_of_zl_chapters"
NUMBER_OF_CATS = "number_of_cats"
NUMBER_OF_ENEMIES = "number_of_enemies"


#files sofar used in the process
specifics = {
    "local":set((
        fn.TALENT_FILE, #used for getting all currently existing talents
        fn.CAT_GUIDE_DATA, #used for getting current cat forms
        fn.ENEMY_STATS, #used for counting the number of enemies
        fn.COMBO_FILE, #used in getting the number of combos
        fn.COMBO_NAME_DATA, #also used in ^
        fn.COMBO_PARAM, #used in getting the number of combo ids
    ))
}
#now each units file
specifics["local"].add(r"^unit\d{3}\.csv$") #I dont understand this but ok
#now for zl stage files (tadbcmc actually uses stages and not map data for counting maps and stages)
specifics["local"].add(r"^stageRND\d{3}_\d{2}\.csv")
#now each zl stage file 






def harvest_config_info_from_apk(config_version:str):
    """ looks for an apk whose name is <version number>.apk and breaks it down to get the pack files from it
    \n sets the version config for that version to what it finds
    \n example: 15.6.1.apk would result in a config of 15.6.1 based on that apk """
    if os.path.exists(config_version + ".apk"):
        breakdown_apk.breakdown_apk(
            apk_path=config_version + ".apk",
            specifics=specifics,
            get_server_files=False,
            henry_style_output=False,
        )
        #get the actual correct path for config
        if "src" in os.listdir(os.getcwd()): base = Path("src")
        else: base = Path("")
        config_dir = base / paths.VERSIONCONFIGS / config_version
        config_dir.mkdir(parents=True,exist_ok=True)
        #now do it
        _make_config_for_version_from_game_files(config_dir)
    else:
        print("couldnt find " + config_version + ".apk in " + __path__ + ", resolve and try again")








def _make_config_for_version_from_game_files(config_version_path:Path):
    """ uses the current gamefiles to make the config for the input version """
    #these dont need to be in any particular order
    _write_misc_info_to_file(config_version_path)
    _get_talent_ids(config_version_path)
    _get_unit_forms(config_version_path)




#NONE
def _write_misc_info_to_file(config_version_path:Path
    ) -> None:
    """ writes all the single bits of information to the same file """
    filepath = config_version_path / MISC_INFO_CONFIG
    info = []
    #now add each bit of info to it
    info.append([NUMBER_OF_COMBOS,_get_number_of_combos()])
    info.append([NUMBER_OF_COMBO_IDS,_get_number_of_combo_ids()])
    info.append([NUMBER_OF_ZL_CHAPTERS,_get_zl_subchapter_counts()])
    info.append([NUMBER_OF_CATS,_get_unit_count()])
    info.append([NUMBER_OF_ENEMIES,_get_enemy_count()])


    #now write it
    fh.array_to_array_type_file_writer(str(filepath),info)



""" Units """

#NONE
def _get_talent_ids(config_version_path:Path
    ) -> None:
    """ logs the talent ability ids for all units and writes them to the current versions config """
    #first step is get the correct filepath to store the information in
    #for now Im just open combining version as a string
    filepath = config_version_path / TALENT_CONFIG
    #ok now the real func can begin
    talents = gf.get_talents(vanilla=True)
    #first get the highest unit id with talents
    highest_unit_id = 0
    for line in talents:
        if line[c.tpos.unit_id] > highest_unit_id:
            highest_unit_id = line[c.tpos.unit_id]
    #now make the talent array with that many entries
    versions_talents = []
    for x in range(0,highest_unit_id+1):
        versions_talents.append([])
    #now go through the talents adding the id of all abilities to the unit_ids index
    for line in talents:
        current_unit_id = line[c.tpos.unit_id]
        for block in range(2,len(line)):
            versions_talents[current_unit_id].append(line[block][c.tpos.ability_id])
    #now write them to file
    fh.array_to_array_type_file_writer(str(filepath),versions_talents)

#NONE
def _get_unit_forms(config_version_path:Path
    ) -> None:
    """ logs the unit forms from nyankobook for all units and writes them to the current versions config """
    #first step is get the correct filepath to store the information in
    #for now Im just open combining version as a string
    filepath = config_version_path / UNIT_FORM_CONFIG
    #get the nyankobook file
    nyankobook = gf.file_reader(fn.CAT_GUIDE_DATA,vanilla=True)
    #forms is contained on the third column
    cat_forms = []
    for x in range(0,len(nyankobook)):
        cat_forms.append(nyankobook[x][2])
    #now write that one 1d array to file
    fh.array_to_array_type_file_writer(str(filepath),[cat_forms])

#INT
def _get_unit_count(
    ) -> int:
    """ returns the current number of unit files """
    cat_stats = gf.get_cat_stats(vanilla=True)
    return len(cat_stats)

""" Enemies """
#INT
def _get_enemy_count(
    ) -> int:
    """ returns the number of enemies """
    stats = gf.file_reader(fn.ENEMY_STATS,vanilla=True)
    return len(stats)


""" Stages """
#INT
def _get_zl_subchapter_counts(
    ) -> int:
    """ Reads the current number of zl subchapters and returns in """
    #just use the count dict for this
    stage_count_dict = gf.get_number_of_stages_in_groups(update_counts=True)
    zl = stage_count_dict[fn.ZL_MLETTER]
    return len(zl)

""" Combos """
#INT
def _get_number_of_combos(
    ) -> int:
    """ returns the number of combos existent in this version
    \n writes to dl in the process """
    #first use tadbcmc to get only the actually visible combos as those are the only ones ever worked with
    #Im making the assumption that combos are only ever added to the bottom of the file, and never in this middle
    (combo_data,combo_names) = combos.readd_all_visible_vanilla_combos()
    return len(combo_data)

#INT
def _get_number_of_combo_ids(
    ) -> int:
    """ returns the number of combo ids """
    combo_params = gf.file_reader(fn.COMBO_PARAM,vanilla=True)
    return len(combo_params)







