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
from atlas.model.model_module import TableAtlasModuleManager

# --------------------------------------------------
# constant variables

MODE_MODULE_MANAGER_ADD = 1
MODE_MODULE_MANAGER_DEL = 2

# --------------------------------------------------
# following are some CGIs

def cgi_getModuleManagers(para, res):
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

    # 3. logic work
    session_mark = False
    try:
        session_api  = DB_SESSION_API
        session_mark = True

        # get managers' userUin
        obj_managers = session_api.query(TableAtlasModuleManager).filter(TableAtlasModuleManager.module == module).all()

        userUinList = []
        for item in obj_managers:
            userUinList.append(item.userUin)

        # get managers' ownerUin, userName, userRemark
        callRsp = call_service_getUserDetail(userUinList, logger)

        # fill response
        res["data"]["userList"] = []

        for user_uin in userUinList:
            user_json = { "userUin" : user_uin }

            if "data" in callRsp and str(user_uin) in callRsp["data"]:
                user_json["ownerUin"]   = callRsp["data"][str(user_uin)]["ownerUin"]
                user_json["userName"]   = callRsp["data"][str(user_uin)]["userName"]
                user_json["userRemark"] = callRsp["data"][str(user_uin)]["userRemark"]

            res["data"]["userList"].append(user_json)

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


def _module_manager_add(session_api, module, userUin):
    res = {
        "module"    : module,
        "userUin"   : userUin,
        "opCode"    : CONF_CODE["success"][0],
        "opMessage" : CONF_CODE["success"][1]
    }

    if judge_exist_moduleManager(session_api, module, userUin) is True:
        res["opCode"]    = CONF_CODE["duplicate_module_manager"][0]
        res["opMessage"] = CONF_CODE["duplicate_module_manager"][1]
    else:
        session_api.add(TableAtlasModuleManager(module, userUin))

    return res


def _module_manager_del(session_api, module, userUin):
    res = {
        "module"    : module,
        "userUin"   : userUin,
        "opCode"    : CONF_CODE["success"][0],
        "opMessage" : CONF_CODE["success"][1]
    }

    obj_manager = session_api.query(
        TableAtlasModuleManager
    ).filter(
        TableAtlasModuleManager.module  == module,
        TableAtlasModuleManager.userUin == userUin
    ).first()

    if obj_manager is None:
        res["opCode"]    = CONF_CODE["invalid_module_manager"][0]
        res["opMessage"] = CONF_CODE["invalid_module_manager"][1]
    else:
        session_api.delete(obj_manager)

    return res


def cgi_updateModuleManagers(para, res):
    # 1. prepare a logger
    logger = get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    for key in ["loginUin", "ownerUin", "module", "opMode", "managers"]:
        if key not in para:
            res["returnCode"]    = CONF_CODE["para_miss"][0]
            res["returnMessage"] = "miss parameter(%s)" % (key)
            return

    loginUin = int(para["loginUin"])
    ownerUin = int(para["ownerUin"])
    opMode   = int(para["opMode"])
    module   = deal_post_str(para["module"])

    managers = para.get("managers", [])
    if not isinstance(managers, list):
        managers = [managers]

    n = len(managers)
    i = 0
    while i < n:
        managers[i] = int(managers[i])
        i += 1

    if opMode != MODE_MODULE_MANAGER_ADD and opMode != MODE_MODULE_MANAGER_DEL:
        fill_error_code(res, "mode_manager")
        return

    if len(managers) == 0:
        fill_error_code(res, "empty_module_managers")
        return

    # 3. logic work
    session_mark = False
    try:
        session_api  = DB_SESSION_API
        session_mark = True

        if judge_exist_module(session_api, module) is False:
            fill_error_code(res, "invalid_module")
        elif judge_exist_moduleManager(session_api, module, loginUin) is False:
            fill_error_code(res, "module_permission")
        else:
            # query all the managers which want to be added or removed
            callRsp = call_service_getUserDetail(managers, logger)

            # deal with each manager which want to be added or removed
            res["data"]["batchRes"] = []

            for manager_uin in managers:
                if "data" not in callRsp or str(manager_uin) not in callRsp["data"]:
                    tmpRes = {
                        "module"    : module,
                        "userUin"   : manager_uin,
                        "opCode"    : CONF_CODE["invalid_user_uin"][0],
                        "opMessage" : CONF_CODE["invalid_user_uin"][1]
                    }
                elif opMode == MODE_MODULE_MANAGER_ADD:
                    tmpRes = _module_manager_add(session_api, module, manager_uin)
                else:
                    tmpRes = _module_manager_del(session_api, module, manager_uin)

                res["data"]["batchRes"].append(tmpRes)

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
