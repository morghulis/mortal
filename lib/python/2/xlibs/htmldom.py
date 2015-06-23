# -*- coding:utf -*-
from htmlparser import HtmlParser
from context import ContextDocker


class HtmlFormatError(Exception): pass


class HtmlDOMNode(object):
    def __init__(self, value, parent=None):
        self.parent = parent
        self.childs = []

        self.value = value

    def addnode(self, node):
        node.parent = self
        self.childs.append(node)


class HtmlDOMTree(object):
    def __init__(self):
        self.root = HtmlDOMNode(value=None)


class HtmlDOM(HtmlDOMTree):
    def __init__(self, allow_unclosed_tags=[]):
        super(HtmlDOM, self).__init__()



ctx = ContextDocker()
ctx.dom = HtmlDOM()
ctx.curnode = ctx.dom.root
ctx.allow_unclosed_tags = ['img','br', 'meta']

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
        if ctx.curnode.value[0] in ctx.allow_unclosed_tags:
            ctx.curnode = ctx.curnode.parent
        else:
            print "tag:", tag
            raise HtmlFormatError
    ctx.curnode = ctx.curnode.parent



htmltext = """
<!doctype html>
    <html>

    <head>
    <meta charset="utf-8">
    </head>
    <body>
        x
        <li>a</li>
        <li>b</li>
    </body>
    </html>
"""

def main():
    parser = HtmlParser(
        starttag_rules=[do_starttag,],
        endtag_rules=[do_endtag,], 
        data_rules=[do_data,])
    parser.feed(htmltext)




if __name__=='__main__':
    main()





