# -*- coding:utf-8 -*-
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