# -*- coding:utf-8 -*-
from errors import XlibError_Xre
import re


class xre(object):

    @staticmethod
    def groups(pattern, text):
        m = re.search(pattern, text)
        if not m:
            return None
        grps = m.groups()
        return grps if len(grps) > 0 else None


    @staticmethod
    def group(pattern, text, name=None):
        m = re.search(pattern, text)
        if not m:
            return None
        if name:
            return m.group(name)
        else:
            return m.group()


    @staticmethod
    def groupdict(pattern, text):
        m = re.search(pattern, text)
        if not m:
            return None
        return m.groupdict()


    @staticmethod
    def findall(pattern, text, flags=0):
        return re.findall(pattern, text, flags)


"""
example:
    class EgMatcher(XreMatcher):
        pattern = 'abc(?P<id>)ef'

        def handle_later(self, key, val):
            maps = {
                'double': lambda val: val*2,
                'threetimes' lambda val: val*3,
            }

            return maps[key](val)

    egm = EgMatcher().getvalue('id', text)
    egm = EgMatcher().getvalue('id')

"""

class XreMatcher(object):
    pattern = None

    def __init__(self):
        if not self.__class__.pattern:
            raise XlibError_Xre, 'Non-None pattern is required, '
        self.groupdict = None


    def handle_later(self, key, val):
        raise XlibError_Xre, 'overriden is required'

        
    def getvalue(self, key, text=None):
        if text:
            self.groupdict = xre.groupdict(
                    self.__class__.pattern, text)
        if not self.groupdict:
            return None

        val = self.groupdict.get(key)
        if not val:
            raise XlibError_Xre, 'invalid key: %s'%(key)

        return self.handle_later(key, val)
