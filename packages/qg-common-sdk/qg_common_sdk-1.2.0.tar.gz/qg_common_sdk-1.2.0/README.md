# 底层封装工具类
## 异常处理
自定义异常信息
catchException.py
```
# 业务异常类封装
class BusinessException(Exception):
    def __init__(self, data: str,msg: str):
        self.data = data
        self.code = StatusCode.BUSINESSEXEC
        self.msg = msg
# 异常封装类
class SysException(Exception):
    def __init__(self, data: str,msg: str):
        self.data = data
        self.code = StatusCode.SYSEXEC
        self.msg = msg
```
需要异常处理的接口上，添加exec_catch_func装饰器即可。
## 返回值信息统一封装
returnInfo.py
每个需要统一返回值的接口上，添加return_info_func装饰器即可。
return_info_func 中封装了异常处理，异常日志记录，操作日志记录等
## 字典统一处理
dictOpr.py
字典统一处理类，支持内存缓存，提供字典查询，清除缓存接口，未来可以支持redis缓存。
## 获取用户信息
operUserInfo.py
提供接口从redis中获取当前用户信息
## 时间转换工具
dateTool.py 时间转换工具
## 系统工具
sysTool.py 操作系统参数的函数封装