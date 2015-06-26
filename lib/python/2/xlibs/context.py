# -*- coding:utf-8 -*-

class ContextDocker(object):

    def __init__(self, **kwargs):
        self.__dict__['default_kvs'] = kwargs

        self.__dict__['varspace'] = {}
        for k in kwargs.keys():
            self.__dict__['varspace'][k] = kwargs[k]

    def docker(self, method):
        def wrapper(*args, **kwargs):
            return method(*args, **kwargs)
        return wrapper

    def clear(self):
        keys = self.__dict__['varspace'].keys()
        for k in keys:
            if k in self.__dict__['default_kvs']:
                continue
            self.__dict__['varspace'].pop(k)


    def __setattr__(self, name, value):
        self.__dict__['varspace'][name] = value


    def __getattr__(self, name):
        return self.__dict__['varspace'].get(name)
