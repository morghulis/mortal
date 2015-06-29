# -*- coding:utf-8 -*-

def json_seek(json_obj, condition):
    ways = []
    if isinstance(json_obj, list):
        i = 0
        for obj in json_obj:
            childways = json_seek(obj, condition)
            if childways:
                ways.extend([
                        '[%d]%s'%(i, childway)
                            for childway in childways
                    ])
            i += 1
    elif isinstance(json_obj, dict):
        for k in json_obj.keys():
            childways = json_seek(json_obj[k], condition)
            if childways:
                ways.extend([
                        '[\'%s\']%s'%(k, childway)
                            for childway in childways
                    ])
    else:
        if condition(json_obj):
            ways.append('')
        else:
            return None
    return ways


def json_seek_key(json_obj, condition):
    ways = []
    if isinstance(json_obj, list):
        i = 0
        for obj in json_obj:
            childways = json_seek_key(obj, condition)
            if childways:
                ways.extend([
                        '[%d]%s'%(i, childway)
                            for childway in childways
                    ])
            i += 1
    elif isinstance(json_obj, dict):
        for k in json_obj.keys():
            if condition(k):
                ways.append('[\'%s\']'%k)
            childways = json_seek_key(json_obj[k], condition)
            if childways:
                ways.extend([
                        '[\'%s\']%s'%(k, childway)
                            for childway in childways
                    ])
    else:
        return None
    return ways


if __name__=='__main__':
    import sys, os
    libpath = os.path.abspath('../')
    if not libpath in sys.path:
        sys.path.append(libpath)

    
