# -*- coding: utf-8 -*-

MODE_URL_SINGLE = 1
MODE_URL_MULTI  = 2

def svrRequestUrl(reqData, urlType, urlAddress):
    """ 后端业务地址 """
    paramDict = reqData["params"]
    svrUrl = None

    if urlType == MODE_URL_SINGLE:
        svrUrl = urlAddress
    else:
        exec urlAddress

    return svrUrl


def svrRequestData(reqData, funcReq):
    """ 后端业务入参转换 """
    paramDict = reqData["params"]

    if funcReq:
        exec funcReq

    return paramDict


def svrRespondData(rspData, funcRsp):
    """ 后端业务返回转换 """
    if funcRsp:
        exec funcRsp

    return rspData


def svrErrorCode(rspData, codeDetail):
    """ 错误码转换 """
    if rspData["code"] and rspData["code"] == codeDetail["code"]:
        rspData["code"]     = codeDetail["codeType"]
        rspData["codeDesc"] = codeDetail["codeDesc"]

        if codeDetail["showSvrError"]:
            rspData["message"] = "(%d)(%s)(%s)" % (codeDetail["code"], codeDetail["message"], rspData["message"])
        else:
            rspData["message"] = "(%d)(%s)" % (codeDetail["code"], codeDetail["message"])

    return rspData
