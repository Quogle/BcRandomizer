import tadbcmc.core.game_files as gf
import tadbcmc.core.seeded_randomization as rand
import tadbcmc.data.enums.nyancombo as nc
import tadbcmc.pieces.combos as combos














def add_all_unit_down_combos():
    """ adds a down combo for all units """
    #initialize needed info
    vanilla_stats = gf.get_cat_stats(vanilla=True)
    r = rand.randinst(43)
    number_of_effects = 1
    for each in nc.effect:
        number_of_effects += 1
        print("wow I iterated through an enum! (idk if that works)")
    #we dont need to consider combo id if using tadbcmc
    for unit_id in range(0,len(vanilla_stats)):
        this_combo_name = "" #dont feel like figuring out how to get cat names rn
        combos.add_combo(u1id=unit_id,u1form=0,comboset=nc.set.Eoc1,effect=r.randrange(0,number_of_effects),level=nc.mult.down,name=this_combo_name) #this would need changing if we wanna do combos per form














