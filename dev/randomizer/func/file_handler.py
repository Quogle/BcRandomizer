import copy
import os
import shutil
from PIL import Image
import dev.randomizer.enums.enemy as e
import dev.randomizer.enums.cats as c
from dev.randomizer.data.filepaths import *





#add those with info on first line to this dictionary
first_line_csv = {}
#establish order for file searching here
server_folders_for_order = [
    SERVERIMAGE,
    SERVERIMAGEDATA,
    SERVERMAP,
    SERVERNUMBER,
    SERVERUNIT
]
#contains the proper order to search server folders in, made on first need
server_folder_order = []


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
        for x in range(0,len(line_array)):
            try:
                line_array[x] = float(line_array[x]) #convert first to float then if that float is an int make it such
                if int(line_array[x]) == line_array[x]:
                    line_array[x] = int(line_array[x])
            except:
                if force_num:
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
        return first_line
    #Im assuming that this has an effect on the object outside this function for now

def array_type_file_reader(file_path, # the full file path
                           separator=",", #separator to use, default ,
                           force_numerical=True, #force set all values in file to 0 if not numeric
                           first_line_check=True, #check if first line is non numeric
                           return_first_line=None #causes file to return the first line as a first entry in the array
                           ):
    """
    returns 2d array of file at path, int if possible
    \n if first line only is unreadable puts it in first_line_csv to read from when writing
    """
    directory_names = file_path.split("\\")
    file_name = directory_names[-1]
    file = open(file_path,"r",encoding="utf-8")
    #set default actions
    force_num = True
    if force_numerical != None:
        force_num = force_numerical
    do_first_line_check = True
    if first_line_check != None:
        do_first_line_check = first_line_check
    slap_first_line_on = False
    if return_first_line != None:
        slap_first_line_on = return_first_line


    if do_first_line_check:
        first_line = figure_if_unreadable_first_line(file,file_name,separator)
    
    array_to_return = interpret_csv_type_file(file,separator,force_num)
    if slap_first_line_on: #slap it on front
        array_to_return = [first_line] + array_to_return
    return array_to_return

def array_to_array_type_file_writer(file_path,info,separator=",",old_file_name=None,first_line_in_array=None):
    """
    writes an array to file using separator default comma
    """
    global first_line_csv 
    directory_names = file_path.split("\\")
    file_name = directory_names[-1]
    if old_file_name != None:
        file_name = old_file_name
    if first_line_in_array:
        first_line_csv[file_name] = info.pop(0)


    #set the line to the first line if its in dict
    file_string = ""
    
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


def search_for_file(file_name,debug=True):
    """
    searches local then server files for the file, returns its full path
    \n returns none if not found in either
    """
    #print("searching for " + file_name)
    local_dir = LOCAL_FILES
    server_dir = SERVER_FILES
    if MODDED_MLETTER in file_name:
        if debug:
            print("looking for modded " + file_name)
        local_dir = MODDED_ADDITIONS_FILES
        server_dir = MODDED_ADDITIONS_FILES

    local_folders = os.listdir(local_dir)
    for each in local_folders:
        if os.path.exists(local_dir + each + "\\" + file_name):
            return local_dir + each + "\\" + file_name
    if server_dir == SERVER_FILES:
        global server_folder_order
        if len(server_folder_order) == 0:
            set_server_folder_order() #make it if first time
        server_folders = server_folder_order
    else:
        server_folders = os.listdir(server_dir)
    #now search in proper order
    for each in server_folders:
        if os.path.exists(server_dir + each + "\\" + file_name):
            return server_dir + each + "\\" + file_name
    if debug:
        print("failed to find file: " + file_name)
    return None
    




def set_server_folder_order():
    """
    puts the order to look in server folders in global variable
    """
    server_folders = os.listdir(SERVER_FILES)
    temp0 = [] #contains the base
    temp1 = [] #contains the number types
    temp2 = [] #contains the letter types
    temp3 = [] #contains all the folders that fit no types
    temp4 = [] #contains all folders that matched a case but failed somehow
    global server_folders_for_order
    for each in server_folders:
        found = False
        for folder in server_folders_for_order:
            if folder in each:
                found = True
                if len(folder) == len(each): #the case when it is the main folder
                    temp0.append(each)
                elif each[len(folder)] == "_": #number case
                    temp2.append(each)
                elif len(folder) + 1 == len(each): #letter case
                    temp1.append(each)
                else:
                    temp4.append(each) #all else
        if not found:
            temp3.append(each) #this was here for modded but that prolly isnt required now
    temp1.sort(reverse=True)
    temp2.sort(reverse=True)
    temp3.sort(reverse=True)
    temp4.sort(reverse=True)
    global server_folder_order
    server_folder_order = temp0 + temp2 + temp1 + temp3 + temp4
    



"""
debug funcs
"""





"""
deprecated
"""


