import json

from .catchException import SysCheckException


class UserInfo(dict):
    def __init__(self, dict_info: dict):
        self.serviceId = dict_info['serviceId']
        self.userId = dict_info['userId']
        self.userAccount = dict_info['userAccount']
        self.username = dict_info['username']
        self.realName = dict_info['realName']
        self.roleCode = dict_info['roleCode']
        self.sysId = dict_info['sysId']
        self.lastOs = dict_info['lastOs']
        self.lastIp = dict_info['lastIp']
        self.deptCode = dict_info['deptCode']
        super().__init__(self.__dict__)


def getUserInfo(token: str, redis):
    dict_info = redis.get(token)

    if (dict_info):
        user_dict = json.loads(dict_info)[1]
        userInfo = UserInfo(user_dict)
        return userInfo
    else:
        raise SysCheckException(token, "用户信息过期")
