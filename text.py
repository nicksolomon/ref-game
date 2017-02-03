# Lot's of stuff for making text prettier
# try to import all the needed libraries, if it doesn't work, 
# make all the functions do nothing.
try:
    import colorama
    from termcolor import colored
    colorama.init()
    def bold(string):
        return colored(string, attrs = ["bold"])
    def underline(string):
        return colored(string, attrs = ["underline"])
    def red(string):
        return colored(string, "red")
    def green(string):
        return colored(string, "green")
except:
    def bold(string):
        return string
    def underline(string):
        return string
    def red(string):
        return string
    def green(string):
        return string

# This makes lines break and makes lists aligned right
import textwrap
import builtins

def print(*arg):
    if len(arg) == 0:
        builtins.print()
    else:
        builtins.print(textwrap.fill(arg[0], 80)) #pad out lines so breaks happen between words

#this is for the hanging indent for lists
wrapper = textwrap.TextWrapper(width = 80, subsequent_indent = "     ")
def print_list(*arg):
    if len(arg) == 0:
        builtins.print()
    else:
        builtins.print(wrapper.fill(arg[0]))


def list_items(items, bold_item = True):
    """
    Lists items in a nice format bi building a dict with the item
    names as keys. Go through the items, if it's already in the dict
    increment the value, else add it to the dict with value 1.
    """
    output = {}
    for i in items:
        if i.name in output:
            output[i.name] += 1
        else:
            output[i.name] = 1
    if bold_item:
        for item in output:
            if output[item] > 1:
                print(bold(str(item)) + " x" + str(output[item]))
            else:
                print(bold(str(item)))
    else:
        for item in output:
            if output[item] > 1:
                print(str(item) + " x" + str(output[item]))
            else:
                print(str(item))      
