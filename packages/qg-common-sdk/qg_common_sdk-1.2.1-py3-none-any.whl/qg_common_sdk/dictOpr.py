from .Mongodb import MongoDB


class DictOpr(object):

    def __init__(self, config, redis=None):
        self.redis = redis
        mongoDB = MongoDB(config.get('spring').get('data').get('mongodb'))
        self.dict_info = mongoDB.mongodb.dict_common

    def getChildren(self, dict_items, dictType):
        dict_list = []
        levelCodeLen = self.get_root_level_code_len(dictType)
        for item in dict_items:
            dict_child = {}
            dict_child['label'] = item.get('value')
            dict_child['description'] = item.get('desc')
            dict_child['value'] = item.get('code')
            dict_child['isLeaf'] = True
            dict_child['levelCodeLen'] = levelCodeLen
            if (item.get('items') != None):
                children_dict = self.getChildren(item.get('items'), dictType)
                if children_dict:
                    dict_child['children'] = children_dict
                    dict_child['isLeaf'] = False
            dict_list.append(dict_child)
        return dict_list

    # 查询所有字典接口
    # @lru_cache(maxsize=1)
    def getAllDicts(self, serv_name):
        dicts = self.dict_info.find_one({"dictType": serv_name, "enabled": True})
        type_list = dicts['items']
        dict_type_list = []
        dict_list = []
        if (type_list):
            for dict_type in type_list:
                dict_type_list.append(dict_type['code'])
        if (dict_type_list):
            result = self.dict_info.find({"dictType": {'$in': dict_type_list}})
            if (result):
                for dict_info in result:
                    dict_list.append(dict_info)
        return dict_list

    # 根据类型查询字典接口
    # @lru_cache()
    def getDictsByType(self, dict_type):
        result = self.dict_info.find({"dictType": dict_type, "enabled": True})
        dict_list = []
        if (result):
            for dict_info in result:
                dict_list.append(dict_info)
        return dict_list

    # 获取字典描述信息
    def getDictInfoByDictType(self, dict_type):
        result = self.dict_info.find({"dictType": 'dicType', "code": dict_type, "enabled": True})
        dict_list = []
        if (result):
            for dict_info in result:
                dict_list.append(dict_info)
        if len(dict_list) >= 1:
            return dict_list[0]
        else:
            return None

    def get_root_level_code_len(self, dictType):
        root_dict = self.getDictInfoByDictType(dictType)
        if root_dict is not None:
            if 'levelCodeLen' in root_dict:
                return root_dict['levelCodeLen']
        return None

    def getDictsByTypes(self):
        result = self.dict_info.find({"enabled": True, "dictType": 'dicType'})
        dict_list = []
        if (result):
            for dict_info in result:
                dict_list.append(dict_info)
        return dict_list

    def clearAllDicts(self):
        self.getAllDicts.cache_clear()
        self.getDictsByType.cache_clear()

    def getDictsByTypeApi(self, dictType, code, queryAll):
        dicts = self.getDictsByType(dictType)
        dictR = []
        levelCodeLen = self.get_root_level_code_len(dictType)
        if code:
            if levelCodeLen is None or levelCodeLen == '':
                levelCodeLen = str(len(code))
            target = self.get_target(dicts, self.get_codes_array(code, levelCodeLen))
            if target:
                children_dict = self.getChildren(target.get('items'), dictType)
                if queryAll:
                    dictR.append({"label": target.get('value'), "value": target.get('code'),
                                  "description": target.get('desc'), "isLeaf": len(children_dict) == 0,
                                  "levelCodeLen": levelCodeLen,
                                  "children": children_dict})
                else:
                    dictR.append({"label": target.get('value'), "value": target.get('code'),
                                  "description": target.get('desc'), "isLeaf": len(children_dict) == 0,
                                  "levelCodeLen": levelCodeLen})
                return dictR
        else:
            for dict_info in dicts:
                children_dict = self.getChildren(dict_info.get('items'), dictType)
                if queryAll:
                    dictR.append({"label": dict_info.get('value'), "value": dict_info.get('code'),
                                  "description": dict_info.get('desc'), "isLeaf": len(children_dict) == 0,
                                  "levelCodeLen": levelCodeLen,
                                  "children": children_dict})
                else:
                    dictR.append({"label": dict_info.get('value'), "value": dict_info.get('code'),
                                  "description": dict_info.get('desc'), "isLeaf": len(children_dict) == 0,
                                  "levelCodeLen": levelCodeLen})
            return dictR

        return []

    def getDictsByTypesApi(self):
        dicts = self.getDictsByTypes()
        dictR = []
        for dict_info in dicts:
            dictR.append({"label": dict_info.get('value'), "value": dict_info.get('code'),
                          "dictType": dict_info.get('dictType')})
        return dictR

    def dictTypes(self, dictType):
        dicts = self.getDictsByType(dictType)
        dictR = []
        levelCodeLen = self.get_root_level_code_len(dictType)
        for dict_info in dicts:
            dictR.append(
                {"label": dict_info.get('value'), "value": dict_info.get('code'), "levelCodeLen": levelCodeLen})
        return dictR

    def getDictByCode(self, dictType, code, queryAll):
        dicts = self.getDictsByType(dictType)
        levelCodeLen = self.get_root_level_code_len(dictType)
        if levelCodeLen is None or levelCodeLen == '':
            levelCodeLen = str(len(code))

        target = self.get_target(dicts, self.get_codes_array(code, levelCodeLen))
        if target:
            if queryAll:
                return {"label": target.get('value'), "value": target.get('code'),
                        "description": target.get('desc'), "isLeaf": len(target.get("items")) == 0,
                        "levelCodeLen": levelCodeLen,
                        "children": target.get("items")}
            else:
                return {"label": target.get('value'), "value": target.get('code'),
                        "description": target.get('desc'), "isLeaf": len(target.get("items")) == 0,
                        "levelCodeLen": levelCodeLen}
        return {}

    def get_codes_array(self, code_str, level_code_len):
        codes = []
        if level_code_len is not None and '' != level_code_len:
            levels = level_code_len.split('-')
            for level_index in levels:
                if code_str is not None and code_str != '':
                    codes.append(code_str[0:int(level_index)])
                    code_str = code_str[int(level_index):]
                else:
                    return codes
        return codes

    def get_target(self, dicts, codes):
        for index in range(len(codes)):
            for dict_info in dicts:
                if dict_info.get('code') == codes[index]:
                    if index != len(codes) - 1:
                        new_codes = codes[index + 1:len(codes)]
                        new_dicts = dict_info["items"]
                        if new_codes is not None and len(new_codes) != 0:
                            if new_dicts is not None and len(new_dicts) != 0:
                                return self.get_target(new_dicts, new_codes)
                    else:
                        return dict_info

        return {}
