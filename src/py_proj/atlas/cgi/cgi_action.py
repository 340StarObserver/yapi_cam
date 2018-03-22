# -*- coding: utf-8 -*-

import sys
import time
import datetime
import traceback

from sqlalchemy import or_
from sqlalchemy import and_

from atlas.conf.conf_code     import *
from atlas.common.global_db   import *
from atlas.common.global_call import *
from atlas.common.global_tool import *

from atlas.model.model_module import TableAtlasModule
from atlas.model.model_module import TableAtlasModuleUrl
from atlas.model.model_action import TableAtlasAction
from atlas.model.model_action import TableAtlasActionRate

# --------------------------------------------------
# constant variables

MODE_ACTION_AUTH_CLOSE = 0
MODE_ACTION_AUTH_OPEN  = 1

MODE_ACTION_RATE_CLOSE = 0
MODE_ACTION_RATE_OPEN  = 1

DEFAULT_ACTION_RATE    = 100

# --------------------------------------------------
# following are some CGIs

def cgi_createAction(para, res):
    # 1. prepare a logger
    logger = get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    for key in ["loginUin", "ownerUin", "module", "action", "actionName", "urlName", "isAuth", "isRate"]:
        if key not in para:
            res["returnCode"]    = CONF_CODE["para_miss"][0]
            res["returnMessage"] = "miss parameter(%s)" % (key)
            return

    loginUin = int(para["loginUin"])
    ownerUin = int(para["ownerUin"])
    isAuth   = int(para["isAuth"])
    isRate   = int(para["isRate"])
    minRate  = abs(int(para.get("minRate", DEFAULT_ACTION_RATE)))

    module     = deal_post_str(para["module"])
    action     = deal_post_str(para["action"])
    actionName = deal_post_str(para["actionName"])
    urlName    = deal_post_str(para["urlName"])

    funcReq       = para.get("funcReq", None)
    funcRsp       = para.get("funcRsp", None)
    funcResource  = para.get("funcResource" , None)
    funcCondition = para.get("funcCondition", None)

    # 3. check validation
    if len(module) == 0:
        fill_error_code(res, "empty_module_enName")
        return

    if len(action) == 0:
        fill_error_code(res, "empty_module_action")
        return

    if len(actionName) == 0:
        fill_error_code(res, "empty_module_actionName")
        return

    if len(urlName) == 0:
        fill_error_code(res, "empty_module_urlName")
        return

    if isAuth != MODE_ACTION_AUTH_CLOSE and isAuth != MODE_ACTION_AUTH_OPEN:
        fill_error_code(res, "mode_isAuth")
        return

    if isRate != MODE_ACTION_RATE_CLOSE and isRate != MODE_ACTION_RATE_OPEN:
        fill_error_code(res, "mode_isRate")
        return

    # 4. logic work
    session_mark = False
    try:
        session_api  = DB_SESSION_API
        session_log  = DB_SESSION_LOG
        session_mark = True

        if judge_exist_module(session_api, module) is False:
            fill_error_code(res, "invalid_module")

        elif judge_exist_moduleManager(session_api, module, loginUin) is False:
            fill_error_code(res, "module_permission")

        elif judge_exist_moduleUrl(session_api, module, urlName) is False:
            fill_error_code(res, "invalid_urlName")

        elif judge_exist_action(session_api, module, action) is True:
            fill_error_code(res, "duplicate_module_action")

        else:
            # s1. prepare current time
            time_obj = datetime.datetime.now()
            time_int = int(time.time())

            # s2. add Action
            obj_action = TableAtlasAction(module, action, actionName, time_obj, time_obj, urlName, isAuth, funcReq, funcRsp, funcResource, funcCondition)
            session_api.add(obj_action)

            # s3. add/update ActionRate
            obj_rate = session_log.query(
                TableAtlasActionRate
            ).filter(
                TableAtlasActionRate.module == module,
                TableAtlasActionRate.action == action
            ).first()

            if obj_rate is None:
                obj_rate = TableAtlasActionRate(module, action, isRate, minRate, time_int, time_int)
                session_log.add(obj_rate)
            else:
                obj_rate.isRate  = isRate
                obj_rate.minRate = minRate

            # s4. action detail
            res["data"]["actionDetail"] = obj_action.to_json()
            res["data"]["actionDetail"]["isRate"]  = isRate
            res["data"]["actionDetail"]["minRate"] = minRate

        session_api.commit()
        session_log.commit()

    except Exception, e:
        if session_mark is True:
            session_api.rollback()
            session_log.rollback()

        traceback_str = traceback.format_exc()
        res["returnCode"]    = CONF_CODE["sql_error"][0]
        res["returnMessage"] = traceback_str

        logger.error(traceback_str)

    finally:
        if session_mark is True:
            session_api.close()
            session_log.close()


