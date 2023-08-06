"""
File management
"""


def save_txt(filename, results):
    with open(filename, 'a') as f:
        f.write('	'.join(map(str, results))+'\n')
