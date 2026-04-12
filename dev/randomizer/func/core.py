import copy
import os
import shutil
import math
from PIL import Image
from dev.randomizer.parse_config import seed



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

#shortens a string to length by taking every Nth character in the string
def ratio_shorten_string(string,length):
    try:
        ratio = int(1000*length/len(string))/1000
    except:
        return  ""
    counter = 0
    position = -1
    new_string = ""
    while True:
        counter += ratio
        position += 1
        if position < len(string):
            if counter >= 1:
                counter -= 1
                new_string += string[position]
        else:
            break
    return new_string

#takes a string of numbers and creates a semi random string of numbers based on it
def generate_random_string_characters(base_string):
    randomlist = ""
    if len(base_string) < 2:
        base_string += "12"
    for x in range(1,len(base_string)):
        radians = str(math.radians(1+int(base_string[x])*int(base_string[x-1])))
        randomlist += radians[2:]
    return randomlist

#dont use
#input seed and it makes random_list an array of single value random numbers 0-9, length varies based on seed
def make_random_list(seed):
    string = generate_random_string_characters(str(abs(seed)))
    if len(string) < 50:
        string = generate_random_string_characters(string)
    if len(string) > 200:
        string = ratio_shorten_string(string,200)
    

    random_array = []
    for x in string:
        random_array.append(int(x))
    global random_list
    random_list = random_array

# creates a string 100-200 characters long of numbers 0-9
def make_random_string(seed):
    string = generate_random_string_characters(str(abs(seed)))
    length_min = 300
    length_max = 400
    while len(string) < length_min:
        string = generate_random_string_characters(string)
    if len(string) > length_max:
        string = ratio_shorten_string(string,length_max)
    return string
    
random_string = make_random_string(seed)

#make an object of this class in each function you want to use random in and give it a unique instance id
class randinst():
    """
    create an object of this class and give it an id you think hasnt been used before and use that for randrange
    """
    def __init__(self,instance_id,user_specified = True):
        global random_string
        self.string = str(random_string)
        self.index = 0
        self.length = len(self.string)
        #these are extras to prevent it from looping as much
        self.user_specified = user_specified #required to stop infinite recursion
        if self.user_specified:
            self.shifter = randinst(instance_id+1,False) #second instance to generate shift
        self.current_shift = 0 #the amount stepped by in step (part of whats changed by shifter)

        self.rotate(instance_id)
    
    # steps an amount and then returns the new indexes value
    def step(self,amount=1):
        self.index += amount
        if amount == 1:
            self.index += self.current_shift
        while self.index >= self.length: #uses a while loop to do this so progressively larger step amounts do actually have an effect
            self.index -= self.length
            self.index += self.shifter.step()
            self.current_shift = self.shifter.step()
        return int(self.string[self.index])
    
    #shifts the index by a large amount
    def rotate(self,amount=1):
        # gets a proper amount
        if amount > self.length-2:
            amount -= self.length-2
        if amount < 1:
            amount += int(self.length/2)
        
        #rotates by a calculated amount
        step_by = (1+self.step(amount))*(1+self.step())
        self.step(int(step_by))
    
    #returns an almost evenly distributed random number
    def randrange(self,lb,ub):
        size = ub-lb
        if size <= 0:
            return lb
        
        #makes number 1 digit longer than digits
        digits = str(size)
        number = ""
        while len(number) <= len(digits):
            number += str(self.step())
        

        number = int(number) % size
        return (number + lb)
    
    def weighted_choice(self, choices, weights):
        total = sum(weights)
        if total <= 0:
            raise ValueError("Weights must sum to a positive value")

        # pick a random position along the weighted line
        pos = self.randrange(0, total)  

         # move down each choice’s segment until the random point falls inside
        for i, weight in enumerate(weights):
            pos -= weight
            if pos < 0:  # once the random point is inside this segment
                return choices[i]

    def weighted_list(self,weights):
        """
        takes weights list and returns an index in that list
        input [20,20,40,20,20] and get an index from 0-4 for example
        """
        total = 0
        for each in weights:
            total += each
        number = self.randrange(0,total)
        for x in range(0,len(weights)):
            if number < weights[x]:
                return x
            else:
                number -= weights[x]
        #if all fails output -1
        return -1
    
    def clamp_value(value):
        """
        clamps a value as an int between 0-100, on r for convenience
        """
        if value<0:
            value = 0
        if value>100:
            value = 100
        return int(value)