def cgi_updateAction(para, res):
    # 1. prepare a logger
    logger = get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    for key in ["loginUin", "ownerUin", "module", "action", "actionName", "urlName", "isAuth", "isRate"]:
        if key not in para:
            res["returnCode"]    = CONF_CODE["para_miss"][0]
            res["returnMessage"] = "miss parameter(%s)" % (key)
            return

    loginUin = int(para["loginUin"])
    ownerUin = int(para["ownerUin"])
    isAuth   = int(para["isAuth"])
    isRate   = int(para["isRate"])
    minRate  = abs(int(para.get("minRate", DEFAULT_ACTION_RATE)))

    module     = deal_post_str(para["module"])
    action     = deal_post_str(para["action"])
    actionName = deal_post_str(para["actionName"])
    urlName    = deal_post_str(para["urlName"])

    funcReq       = para.get("funcReq", None)
    funcRsp       = para.get("funcRsp", None)
    funcResource  = para.get("funcResource" , None)
    funcCondition = para.get("funcCondition", None)

    # 3. check validation
    if len(module) == 0:
        fill_error_code(res, "empty_module_enName")
        return

    if len(action) == 0:
        fill_error_code(res, "empty_module_action")
        return

    if len(actionName) == 0:
        fill_error_code(res, "empty_module_actionName")
        return

    if len(urlName) == 0:
        fill_error_code(res, "empty_module_urlName")
        return

    if isAuth != MODE_ACTION_AUTH_CLOSE and isAuth != MODE_ACTION_AUTH_OPEN:
        fill_error_code(res, "mode_isAuth")
        return

    if isRate != MODE_ACTION_RATE_CLOSE and isRate != MODE_ACTION_RATE_OPEN:
        fill_error_code(res, "mode_isRate")
        return

    # 4. logic work
    session_mark = False
    try:
        session_api  = DB_SESSION_API
        session_log  = DB_SESSION_LOG
        session_mark = True

        if judge_exist_module(session_api, module) is False:
            fill_error_code(res, "invalid_module")

        elif judge_exist_moduleManager(session_api, module, loginUin) is False:
            fill_error_code(res, "module_permission")

        elif judge_exist_moduleUrl(session_api, module, urlName) is False:
            fill_error_code(res, "invalid_urlName")

        else:
            obj_action = session_api.query(
                TableAtlasAction
            ).filter(
                TableAtlasAction.module == module,
                TableAtlasAction.action == action
            ).first()

            if obj_action is None:
                fill_error_code(res, "invalid_action")
            else:
                # s1. prepare current time
                time_obj = datetime.datetime.now()
                time_int = int(time.time())

                # s2. update Action
                obj_action.actionName = actionName
                obj_action.modTime    = time_obj
                obj_action.urlName    = urlName
                obj_action.isAuth     = isAuth
                obj_action.funcReq    = funcReq
                obj_action.funcRsp    = funcRsp
                obj_action.funcResource  = funcResource
                obj_action.funcCondition = funcCondition

                # s3. add/update ActionRate
                obj_rate = session_log.query(
                    TableAtlasActionRate
                ).filter(
                    TableAtlasActionRate.module == module,
                    TableAtlasActionRate.action == action
                ).first()

                if obj_rate is None:
                    obj_rate = TableAtlasActionRate(module, action, isRate, minRate, time_int, time_int)
                    session_log.add(obj_rate)
                else:
                    obj_rate.isRate  = isRate
                    obj_rate.minRate = minRate

                # s4. action detail
                res["data"]["actionDetail"] = obj_action.to_json()
                res["data"]["actionDetail"]["isRate"]  = isRate
                res["data"]["actionDetail"]["minRate"] = minRate

        session_api.commit()
        session_log.commit()

    except Exception, e:
        if session_mark is True:
            session_api.rollback()
            session_log.rollback()

        traceback_str = traceback.format_exc()
        res["returnCode"]    = CONF_CODE["sql_error"][0]
        res["returnMessage"] = traceback_str

        logger.error(traceback_str)

    finally:
        if session_mark is True:
            session_api.close()
            session_log.close()


def cgi_getActionList(para, res):
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
            sql = session_api.query(
                TableAtlasAction
            ).filter(
                TableAtlasAction.module == module
            )

            # add condtion : action
            if "action" in para:
                action = deal_post_str(para["action"])
                if len(action) != 0:
                    sql = sql.filter(TableAtlasAction.action.like("%" + action + "%"))

            if "actionName" in para:
                actionName = deal_post_str(para["actionName"])
                if len(actionName) != 0:
                    sql = sql.filter(TableAtlasAction.actionName.like("%" + actionName + "%"))

            if "urlName" in para:
                urlName = deal_post_str(para["urlName"])
                if len(urlName) != 0:
                    sql = sql.filter(TableAtlasAction.urlName.like("%" + urlName + "%"))

            if "modTimeRange" in para:
                modTimeRange = deal_post_str(para["modTimeRange"])
                if len(modTimeRange) != 0:
                    modTimeRange = modTimeRange.split(":")
                    time_func = datetime.datetime.strptime
                    time_beg  = time_func("%s 00:00:00" % (modTimeRange[0]), "%Y-%m-%d %H:%M:%S")
                    time_end  = time_func("%s 23:59:59" % (modTimeRange[1]), "%Y-%m-%d %H:%M:%S")
                    sql = sql.filter(
                        TableAtlasAction.modTime >= time_beg,
                        TableAtlasAction.modTime <= time_end
                    )

            # get total count
            res["data"]["totalNum"] = sql.count()
            res["data"]["actionList"] = []

            # page query
            if  "pageId"   in para and int(para["pageId"])   > 0 and \
                "pageSize" in para and int(para["pageSize"]) > 0:
                pageId   = int(para["pageId"])
                pageSize = int(para["pageSize"])
                sql = sql.limit(pageSize).offset((pageId - 1) * pageSize)

            action_list = sql.all()

            kSet = ["module", "action", "actionName", "urlName", "addTime", "modTime"]

            for obj_action in action_list:
                json_action = obj_action.to_json()
                json_action = { k : v for k, v in json_action.items() if k in kSet }
                res["data"]["actionList"].append(json_action)

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


