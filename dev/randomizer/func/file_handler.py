import copy
import os
import shutil
from PIL import Image
import dev.randomizer.enums.enemy as e
import dev.randomizer.enums.cats as c
from dev.randomizer.data.filepaths import *





#add those with info on first line to this dictionary
first_line_csv = {}



"""
Directory Management
"""
#these functions serve no real purpose
#returns a list of all file paths in a directory, returns full paths if given full path
def recursive_directory_content_getter(directory):
    '''
    returns all files in a given directory, paths are full if given full path
    '''
    #returns path array if directory was a folder, if directory is file fails and returns the file path in an array
    try:
        current_dir_paths = os.listdir(directory)
    except:
        return [directory]
    

    output = []
    #search searches all paths further
    for each in current_dir_paths:
        dug_deeper = recursive_directory_content_getter(directory + "\\" + each)
        for each2 in dug_deeper:
            output.append(each2)
    #all entries in array are full paths
    return output

#I still gotta see if folders in download local work (it would make this pointless) 
def copy_many_directory_files_to_single(directory_from,directory_to):
    '''
    copies all files under first directory to the second
    '''
    files = recursive_directory_content_getter(directory_from)

    #gets a list of the files names
    file_names = []
    for each in files:
        current = each.split("\\")
        file_names.append(current[-1])
    
    #puts destination directory in front of file names
    new_files = []
    for each in file_names:
        new_files.append(directory_to + "\\" + each)
    
    #copies from files to new files
    for x in range(0,len(files)):
        shutil.copy(files[x],new_files[x])




"""
File Readers
"""
def numerize_string(string,separator=","):
    """
    removes all non numerical values from the string except the separator
    """
    csv_characters = ["0","1","2","3","4","5","6","7","8","9","-",".",separator]
    return_string = ""
    for char in string:
        if char in csv_characters:
            return_string += char
    return return_string

def interpret_csv_type_file(file,separator=",",force_num=True):
    """
    reads through lines in the file and returns an array
    """
    file = open()
    array_to_return = []
    while True:
        line = file.readline()
        if line == "":
            break
        #remove everything commented out
        comment = line.find()
        if comment != -1:
            line = line[:comment]
        #force num and remove \n and stupid chara
        if force_num:
            line = numerize_string(line,separator)
        else:
            line = line.replace("\n","")
            line = line.replace("\ufeff","")
        #process it
        line_array = line.split(separator)
        if force_num:
            for x in range(0,len(line_array)):
                try:
                    line_array[x] = float(line_array[x]) #convert first to float then if that float is an int make it such
                    if int(line_array[x]) == line_array[x]:
                        line_array[x] = int(line_array[x])
                except:
                    if x != len(line_array)-1: #prevent it from adding values on trailing commas
                        line_array[x] = 0
        array_to_return.append(line_array)
    return array_to_return

def figure_if_unreadable_first_line(file,name,separator):
    """
    determines if the first line in a file is readable by trying to float it
    """
    first_line = file.readline()
    first_line_array = first_line.split(separator)
    try:
        float(first_line_array[0].replace("\ufeff",""))
        file.seek(0)
    except:
        global first_line_csv
        first_line_csv[name] = first_line
    #Im assuming that this has an effect on the object outside this function for now

def array_type_file_reader(file_path,separator=",",force_num=True,non_num=False):
    """
    returns 2d array of file at path, int if possible
    \n if first line only is unreadable puts it in first_line_csv to read from when writing
    """
    directory_names = file_path.split("\\")
    file_name = directory_names[-1]
    file = open(file_path,"r",encoding="utf-8")

    if not non_num:
        figure_if_unreadable_first_line(file,file_name,separator)
    
    array_to_return = interpret_csv_type_file(file,separator,force_num)
    return array_to_return

def array_to_array_type_file_writer(file_path,info,separator=","):
    """
    writes an array to file using separator default comma
    """
    directory_names = file_path.split("\\")
    file_name = directory_names[-1]
    
    #set the line to the first line if its in dict
    file_string = ""
    global first_line_csv 
    if file_name in first_line_csv:
        file_string = first_line_csv[file_name]
    
    #write the rest of the array
    for line in info:
        line_string = ""
        for entry in line:
            line_string += entry + separator
        file_string += line_string[:-1] + "\n"
    #write to file
    file = open(file_path,"w",encoding="utf-8")
    file.write(file_string)
    file.close()







