"""
Console
"""

from termcolor import colored


def units(s, u):
    if not isinstance(s, type(str)):
        s = str(s)
    return s + ' '*(20-len(s.replace("\n", ""))) + '[{}]'.format(u.rstrip())


def result(var, val, u, r=5):
    print(units(str('{} = {:,.'+'{}'.format(r)+'f}').format(var, val), u))
    
    
def print_color(text, color):
    print(colored(text, color))


def print_positive(text, attrs=None):
    print(colored(text, 'grey', attrs=attrs))


def print_negative(text, attrs=None):
    print(colored(text, 'red', attrs=attrs))
