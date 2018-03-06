# -*- coding: utf-8 -*-

import sys
import datetime
import traceback

from sqlalchemy import or_

from atlas.conf   import conf_code
from atlas.common import global_db
from atlas.common import global_tool
from atlas.common import global_call

from atlas.model.model_module import TableAtlasModule
from atlas.model.model_module import TableAtlasModuleManager


# --------------------------------------------------
# following are some CGIs

def cgi_createModule(para, res):
    # 1. prepare a logger
    logger = global_tool.get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    for key in ["loginUin", "ownerUin", "module", "zhName", "managers"]:
        if key not in para:
            res["returnCode"]    = conf_code.CONF_CODE["para_miss"][0]
            res["returnMessage"] = "miss parameter(%s)" % (key)
            return

    loginUin = int(para["loginUin"])
    ownerUin = int(para["ownerUin"])
    module   = global_tool.deal_post_str(para["module"])
    zhName   = global_tool.deal_post_str(para["zhName"])

    managers = para["managers"]
    if not isinstance(managers, list):
        managers = [managers]

    if len(module) == 0:
        global_tool.fill_error_code(res, "empty_module_enName")
        return

    if len(zhName) == 0:
        global_tool.fill_error_code(res, "empty_module_zhName")
        return

    if len(managers) == 0:
        global_tool.fill_error_code(res, "empty_module_managers")
        return

    # 3. logic work
    session_mark = False
    try:
        session_api  = global_db.DB_SESSION_API
        session_mark = True

        check_moduleEnName = global_tool.judge_exist_module(session_api, module)
        check_moduleZhName = session_api.query(TableAtlasModule).filter(TableAtlasModule.zhName == zhName).first()

        user_list = list(managers)
        user_list.append(ownerUin)
        check_userUinList  = global_call.call_service_getUserDetail(user_list, logger)

        if check_moduleEnName is True:
            global_tool.fill_error_code(res, "duplicate_module_enName")
        elif check_moduleZhName is not None:
            global_tool.fill_error_code(res, "duplicate_module_zhName")
        elif "data" not in check_userUinList or str(ownerUin) not in check_userUinList["data"]:
            global_tool.fill_error_code(res, "invalid_owner_uin")
        elif len(user_list) != len(check_userUinList["data"]):
            global_tool.fill_error_code(res, "invalid_user_uin")
        else:
            # add module
            time_now   = datetime.datetime.now()
            obj_module = TableAtlasModule(module, zhName, time_now, time_now)
            session_api.add(obj_module)

            # add module managers
            for one_manager in managers:
                session_api.add(TableAtlasModuleManager(module, one_manager))

            # fill return data
            res["data"]["moduleDetail"] = obj_module.to_json()

        session_api.commit()

    except Exception, e:
        if session_mark is True:
            session_api.rollback()

        traceback_str = traceback.format_exc()
        res["returnCode"]    = conf_code.CONF_CODE["sql_error"][0]
        res["returnMessage"] = traceback_str

        logger.error(traceback_str)

    finally:
        if session_mark is True:
            session_api.close()


def cgi_renameModule(para, res):
    # 1. prepare a logger
    logger = global_tool.get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    for key in ["loginUin", "ownerUin", "module", "zhName"]:
        if key not in para:
            res["returnCode"]    = conf_code.CONF_CODE["para_miss"][0]
            res["returnMessage"] = "miss parameter(%s)" % (key)
            return

    loginUin = int(para["loginUin"])
    ownerUin = int(para["ownerUin"])
    module   = global_tool.deal_post_str(para["module"])
    zhName   = global_tool.deal_post_str(para["zhName"])

    if len(module) == 0:
        global_tool.fill_error_code(res, "empty_module_enName")
        return

    if len(zhName) == 0:
        global_tool.fill_error_code(res, "empty_module_zhName")
        return

    # 3. logic work
    session_mark = False
    try:
        session_api  = global_db.DB_SESSION_API
        session_mark = True

        obj_module = session_api.query(TableAtlasModule).filter(
            TableAtlasModule.module == module
        ).first()

        obj_duplicate = session_api.query(TableAtlasModule).filter(
            TableAtlasModule.zhName == zhName,
            TableAtlasModule.module != module
        ).first()

        obj_permission = global_tool.judge_exist_moduleManager(session_api, module, loginUin)

        if obj_module is None:
            global_tool.fill_error_code(res, "invalid_module")
        elif obj_duplicate is not None:
            global_tool.fill_error_code(res, "duplicate_module_zhName")
        elif obj_permission is False:
            global_tool.fill_error_code(res, "module_permission")
        else:
            obj_module.zhName  = zhName
            obj_module.modTime = datetime.datetime.now()

            res["data"]["moduleDetail"] = obj_module.to_json()

        session_api.commit()

    except Exception, e:
        if session_mark is True:
            session_api.rollback()

        traceback_str = traceback.format_exc()
        res["returnCode"]    = conf_code.CONF_CODE["sql_error"][0]
        res["returnMessage"] = traceback_str

        logger.error(traceback_str)

    finally:
        if session_mark is True:
            session_api.close()


