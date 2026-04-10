import copy
import os
import shutil
from PIL import Image
import dev.randomizer.enums.enemy as e
import dev.randomizer.enums.cats as c
from dev.randomizer.func.core import number_string_stepper
from dev.randomizer.data.filepaths import *





#add those with info on first line to this dictionary
first_line_csv = {}



#removes all burrow files in the directory given
def burrow_animation_killer(randomizer_directory):
    append00 = "_e_zombie00.maanim"
    append01 = "_e_zombie01.maanim"
    append02 = "_e_zombie02.maanim"
    for x in range(0,800):
        if x < 10:
            number = "00" + str(x)
        elif x < 100:
            number = "0" + str(x)
        else:
            number = str(x)
        if os.path.exists(randomizer_directory + "\\" + number + append00):
            os.remove(randomizer_directory + "\\" + number + append00)
        if os.path.exists(randomizer_directory + "\\" + number + append01):
            os.remove(randomizer_directory + "\\" + number + append01)
        if os.path.exists(randomizer_directory + "\\" + number + append02):
            os.remove(randomizer_directory + "\\" + number + append02)

#places burrow animations for zombies given in directory given, needs to be updated to not use absolute path
def burrow_animation_getter(dummy_stats,randomizer_directory):
    animation_directory = "C:\\Users\\tad\\game_files\\added_to_each_instance\\animations\\"
    append00 = "_e_zombie00.maanim"
    append01 = "_e_zombie01.maanim"
    append02 = "_e_zombie02.maanim"


    for x in range(2,len(dummy_stats)):
        if dummy_stats[x][e.s.zombie] != 0:
            enemy_number = x-2
            if enemy_number < 10:
                enemy_number_string = "00" + str(enemy_number)
            elif enemy_number < 100:
                enemy_number_string = "0" + str(enemy_number)
            else:
                enemy_number_string = str(enemy_number)
            if os.path.exists(animation_directory + enemy_number_string + append00):
                shutil.copyfile(animation_directory + enemy_number_string + append00,randomizer_directory + "\\" + enemy_number_string + append00)
            if os.path.exists(animation_directory + enemy_number_string + append01):
                shutil.copyfile(animation_directory + enemy_number_string + append01,randomizer_directory + "\\" + enemy_number_string + append01)
            if os.path.exists(animation_directory + enemy_number_string + append02):
                shutil.copyfile(animation_directory + enemy_number_string + append02,randomizer_directory + "\\" + enemy_number_string + append02)

#currently makes burrow animations for all enemies and stores them in an absolute path
def burrow_animation_maker():
    burrow_down_append = "0,12,-1,0,0,\n"
    burrow_down_append += "2\n"
    burrow_down_append += "0,1000,0,0,\n"
    burrow_down_append += "30,0,0,0,\n"


    burrow_up_append = "0,12,-1,0,0,\n"
    burrow_up_append += "2\n"
    burrow_up_append += "0,0,0,0,\n"
    burrow_up_append += "30,1000,0,0,\n"

    burrow_walk_string = "[modelanim:animation]\n"
    burrow_walk_string += "1\n"
    burrow_walk_string += "1\n"
    burrow_walk_string += "0,12,-1,0,0,\n"
    burrow_walk_string += "1\n"
    burrow_walk_string += "0,0,0,0,\n"


    current_count = "000"
    burrow_down_location_name = "_e_zombie00.maanim"
    burrow_up_location_name = "_e_zombie02.maanim"
    burrow_walk_location_name = "_e_zombie01.maanim"
    idle_location_name = "_e01.maanim"

    vanilla_directory = "C:\\Users\\tad\\game_files\\ImageDataLocal\\"
    directory_location = "C:\\Users\\tad\\game_files\\added_to_each_instance\\animations\\"


    for x in range(0,1000):
        vanilla_location = vanilla_directory + current_count + idle_location_name
        if os.path.exists(vanilla_location):
            vanilla_idle_file = open(vanilla_location, "r", encoding="utf-8")
            first_frame_string = ""
            plus_one = 1
            first_frame_string += vanilla_idle_file.readline()
            first_frame_string += vanilla_idle_file.readline()
            plus_one_string = vanilla_idle_file.readline()
            plus_one_string = plus_one_string.replace("\n","")
            plus_one += int(plus_one_string)
            plus_one_string = str(plus_one) + "\n"
            first_frame_string += str(plus_one_string)
            while True:
                vanilla_idle_line = vanilla_idle_file.readline()
                if vanilla_idle_line == "":
                    break
                first_frame_string += vanilla_idle_line
                
                
            first_frame_down = first_frame_string + burrow_down_append
            first_frame_up = first_frame_string + burrow_up_append

            burrow_down_file_location = directory_location + current_count + burrow_down_location_name
            burrow_up_file_location = directory_location + current_count + burrow_up_location_name
            burrow_walk_file_location = directory_location + current_count + burrow_walk_location_name
            burrow_down_file = open(burrow_down_file_location, "w", encoding="utf-8")
            burrow_down_file.write(first_frame_down)
            burrow_down_file.close()
            burrow_up_file = open(burrow_up_file_location, "w", encoding="utf-8")
            burrow_up_file.write(first_frame_up)
            burrow_up_file.close()
            burrow_walk_file = open(burrow_walk_file_location,"w",encoding="utf-8")
            burrow_walk_file.write(burrow_walk_string)
            burrow_walk_file.close()

        count_integer = int(current_count)
        count_integer += 1
        if count_integer < 10:
            current_count = "00" + str(count_integer)
        elif count_integer < 100:
            current_count = "0" + str(count_integer)
        else:
            current_count = str(count_integer)



