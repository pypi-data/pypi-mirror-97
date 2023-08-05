import logging
import traceback
from functools import wraps

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from py_bootstrap import config

from qg_common_sdk.RedisConnect import get_redis
from qg_common_sdk.catchException import SysCheckException


def verify_code_func(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        request = kwargs['request']
        scope = dict(request)
        headers = scope.get('headers')
        guestUid = ''
        verifyCode = ''
        verify_code_error = False
        for header in headers:
            if bytes.decode(header[0]) == 'guestUid'.lower():
                guestUid = bytes.decode(header[1])
            elif bytes.decode(header[0]) == 'verifyCode'.lower():
                verifyCode = bytes.decode(header[1])
        try:

            if guestUid is not None and guestUid != '':
                if verifyCode is None or verifyCode == '':
                    raise SysCheckException('', '验证码不能为空')
                else:
                    real_verify_code = get_redis(config).get(guestUid)
                    if real_verify_code is None or real_verify_code == '':
                        raise SysCheckException('', '验证码已过期')
                    real_verify_code = str(real_verify_code).replace('"', '')
                    if verifyCode == real_verify_code or verifyCode.upper() == real_verify_code.upper:
                        get_redis(config).delete(guestUid)
                    else:
                        raise SysCheckException('', '验证码不正确')
        except SysCheckException as e:
            verify_code_error = True
            http_status_code = e.code
            return_data = {"data": None,
                           "code": http_status_code, "msg": e.msg}
            logging.exception(e)
            logging.error(traceback.format_exc(), extra={
                          "method": func.__name__, "params": args, "exec": e.data})
            return JSONResponse(
                status_code=http_status_code,
                content=jsonable_encoder(return_data),
            )
        except Exception as e:
            verify_code_error = True
            http_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return_data = {
                "data": None, "code": http_status_code, "msg": str(e)}
            logging.exception(e)
            logging.error(traceback.format_exc(), extra={
                          "method": func.__name__, "params": args})
            return JSONResponse(
                status_code=http_status_code,
                content=jsonable_encoder(return_data),
            )
        finally:
            if not verify_code_error:
                return func(*args, **kwargs)

    return wrapped_function
