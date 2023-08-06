"""
This method is going to iterate through list and n Sublist and display the Values
"""

def print_list (the_list) :
    #Use recursive function limits to 1000 iterations

    for litem in (the_list) :
        if (isinstance (litem,list)) :
            print_list(litem)
        else:
            print(litem)