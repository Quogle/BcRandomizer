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
    length = 300
    if len(string) < length:
        string = generate_random_string_characters(string)
    if len(string) > length+100:
        string = ratio_shorten_string(string,200)
    
    return string
    
random_string = make_random_string(seed)

#make an object of this class in each function you want to use random in and give it a unique instance id
class randinst():
    """
    create an object of this class and give it an id you think hasnt been used before and use that for randrange
    """
    def __init__(self,instance_id):
        global random_string
        self.string = str(random_string)
        self.index = 0
        self.length = len(self.string)
        self.rotate(instance_id)
    
    # steps an amount and then returns the new indexes value
    def step(self,amount=1):
        self.index += amount
        while self.index >= self.length:
            self.index -= self.length
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
        

        number = int(number)
        while number >= size:
            number -= size
        return (number + lb)








