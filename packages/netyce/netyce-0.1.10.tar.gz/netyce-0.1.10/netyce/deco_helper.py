from time import time
import functools


def timer(func):
    """Functools makes sure the function identification is correct.
    e.g. with functools:
    func
    <function func at 0x7f7bbc020620>

    without functools:
    func
    <function timer.<locals>.wrapper at 0x7faaf999d378>

    https://realpython.com/python-timer/#a-python-timer-decorator
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        before = time()
        rv = func(*args, **kwargs)
        print('time required (%s): %s' % (func.__name__, time() - before))
        return rv
    return wrapper
