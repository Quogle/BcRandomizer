import tadbcmc.core.game_files as game_files

import tadbcmc.data.enums.cats as c
import tadbcmc.data.enums.enemy as e


def fix_zombie():
    vanilla_cat_array = game_files.get_cat_stats(vanilla=True)

    img015 = game_files.file_reader("img015.imgcut", vanilla=True)
    img015[331][0] = 211
    img015[331][1] = 698
    img015[331][2] = 41
    img015[331][3] = 41

    img015[229][0] = 410
    img015[229][1] = 856
    img015[229][2] = 51
    img015[229][3] = 51

    game_files.file_writer("img015.imgcut", img015)

    # get rid of zombie button
    book_attribute = game_files.file_reader(
        "nyankoPictureBookData_Attribute.csv",
        vanilla=True
    )    
    book_attribute[6][1] = 99
    book_attribute[6][2] = -1   # icon
    book_attribute[6][3] = ""

    book_attribute[13][2] = 83  # make witch icon into zombie

    game_files.file_writer(
        "nyankoPictureBookData_Attribute.csv",
        book_attribute
    )
    

    # turn colossus slayer into zombie sorting
    book_effect = game_files.file_reader(
        "nyankoPictureBookData_EffectAbility.csv",
        vanilla=True
    )

    for row in book_effect:
        row[1] += 1

    book_effect[67][1] = 0     # position within section in cat guide
    book_effect[67][3] = 39
    book_effect[67][4] = 225
    book_effect[67][5] = 83    # the icon
    book_effect[67][6] = 0     # section in cat guide

    game_files.file_writer(
        "nyankoPictureBookData_EffectAbility.csv",
        book_effect
    )

    enemy_file = game_files.file_reader(
        "t_unit.csv",
        vanilla=True
    )

    for i in range(1, len(enemy_file)):
        if enemy_file[i][e.s.collosus] == 1:
            enemy_file[i][e.s.collosus] = 0
            game_files.file_writer("t_unit.csv", enemy_file)
            print(f"Zombie Fix: Remove colossus from enemy {i}")

        if enemy_file[i][e.s.zombie] == 1:
            enemy_file[i][e.s.witch] = 1
            game_files.file_writer("t_unit.csv", enemy_file)
            print(f"Zombie Fix: Fix applied to {i}")

    for i in range(1, len(vanilla_cat_array) + 1):

        file_name = f"unit{i:03}.csv"

        unit_file = game_files.file_reader(
            file_name,
            vanilla=True
        )

        # Extend rows in unit file so they long n shit
        for row in unit_file:
            if len(row) < 100:
                row.extend([0] * (100 - len(row)))

        # Remove colossus slayer from units
        for x in range(len(unit_file)):
            if unit_file[x][c.s.collosus_slayer] == 1:
                unit_file[x][c.s.collosus_slayer] = 0
                game_files.file_writer(file_name, unit_file)

                print(
                    f"Zombie Fix: Collosus Slayer removed "
                    f"from unit {i - 1} form {x + 1}"
                )

        # Make anti zombie units target witch and have collosus slayer
        for x in range(len(unit_file)):
            if unit_file[x][c.s.zombie] == 1:
                unit_file[x][c.s.witch_target] = 1
                unit_file[x][c.s.collosus_slayer] = 1
                unit_file[x][c.s.zombie] = 0

                game_files.file_writer(file_name, unit_file)

                print(
                    f"Zombie Fix: zombie fix applied on "
                    f"unit {i - 1} form {x + 1}"
                )