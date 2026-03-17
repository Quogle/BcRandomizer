import core
random_list = []


#generates a predictable random array with respect to a seed and an id (dont use)
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

#steps the input array by amount default to one (dont use)
def step(random_array,amount=1):
    for x in range(0,amount):
        random_array.append(random_array[0])
        random_array.pop(0)
    return random_array

#input seed and it makes random_list an array of single value random numbers 0-9, length varies based on seed
def make_random_list(seed):
    string = core.generate_random_string_characters(str(abs(seed)))
    if len(string) < 50:
        string = core.generate_random_string_characters(string)
    if len(string) > 200:
        string = core.ratio_shorten_string(string,200)
    

    random_array = []
    for x in string:
        random_array.append(int(x))
    global random_list
    random_list = random_array

#make an object of this class in each function you want to use random in and give it a unique instance id
class randinst():
    def __init__(self,instance_id):
        global random_list
        self.list = []
        #didnt feel like using copy
        for each in random_list:
            self.list.append(int(each))
        self.rotate(instance_id)
    

    def step(self,amount=1):
        for x in range(0,amount):
            self.list.append(self.list[0])
            self.list.pop(0)
    
    def rotate(self,amount=1):
        #finds the position to look
        if amount > len(self.list)-2:
            amount -= len(self.list)-2
        if amount < 1:
            amount += int(len(self.list)/2)
        
        #rotates by a calculated amount
        step_by = (self.list[amount]+1)*(self.list[amount+1]+1)+amount
        self.step(step_by)
    
    def randrange(self,lb,ub):
        size = ub-lb
        if size <= 0:
            return lb
        digits = len(str(size))
        result = ""
        while len(result) < digits:
            result += str(self.list[0])
            step(1)
        result = int(result)
        while result >= size:
            result -= size
        return result + lb












