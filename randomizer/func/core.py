import copy
import os
import shutil
import math
from PIL import Image





#steps the string number by 1, maintains length, can be specified to give a certain length
def number_string_stepper(number,string_length=-1):
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
    absolute_counter = 0
    counter = 0
    loop_counter = -1
    new_string = ""
    while absolute_counter < length:
        counter += ratio
        absolute_counter += ratio
        loop_counter += 1
        if counter >= 1:
            counter = 0
            new_string += string[loop_counter]
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










