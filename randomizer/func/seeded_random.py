import core



#generates a predictable random array with respect to a seed and an id
def rand(random_array,id):
    #clamp id to within the bounds of the array
    if id > len(random_array)-2:
        id -= len(random_array)
    if id < 1:
        id += int(len(random_array)/2)
    
    #rotates the array by an amount and returns it
    step_amount = (random_array[id]+1) * (random_array[id+1]+1)
    random_array = step(random_array,step_amount)
    return random_array

#steps the input array by amount default to one
def step(random_array,amount=1):
    for x in range(0,amount):
        random_array.append(random_array[0])
        random_array.pop(0)
    return random_array

#input seed and it returns an array of single value random numbers 0-9, length is based on the size of the seed
def make_random_list(seed):
    string = core.generate_random_string_characters(str(abs(seed)))
    if len(string) < 50:
        string = core.generate_random_string_characters(string)
    if len(string) > 200:
        string = core.ratio_shorten_string(string,200)
    

    random_array = []
    for x in string:
        random_array.append(int(x))
    return random_array














