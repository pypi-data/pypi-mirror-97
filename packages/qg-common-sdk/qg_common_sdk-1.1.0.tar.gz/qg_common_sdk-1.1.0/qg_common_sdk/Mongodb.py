import pymongo
from pymongo import MongoClient



class PageResult(object):
    def __init__(self,list,pageSize,totalItem,cpage):
        self.list = list
        self.pageSize = pageSize
        self.totalitem = totalItem
        self.cpage = cpage


class MongoDB(object):
    def __init__(self,config):
        uri = '{driver}://{ip}:{port}'.format(
            driver=config['driver']
        ,ip=config['ip']
        ,port=config['port'])
        client = MongoClient(uri)
        db = client[config.get('database')]
        db.authenticate(config.get('username'),str(config.get('password')))
        self.mongodb = db

    def getMongoDb(self):
        return self.mongodb

    def getPageResult(self,db_name,query_map,page,page_len,sort):
        skip = page_len * (page - 1)
        if (sort):
            if (sort[0].get("columnOrder")=='asc'):
                sort = [(sort[0].get("columnProp"),pymongo.ASCENDING)]
            else:
                sort = [(sort[0].get("columnProp"),pymongo.DESCENDING)]
            infos = db_name.find(query_map).limit(page_len).skip(skip).sort(sort)
        else:
            infos = db_name.find(query_map).limit(page_len).skip(skip)
        info_list = []
        for info in infos:
            info['key'] = info['_id']
            info_list.append(info)
        return PageResult(info_list,page_len,infos.count(),page)

    def getNewId(self,modelName):
       key_info = self.mongodb.model_key.find_one({"modelName":modelName})
       if (key_info):
            model_num = key_info['model_num']
            return model_num