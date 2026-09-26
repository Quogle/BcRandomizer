""" module for obtaining the version config data from the versions set in config """
from ...config.defaults import DEFAULT_CONFIG
from ..version_config import version_config_file_reader as vcfr
from ..version_config import internal_version_names as ivn
from ..version_config import version_config_keys as vck












def VC_from_config(config=DEFAULT_CONFIG):
    """ gets the version config from config 
    \n keys:
    trait_rand_forms: for freezing unit trait rand
    trait_rand_talents: for freezing unit trait rand
    """
    version_config = {}
    #I will be adding these as I need them as I do not know all their names and what they do
    #Im making these call to the same one, unit talent can be for freezing talent randomizaion separately
    version_config[vck.unit_trait_rand_forms] = vcfr.get_version_config_information(config["mod"]["unit_trait"])[ivn.NUMBER_OF_CAT_FORMS]
    version_config[vck.unit_trait_rand_talents] = vcfr.get_version_config_information(config["mod"]["unit_trait"])[ivn.TALENT_INFORMATION]




    return version_config



DEFAULT_VC_CONFIG = VC_from_config()




