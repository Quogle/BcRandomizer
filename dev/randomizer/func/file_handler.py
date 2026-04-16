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

def copy_file_to_download_local(file_path,filename=None):
    """
    copies file from path into download local
    """
    if filename == None:
        split_paths = file_path.split("\\")
        filename = split_paths[-1]
    print("copying " + file_path + " to dl as " + filename)
    shutil.copy(file_path,DOWNLOAD_LOCAL + filename)


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
    array_to_return = []
    while True:
        line = file.readline()
        if line == "":
            break
        #remove everything commented out
        comment = line.find("//")
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
                    else:
                        line_array.pop()
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
            line_string += str(entry) + separator
        file_string += line_string[:-1] + "\n"
    #write to file
    file = open(file_path,"w",encoding="utf-8")
    file.write(file_string)
    file.close()


def search_for_file(file_name):
    """
    searches local then server files for the file
    \n returns none if not found in either
    """
    #print("searching for " + file_name)
    local_dir = LOCAL_FILES
    server_dir = SERVER_FILES
    if MODDED_MLETTER in file_name:
        print("looking for modded " + file_name)
        local_dir = MODDED_ADDITIONS_FILES
        server_dir = MODDED_ADDITIONS_FILES

    local_folders = os.listdir(local_dir)
    for each in local_folders:
        if os.path.exists(local_dir + each + "\\" + file_name):
            return local_dir + each + "\\" + file_name
    server_folders = os.listdir(server_dir)
    for each in server_folders:
        if os.path.exists(server_dir + each + "\\" + file_name):
            return server_dir + each + "\\" + file_name
    print("failed to find file: " + file_name)
    return None
    





"""
deprecated
"""


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

