from django.utils.encoding import escape_uri_path
from fastapi import Response, File
from py_bootstrap.config import config

from qg_common_sdk.dictOpr import DictOpr
from qg_common_sdk.excelToDeal import ExcelToDeal
from qg_common_sdk.returnInfo import return_info_func
from qg_common_sdk.routers import router

dict_opr = DictOpr(config)


@router.get("/dicts/{dictType}/children")
@return_info_func
def getDictByType(dictType: str, code: str = None, queryAll: bool = False):
    return dict_opr.getDictsByTypeApi(dictType, code, queryAll)


@router.get("/dicts/{dictType}")
@return_info_func
def getDictByCode(dictType: str, code: str, queryAll: bool = False):
    return dict_opr.getDictByCode(dictType, code, queryAll)


@router.get("/dictTypes/{dictType}")
@return_info_func
def getDictWithDictTypeAndCode(dictType: str):
    return dict_opr.dictTypes(dictType)


@router.get("/dictTypes")
@return_info_func
def getDictTypes():
    return dict_opr.getDictsByTypesApi()


@router.get("/exportExcel")
# @return_info_func
def exportExcel():
    ex = ExcelToDeal()
    titleList = ['名称', '性别']
    dataList = [['六', '南'], ['wu', '女'], ['菜', ['a', 'b']]]
    sio = ex.listToExcel(titleList, dataList)
    response = Response(sio.getvalue())
    response.headers['content-type'] = 'application/x-xlsx'
    response.headers['content-disposition'] = "attachment;filename={}".format(
        escape_uri_path('哈哈.xlsx')
    )

    print("===============")
    return response


@router.post("/vvv/importExcel/bb")
# @return_info_func
async def importExcel(file: bytes = File(...)):
    print("===========111==================")

    ex = ExcelToDeal()
    dataList = ex.excelToList(file)
    print(dataList)
    return dataList
