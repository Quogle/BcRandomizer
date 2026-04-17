import dev.randomizer.enums.unit_info as unit_info
from dev.randomizer.data.filepaths import *
import os

#steps the string number by 1, maintains length, can be specified to give a certain length
def number_string_stepper(number,string_length=-1):
    """
    turns 001 into 002 
    """
    if string_length==-1:
        string_length = len(number)
    number = str(int(number)+1)
    number_string = "0"*(string_length-len(number)) + number
    return number_string

def stringize_number(number,length):
    """
    turns (43,3) into 043
    """
    output = "0"*length + str(number)
    return output[-length:]

def clamp_value(value):
        """
        clamps a value as an int between 0-100
        """
        if value<0:
            value = 0
        if value>100:
            value = 100
        return int(value)

def get_new_modded_unit_id(unit_info_array,enemy=True):
    """
    sets the first unit id allowed to no longer allowed and returns its id
    \n returns (unit_id,input_array)
    """
    #set cat here
    if enemy:
        modded_id = unit_info.e.is_modded_available
        unit_id = unit_info.e.unit_id

    for unit in unit_info_array:
        if unit[modded_id] == 1:
            unit[modded_id] = 0
            return (unit[unit_id],unit_info_array)

def get_all_vanilla_stages(include_eoc=True):
    """
    returns a list of the stage name of every vanilla stage
    """
    all_data_local_files = os.listdir(DATA_LOCAL)
    stage_names = []
    for file in all_data_local_files:
        stage_location = file.find(STAGE_SCHEM)
        __location = file.find("_")
        dot_location = file.find(".")
        check = True
        if stage_location != 0:
            check = False
        if __location == 5:
            check = False
        if dot_location == 5:
            check = False
        if not include_eoc and dot_location == 7:
            check = False
        if MAIN_STORY_MAPSTAGEDATA in file:
            check = False
        if check:
            stage_names.append(file)
    return stage_names

def print_array_one_by_one(array):
    for each in array:
        print(each)





