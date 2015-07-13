# -*- coding:utf-8 -*-
from HTMLParser import HTMLParser
from xlibs.langex import enum


__all__ = ['HtmlParser',]


class HtmlParser(HTMLParser):

    def __init__(self, 
            starttag_rules=None, endtag_rules=None, data_rules=None):

        HTMLParser.__init__(self)

        self.rules = {
            'starttag': starttag_rules if starttag_rules else [],
            'endtag': endtag_rules if endtag_rules else [],
            'data': data_rules if data_rules else [],
        }


    def apply_all_rules(self, where, *args, **kwargs):
        for do_rule in self.rules[where]:
            do_rule(*args, **kwargs)


    def handle_starttag(self, tag, attrs):
        self.apply_all_rules('starttag', tag, attrs)


    def handle_endtag(self, tag):
        self.apply_all_rules('endtag', tag)


    def handle_data(self, data):
        self.apply_all_rules('data', data)

    @staticmethod
    def new_attrs(attrs, key, value):
        d = dict(attrs)
        d[key] = value
        return tuple(d)
