# -*- coding:utf -*-
from htmlparser import HtmlParser
from context import ContextDocker

#
# Exceptions for htmldomlib
#
class HtmlFormatError(Exception): pass
class HtmlInvalidPatternError(Exception): pass


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

    def __getitem__(self, key):
        results = []
        for node in self.childs:
            if node.value[0] == key:
                results.append(node)
        return results if results != [] else None


class HtmlDOMTree(object):
    def __init__(self, root=None):
        self.root = root if root else HtmlDOMNode(value=None)


#
# default configuration for most case
#
DEFAULT_SINGULAR_TAGS = [
    'img','br', 'meta', 'input',
]


#
# Core class and functions for users
#
class HtmlDOM(HtmlDOMTree):
    def __init__(self, singular_tags=None, root=None):
        super(HtmlDOM, self).__init__(root)

        if not singular_tags:
            singular_tags = DEFAULT_SINGULAR_TAGS
        self.singular_tags = singular_tags

    def walk(self, visit):
        def traverse(node, visit):
            if node.value:
                visit(node.value)
            for child in node.childs:
                traverse(child, visit)
        traverse(self.root, visit)


def load(html_dom, htmltext):
    ctx = ContextDocker(curnode=html_dom.root)

    @ctx.docker
    def do_starttag(tag, attrs):
        # print tag, attrs
        node = HtmlDOMNode((tag, attrs))
        ctx.curnode.addnode(node)
        ctx.curnode = node


    @ctx.docker
    def do_data(data):
        data = data.strip()
        if (not data) or data == '':
            return 
        #     print data
        # else:
        #     print 'None'; return
        node = HtmlDOMNode((None, data))
        ctx.curnode.addnode(node)

    @ctx.docker
    def do_endtag(tag):
        # print '/%s'%tag
        while tag != ctx.curnode.value[0]:
            if ctx.curnode.value[0] in html_dom.singular_tags:
                ctx.curnode = ctx.curnode.parent
            else:
                # print "tag:", tag
                raise HtmlFormatError
        ctx.curnode = ctx.curnode.parent

    parser = HtmlParser(
        starttag_rules=[do_starttag,],
        endtag_rules=[do_endtag,], 
        data_rules=[do_data,])
    parser.feed(htmltext)


def seek(html_dom, pattern):
    """
      tagname$1.classname#idname>tagname
      return a node or list of nodes matched with `pattern`
      based on last taginfo.
    """
    def getheadtail(s, seps='$.#['):
        i = 0
        while i < len(s):
            if s[i] in seps:
                break
            i += 1
        return (s[:i], s[i:])

    node = html_dom.root; _nodes = []
    for tagdesc in pattern.split('>'):
        # print tagdesc

        fornodes = False if '$' in tagdesc else True

        tag, _tail = getheadtail(tagdesc)
        if len(_nodes) > 1:
            raise HtmlInvalidPatternError
        elif len(_nodes) == 1:
            node = _nodes[0]
        else:
            pass

        _nodes = node[tag]
        if not _nodes:
            return None

        funcs = []
        while _tail != '':
            chsep = _tail[0]
            head, _tail = getheadtail(_tail[1:])
            if chsep == '$':
                if not head.isdigit():
                    raise HtmlInvalidPatternError
                funcs.append(
                    lambda x: x == _nodes[int(head)])
            elif chsep == '.':
                funcs.append(
                    lambda x: ('class', head) in x.value[1])
            elif chsep == '#':
                funcs.append(
                    lambda x: ('id', head) in x.value[1])
            else:
                # print _tail[0]
                raise HtmlInvalidPatternError
        if funcs != []:
            def do_funcs(x):
                return not (False in [f(x) for f in funcs])
            _nodes = filter(do_funcs, _nodes)

        if _nodes == []:
            raise HtmlInvalidPatternError
        # node = _nodes[0]

    return _nodes if fornodes else _nodes[0]




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
