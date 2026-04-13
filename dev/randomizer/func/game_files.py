import os
import shutil
import dev.randomizer.func.file_handler as fh
from dev.randomizer.data.filepaths import *
import dev.randomizer.func.misc as misc
import dev.randomizer.enums.enemy as e
import dev.randomizer.enums.cats as c





"""these functions really need not exist like this, Im just gonna remake them eventually"""

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
    """deliberately broken"""
    animation_directory = "C:\\Users\\tad\\game_files\\added_to_each_instance\\animations\\"
    append00 = "_e_zombie00.maanim"
    append01 = "_e_zombie01.maanim"
    append02 = "_e_zombie02.maanim"

    """
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
    """
                
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


""" these are the functions used for getting game files """

def file_reader(file):
    """
    returns 2d array from file
    \n filename and not path will return the downloadlocal version of the file if it exist
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

    if ending in tsv:
        return fh.array_type_file_reader(input,"\t",False)
    elif ending in num_csv:
        return fh.array_type_file_reader(input,",")
    elif ending in non_num_csv:
        return fh.array_type_file_reader(input,",",False)
    elif ending in skip:
        pass
    else:
        return fh.array_type_file_reader(input,",",False) #current default to non numercial csv

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
        fh.array_to_array_type_file_writer(DOWNLOAD_LOCAL + file,info,"\t")
    elif end in non_num_csv: #theyre separated but Im not sure if theres actually a reason to
        fh.array_to_array_type_file_writer(DOWNLOAD_LOCAL + file,info)
    elif end in num_csv:
        fh.array_to_array_type_file_writer(DOWNLOAD_LOCAL + file,info)
    elif end in skip:
        pass
    else:
        fh.array_to_array_type_file_writer(DOWNLOAD_LOCAL + file,info) #defaults to a csv

def get_cat_stats(vanilla=False):
    """
    gets a length normalized version of cat array
    """
    egg_id = 757
    file_name_start = "unit"
    if vanilla:
        file_name_start = DATA_LOCAL + "unit"
    units = []
    for x in range(1,1000):
        unit = []
        file_path = file_name_start + misc.stringize_number(x,3) + ".csv"
        if not os.path.exists(file_path):
            unit = 0 #if unit doesnt exist slap a zero
        else:
            unit = file_reader(file_path)
        units.append(unit)
    
    #remove trailing zeros
    while True:
        if units[-1] == 0:
            units.pop()
        else:
            break
    
    #replace all missing units with egg
    for x in range(0,len(units)):
        if units[x] == 0:
            units[x] = units[egg_id]
    
    #now lengthen all units to egg length using egg values
    egg_length = len(units[egg_id])
    for x in range(0,len(units)):
        while len(units[x]) < egg_length:
            units[x].append(units[egg_id][len(units[x])])
    
    #now find the longest length
    max_length = 0
    for x in units:
        if len(x) > max_length:
            max_length = len(x)
    
    #now slap 0s on everything until theyre that length
    for x in range(0,len(units)):
        while len(units[x]) < max_length:
            units[x].append(0)
    
    return units



def get_talents(vanilla=False):
    """
    gets and process talent file
    \n each line is 2 ints followed by an array of each talent
    """
    path = TALENT_FILE
    if vanilla:
        path = DATA_LOCAL + TALENT_FILE
    base = file_reader(path)
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







""" classes for opening specific file types nicely """

class csv():
    def __init__(self,file_name):
        self.file_name = file_name
        self.array = file_reader(file_name)
        self.exists = True
        if self.array == None:
            self.exists = False

    
    def write_csv(self):
        file_writer(self.file_name,self.array)

class stage_sche(csv):
    def __init__(s, file_name):
        super().__init__(file_name)
        s.number_of_starting_lines = 2
        if s.array != None:
            if s.array[1][0] > 2000: #figure out if its got 2 starting lines by seeing if first entry on second row is stage length worthy
                pass
            else:
                s.number_of_starting_lines = 1
        
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
            for x in range(s.number_of_starting_lines,len(s.array)):
                if len(s.array[x]) < 2: #break if empty line
                    break
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
        s.drop5_rate = 18
        s.drop5_id = 19
        s.drop5_count = 20

        


    def establish_data(s):
        if s.array == None:
            return
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
        if s.array != None:
            empty_line = False
            for x in range(2,len(s.array)): #idk if any maps dont have 2 lines but if they do this needs to be changed to be like stage class
                if s.array[x] == [] or empty_line:
                    empty_line = True
                else:
                    grid.append(s.array[x])
        s.stages = grid
    
    def submit(s):
        s.array = []
        s.array.append([
            s.map_background,
            s.normal_reward_id,
            s.score_reward_id,
            s.visible_key,
            s.unlock_key
        ])
        s.array.append([s.map_pattern])
        for each in s.stages:
            s.array.append(each)

        s.write_csv()




