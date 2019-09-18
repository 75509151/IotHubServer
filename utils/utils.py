import functools
import threading

from rest_framework.exceptions import ValidationError

from .exceptions import *

class Singleton():
    __instance = None
    __lock = threading.Lock()

    def __new__(cls, *args, **kw):
        if cls.__instance is None:
            with cls.__lock:
                if cls.__instance is None:
                    cls.__instance = super(Singleton, cls).__new__(cls)
        return cls.__instance


def get_param(req,param, default):
    return req.query_params.get("param", default)

def gen_condition(req, params, not_empty=False):
    condition = {}
    for p in params:
        val = req.get(p, None)
        if val is not None:
            condition[p] = val
        elif not_empty:
            raise ValidationError(p)

    return condition