"""
Directory Management
"""

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

def file_reader(file):
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
        return

    if ending in tsv:
        csv_reader(input,False,"\t")
    elif ending in num_csv:
        return csv_reader(input)
    elif ending in non_num_csv:
        return csv_reader(input,False)
    elif ending in skip:
        pass
    else:
        return csv_reader(input,False) #current default to non numercial csv
    
def file_writer(file,info):
    """
    writes file to dl
    """
    non_num_csv = ["imgcut","mamodel","maanim"]
    num_csv = ["csv"]
    tsv = ["tsv"]
    skip = ["json","png","preset"] #json and preset seem the same and can prolly be split
    end_check = file.split(".")
    end = end_check[-1]

    if end in tsv:
        pass
    elif end in non_num_csv: #theyre separated but Im not sure if theres actually a reason to
        csv_writer(DOWNLOAD_LOCAL + file,info)
    elif end in num_csv:
        csv_writer(DOWNLOAD_LOCAL + file,info)
    elif end in skip:
        pass
    else:
        csv_writer(DOWNLOAD_LOCAL + file,info)

#reads 2d array from path, cut and pastes first line if file is in first_line_csv
def csv_reader(file_path,force_num=True,splitter=","):
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
        int(first_line_array[0])
    except:
        first_line_unreadable = True
    
    #shove first line in dict
    if first_line_unreadable:
        global first_line_csv
        first_line_csv[file_path] = first_line
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
        line_string = ""
        for x in next_line:
            if x in csv_characters:
                line_string += x
        line_array = line_string.split(splitter)
        for x in range(0,len(line_array)):
            try:
                line_array[x] = float(line_array[x])
                if int(line_array[x]) == line_array[x]:
                    line_array[x] = int(line_array[x])
            except:
                if force_num:
                    line_array[x] = 0
        output.append(line_array)
    file.close()
    
    return output

#writes 2d array info to path, attatches first line before if file is in first_line_csv
def csv_writer(path,info):
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
            line_string += ","
        line_string = line_string[:-1] + "\n"
        file_string += line_string
    file = open(path,"w",encoding="utf-8")
    file.write(file_string)
    file.close()

def tsv_writer(path,info):
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
            line_string += "\t"
        line_string = line_string[:-1] + "\n"
        file_string += line_string
    file = open(path,"w",encoding="utf-8")
    file.write(file_string)
    file.close()


#maanim reader/writer arent needed anymore as file reader can handle them
#gets the maanim as an array first line is first entry, tries making all entries integers
def maanim_reader(path):
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
def maanim_writer(path,info):
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







# returns the 2d enemy stats array
def read_vanilla_enemy_stats():
    """
    returns the 2d enemys stats array
    """
    path = LOCAL_FILES + "DataLocal\\t_unit.csv"
    return csv_reader(path)

# returns the 3d cat stats array
def read_vanilla_cat_stats():
    """
    returns the 3d cat stats array
    """
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

def read_vanilla_unitbuy():
    """
    returns the 2d unitbuy stats array
    """
    path = LOCAL_FILES + "DataLocal\\unitbuy.csv"
    return csv_reader(path)

def write_enemy_stats_to_dl(estat):
    """
    writes input stats to downloadlocal t_unit
    """
    path = WORKSPACE + "DownloadLocal\\t_unit.csv"
    csv_writer(path,estat)

def write_cat_stats_to_dl(cstat):
    """
    writes input stats to downloadlocal cat files
    """
    directory = WORKSPACE + "DownloadLocal\\unit"
    ending = ".csv"
    for x in range(0,len(cstat)):
        #using number step to set the string increases it to the correct number
        number = number_string_stepper(x,3)
        path = directory + number + ending
        csv_writer(path,cstat[x])

def read_vanilla_talents():
    """
    returns a 3d array of talents, first two in each unit are integers
    """
    path = LOCAL_FILES + "DataLocal\\SkillAcquisition.csv"
    base = csv_reader(path)
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





"""
Image Files
needs cat_sprite_killer() prolly
"""

#kills all enemy sprites in directory
def enemy_sprite_killer(directory):
    sprite_enemy_append_string = "_e.png"
    for unit_id in range(0,1000):
        sprite_string = "000" + str(unit_id)
        sprite_string = "\\" + sprite_string[-3:] + sprite_enemy_append_string
        if os.path.exists(directory + sprite_string):
            os.remove(directory + sprite_string)









"""
classes for things
"""

class csv():
    def __init__(self,file_name):
        self.file_name = file_name
        self.array = file_reader(file_name)

    
    def write_csv(self):
        file_writer(self.file_name,self.array)




