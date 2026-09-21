
import tadbcmc.data.enums.cats as c
import copy
""" simpler algo:
get info on traits on forms and talents


"""




#first step is process the information from the input arrays
def _establish_initial_variables(all_traits:list[int],form_traits:list[list[int]],talent_traits:list[int]
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





















