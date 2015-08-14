# -*- coding:utf -*-
import sys, os

sys.path.append(os.path.abspath('../'))

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

    def traversal(self, visit, on_finish_allchilds=None):
        if visit(self):
            for child in self.childs:
                child.traversal(visit, on_finish_allchilds)
        if on_finish_allchilds:
            on_finish_allchilds(self)



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

    def walk(self, visit, on_finish_allchilds=None):
        # def traverse(node, visit):
        #     if node.value:
        #         visit(node.value)
        #     for child in node.childs:
        #         traverse(child, visit)
        traverse(self.root, visit, on_finish_allchilds)


def htmldom_load(html_dom, htmltext):
    ctx = ContextDocker(curnode=html_dom.root)

    @ctx.docker
    def do_starttag(tag, attrs):
        # print tag, attrs
        node = HtmlDOMNode((tag, attrs))
        ctx.curnode.addnode(node)
        ctx.curnode = node


    @ctx.docker
    def do_data(data):
        # data = data.strip()
        if (not data) or data.strip() == '':
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

    @ctx.docker
    def do_charref(name):
        node = HtmlDOMNode((None, '&%s;'%name))
        ctx.curnode.addnode(node)

    @ctx.docker
    def do_entityref(name):
        node = HtmlDOMNode((None, '&%s;'%name))
        ctx.curnode.addnode(node)



    parser = HtmlParser(
        starttag_rules=[do_starttag,],
        endtag_rules=[do_endtag,], 
        data_rules=[do_data,],
        charref_rules=[do_charref,],
        entityref_rules=[do_entityref,],)
    parser.feed(htmltext)

    return html_dom


def htmldom_seek(html_dom_root, pattern):
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

    node = html_dom_root; _nodes = []
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
                raise HtmlInvalidPatternError
        if funcs != []:
            def do_funcs(x):
                return not (False in [f(x) for f in funcs])
            _nodes = filter(do_funcs, _nodes)

        if _nodes == []:
            raise HtmlInvalidPatternError

    return _nodes if fornodes else _nodes[0]



def htmldom_dump(html_dom_root):
    ctx = ContextDocker(htmltext=[])
    @ctx.docker
    def visit(node):
        if node.value:
            if not node.value[0]:
                ctx.htmltext.append(node.value[1])
            else:
                tag = node.value[0]; attrs = node.value[1]

                attrmsg = ' '.join(
                    [ '%s=\"%s\"'%(attr[0], attr[1]) for attr in attrs ])
                ctx.htmltext.append(
                    '<%s>'%(
                        ' '.join([tag, attrmsg]).strip()
                        )
                    )

    @ctx.docker
    def on_finish_allchilds(node):
        if node.value and node.value[0]:
            tag = node.value[0]
            if tag in DEFAULT_SINGULAR_TAGS and len(node.childs) == 0:
                return
            ctx.htmltext.append('</%s>'%node.value[0])

    html_dom_root.traversal(visit, on_finish_allchilds)
    return ''.join(ctx.htmltext)




htmltext = """
<!doctype html>
    <html>

    <head>
    <meta charset="utf-8">
    </head>
    <body>
    y
       <br><img src=''> x
        <li>a</li>
        <li>b</li>
    </body>
    </html>
"""

if __name__=='__main__':

    html_dom = HtmlDOM()
    htmldom_load(html_dom, htmltext)

    print htmldom_dump(html_dom.root)
