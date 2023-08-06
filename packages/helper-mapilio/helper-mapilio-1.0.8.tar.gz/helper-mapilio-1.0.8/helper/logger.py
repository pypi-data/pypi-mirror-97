import os
import time
import warnings

from functools import wraps

_total_time_call_stack = [0]


def timeLog(log_fun):
    def _timeLog(fn):
        @wraps(fn)
        def wrapped_fn(*args, **kwargs):
            global _total_time_call_stack
            _total_time_call_stack.append(0)

            start_time = time.time()

            try:
                result = fn(*args, **kwargs)
            finally:
                elapsed_time = time.time() - start_time

                _total_time_call_stack[-1] += elapsed_time

                hours, rem = divmod(time.time() - start_time, 3600)
                minutes, seconds = divmod(rem, 60)
                elapsed_time = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)

                # log the result
                log_fun(message={
                    'function_name': fn.__name__,
                    'total_time': elapsed_time,
                })

            return result

        return wrapped_fn

    return _timeLog


def _log(message):
    timing_save_as_log(message)


def timing_save_as_log(message):
    PATH = 'TimingResult.log'
    tLf = Logger.file_exist_check_and_open(PATH)

    L = '[TimeTracker >] {function_name} {total_time}'.format(**message)
    tLf.writelines(L + '\n')
    tLf.close()


class Logger:

    @staticmethod
    def file_exist_check_and_open(path: str):
        if os.path.exists(path):
            append_write = 'a'  # append if already exists
        else:
            append_write = 'w'  # make a new file if not

        return open(path, append_write)

    @staticmethod
    def file_check():
        if not os.path.exists(os.path.dirname("exports")):
            try:
                os.makedirs("src/visiobrain/exports")
                os.makedirs("src/visiobrain/exports/calc")
            except OSError as err:
                print(err)

    @staticmethod
    def disable_warnings():
        # remove all the annoying warnings from tf v1.10 to v1.13
        import logging

        logging.getLogger('tensorflow').disabled = True

        def warn(*args, **kwargs):
            pass

        warnings.warn = warn