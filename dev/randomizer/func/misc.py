



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

def stringize_number(number,length):
    """
    turns (43,3) into 043
    """
    output = "0"*length + str(number)
    return output[-length:]

def clamp_value(value):
        """
        clamps a value as an int between 0-100
        """
        if value<0:
            value = 0
        if value>100:
            value = 100
        return int(value)












