# -*- coding: utf-8 -*-

import sys
import datetime
import traceback

from sqlalchemy import or_

from atlas.conf.conf_code     import *
from atlas.common.global_db   import *
from atlas.common.global_call import *
from atlas.common.global_tool import *

from atlas.model.model_module import TableAtlasModule
from atlas.model.model_module import TableAtlasModuleCode

# --------------------------------------------------
# constant variables

MODE_SVR_ERROR_UNSHOW = 0
MODE_SVR_ERROR_SHOW   = 1

MODE_CODETYPE = {
    "3000" : u"后端返回格式错误",
    "4000" : u"用户错误",
    "4100" : u"频次超限",
    "4200" : u"签名密钥不存在",
    "4300" : u"签名过期",
    "4400" : u"签名错误",
    "4500" : u"权限不足",
    "5000" : u"后端错误"
}

# --------------------------------------------------
# following are some CGIs

def cgi_createModuleErrorCode(para, res):
    # 1. prepare a logger
    logger = get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    for key in ["loginUin", "ownerUin", "module", "code", "codeType", "codeDesc", "showSvrError", "message"]:
        if key not in para:
            res["returnCode"]    = CONF_CODE["para_miss"][0]
            res["returnMessage"] = "miss parameter(%s)" % (key)
            return

    loginUin = int(para["loginUin"])
    ownerUin = int(para["ownerUin"])
    code     = int(para["code"])
    codeType = int(para["codeType"])
    showSvrError = int(para["showSvrError"])

    module   = deal_post_str(para["module"])
    codeDesc = deal_post_str(para["codeDesc"])
    message  = deal_post_str(para["message"])

    # 3. check validation
    if len(module) == 0:
        fill_error_code(res, "empty_module_enName")
        return

    if str(codeType) not in MODE_CODETYPE:
        fill_error_code(res, "mode_codeType")
        return

    if showSvrError != MODE_SVR_ERROR_SHOW and showSvrError != MODE_SVR_ERROR_UNSHOW:
        fill_error_code(res, "mode_showSvrError")
        return

    # 4. logic work
    session_mark = False
    try:
        session_api  = DB_SESSION_API
        session_mark = True

        if judge_exist_module(session_api, module) is False:
            fill_error_code(res, "invalid_module")

        elif judge_exist_moduleManager(session_api, module, loginUin) is False:
            fill_error_code(res, "module_permission")

        elif judge_exist_moduleCode(session_api, module, code) is True:
            fill_error_code(res, "duplicate_module_code")

        else:
            obj_code = TableAtlasModuleCode(module, code, showSvrError, codeType, codeDesc, message)
            session_api.add(obj_code)
            res["data"]["errorCodeDetail"] = obj_code.to_json()

        session_api.commit()

    except Exception, e:
        if session_mark is True:
            session_api.rollback()

        traceback_str = traceback.format_exc()
        res["returnCode"]    = CONF_CODE["sql_error"][0]
        res["returnMessage"] = traceback_str

        logger.error(traceback_str)

    finally:
        if session_mark is True:
            session_api.close()


def cgi_updateModuleErrorCode(para, res):
    # 1. prepare a logger
    logger = get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    for key in ["loginUin", "ownerUin", "module", "code", "codeType", "codeDesc", "showSvrError", "message"]:
        if key not in para:
            res["returnCode"]    = CONF_CODE["para_miss"][0]
            res["returnMessage"] = "miss parameter(%s)" % (key)
            return

    loginUin = int(para["loginUin"])
    ownerUin = int(para["ownerUin"])
    code     = int(para["code"])
    codeType = int(para["codeType"])
    showSvrError = int(para["showSvrError"])

    module   = deal_post_str(para["module"])
    codeDesc = deal_post_str(para["codeDesc"])
    message  = deal_post_str(para["message"])

    # 3. check validation
    if len(module) == 0:
        fill_error_code(res, "empty_module_enName")
        return

    if str(codeType) not in MODE_CODETYPE:
        fill_error_code(res, "mode_codeType")
        return

    if showSvrError != MODE_SVR_ERROR_SHOW and showSvrError != MODE_SVR_ERROR_UNSHOW:
        fill_error_code(res, "mode_showSvrError")
        return

    # 4. logic work
    session_mark = False
    try:
        session_api  = DB_SESSION_API
        session_mark = True

        if judge_exist_module(session_api, module) is False:
            fill_error_code(res, "invalid_module")

        elif judge_exist_moduleManager(session_api, module, loginUin) is False:
            fill_error_code(res, "module_permission")

        else:
            obj_code = session_api.query(
                TableAtlasModuleCode
            ).filter(
                TableAtlasModuleCode.module == module,
                TableAtlasModuleCode.code   == code
            ).first()

            if obj_code is None:
                fill_error_code(res, "invalid_errorCode")
            else:
                obj_code.codeType = codeType
                obj_code.codeDesc = codeDesc
                obj_code.message  = message
                obj_code.showSvrError = showSvrError

                res["data"]["errorCodeDetail"] = obj_code.to_json()

        session_api.commit()

    except Exception, e:
        if session_mark is True:
            session_api.rollback()

        traceback_str = traceback.format_exc()
        res["returnCode"]    = CONF_CODE["sql_error"][0]
        res["returnMessage"] = traceback_str

        logger.error(traceback_str)

    finally:
        if session_mark is True:
            session_api.close()


