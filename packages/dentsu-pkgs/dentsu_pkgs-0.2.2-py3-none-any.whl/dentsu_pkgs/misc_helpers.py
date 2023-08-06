#!/usr/bin/env python3

from datetime import datetime, timedelta


def get_dates_range(start_year, start_month, start_day, end_year, end_month, end_day):
    """Get an inclusive range of dates."""
    end_date = datetime(end_year, end_month, end_day)
    start_date = datetime(start_year, start_month, start_day)

    date_range = [start_date + timedelta(days=n) for n in range((end_date - start_date).days + 1)]

    return date_range


def flatten_json(y):
    out = {}

    def flatten(x, name=""):
        if type(x) is dict:
            if len(x) != 2:
                for a in x:
                    flatten(x[a], name + a + "_")
            else:
                j = 0
                for a in x:
                    while j < 1:
                        flatten(x["value"], name + x[a] + "_")
                        j += 1
        elif type(x) is list:

            i = 0
            for a in x:
                flatten(a, name)
                i += 1
        else:
            out[str(name[:-1]).replace(".", "_")] = str(x)

    flatten(y)
    return out


def split_list(list_, n):
    """Splits a list by a given number (n) and returns a generator object."""
    list_size = len(list_)
    for chunk in range(0, list_size, n):
        yield list_[chunk : min(chunk + n, list_size)]
