import datetime as dt

from math.interpolation import derivative


"""
datetime manipulations
"""


def string_to_datetime(dates):
    return [dt.datetime.strptime(d, '%Y-%m-%d').date() for d in dates]


def datetime_to_string(dt_objs, format='%Y-%m-%d'):
    return [dt.datetime.strftime(d, format) for d in dt_objs]


def datetime_to_float(dates, year_0=1979):
    _d = []
    for date in dates:
        d = str(date).split('-')
        d = (float(d[0])-2020)*365 + float(d[1])*30 + float(d[2])
        _d.append(d)
    return _d