def _deleteErrorCode(session_api, loginUin, module, code):
    res = {
        "module"    : module,
        "code"      : code,
        "opCode"    : CONF_CODE["success"][0],
        "opMessage" : CONF_CODE["success"][1]
    }

    if len(module) == 0:
        res["opCode"]    = CONF_CODE["empty_module_enName"][0]
        res["opMessage"] = CONF_CODE["empty_module_enName"][1]
        return res

    if judge_exist_module(session_api, module) is False:
        res["opCode"]    = CONF_CODE["invalid_module"][0]
        res["opMessage"] = CONF_CODE["invalid_module"][1]
        return res

    if judge_exist_moduleManager(session_api, module, loginUin) is False:
        res["opCode"]    = CONF_CODE["module_permission"][0]
        res["opMessage"] = CONF_CODE["module_permission"][1]
        return res

    obj_code = session_api.query(
        TableAtlasModuleCode
    ).filter(
        TableAtlasModuleCode.module == module,
        TableAtlasModuleCode.code   == code
    ).first()

    if obj_code is None:
        res["opCode"]    = CONF_CODE["invalid_errorCode"][0]
        res["opMessage"] = CONF_CODE["invalid_errorCode"][1]
    else:
        session_api.delete(obj_code)

    return res


def cgi_deleteModuleErrorCode(para, res):
    # 1. prepare a logger
    logger = get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    for key in ["loginUin", "ownerUin", "errorCodeList"]:
        if key not in para:
            res["returnCode"]    = CONF_CODE["para_miss"][0]
            res["returnMessage"] = "miss parameter(%s)" % (key)
            return

    loginUin  = int(para["loginUin"])
    ownerUin  = int(para["ownerUin"])
    errorCodeList = para.get("errorCodeList", [])

    if not isinstance(errorCodeList, list):
        errorCodeList = [errorCodeList]

    n = len(errorCodeList)
    i = 0
    while i < n:
        errorCodeList[i]["module"] = deal_post_str(errorCodeList[i]["module"])
        errorCodeList[i]["code"]   = int(errorCodeList[i]["code"])
        i += 1

    # 3. logic work
    session_mark = False
    try:
        session_api  = DB_SESSION_API
        session_mark = True

        res["data"]["batchRes"] = []

        for item in errorCodeList:
            res["data"]["batchRes"].append(_deleteErrorCode(
                session_api, loginUin, item["module"], item["code"]
            ))

        session_api.commit()

    except Exception, e:
        if session_mark is True:
            session_api.rollback()

        traceback_str = traceback.format_exc()
        res["returnCode"]    = CONF_CODE["sql_error"][0]
        res["returnMessage"] = traceback_str

        logger.error(traceback_str)

    finally:
        if session_mark is True:
            session_api.close()


def cgi_getModuleErrorCodeList(para, res):
    # 1. prepare a logger
    logger = get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    for key in ["loginUin", "ownerUin", "module"]:
        if key not in para:
            res["returnCode"]    = CONF_CODE["para_miss"][0]
            res["returnMessage"] = "miss parameter(%s)" % (key)
            return

    loginUin = int(para["loginUin"])
    ownerUin = int(para["ownerUin"])
    module   = deal_post_str(para["module"])

    # 3. check validation
    if len(module) == 0:
        fill_error_code(res, "empty_module_enName")
        return

    if "showSvrError" in para:
        showSvrError = int(para["showSvrError"])
        if showSvrError != MODE_SVR_ERROR_SHOW and showSvrError != MODE_SVR_ERROR_UNSHOW:
            fill_error_code(res, "mode_showSvrError")
            return

    # 4. logic work
    session_mark = False
    try:
        session_api  = DB_SESSION_API
        session_mark = True

        if judge_exist_module(session_api, module) is False:
            fill_error_code(res, "invalid_module")

        elif judge_exist_moduleManager(session_api, module, loginUin) is False:
            fill_error_code(res, "module_permission")

        else:
            # init a sql
            sql = session_api.query(TableAtlasModuleCode).filter(TableAtlasModuleCode.module == module)

            # add conditions
            if "code" in para:
                sql = sql.filter(TableAtlasModuleCode.code == int(para["code"]))

            if "codeType" in para:
                sql = sql.filter(TableAtlasModuleCode.codeType == int(para["codeType"]))

            if "showSvrError" in para:
                sql = sql.filter(TableAtlasModuleCode.showSvrError == int(para["showSvrError"]))

            if "keyword" in para:
                keyword = deal_post_str(para["keyword"])
                if len(keyword) != 0:
                    sql = sql.filter(or_(
                        TableAtlasModuleCode.codeDesc.like("%" + keyword + "%"),
                        TableAtlasModuleCode.message.like( "%" + keyword + "%")
                    ))

            # get total count
            res["data"]["totalNum"] = sql.count()
            res["data"]["errorCodeList"] = []

            # page query
            if  "pageId"   in para and int(para["pageId"])   > 0 and \
                "pageSize" in para and int(para["pageSize"]) > 0:
                pageId   = int(para["pageId"])
                pageSize = int(para["pageSize"])
                sql = sql.limit(pageSize).offset((pageId - 1) * pageSize)

            obj_code_list = sql.all()

            for obj_code in obj_code_list:
                res["data"]["errorCodeList"].append(obj_code.to_json())

        session_api.commit()

    except Exception, e:
        if session_mark is True:
            session_api.rollback()

        traceback_str = traceback.format_exc()
        res["returnCode"]    = CONF_CODE["sql_error"][0]
        res["returnMessage"] = traceback_str

        logger.error(traceback_str)

    finally:
        if session_mark is True:
            session_api.close()
