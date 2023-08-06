import functools
import inspect
import datetime
import traceback
import sys


class _StdoutHandler:
    def __init__(self, filename):
        self.filename = filename

    def write(self, text):
        with open(self.filename, 'a') as f:
            if text != '\n':
                f.write(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")}]\n{text}')
            f.write('\n')

    def flush(self):
        pass


class _Print2Log:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        original_stdout = sys.stdout
        sys.stdout = _StdoutHandler(f'{inspect.stack()[2].filename.replace(".py", "")}_[{self.func.__name__}].log')
        try:
            result = self.func(*args, **kwargs)
            return result
        finally:
            sys.stdout = original_stdout

    def __get__(self, instance, owner):
        return functools.partial(self.__call__, instance)


def print2log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return _Print2Log(func)(*args, **kwargs)

    return wrapper
