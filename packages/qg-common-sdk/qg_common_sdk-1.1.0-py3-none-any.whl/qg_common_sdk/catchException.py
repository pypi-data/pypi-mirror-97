import logging
import traceback
from functools import wraps

from fastapi import status


class StatusCode():
    OK = status.HTTP_200_OK
    BAD_REQUEST = status.HTTP_400_BAD_REQUEST
    INTERNAL_SERVER_ERROR = status.HTTP_500_INTERNAL_SERVER_ERROR


class BusinessException(Exception):
    def __init__(self, data: str, msg: str):
        self.data = data
        self.code = StatusCode.INTERNAL_SERVER_ERROR
        self.msg = msg


class SysException(Exception):
    def __init__(self, data: str, msg: str):
        self.data = data
        self.code = StatusCode.INTERNAL_SERVER_ERROR
        self.msg = msg


class SysRunException(Exception):
    def __init__(self, data: str, msg: str):
        self.data = data
        self.code = StatusCode.INTERNAL_SERVER_ERROR
        self.msg = msg


class SysCheckException(Exception):
    def __init__(self, data: str, msg: str):
        self.data = data
        self.code = StatusCode.BAD_REQUEST
        self.msg = msg


class EntityNotFoundException(Exception):
    def __init__(self, data: str, msg: str):
        self.data = data
        self.code = StatusCode.BAD_REQUEST
        self.msg = msg


# 捕获异常1
def exec_catch_func(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except BusinessException as e:
            logging.error(e.msg, extra={"method": func.__name__, "params": args, "exec": traceback.format_exc()})
        except EntityNotFoundException as e:
            logging.error(e.msg, extra={"method": func.__name__, "params": args, "exec": traceback.format_exc()})
        except SysCheckException as e:
            logging.warning(e.msg, extra={"method": func.__name__, "params": args, "exec": traceback.format_exc()})
        except SysRunException as e:
            logging.error(e.msg, extra={"method": func.__name__, "params": args, "exec": traceback.format_exc()})
        except SysException as e:
            logging.error(e.msg, extra={"method": func.__name__, "params": args, "exec": traceback.format_exc()})
        except Exception as e:
            logging.error(e.args[0], extra={"method": func.__name__, "params": args, "exec": traceback.format_exc()})
        finally:
            return result

    return wrapped_function
