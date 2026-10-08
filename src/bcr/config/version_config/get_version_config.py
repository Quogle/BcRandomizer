""" module for obtaining the version config data from the versions set in config """
from ...config.defaults import DEFAULT_CONFIG
from ..version_config import version_config_file_reader as vcfr
from ..version_config import internal_version_names as ivn
from ..version_config import version_config_keys as vck











#this is the function to put any vck variable in
def VC_from_config(config=DEFAULT_CONFIG):
    """ gets the version config from config 
    \n keys:
    trait_rand_forms: for freezing unit trait rand
    trait_rand_talents: for freezing unit trait rand
    """
    version_config = {}
    #I will be adding these as I need them as I do not know all their names and what they do
    #Im making these call to the same one, unit talent can be for freezing talent randomizaion separately
    #unit trait rand
    version_config[vck.unit_trait_rand_forms] = vcfr.get_version_config_information(config["mod"]["unit_trait"])[ivn.NUMBER_OF_CAT_FORMS]
    version_config[vck.unit_trait_rand_talents] = vcfr.get_version_config_information(config["mod"]["unit_trait"])[ivn.TALENT_INFORMATION]
    #talent rand
    version_config[vck.unit_talent_rand_talent_ids] = vcfr.get_version_config_information(config["mod"]["talents"])[ivn.TALENT_INFORMATION]
    version_config[vck.unit_talent_rand_orb_counts] = vcfr.get_version_config_information(config["mod"]["talents"])[ivn.ORB_INFORMATION]



    #all unit down combos
    version_config[vck.all_unit_down_max_combo_id] = vcfr.get_version_config_information(config["mod"]["combos"])[ivn.NUMBER_OF_COMBO_IDS]
    version_config[vck.all_unit_down_max_unit_id] = vcfr.get_version_config_information(config["mod"]["combos"])[ivn.NUMBER_OF_CATS]
    #normal combo randomization
    version_config[vck.combo_rand_max_combo_id] = vcfr.get_version_config_information(config["mod"]["combos"])[ivn.NUMBER_OF_COMBO_IDS]
    version_config[vck.combo_rand_combo_count] = vcfr.get_version_config_information(config["mod"]["combos"])[ivn.NUMBER_OF_COMBOS]
    version_config[vck.combo_rand_unit_forms] = vcfr.get_version_config_information(config["mod"]["combos"])[ivn.NUMBER_OF_CAT_FORMS]


    #enemy
    #enemy swap
    version_config[vck.enemy_swap_max_enemy_id] = vcfr.get_version_config_information(config["mod"]["enemy_swap_id"])[ivn.NUMBER_OF_ENEMIES] #note this is the length of t unit so its number of enemies +2





    return version_config



DEFAULT_VC_CONFIG = VC_from_config()




