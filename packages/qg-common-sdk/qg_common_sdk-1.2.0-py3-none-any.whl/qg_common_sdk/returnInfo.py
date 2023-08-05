import json
import json
import logging
import time
import traceback
import uuid
from contextvars import ContextVar
from functools import wraps

from fastapi import Request, FastAPI, Response
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from py_bootstrap.config import config as bootstrap_config
from pymongo.errors import DuplicateKeyError

from .RedisConnect import get_redis
from .catchException import StatusCode, EntityNotFoundException, SysCheckException, SysException, BusinessException, \
    SysRunException
from .headerResolve import HeaderResolve
from .operUserInfo import getUserInfo

REQUEST_CTX_KEY = "request"
_request_ctx_var: ContextVar[dict] = ContextVar(REQUEST_CTX_KEY, default=None)


def get_service_id() -> str:
    return _request_ctx_var.get().get('serviceId')


def get_request_id() -> str:
    if not _request_ctx_var.get():
        _request_ctx_var.set({})
    return _request_ctx_var.get().get('requestId')


def get_operator() -> dict:
    return _request_ctx_var.get().get('operator')


def get_request() -> dict:
    return _request_ctx_var.get().get('request')


def get_header() -> HeaderResolve:
    return _request_ctx_var.get().get('header')


def get_logic_entity() -> dict:
    return _request_ctx_var.get().get('logic_entity')


def return_info_func(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):

        exception = None
        http_status_code = status.HTTP_200_OK
        operate_log = {}
        request = None
        if 'request' in kwargs:
            request = kwargs.pop('request')
        operate_log["parameter"] = jsonable_encoder({'args': args, 'kwargs': kwargs})
        operate_log["header"] = get_header().header_dict
        operate_log["operatorInfo"] = get_operator()
        operate_log["methodName"] = func.__name__

        if request:
            kwargs['request'] = request
        try:
            start_time = time.time()
            result = func(*args, **kwargs)
            process_time = time.time() - start_time
            operate_log["status"] = http_status_code
            return_data = {"data": result, "code": http_status_code, "msg": "操作成功"}
            operate_log["workTime"] = str(process_time)
            if process_time > 3:
                logging.warning(operate_log)
            else:
                logging.info(operate_log)
            return JSONResponse(
                status_code=http_status_code,
                content=jsonable_encoder(return_data),
            )
        except (SysCheckException, EntityNotFoundException, BusinessException, SysException, SysRunException) as e:
            http_status_code = e.code
            operate_log["status"] = http_status_code
            # return_data = {"data": e.data, "code": http_status_code, "msg": e.msg}
            logging.error(operate_log, extra={"method": func.__name__, "params": args, "exec": e.data,
                                              "track": traceback.format_exc()}, exc_info=True)
            print(traceback.format_exc())
            exception = e

        except DuplicateKeyError as e:
            http_status_code = StatusCode.BAD_REQUEST
            operate_log["status"] = http_status_code
            # return_data = {"data": e.args[0], "code": http_status_code, "msg": e.details.get('errmsg')}
            logging.error(operate_log, extra={"method": func.__name__, "params": args, "exec": e.args[0],
                                              "track": traceback.format_exc()})
            print(traceback.format_exc())
            exception = e
        except Exception as e:
            http_status_code = StatusCode.INTERNAL_SERVER_ERROR
            operate_log["status"] = http_status_code
            return_data = {"data": e.args[0], "code": http_status_code, "msg": e.args[0]}
            logging.error(operate_log, extra={"method": func.__name__, "params": args, "exec": e.args[0],
                                              "track": traceback.format_exc()})
            print(traceback.format_exc())
            return JSONResponse(
                status_code=http_status_code,
                content=jsonable_encoder(return_data),
            )
        finally:
            if exception:
                raise exception

    return wrapped_function


app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    try:
        scope = dict(request)
        headers = scope.get('headers')
        has_request_id = False
        context_info = {"serviceId": bootstrap_config['app_name']}
        for header in headers:
            if bytes.decode(header[0]) == 'requestid':
                requestid = bytes.decode(header[1])
                if requestid is not None and requestid != '':
                    has_request_id = True
                    context_info["requestId"] = requestid
            elif bytes.decode(header[0]) == 'token':
                token = bytes.decode(header[1])
                try:
                    operator = getUserInfo(token, get_redis(bootstrap_config))
                    context_info["operator"] = operator
                except SysCheckException as e:
                    code = StatusCode.BAD_REQUEST
                    return_data = {"data": None, "code": code, "msg": e.msg}
                    return JSONResponse(
                        status_code=code,
                        content=jsonable_encoder(return_data),
                    )

                # scope['userInfo'] = getUserInfo(token,redis)
                # scope['userInfo'] = {"a": 1}
                # for item in carrier:
                #     sw_http = item.key
                #     if sw_http in request.

        if not has_request_id:
            scope = request.scope
            request_id = str(uuid.uuid1())
            context_info["requestId"] = request_id

            scope.get('headers').append((str('requestid').encode(), request_id.encode()))
            request = Request(scope, request.receive)
        context_info["request"] = request
        context_info["header"] = HeaderResolve(request)
        _request_ctx_var.set(context_info)
        response = await call_next(request)
        return response
    except Exception:
        print(traceback.format_exc())


def deal_common_business_exec(exc):
    http_status_code = exc.code
    return_data = {"data": exc.data, "code": http_status_code, "msg": exc.msg}
    return JSONResponse(
        status_code=http_status_code,
        content=jsonable_encoder(return_data),
    )


# SysCheckException
@app.exception_handler(SysCheckException)
async def unicorn_exception_handler(request: Request, exc: SysCheckException) -> Response:
    return deal_common_business_exec(exc)


# EntityNotFoundException
@app.exception_handler(EntityNotFoundException)
async def unicorn_exception_handler(request: Request, exc: EntityNotFoundException) -> Response:
    return deal_common_business_exec(exc)


# BusinessException
@app.exception_handler(BusinessException)
async def unicorn_exception_handler(request: Request, exc: BusinessException) -> Response:
    return deal_common_business_exec(exc)


# SysRunException
@app.exception_handler(SysRunException)
async def unicorn_exception_handler(request: Request, exc: SysRunException) -> Response:
    return deal_common_business_exec(exc)


# SysException
@app.exception_handler(DuplicateKeyError)
async def unicorn_exception_handler(request: Request, exc: DuplicateKeyError) -> Response:
    http_status_code = StatusCode.BAD_REQUEST
    logic_entity = get_logic_entity()
    details = exc.details
    properties = logic_entity.get('entity').get('properties')
    msg = ''
    for k, v in details["keyValue"].items():
        msg += properties.get(k).get('title') + ","
    if msg:
        msg = msg[:-1] + '重复'
    return_data = {"data": exc.args[0], "code": http_status_code, "msg": msg}
    return JSONResponse(
        status_code=http_status_code,
        content=jsonable_encoder(return_data),
    )


@app.exception_handler(ValueError)
async def unicorn_exception_handler(request: Request, exc: ValueError) -> Response:
    http_status_code = StatusCode.INTERNAL_SERVER_ERROR
    return_data = {"data": exc.args[0], "code": http_status_code, "msg": exc.args[0]}
    return JSONResponse(
        status_code=http_status_code,
        content=jsonable_encoder(return_data),
    )


# 初始化系统异常代码
@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception) -> Response:
    http_status_code = StatusCode.INTERNAL_SERVER_ERROR
    return_data = {"data": exc.args[0], "code": http_status_code, "msg": exc.args[0]}
    return JSONResponse(
        status_code=http_status_code,
        content=jsonable_encoder(return_data),
    )
