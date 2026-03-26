import tomllib
import random

CONFIGS = "configs\\"
DEFAULTS = "defaults\\"
CAT_CONFIG = "cat config.toml"
ENEMY_CONFIG = "enemy config.toml"
GAME_CONFIG = "game config.toml"
VALID_WORDS = ["none","swap","randomize"]
SPELLCHECK = [["white","traitless"],["true","yes"],["false","no"]]

#I dont like this one
def deprecated_get_settings_dict():
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

#gets path list [[enemy.traits.gimmicks.black.boost,1.5],] from config files
def parse_file(path):
    config = {

    }
    predict_list = []
    group_name = ""
    value_string = ""

    config_file = open(path,"r")
    #adds all variables to preict list in the form [traits.gimmicks.black.speed,boost]
    while True:
        line = config_file.readline()
        if line == "":
            break
        #remove comments from being read
        cutoff = line.find("#")
        if cutoff != -1:
            line = line[:cutoff]

        
        #line = line + " " #here to make it so lines starting with # arent empty and break the group name check
        #get group name
        if len(line) > 0 and line[0] == "[":
            end_group_name = line.find("]")
            group_name = line[1:end_group_name]
        else:
            line = line.replace(" ","") #remove all spaces to make lines with no info blank
            line = line.replace("\n","")
            if len(line) > 0:
                if "=" in line:
                    line_split = line.split("=")
                    variable_name = line_split[0]
                    value_string += line_split[1]
                else:
                    value_string += line
                if value_string.count("[") == value_string.count("]"):
                    path_name = group_name + "." + variable_name
                    predict_list.append([str(path_name),usefulize_result(value_string)])
                    value_string = ""
    config_file.close()
    #as proccessed as needed
    return predict_list
  
#gets the {cats,enemy,game} settings dict
def get_settings_dict():
    config = {
        "cat":get_config(CAT_CONFIG),
        "enemy":get_config(ENEMY_CONFIG),
        "game":get_config(GAME_CONFIG)
    }
    return config

#returns integer if is integer and float otherwise
def parse_number(number):
    floa = float(number)
    inte = int(floa)
    if inte == floa:
        output = inte
    else:
        output = floa
    return output

#turns a config value into a real value
def usefulize_result(result):
    output = ""
    result = spellcheck_value(result)
    if "[" in result:
        output = turn_string_array_to_array(result)
    elif "true" in result:
        output = True
    elif "false" in result:
        output = False
    else:
        try:
            output = parse_number(result)
        except:
            result = result.replace("\"","")
            for each in VALID_WORDS:
                if each == result:
                    output = result
    return output

# turns a string array into an actual array
def turn_string_array_to_array(string):
    output = []
    depth = -1
    posit = []
    check_number = False
    number = ""
    decrease_depth = False
    pop_posit = False
    increment_posit = False
    for x in range(0,len(string)):
        st = string[x]


        #if st is [ ] or ,
        if st == "[":
            posit.append(0)
            depth += 1  #shift pos 1 deeper
            check_number = False
        elif st == "]":
            pop_posit = True
            decrease_depth = True
            check_number = True
        elif st == ",":
            increment_posit = True
            check_number = True
        elif st != "\"":
            number += st
        

        if check_number and number != "":
            #figure what is being put in output
            number = spellcheck_value(number)
            try:
                entry = parse_number(number)
            except:
                entry = number
            
            #add the arrays to output and get lookin
            look_in = output
            for y in range(0,len(posit)-1):
                if len(look_in) <= posit[y]:
                    look_in.append([]) #add array if there will be no array to set as new lookin
                look_in = look_in[posit[y]]
            
            #add entry to lookin
            look_in.append(entry)

            #reset number
            number = ""
            check_number = False

        #all these are moved to the end to stop the check number part from breaking
        if decrease_depth:
            depth -= 1
            decrease_depth = False
        if pop_posit:
            posit.pop()
            pop_posit = False
        if increment_posit:
            posit[-1] += 1
            increment_posit = False
    return output

# turns [[enemy.traits.gimmicks.black.boost,1.5]]
def turn_path_list_into_dict(path_list):
    #split them up
    config = {}
    total_list = []
    for each in path_list:
        names = each[0].split(".")
        temp = []
        for zeach in names:
            temp.append(str(zeach))
        temp.append(str(each[1]))
        total_list.append(temp)
    #[enemy,traits,gimmicks,black,boost,1.5]
    for x in range(0,len(total_list)):
        lookin = config
        for y in range(0,len(total_list[x])-2):
            if total_list[x][y] not in lookin:
                lookin[total_list[x][y]] = {}
            lookin = lookin[total_list[x][y]]
        lookin[total_list[x][-2]] = total_list[x][-1]
    
    return config

# overwrites values that are valid in new onto default, returns a pathlist
def overwrite_default_path_list(default,new):
    output = []
    for each in default:
        name = each[0]
        value = each[1]
        found = False
        for zeach in new:
            if zeach[0] == name:
                #print(zeach[0] + "      " + str(zeach[1]))
                if zeach[1] != "":
                    value = zeach[1]
                    found = True
        # this is where you should name if found == false
        if not found:
            print("failed to find " + name)
        output.append([name,value])
    return output

# gets the fully prepared config from a path
def get_config(path):

    default = parse_file(CONFIGS+DEFAULTS+path)
    new = parse_file(CONFIGS+path)
    path_list = overwrite_default_path_list(default,new)
    this_config = turn_path_list_into_dict(path_list)
    return this_config

def spellcheck_value(value):
    entry = value.lower()
    #goes through spellcheck and sets any matches past first index to the first index
    for zeach in SPELLCHECK:
        for x in range(1,len(zeach)):
            if zeach[x] == entry:
                entry = zeach[0]
    return entry

settings = get_settings_dict()

# gets seed, randomizes it if seed=0
def get_seed():
    global settings
    seed = settings["game"]["general"]["seed"]
    try:
        seed = int(seed)
    except:
        seed = 0
    if seed == 0:
        new_seed = ""
        for x in range(0,6):
            new_seed += str(random.randrange(0,10))
        new_seed = str(int(new_seed))
        set_seed(new_seed)
        seed = new_seed
    return int(seed)
    
# sets the seed in config
def set_seed(seed):
    file = open(CONFIGS + GAME_CONFIG,"r")
    config_file = []
    while True:
        line = file.readline()
        if line == "":
            break
        else:
            config_file.append(line)
    file.close()
    new_file = ""
    for each in range(0,len(config_file)):
        if "seed =" in config_file[each]:
            config_file[each] = config_file[each].replace("0",seed)
        new_file += config_file[each]
    file = open(CONFIGS + GAME_CONFIG,"w")
    file.write(new_file)
    file.close()
    print("I set seed to " + str(seed))

seed = get_seed()


