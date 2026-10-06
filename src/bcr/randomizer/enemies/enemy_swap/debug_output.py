
import tadbcmc.core.simple_funcs as simp




def output_somewhere(output_info,output_one_by_one:bool=False,log=None):
    """  """
    #first get the means through which to output it
    if log == None:
        output_method = print
    else:
        output_method = log
    #this currently has no functionality for log
    if output_one_by_one:
        simp.print_array_one_by_one(output_info)
    else: #now just do it elsewise
        output_method(output_info)

