def cgi_getModuleList(para, res):
    # 1. prepare a logger
    logger = global_tool.get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    for key in ["loginUin", "ownerUin"]:
        if key not in para:
            res["returnCode"]    = conf_code.CONF_CODE["para_miss"][0]
            res["returnMessage"] = "miss parameter(%s)" % (key)
            return

    loginUin = int(para["loginUin"])
    ownerUin = int(para["ownerUin"])

    # 3. logic work
    session_mark = False
    try:
        session_api  = global_db.DB_SESSION_API
        session_mark = True

        # init a sql
        sql = session_api.query(TableAtlasModule).join(
            TableAtlasModuleManager,
            TableAtlasModuleManager.module == TableAtlasModule.module
        ).filter(
            TableAtlasModuleManager.userUin == loginUin
        )

        # add condtion : keyword
        keyword = global_tool.deal_post_str(para.get("keyword", ""))
        if len(keyword) != 0:
            sql = sql.filter(or_(
                TableAtlasModule.module.like("%" + keyword + "%"),
                TableAtlasModule.zhName.like("%" + keyword + "%")
            ))

        # get total count
        res["data"]["totalNum"]   = sql.count()
        res["data"]["moduleList"] = []

        # page query
        if  "pageId"   in para and int(para["pageId"])   > 0 and \
            "pageSize" in para and int(para["pageSize"]) > 0:
            pageId   = int(para["pageId"])
            pageSize = int(para["pageSize"])
            sql = sql.limit(pageSize).offset((pageId - 1) * pageSize)

        module_list = sql.all()
        for obj_module in module_list:
            res["data"]["moduleList"].append(obj_module.to_json())

        session_api.commit()

    except Exception, e:
        if session_mark is True:
            session_api.rollback()

        traceback_str = traceback.format_exc()
        res["returnCode"]    = conf_code.CONF_CODE["sql_error"][0]
        res["returnMessage"] = traceback_str

        logger.error(traceback_str)

    finally:
        if session_mark is True:
            session_api.close()


def cgi_getModuleDetail(para, res):
    # 1. prepare a logger
    logger = global_tool.get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    for key in ["loginUin", "ownerUin", "module"]:
        if key not in para:
            res["returnCode"]    = conf_code.CONF_CODE["para_miss"][0]
            res["returnMessage"] = "miss parameter(%s)" % (key)
            return

    loginUin = int(para["loginUin"])
    ownerUin = int(para["ownerUin"])
    module   = global_tool.deal_post_str(para["module"])

    # 3. logic work
    session_mark = False
    try:
        session_api  = global_db.DB_SESSION_API
        session_mark = True

        obj_module = session_api.query(TableAtlasModule).filter(
            TableAtlasModule.module == module
        ).first()

        obj_permission = global_tool.judge_exist_moduleManager(session_api, module, loginUin)

        if obj_module is None:
            global_tool.fill_error_code(res, "invalid_module")
        elif obj_permission is False:
            global_tool.fill_error_code(res, "module_permission")
        else:
            res["data"]["moduleDetail"] = obj_module.to_json()

        session_api.commit()

    except Exception, e:
        if session_mark is True:
            session_api.rollback()

        traceback_str = traceback.format_exc()
        res["returnCode"]    = conf_code.CONF_CODE["sql_error"][0]
        res["returnMessage"] = traceback_str

        logger.error(traceback_str)

    finally:
        if session_mark is True:
            session_api.close()
