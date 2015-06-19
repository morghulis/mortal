# -*- coding:utf-8 -*-
import os, time
import random



__all__ = ['DebugHelper',]


Default_Separator = '\r\n-*--*--*--*--*--*--*--*--*--*--*--*--*-\r\n'



class DebugHelper(object):
    """
    eg. dbg = DebugHelper(<basedir>)
        dbg.dumps([a,b,c,d])
    """

    def __init__(self, basedir, sep=Default_Separator, 
            echo=False, prefer_newfile=True, filename_generator=None):

        self.basedir = basedir
        self.sep = sep
        self.echo = echo
        self.newfile = prefer_newfile
        self.logfilename = None

        if filename_generator: 
            self.filename_generator = filename_generator
        else:
            self.filename_generator = self._filename_generator()


    def _filename_generator(self):
        while True:
            while True:
                fullname = os.path.join(self.basedir, 
                        '%012f.%04d.log'%(
                        time.time(), random.randint(0, 9999))
                    )
                if not os.path.exists(fullname):
                    break

            yield fullname


    def echo_message(self, message, echo):
        if echo is None:
            echo = self.echo

        if echo:
            print(message)


    def save(self, message, newfile):
        if newfile is None:
            newfile = self.newfile

        if newfile or self.logfilename is None:
            self.logfilename = self.filename_generator.next()

        with open(self.logfilename, 'w') as f:
            f.write(message)


    def format_message(self, message):
        prefix = '----------\r\n%012f\r\n----------\r\n'%(time.time())
        suffix = '\r\n'

        return '%s%s%s'%(prefix, message, suffix)


    def dump(self, message, echo=None, newfile=None):
        message = self.format_message(message)

        self.echo_message(message, echo)
        self.save(message, newfile)


    def dumps(self, messagelist, echo=None, newfile=None):

        self.dump(
            self.sep.join(messagelist), echo, newfile)


if __name__=='__main__':
    import sys
    basedir = os.path.abspath(os.path.split(sys.argv[0])[0])

    dbg = DebugHelper(basedir)

    dbg.dumps([
            'dfjklxcckla', 
            '发生的建',
            open('sss.txt').read()
        ])
