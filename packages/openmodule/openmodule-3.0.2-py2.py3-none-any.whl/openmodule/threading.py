import traceback

import os
import sys
from functools import partial

import logging
import time
from zmq import ContextTerminated


def _thread_wrapper(*args, _run_function, _return_code, **kwargs):
    try:
        _run_function(*args, **kwargs)
    except (KeyboardInterrupt, ContextTerminated):  # pragma: no cover
        pass
    except Exception as e:  # pragma: no cover
        logging.exception(e)
        sys.stderr.flush()
        time.sleep(1)
        os._exit(_return_code)


def get_thread_wrapper(function, return_code=10):
    return partial(_thread_wrapper, _run_function=function, _return_code=return_code)
