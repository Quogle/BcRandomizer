
import tadbcmc.data.enums.cats as c
import copy
""" simpler algo:
first handle the 1 allowed trait exception
get info on traits on forms and talents
if but white, map white to something and remove it from further allowed traits
map traits common across forms first
if avoid old, map unused traits (non form specific have priority) to currently unused allowed traits
map traits specific to one form to those of others if possible


"""


def _one_allowed_trait(allowed_traits:list[int],look_order:list[int]):
    """ maps all in all_traits to the one allowed trait """
    that_trait = allowed_traits[0]
    to_traits = [that_trait]*len(look_order)
    from_traits = copy.deepcopy(look_order)
    return (from_traits,to_traits)

#first step is process the information from the input arrays
def _establish_initial_variables(
        all_traits:list[int],
        form_traits:list[list[int]],
        talent_traits:list[int]
    ) -> tuple[list[int],list[int],bool]:
    """ return (output_forms, output_talents, but_white)
    \n creates a list of traits per form from the traits in all traits and returns it
    \n considers all traits and all but one trait as no traits, returns a bool for if it is all except white specifically """
    output_forms = []
    output_talents = []
    but_white = False
    #first do forms
    for form in range(0,len(form_traits)):
        this_form = []
        for trait in all_traits:
            if trait in form_traits[form]:
                this_form.append(trait)
        #now all buts
        if len(form_traits[form]) >= len(all_traits)-1:
            this_form = []
            if int(c.t.white) not in form_traits[form]:
                but_white = True
        #attatch the remaining array
        output_forms.append(this_form)
    #now do talents
    for trait in all_traits:
        if trait in talent_traits:
            output_talents.append(trait)
    #now all buts
    if len(output_talents) >= len(all_traits)-1:
        if int(c.t.white) not in output_talents:
                but_white = True
        output_talents = []
    return (output_forms,output_talents,but_white)

def _handle_all_but_white_exception(
        from_traits:list[int],
        to_traits:list[int],
        all_but_white:bool,
        allowed_traits:list[int],
        look_order:bool,
        form_traits:list[int],
        avoid_old:bool,
        talent_traits:list[int]
        ) -> tuple[list[int],list[int],list[int]]:
    """ return (from_traits,to_traits,allowed_traits)
    \n maps white to a trait and removes it from allowed traits """
    allowed_traits = copy.deepcopy(allowed_traits)
    if all_but_white:
        failed = True
        if avoid_old:
            #get all traits a unit has
            has_traits = []
            for form in form_traits:
                for trait in form:
                    if trait not in has_traits:
                        has_traits.append(trait)
            for trait in talent_traits:
                if trait not in has_traits:
                    has_traits.append(trait)
            #now get the first non white one in look order
            for trait in look_order:
                if trait in allowed_traits and trait in has_traits and trait != int(c.t.white):
                    failed = False
                    from_traits.append(int(c.t.white))
                    to_traits.append(trait)
                    #now remove it from allowed
                    allowed_traits.remove(trait)
                    break
        if failed:
            #set white to the first in look order thats in allowed
            for trait in look_order:
                if trait in allowed_traits and trait != int(c.t.white):
                    from_traits.append(int(c.t.white))
                    to_traits.append(trait)
                    #now remove it from allowed
                    allowed_traits.remove(trait)
                    break
    return (from_traits,to_traits,allowed_traits)

