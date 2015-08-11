# -*- coding:utf-8 -*-
import threading
from context import ContextDocker


def async(daemon=True, block=False, callback=None):
    def async_stub(f):
        def wrapper(*args, **kwargs):
            ctx= ContextDocker()
            @ctx.docker
            def call_func(f, *args, **kwargs):
                ctx.return_val = f(*args, **kwargs)

            thd = threading.Thread(
                target=call_func, args=(f,)+args, kwargs=kwargs)
            thd.setDaemon(daemon)
            thd.start()
            if block:
                thd.join()

            if callback:
                callback(ctx.return_val)

            return ctx.return_val if block else None

        return wrapper
    return async_stub



class ThreadPool(object):    
    pass