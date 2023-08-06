from inspect import currentframe, getframeinfo
from time import time, ctime
from os import path, sys 
from functools import wraps


class PyExecTime():
    def __init__(self, file=sys.stdout):
        __current_frame = currentframe()
        self.__back_frame = __current_frame.f_back
        self.__back_s_line = self.__back_frame.f_lineno
        self.__text = "Execution took %lf seconds"
        self.__filename = getframeinfo(self.__back_frame).filename
        self.__file = file

    def __exit__(self, exc_type, exc_val, exc_tb):
        __time_taken = (time() - self.__start_t)/1000
        __back_e_line = self.__back_frame.f_lineno
        final_text = '[{0} {1}({2}) <{3}:{4}>] -> {5}'.format(
            ctime(), type(self).__name__, path.relpath(self.__filename),
            self.__back_s_line, __back_e_line, (self.__text % __time_taken)
        )
        print('\n' + final_text, file=self.__file, end='\n\n')

    def __enter__(self):
        self.__start_t = time()


def py_exec_time(file=sys.stdout):
    def wrapper(fn):
        @wraps(fn)
        def inner(*argv, **kwargv):
            __text="Execution took %lf seconds"
            __current_frame = currentframe()
            __back_frame = __current_frame.f_back
            __back_s_line = __back_frame.f_lineno
            __filename = getframeinfo(__back_frame).filename
            __start_time = time()
            result = fn(*argv, **kwargv)
            __time_taken = (time() - __start_time)/1000
            final_text = '[{0} {1}({2}) <@{3}:{4}>] -> {5}'.format(
                ctime(), 'PyExecTime', path.relpath(__filename),
                fn.__name__, __back_s_line, (__text % __time_taken)
            )
            print('\n' + final_text, file=file, end='\n\n')
            return result
        return inner
    return wrapper