"""
deprecated
"""
#reads 2d array from path, cut and pastes first line if file is in first_line_csv
def old_csv_reader(file_path,force_num=True,splitter=","):
    """
    returns int 2d array of csv at path
    \n now capable of reading non numerical csv if force_num is false
    \n can also read from tsv if splitter is \\t
    """
    file = open(file_path,"r",encoding="utf-8")
    

    #check if first line integerable
    first_line = file.readline()
    first_line_array = first_line.split(splitter)
    first_line_unreadable = False
    try:
        int(first_line_array[0].replace("\ufeff",""))
    except:
        first_line_unreadable = True
    
    #shove first line in dict
    if first_line_unreadable:
        global first_line_csv
        file_names = file_path.split("\\")
        first_line_csv[file_names[-1]] = first_line
    else:
        file.seek(0)
    
    #read csv
    output = []
    csv_characters = ["0","1","2","3","4","5","6","7","8","9",",","-","."]
    if splitter not in csv_characters:
        csv_characters.append(splitter)
    while True:
        next_line = file.readline()
        if next_line == "":
            break
        #remove anything after //
        if next_line.find("//") != -1:
            next_line = next_line[:next_line.find("//")]
        #strip of all non numerical characters if force num
        line_string = ""
        if force_num:
            for x in next_line:
                if x in csv_characters:
                    line_string += x
        else:
            line_string = next_line.replace("\n","") #make sure to remove the \n character
        #process it into array
        line_array = line_string.split(splitter)
        for x in range(0,len(line_array)):
            try:
                line_array[x] = float(line_array[x])
                if int(line_array[x]) == line_array[x]:
                    line_array[x] = int(line_array[x])
            except:
                if force_num:
                    line_array[x] = 0
                    if x == len(line_array)-1: #stop it from adding values on trailing commas
                        line_array.pop()
        output.append(line_array)
    file.close()
    
    return output

#writes 2d array info to path, attatches first line before if file is in first_line_csv
def old_csv_writer(path,info,character=","):
    # make initial file string first line if in csv dict
    global first_line_csv
    split_path = path.split("\\")
    file_string = ""
    if split_path[-1] in first_line_csv:
        file_string = first_line_csv[split_path[-1]]

    for line in info:
        line_string = ""
        for x in line:
            line_string += str(x)
            line_string += character
        line_string = line_string[:-1] + "\n"
        file_string += line_string
    file = open(path,"w",encoding="utf-8")
    file.write(file_string)
    file.close()

def old_file_writer(file,info):
    """
    writes file to dl
    """
    non_num_csv = ["imgcut","mamodel","maanim"]
    num_csv = ["csv"]
    tsv = ["tsv"]
    skip = ["json","png","preset"] #json and preset seem the same and can prolly be split
    end_check = file.split(".")
    end = end_check[-1]
    return #added to break it
    if end in tsv:
        csv_writer(DOWNLOAD_LOCAL + file,info,"\t")
    elif end in non_num_csv: #theyre separated but Im not sure if theres actually a reason to
        csv_writer(DOWNLOAD_LOCAL + file,info)
    elif end in num_csv:
        csv_writer(DOWNLOAD_LOCAL + file,info)
    elif end in skip:
        pass
    else:
        csv_writer(DOWNLOAD_LOCAL + file,info)

def old_file_reader(file,force_numercial = False):
    """
    returns 2d array from file, use only file name to check if in dl first
    """
    non_num_csv = ["imgcut","mamodel","maanim"]
    num_csv = ["csv"]
    tsv = ["tsv"]
    skip = ["json","png","preset"] #json and preset seem the same and can prolly be split
    #get csv or tsv
    check_ending = file.split(".")
    ending = check_ending[-1]

    input = file
    #get path
    use_path = False
    if "\\" in file:
        use_path = True
    
    if not use_path:
        if os.path.exists(DOWNLOAD_LOCAL+file):
            input = DOWNLOAD_LOCAL + file
        else:
            subfolders = []
            locals = os.listdir(LOCAL_FILES)
            servers = os.listdir(SERVER_FILES)
            for each in locals:
                subfolders.append("local\\" + each)
            for each in servers:
                subfolders.append("server\\" + each)
            for each in subfolders:
                if os.path.exists(GAME_FILES+each+"\\"+file):
                    input = GAME_FILES+each+"\\"+file
                    break
    if not os.path.exists(input): #stop it from attempting to read a file that doesnt exist
        #print("file \"" + str(input) + "\" does not exist")
        return
    return #added to break it
    if ending in tsv:
        return csv_reader(input,False,"\t")
    elif ending in num_csv:
        return csv_reader(input,not force_numercial)
    elif ending in non_num_csv:
        return csv_reader(input,False)
    elif ending in skip:
        pass
    else:
        return csv_reader(input,False) #current default to non numercial csv

