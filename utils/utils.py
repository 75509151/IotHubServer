import functools
import threading

class Singleton():
    __instance = None
    __lock = threading.Lock()

    def __new__(cls, *args, **kw):
        if cls.__instance is None:
            with cls.__lock:
                if cls.__instance is None:
                    cls.__instance = super(Singleton, cls).__new__(cls)
        return cls.__instance

