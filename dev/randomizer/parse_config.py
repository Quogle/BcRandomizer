import tomllib

CAT_CONFIG = "config\\cat config.toml"
ENEMY_CONFIG = "config\\enemy config.toml"
GAME_CONFIG = "config\\game config.toml"


def get_settings_dict():
    # Load TOML
    with open(CAT_CONFIG, "rb") as f:
        cat_config = tomllib.load(f)
        f.close()
    # Load TOML
    with open(ENEMY_CONFIG, "rb") as f:
        enemy_config = tomllib.load(f)
        f.close()
    # Load TOML
    with open(GAME_CONFIG, "rb") as f:
        game_config = tomllib.load(f)
        f.close()
    
    settings = {
        "cat":cat_config,
        "enemy":enemy_config,
        "game":game_config,
    }
    return settings

settings = get_settings_dict()

def parse_file(path):
    config = {

    }
    predict_list = []



    config_file = open(path,"r")
    while True:
        line = config_file.readline()

        #remove comments from being read
        cutoff = line.find("#")
        line = line[:cutoff]

        #remove spaces dont do that actually it would fuck zombies n other lists
        #line.replace(" ","")

        #grab group name
        if line[0] == "[":
            end_group_name = line.find("]")+1
            group_name = line[1:end_group_name]
            if end_group_name == 0:
                group_name = "fail"
        else:
            #now remove spaces
            line.replace(" ","")
            if "=" in line:
                split_line = line.split("=")
                path_name = group_name + "." + split_line[0]
                current_list_string = ""
                if "[" not in split_line[1]:
                    read = False
                    try:
                        value = int(split_line[1])
                        read = True
                    except:
                        if "true" in split_line[1].lower():
                            value = True
                            read = True
                        elif "false" in split_line[1].lower():
                            value = False
                            read = True
                    if read:
                        predict_list.append([path_name,value])
                else:
                    current_list_string += split_line[1]
            elif "[" in line or "]" in line:
                current_list_string += line
            
            if len(current_list_string)>0:
                if current_list_string.count("[") == current_list_string.count("]"):
                    pass


#takes a string array and turns it into an actual array
def turn_string_array_to_array(string_array):
    output = []
    current_depth = 0
    breakage = []
    max_depth = 0
    while True:
        breakage.append([])
        deepness = 0
        for x in range(0,len(string_array)):
            if string_array[x] == "[":
                deepness += 1
                if max_depth < deepness:
                    max_depth = deepness
            elif string_array[x] == "]":
                deepness -= 1
            elif string_array[x] == ",":
                if deepness == current_depth:
                    breakage[current_depth].append(x)
        current_depth += 1
        if current_depth > max_depth:
            break
    

    current_depth = 0
    while current_depth < max_depth:
        pass