# returns the 3d cat stats array
def old_read_vanilla_cat_stats():
    """
    returns the 3d cat stats array
    """
    return #added to break it
    directory = LOCAL_FILES + "DataLocal\\unit"
    ending = ".csv"
    current_unit = "000"
    units = []
    while len(current_unit) < 4:

        current_unit = number_string_stepper(current_unit,3)
        path = directory + current_unit + ending
        unit = 0 #puts a 0 instead of the unit array if unit file not found (helps fix if a random unit csv is missing)
        if os.path.exists(path):
            unit = csv_reader(path)
        units.append(unit)
    

    #reads backwards through the array removing all 0 
    while True:
        if 0 == units[-1]:
            units.pop()
        else:
            break
    
    #now replaces all remaining instances of 0 with basic cat
    for x in range(0,len(units)):
        if 0 == units[x]:
            units[x] = units[0]
    
    #find the longest array
    max_length = 0
    for unit in units:
        if len(unit[0]) > max_length:
            max_length = len(unit[0])
    

    #now lengthen them
    egg_id = 757
    egg_length = len(units[egg_id][0])
    for unit_id in range(0,len(units)):
        for form_id in range(0,len(units[unit_id])):
            current_length = len(units[unit_id][form_id])
            while current_length < egg_length:
                units[unit_id][form_id].append(units[egg_id][0][current_length])
                current_length += 1
            while current_length < max_length:
                units[unit_id][form_id].append(0)
                current_length += 1

    return units

# returns the 2d enemy stats array
def old_read_vanilla_enemy_stats():
    """
    returns the 2d enemys stats array
    """
    return #added to break it
    path = LOCAL_FILES + "DataLocal\\t_unit.csv"
    return csv_reader(path)

#this never had a reason to exist in the first place
def old_read_vanilla_unitbuy():
    """
    returns the 2d unitbuy stats array, broken
    """
    path = LOCAL_FILES + "DataLocal\\unitbuy.csv"
    return #csv_reader(path)

#this also never had a reason to exist in the first place
def old_read_vanilla_talents():
    """
    returns a 3d array of talents, first two in each unit are integers, broken
    """
    path = LOCAL_FILES + "DataLocal\\SkillAcquisition.csv"
    base = 0#csv_reader(path)
    talents = []
    for each in base:
        line = []
        line.append(each[0])
        line.append(each[1])
        pos = 2
        while pos < len(each):
            talent = []
            for x in range(0,c.tpos.length):
                talent.append(each[pos+x])
            pos += c.tpos.length
        talents.append(line)
    
    return talents

#I lied these dont need to exist
#maanim reader/writer you need to use these if you are not writing to a file of the same name as was read from
#gets the maanim as an array first line is first entry, tries making all entries integers
def old_maanim_reader(path):
    output = []
    file = open(path,"r",encoding = "utf-8")
    output.append(file.readline())
    while True:
        next_line = file.readline()
        if next_line == "":
            break
        line_array = next_line.split(",")
        for x in range(0,len(line_array)):
            try:
                line_array[x] = int(line_array[x])
            except:
                pass
        output.append(line_array)
    file.close()
    return output

#writer maanim
def old_maanim_writer(path,info):
    file_string = info[0]
    for x in range(1,len(info)):
        line_string = ""
        for y in info[x]:
            line_string += str(y)
            line_string += ","
        line_string = line_string[:-1]
        if "\n" not in line_string:
            line_string += "\n"
        file_string += line_string
    file = open(path,"w",encoding="utf-8")
    file.write(file_string)
    file.close()

#I see no reason for this to exist rn, if it ever does it shouldnt be in here
#kills all enemy sprites in directory
def old_enemy_sprite_killer(directory):
    sprite_enemy_append_string = "_e.png"
    for unit_id in range(0,1000):
        sprite_string = "000" + str(unit_id)
        sprite_string = "\\" + sprite_string[-3:] + sprite_enemy_append_string
        if os.path.exists(directory + sprite_string):
            os.remove(directory + sprite_string)

