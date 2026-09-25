""" this module is what makes the config files for the current version\n
 """
import tadbcmc.core.game_files as gf
import tadbcmc.data.filenames as fn
from ..config import paths
import tadbcmc.data.enums.cats as c
import tadbcmc.core.file_handler as fh



#I have no idea what the version config is going to look like

#putting the file names here for now, they can be moved to paths if needed
TALENT_CONFIG = "talent_ids.csv"




""" Units """

def get_talent_ids(config_version:str):
    """ logs the talent ability ids for all units and writes them to the current versions config """
    #first step is get the correct filepath to store the information in
    #for now Im just open combining version as a string
    filepath = paths.VERSIONCONFIGS / config_version / TALENT_CONFIG
    #ok now the real func can begin
    talents = gf.get_talents(vanilla=True)
    #first get the highest unit id with talents
    highest_unit_id = 0
    for line in talents:
        if line[c.tpos.unit_id] > highest_unit_id:
            highest_unit_id = line[c.tpos.unit_id]
    #now make the talent array with that many entries
    versions_talents = []
    for x in range(0,highest_unit_id):
        versions_talents.append([])
    #now go through the talents adding the id of all abilities to the unit_ids index
    for line in talents:
        current_unit_id = line[c.tpos.unit_id]
        for block in range(2,len(line)):
            versions_talents[current_unit_id].append(line[block][c.tpos.ability_id])
    #now write them to file
    fh.array_to_array_type_file_writer(filepath,versions_talents)



























