# -*- coding:utf -*-
from htmlparser import HtmlParser
from context import ContextDocker

#
# Exceptions for htmldomlib
#
class HtmlFormatError(Exception): pass


#
# Data structures for htmldomlib
#
class HtmlDOMNode(object):
    def __init__(self, value, parent=None):
        self.parent = parent
        self.childs = []

        self.value = value

    def addnode(self, node):
        node.parent = self
        self.childs.append(node)


class HtmlDOMTree(object):
    def __init__(self, root=None):
        
        self.root = root if root else HtmlDOMNode(value=None)


#
# default configuration for most case
#
DEFAULT_SINGULAR_TAGS = ['img','br', 'meta']


#
# Core class and functions for users
#
class HtmlDOM(HtmlDOMTree):
    def __init__(self, singular_tags=None, root=None):
        super(HtmlDOM, self).__init__(root)

        if not singular_tags:
            singular_tags = DEFAULT_SINGULAR_TAGS
        self.singular_tags = singular_tags


def load(htmltext):
    html_dom = HtmlDOM()

    ctx = ContextDocker(curnode=html_dom.root)

    @ctx.docker
    def do_starttag(tag, attrs):
        print tag, attrs
        node = HtmlDOMNode((tag, attrs))
        ctx.curnode.addnode(node)
        ctx.curnode = node


    @ctx.docker
    def do_data(data):
        if data:
            print data
        else:
            print 'None'
        node = HtmlDOMNode((None, data))
        ctx.curnode.addnode(node)

    @ctx.docker
    def do_endtag(tag):
        print tag
        while tag != ctx.curnode.value[0]:
            if ctx.curnode.value[0] in html_dom.singular_tags:
                ctx.curnode = ctx.curnode.parent
            else:
                print "tag:", tag
                raise HtmlFormatError
        ctx.curnode = ctx.curnode.parent

    parser = HtmlParser(
        starttag_rules=[do_starttag,],
        endtag_rules=[do_endtag,], 
        data_rules=[do_data,])
    parser.feed(htmltext)

    return html_dom



# htmltext = """
# <!doctype html>
#     <html>

#     <head>
#     <meta charset="utf-8">
#     </head>
#     <body>
#         x
#         <li>a</li>
#         <li>b</li>
#     </body>
#     </html>
# """
