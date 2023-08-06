import functools


class _Cache:
    register = dict()

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        arg_key = f'{self.func.__name__}-{args}-{kwargs}'
        if arg_key in self.register.keys():
            return self.register[arg_key]
        else:
            result = self.func(*args, **kwargs)
            self.register[arg_key] = result
            return result

    def __get__(self, instance, owner):
        return functools.partial(self.__call__, instance)


def cache(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return _Cache(func)(*args, **kwargs)
    return wrapper
