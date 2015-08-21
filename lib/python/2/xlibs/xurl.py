# -*- coding:utf-8 -*-
import os


_DEFAULT_PORTS = {
    'http': 80,
    'https': 443,
}


def split(url):
    proto, _rest = url.split('://', 1)
    proto = proto.lower()

    host_port, location = _rest.split('/', 1)

    hp = host_port.split(':')
    host = hp[0].lower()
    port = int(hp[1]) if len(hp) > 1 else _DEFAULT_PORTS[proto]

    return (proto, host, port, location)


def is_absurl(url):
    return len(url.split('://', 1)) > 1


def absurl(url, refer_url):
    if url == '':
        return refer_url

    if is_absurl(url):
        return url

    proto, host, port, location = split(refer_url)

    if _DEFAULT_PORTS[proto] == port:
        host_port = host
    else:
        host_port = '%s:%d'%(host, port)


    if url[0] == '/':
        return '%s://%s/%s'%(proto, host_port, url[1:])

    else:
        return '%s://%s/%s/%s'%(
            proto, host_port, 
            refer_url.rsplit('/', 1)[0], url)
