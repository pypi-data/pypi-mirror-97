import re


def find_between_quotations(s):
    try:
        return re.findall('"([^"]*)"', str(s))[0]
    except IndexError:
        return print('No match')


def find_number(s):
    return re.findall(r'\d+', s)
