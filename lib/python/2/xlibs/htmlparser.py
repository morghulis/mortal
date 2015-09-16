# -*- coding:utf-8 -*-
from HTMLParser import HTMLParser
from xlibs.langex import enum


__all__ = ['HtmlParser',]


class HtmlParser(HTMLParser):

    def __init__(self, 
            starttag_rules=None, endtag_rules=None, data_rules=None,
            charref_rules=None, entityref_rules=None):

        HTMLParser.__init__(self)

        self.rules = {
            'starttag': starttag_rules if starttag_rules else [],
            'endtag': endtag_rules if endtag_rules else [],
            'data': data_rules if data_rules else [],
            'charref': charref_rules if charref_rules else [],
            'entityref': entityref_rules if entityref_rules else [],
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


    def handle_charref(self, name):
        self.apply_all_rules('charref', name)


    def handle_entityref(self, name):
        self.apply_all_rules('entityref', name)
        

    @staticmethod
    def new_attrs(attrs, key, value):
        d = dict(attrs)
        d[key] = value
        return tuple(d)


class PseudoAttrsdict(object):
    def __init__(self, attrs):
        self.attrs = attrs

    def __getitem__(self, name):
        for attr in self.attrs:
            if attr[0] == name:
                return attr[1]
        raise KeyError, name

    def get(self, name, default_value=None):
        try:
            return self.__getitem__(name)
        except KeyError:
            return default_value