class stage_sche(csv):
    def __init__(s, file_name,number_of_starting_lines=2):
        super().__init__(file_name)
        s.number_of_starting_lines = number_of_starting_lines
        #line 1
        s.base_id = 1
        s.no_continues = 0
        #map decides what map the stage is chosen from and it appears to choose an equally weighted stage from first to last
        s.extra_chance = 0
        s.extra_map = 0
        s.extra_first_stage = 0
        s.extra_last_stage = 0
        s.establish_first_line()

        #line 2
        s.stage_length = 5000
        s.base_hp = 1000
        s.min_respawn = 1
        s.max_respawn = 1
        s.background = 1
        s.enemy_limit = 8
        s.animated_base = 0
        s.dojo_time = 0
        s.green_barrier = 0
        s.second_row_mystery = 0 #idk what it does
        s.establish_second_line()
        

        #position info
        s.enemy_id = 0
        s.number_of_spawns = 1
        s.spawn_start_halved = 2
        s.respawn_start_halved = 3
        s.respawn_end_halved = 4
        s.spawn_hp = 5
        s.zmin = 6
        s.zmax = 7
        s.boss = 8
        s.magnification = 9
        s.score = 10
        s.attack_mag = 11
        s.time = 12 #what is this
        s.kill_count = 13

        s.enemies = []
        s.establish_grid()





    def establish_first_line(s):
        size = 0
        if s.array != None: #prevent it from trying to read data if stage doesnt naturally exist
            size = len(s.array[0])
            first = s.array[0]
        if size>0:
            s.base_id = first[0]
        if size>1:
            s.no_continues = first[1]
        if size>2:
            s.extra_chance = first[2]
        if size>3:
            s.extra_map = first[3]
        if size>4:
            s.extra_first_stage = first[4]
        if size>5:
            s.extra_last_stage = first[5]
    
    def establish_second_line(s):
        size = 0
        if s.array != None:
            size = len(s.array[1])
            first = s.array[1]
        if size>0:
            s.stage_length = first[0]
        if size>1:
            s.base_hp = first[1]
        if size>2:
            s.min_respawn = first[2]
        if size>3:
            s.max_respawn = first[3]
        if size>4:
            s.background = first[4]
        if size>5:
            s.enemy_limit = first[5]
        if size>6:
            s.animated_base = first[6]
        if size>7:
            s.dojo_time = first[7]
        if size>8:
            s.green_barrier = first[8]
        if size>9:
            s.second_row_mystery = first[9]

    def establish_grid(s):
        enemy = []
        if s.array != None:
            for x in range(2,len(s.array)):
                enemy.append(s.array[x])
        s.enemies = enemy

    def submit(s):
        s.array = []
        if s.number_of_starting_lines == 2: #this allows me to write eoc/itf/cotc stages
            s.array.append([
                s.base_id,
                s.no_continues,
                s.extra_chance,
                s.extra_map,
                s.extra_first_stage,
                s.extra_last_stage
            ])
        s.array.append([
            s.stage_length,
            s.base_hp,
            s.min_respawn,
            s.max_respawn,
            s.background,
            s.enemy_limit,
            s.animated_base,
            s.dojo_time,
            s.green_barrier,
            s.second_row_mystery
        ])
        for each in s.enemies:
            s.array.append(each)
        s.write_csv()

class map_data(csv):
    def __init__(s, file_name):
        super().__init__(file_name)
        s.map_background = 0
        s.normal_reward_id = 0 #never did check if this was what it was
        s.score_reward_id = -1
        s.visible_key = -1
        s.unlock_key = -1

        s.map_pattern = 0
        s.establish_data()
        s.establish_grid()


        s.energy = 0
        s.xp = 1
        s.music1 = 2
        s.swap_music_at = 3
        s.music2 = 4
        s.drop1_rate = 5
        s.drop1_id = 6
        s.drop1_count = 7
        s.drop_scheme = 8
        s.drop2_rate = 9
        s.drop2_id = 10
        s.drop2_count = 11
        s.drop3_rate = 12
        s.drop3_id = 13
        s.drop3_count = 14
        s.drop4_rate = 15
        s.drop4_id = 16
        s.drop4_count = 17

        


    def establish_data(s):
        first = s.array[0]
        le = len(first)
        if le>0:
            s.map_background = first[0]
        if le>1:
            s.normal_reward_id = first[1]
        if le>2:
            s.score_reward_id = first[2]
        if le>3:
            s.visible_key = first[3]
        if le>4:
            s.unlock_key = first[4]
        s.map_background = s.array[1][0]
    
    def establish_grid(s):
        grid = []
        for x in range(2,len(s.array)):
            grid.append(s.array[x])
        s.stages = grid
    
    def submit(s):
        array = []
        array.append([
            s.map_background,
            s.normal_reward_id,
            s.score_reward_id,
            s.visible_key,
            s.unlock_key
        ])
        array.append([s.map_pattern])
        for each in s.stages:
            array.append(each)
        s.write_csv(s.file_name,array)



