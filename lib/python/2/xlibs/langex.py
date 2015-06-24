# -*- coding:utf-8 -*-

pairs2dict = lambda p: {  e[0]:e[1] for e in p }

dicts2pair = lambda d: ( (k, d[k]) for k in d.keys() )


def enum(**items):
    """
    eg:  numbers = enum(one=1, two=2, three=3)
         numbers.one = 1, numbers.two = 2
    """
    return type('enum', (object,), **items)
