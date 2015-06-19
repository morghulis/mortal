# -*- coding:utf-8 -*-

class ContextDocker(object):

    def __init__(self):
        self.__dict__['gvars'] = {}


    def docker(self, method):
        def wrapper(*args, **kwargs):
            return method(*args, **kwargs)
        return wrapper


    def __setattr__(self, name, value):
        self.__dict__[name] = value


    def __getattr__(self, name):
        return self.__dict__.get(name)
