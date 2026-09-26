import bcr.randomizer.file_local as fl
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
from ...config import paths as internalPaths
import tadbcmc.data.enums.cats as c
import tadbcmc.core.file_handler as fh
import tadbcmc.pieces.combos as combos
import bcr.apk.breakdown_apk as breakdown_apk
import tadbcmc.core.simple_funcs as simp
import os
from pathlib import Path
from ..version_config import internal_version_names as ivn










def get_version_config_information(config_version:str):
    """ gets all the version config for that specific version """
    #first get the location of version info
    if "src" in os.listdir(os.getcwd()): base = Path("src")
    else: base = Path("")
    config_dir = base / internalPaths.VERSIONINFO
    #get the one to use
    correct_version = _get_last_existing_config_version(config_version,config_dir)
    this_config_version = config_dir / correct_version
    #read it and add it to the version config to output
    output = _read_misc_information(this_config_version)
    output[ivn.NUMBER_OF_CAT_FORMS] = _read_unit_form_information(this_config_version)
    output[ivn.TALENT_INFORMATION] = _read_unit_talent_information(this_config_version)
    return output



def _get_last_existing_config_version(config_version:str,version_info_path:Path):
    """ searches down in version numbers until it finds a corresponding version info """
    #we need to find the correct config version to use, search down till one is found
    config_split = config_version.split(".")
    (large,medium,small) = (int(config_split[0]),int(config_split[1]),int(config_split[2])) #im making the assumption itll always have 3 parts
    #make sure none of them would make the program run for an excessive time
    large = simp.clamp(large,-1,30)
    medium = simp.clamp(medium,-1,20)
    small = simp.clamp(small,-1,10)
    failed = False
    while not os.path.exists(version_info_path / (str(large) + "." + str(medium) + "." + str(small))):
        if large < 15:
            failed = True
            break #something to do about not found here
        #reduce each one until its below 0
        if small < 0:
            small = 10
            medium -= 1
        else:
            small -= 1
        if medium < 0:
            medium = 20
            large -= 1
    #now make the config str from it
    output_version = str(large) + "." + str(medium) + "." + str(small)
    #if failed just use the lowest config version
    if failed:
        all_in_dir = os.listdir(version_info_path)
        all_in_dir.sort()
        output_version = all_in_dir[0]
    return output_version





def _read_misc_information(config_version_path:Path
    ) -> dict[str,int|any]:
    """ reads information from the mics info file
    \n returns a dictionary with variables shared between this module and vc maker as the keys """
    filepath = config_version_path / ivn.MISC_INFO_CONFIG
    misc_info = fh.array_type_file_reader(str(filepath),force_numerical=False,first_line_check=False)
    #now put it in the dict
    output = {}
    for line in misc_info:
        output[line[0]] = line[-1]
    return output

def _read_unit_form_information(config_version_path:Path
    ) -> list[int]:
    """ reads information from the unit forms file
    \n index in array corresponds to unit id """
    filepath = config_version_path / ivn.UNIT_FORM_CONFIG
    form_info = fh.array_type_file_reader(str(filepath),first_line_check=False)
    return form_info[0]

def _read_unit_talent_information(config_version_path:Path
    ) -> list[list[int]]:
    """ reads information from the talent file 
    \n index in array corresponds to unit id 
    \n first value is the talent sum (is -1 if unit had no talents) """
    filepath = config_version_path / ivn.TALENT_CONFIG
    talent_info = fh.array_type_file_reader(str(filepath),first_line_check=False)
    return talent_info












