
import json
class EnumDatabase():
    MYSQL  = 'mysql'
    MONGO     = 'mongodb'
    ORACLE11g   = 'oracle'

class DataBaseConnectConfig(dict):
    def __init__(self,info:dict):
        self.connPref = info['connPref']
        self.ip = info['ip']
        self.port = info['port']
        self.dbType = info['dbType']
        self.dbName = info['dbName']
        self.userName = info['userName']
        self.password = info['password']
        self.driver = info['driver']
        self.sid = info['sid']
        self.jdbcUrlModel = info['jdbcUrlModel']
        self.devLanguage = info['devLanguage']
        super().__init__(self.__dict__)

def getDataBaseConnectUrl(info:DataBaseConnectConfig):
    jdbcUrl = ""
    if info.dbType == EnumDatabase.MYSQL:
        jdbcUrl = getDefaultMysqlConnect(info)
    elif info.dbType == EnumDatabase.MONGO:
        jdbcUrl = getDefaultMongoConnect(info)
    elif info.dbType == EnumDatabase.ORACLE11g:
        jdbcUrl = getDefaultOracleConnect(info)
    if info.jdbcUrlModel:
        jdbcUrl = getModelConnect(info)
    return jdbcUrl

def getModelConnect(info:DataBaseConnectConfig):
    uri = info.jdbcUrlModel
    uri = uri.replace("#userName", info.userName)
    uri = uri.replace("#passowrd", info.passowrd)
    uri = uri.replace("#ip", info.ip)
    uri = uri.replace("#port", info.port)
    uri = uri.replace("#dbName", info.dbName)
    uri = uri.replace("#driver", info.driver)
    uri = uri.replace("#sid", info.sid)

def getDefaultMysqlConnect(info:DataBaseConnectConfig):
    uri = 'mysql+pymysql://'+info.userName+':'+info.password+'@'+info.ip+':'+info.port+'/'+info.dbName+'?charset=utf8'
    return uri

def getDefaultMongoConnect(info:DataBaseConnectConfig):
    uri = 'mongodb://'+info.ip+':'+info.port
    return uri

def getDefaultOracleConnect(info:DataBaseConnectConfig):
    uri = info.userName+'/'+info.password+'@'+info.ip+':'+info.port+'/'+info.port
    return uri