def _handle_persistant_traits(
        from_traits:list[int],
        to_traits:list[int],
        all_traits:list[int],
        look_order:list[int],
        allowed_traits:list[int],
        form_traits:list[int],
        talent_traits:list[int],
        avoid_old:list[int],
    ) -> tuple[list[int],list[int]]:
    """ return (from_traits,to_traits)
    \n maps those traits existing across multiples forms not already mapped """
    #first step is getting those traits not mapped (counting talents on third form)
    unplaced_form_traits = []
    for form in range(0,len(form_traits)):
        this_form = []
        for trait in all_traits:
            if trait in form_traits[form] and trait not in from_traits:
                this_form.append(trait)
            if form == 2:
                if trait in talent_traits and trait not in form_traits:
                    this_form.append(trait)
        unplaced_form_traits.append(this_form)
    #now we get persistant traits
    persistant_traits = []
    for trait in all_traits:
        count = 0
        for form in unplaced_form_traits:
            if trait in form:
                count += 1
        if count > 1 and trait not in from_traits: #no sense in doing aleady mapped traits afterall
            persistant_traits.append(trait)
    #now place those according avoid old or not
    if avoid_old:
        #gonna need all traits on the unit originally for this
        old_traits = []
        for trait in all_traits:
            for form in form_traits:
                if trait in form and trait not in old_traits:
                    old_traits.append(trait)
            if trait in talent_traits and trait not in old_traits:
                old_traits.append(trait)
        #first step is getting all allowed not mapped to yet and all allowed not on og unit not mapped to yet
        unused_allowed = []
        unused_allowed_not_old = []
        for trait in all_traits:
            if trait in allowed_traits and trait not in to_traits:
                unused_allowed.append(trait)
                if trait not in old_traits:
                    unused_allowed_not_old.append(trait)
        #a persistant trait can never also be an unused not in old so this doesnt need any duplicate check
        #however I would prefer to make those traits that are duplicates have priority in being placed so I will put them at the start of persistant traits
        for x in range(0,len(persistant_traits)):
            if persistant_traits[x] in unused_allowed:
                persistant_traits.insert(0,persistant_traits.pop(x))
        set_to_remove = []
        for trait in persistant_traits:
            found = False
            for new_trait in look_order:
                if not found and new_trait in unused_allowed_not_old:
                    #set it and remove from both
                    found = True
                    to_traits.append(new_trait)
                    from_traits.append(trait)
                    unused_allowed_not_old.remove(new_trait)
                    unused_allowed.remove(new_trait)
                    set_to_remove.append(trait)
        for trait in set_to_remove:
            persistant_traits.remove(trait)
        #now if there are any persistant traits remaining try to map them to unused allowed traits
        set_to_remove = []
        for trait in persistant_traits:
            found = False
            for new_trait in look_order:
                if not found and new_trait in unused_allowed and new_trait != trait: #just skip it if its a duplicate and somehow didnt get fixed earlier
                    #set it and remove
                    found = True
                    to_traits.append(new_trait)
                    from_traits.append(trait)
                    unused_allowed.remove(new_trait)
                    set_to_remove.append(trait)
        for trait in set_to_remove:
            persistant_traits.remove(trait) #is there any sense in this since its never used after this?
        #if theres any persistant trait remaining at this point it will simply be mapped to a duplicate trait in a function later on
    else:
        #what to do if its not supposed to avoid old?
        #just map it to literally anything except itself
        unused_allowed = []
        for trait in all_traits:
            if trait in allowed_traits and trait not in to_traits:
                unused_allowed.append(trait)
        #put the duplicates at the front of persistant
        for x in range(0,len(persistant_traits)):
            if persistant_traits[x] in unused_allowed:
                persistant_traits.insert(0,persistant_traits.pop(x))
        #now just set each one to one that isnt itself
        set_to_remove = []
        for trait in persistant_traits:
            found = False
            for new_trait in look_order:
                if not found and new_trait in unused_allowed and new_trait != trait:
                    #set and remove
                    found = True
                    to_traits.append(new_trait)
                    unused_allowed.remove(new_trait)
                    from_traits.append(trait)
                    set_to_remove.remove(trait)
        #now remove em all
        for trait in set_to_remove:
            persistant_traits.remove(trait) #is there any point in this?
    return (from_traits,to_traits)

def _handle_avoid_old_unused_traits(
        from_traits:list[int],
        to_traits:list[int],
        all_traits:list[int],
        look_order:list[int],
        allowed_traits:list[int],
        form_traits:list[int],
        talent_traits:list[int],
        avoid_old:list[int],
    ) -> tuple[list[int],list[int]]:
    """ return (form_traits,to_traits)
    \n attempts to map those traits that arent form specific first, then those that are to traits a unit didnt originally have """
    if avoid_old: #this function just shouldnt do anything if it isnt avoid old
        old_traits = [] #all traits a unit originally had
        unplaced_traits = [] #traits a unit has that still need to be placed
        unplaced_single_form_traits = [] #traits a unit has on only one form that still need to be placed
        for trait in all_traits:
            form_count = 0
            for form in form_traits:
                if trait in form:
                    form_count += 1
                    if trait not in old_traits:
                        old_traits.append(trait)
                    if trait not in from_traits and trait not in unplaced_traits:
                        unplaced_traits.append(trait)
            if trait in talent_traits:
                form_count += 1
                if trait not in old_traits:
                    old_traits.append(trait)
                if trait not in from_traits and trait not in unplaced_traits:
                    unplaced_traits.append(trait)
            if form_count == 1: #it only appeared on one form/talents
                if trait not in from_traits:
                    unplaced_single_form_traits.append(trait)
        #now get all the currently unused allowed
        unused_allowed = []
        unused_allowed_not_old = []
        for trait in all_traits:
            if trait in allowed_traits and trait not in to_traits:
                unused_allowed.append(trait)
                if trait not in old_traits:
                    unused_allowed_not_old.append(trait)
        #get the multi form traits
        unplaced_multiform_traits = []
        for trait in unplaced_traits:
            if trait not in unplaced_single_form_traits:
                unplaced_multiform_traits.append(trait)
        



def _handle_form_specific_traits(
        from_traits:list[int],
        to_traits:list[int],
        all_traits:list[int],
        look_order:list[int],
        allowed_traits:list[int],
        form_traits:list[int],
        talent_traits:list[int],
        avoid_old:list[int],
    ) -> tuple[list[int],list[int]]:
    """ attempts to map traits only on one form to traits on other forms, unused first """
    #first step is getting the traits specific to each form (and also the ones still not place)
    specific_to_form_traits = []
    specific_to_form_traits_unplaced = []
    for trait in all_traits:
        for x in range(0,len(form_traits)):
            pass
















