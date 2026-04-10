from pathlib import Path 
import json
from dev.randomizer.parse_config import settings
from dev.randomizer.func.core import randinst as randinst
from dev.randomizer.func.unit import vanilla_cat_array
from dev.randomizer.func.unit import vanilla_unitbuy_array
import dev.randomizer.func.files as f
from dev.randomizer.data.filepaths import *
import dev.randomizer.enums.cats as c

#id,combo set, IDFK, S1 id,S1 form,S2 id,S2 form,S3 id,S3 form,S4 id,S4 form,S5 id,S5 form,effect,level,always -1

BASE = Path(__file__).resolve().parents[2]


def fix_zombie():
    
    # get rid of zombie button
    book_attribute = f.file_reader("nyankoPictureBookData_Attribute.csv")
    book_attribute[6][1] = 99
    book_attribute[6][2] = -1
    book_attribute[6][3] = ""
    f.file_writer("nyankoPictureBookData_Attribute.csv",book_attribute)

    # turn collosus slayer into zombie sorting
    book_effect = f.file_reader("nyankoPictureBookData_EffectAbility.csv")
    book_effect[67][1] = -1
    book_effect[67][3] = 39
    book_effect[67][4] = 225
    book_effect[67][5] = 83
    book_effect[67][6] = 0
    f.file_writer("nyankoPictureBookData_EffectAbility.csv",book_effect)

    #cat_guide = f.file_reader("img015.imgcut")
    #cat_guide[301][0] = 654
    #cat_guide[301][1] = 955
    #cat_guide[301][2] = 51
    #cat_guide[301][3] = 51

    #cat_guide[302][0] = 654
    #cat_guide[302][1] = 955
    #cat_guide[302][2] = 51
    #cat_guide[302][3] = 51

    
    for i in range(1,len(vanilla_cat_array) + 1):
       
       # loop through all units
        file_name = f"unit{i:03}.csv"
        unit_file = f.file_reader(file_name)

        # Extend row
        for row in unit_file:
            if len(row) < 100:
                row.extend([0] * (100 - len(row)))

        # Remove collosus slayer from units  
        for x in range(len(unit_file)):
            if unit_file[x][c.s.collosus_slayer] == 1:
                unit_file[x][c.s.collosus_slayer] = 0
                f.file_writer(file_name,unit_file)
                print(f"Zombie Fix: Collosus Slayer removed from unit {i - 1} form {x + 1}")

        # Make anti zombie units target witch and have collosus slayer
        for x in range(len(unit_file)):
            if unit_file[x][c.s.zombie] == 1:
                unit_file[x][c.s.witch_target] = 1
                unit_file[x][c.s.collosus_slayer] = 1
                unit_file[x][c.s.zombie] = 0
                f.file_writer(file_name,unit_file)
                print(f"Zombie Fix: zombie fix applied on unit {i - 1} form {x + 1}")

        

                


def config_settings():
    print("temp")