def cgi_getActionDetail(para, res):
    # 1. prepare a logger
    logger = get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    for key in ["loginUin", "ownerUin", "module", "action"]:
        if key not in para:
            res["returnCode"]    = CONF_CODE["para_miss"][0]
            res["returnMessage"] = "miss parameter(%s)" % (key)
            return

    loginUin = int(para["loginUin"])
    ownerUin = int(para["ownerUin"])
    module   = deal_post_str(para["module"])
    action   = deal_post_str(para["action"])

    # 3. check validation
    if len(module) == 0:
        fill_error_code(res, "empty_module_enName")
        return

    if len(action) == 0:
        fill_error_code(res, "empty_module_action")
        return

    # 4. logic work
    session_mark = False
    try:
        session_api  = DB_SESSION_API
        session_log  = DB_SESSION_LOG
        session_mark = True

        if judge_exist_module(session_api, module) is False:
            fill_error_code(res, "invalid_module")

        elif judge_exist_moduleManager(session_api, module, loginUin) is False:
            fill_error_code(res, "module_permission")

        else:
            obj_data = session_api.query(
                TableAtlasAction,
                TableAtlasModuleUrl
            ).join(
                TableAtlasModuleUrl,
                and_(
                    TableAtlasAction.module  == TableAtlasModuleUrl.module,
                    TableAtlasAction.urlName == TableAtlasModuleUrl.urlName
                )
            ).filter(
                TableAtlasAction.module == module,
                TableAtlasAction.action == action
            ).first()

            if obj_data is None:
                fill_error_code(res, "invalid_action")
            else:
                res["data"]["actionDetail"] = obj_data[0].to_json()

                json_url = obj_data[1].to_json()
                res["data"]["actionDetail"]["urlType"]    = json_url["urlType"]
                res["data"]["actionDetail"]["urlAddress"] = json_url["urlAddress"]

                obj_rate = session_log.query(
                    TableAtlasActionRate
                ).filter(
                    TableAtlasActionRate.module == module,
                    TableAtlasActionRate.action == action
                ).first()

                if obj_rate is not None:
                    res["data"]["actionDetail"]["isRate"]  = obj_rate.isRate
                    res["data"]["actionDetail"]["minRate"] = obj_rate.minRate
                else:
                    res["data"]["actionDetail"]["isRate"]  = MODE_ACTION_RATE_CLOSE
                    res["data"]["actionDetail"]["minRate"] = DEFAULT_ACTION_RATE

        session_api.commit()
        session_log.commit()

    except Exception, e:
        if session_mark is True:
            session_api.rollback()
            session_log.rollback()

        traceback_str = traceback.format_exc()
        res["returnCode"]    = CONF_CODE["sql_error"][0]
        res["returnMessage"] = traceback_str

        logger.error(traceback_str)

    finally:
        if session_mark is True:
            session_api.close()
            session_log.close()


def cgi_getServiceApiList(para, res):
    # 1. prepare a logger
    logger = get_logger(sys._getframe().f_code.co_name)

    # 2. logic work
    session_mark = False
    try:
        session_api  = DB_SESSION_API
        session_mark = True

        # query modules
        obj_module_list = session_api.query(
            TableAtlasModule.module,
            TableAtlasModule.zhName
        ).all()

        # query actions
        obj_action_list = session_api.query(
            TableAtlasAction.module,
            TableAtlasAction.action,
            TableAtlasAction.actionName
        ).all()

        # data format
        tmp_action_list = {}
        for item in obj_action_list:
            if item[0] not in tmp_action_list:
                tmp_action_list[item[0]] = []
            tmp_action_list[item[0]].append({
                "actionEnName" : item[1],
                "actionZhName" : item[2]
            })

        res["data"]["apiList"] = []
        for item in obj_module_list:
            res["data"]["apiList"].append({
                "moduleEnName" : item[0],
                "moduleZhName" : item[1],
                "actionList"   : tmp_action_list.get(item[0], [])
            })

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
