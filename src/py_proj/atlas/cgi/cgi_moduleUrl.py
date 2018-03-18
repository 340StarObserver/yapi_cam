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
from atlas.model.model_module import TableAtlasModuleUrl

# --------------------------------------------------
# constant variables

MODE_MODULE_URLTYPE_ALL    = 0
MODE_MODULE_URLTYPE_SINGLE = 1
MODE_MODULE_URLTYPE_MULTI  = 2

# --------------------------------------------------
# following are some CGIs

def cgi_createModuleUrl(para, res):
    # 1. prepare a logger
    logger = get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    for key in ["loginUin", "ownerUin", "module", "urlName", "urlType", "urlAddress"]:
        if key not in para:
            res["returnCode"]    = CONF_CODE["para_miss"][0]
            res["returnMessage"] = "miss parameter(%s)" % (key)
            return

    loginUin = int(para["loginUin"])
    ownerUin = int(para["ownerUin"])
    urlType  = int(para["urlType"])

    module     = deal_post_str(para["module"])
    urlName    = deal_post_str(para["urlName"])
    urlAddress = deal_post_str(para["urlAddress"])

    # 3. check validation
    if len(module) == 0:
        fill_error_code(res, "empty_module_enName")
        return

    if len(urlName) == 0:
        fill_error_code(res, "empty_module_urlName")
        return

    if len(urlAddress) == 0:
        fill_error_code(res, "empty_module_urlAddress")
        return

    if urlType != MODE_MODULE_URLTYPE_SINGLE and urlType != MODE_MODULE_URLTYPE_MULTI:
        fill_error_code(res, "mode_urlType")
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
        elif judge_exist_moduleUrl(session_api, module, urlName) is True:
            fill_error_code(res, "duplicate_module_urlName")
        else:
            time_now = datetime.datetime.now()
            obj_url  = TableAtlasModuleUrl(module, urlName, urlType, urlAddress, time_now, time_now)
            session_api.add(obj_url)
            res["data"]["urlDetail"] = obj_url.to_json()

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


def cgi_updateModuleUrl(para, res):
    # 1. prepare a logger
    logger = get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    for key in ["loginUin", "ownerUin", "module", "urlName", "urlType", "urlAddress"]:
        if key not in para:
            res["returnCode"]    = CONF_CODE["para_miss"][0]
            res["returnMessage"] = "miss parameter(%s)" % (key)
            return

    loginUin = int(para["loginUin"])
    ownerUin = int(para["ownerUin"])
    urlType  = int(para["urlType"])

    module     = deal_post_str(para["module"])
    urlName    = deal_post_str(para["urlName"])
    urlAddress = deal_post_str(para["urlAddress"])

    # 3. check validation
    if len(module) == 0:
        fill_error_code(res, "empty_module_enName")
        return

    if len(urlName) == 0:
        fill_error_code(res, "empty_module_urlName")
        return

    if len(urlAddress) == 0:
        fill_error_code(res, "empty_module_urlAddress")
        return

    if urlType != MODE_MODULE_URLTYPE_SINGLE and urlType != MODE_MODULE_URLTYPE_MULTI:
        fill_error_code(res, "mode_urlType")
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
            obj_url = session_api.query(
                TableAtlasModuleUrl
            ).filter(
                TableAtlasModuleUrl.module  == module,
                TableAtlasModuleUrl.urlName == urlName
            ).first()

            if obj_url is None:
                fill_error_code(res, "invalid_urlName")
            else:
                obj_url.urlType    = urlType
                obj_url.urlAddress = urlAddress
                obj_url.modTime    = datetime.datetime.now()

                res["data"]["urlDetail"] = obj_url.to_json()

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


def cgi_getModuleUrlList(para, res):
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
    urlType  = int(para.get("urlType", MODE_MODULE_URLTYPE_ALL))
    module   = deal_post_str(para["module"])
    urlName  = deal_post_str(para.get("urlName", ""))

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
                TableAtlasModuleUrl
            ).filter(
                TableAtlasModuleUrl.module == module
            )

            # add condtion : urlName
            if len(urlName) != 0:
                sql = sql.filter(TableAtlasModuleUrl.urlName.like("%" + urlName + "%"))

            # add condition : urlType
            if urlType == MODE_MODULE_URLTYPE_SINGLE or urlType == MODE_MODULE_URLTYPE_MULTI:
                sql = sql.filter(TableAtlasModuleUrl.urlType == urlType)

            # get total count
            res["data"]["totalNum"] = sql.count()
            res["data"]["moduleUrlList"] = []

            # page query
            if  "pageId"   in para and int(para["pageId"])   > 0 and \
                "pageSize" in para and int(para["pageSize"]) > 0:
                pageId   = int(para["pageId"])
                pageSize = int(para["pageSize"])
                sql = sql.limit(pageSize).offset((pageId - 1) * pageSize)

            url_list = sql.all()
            for one_url in url_list:
                res["data"]["moduleUrlList"].append(one_url.to_json())

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


def cgi_getModuleUrlDetail(para, res):
    # 1. prepare a logger
    logger = get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    for key in ["loginUin", "ownerUin", "module", "urlName"]:
        if key not in para:
            res["returnCode"]    = CONF_CODE["para_miss"][0]
            res["returnMessage"] = "miss parameter(%s)" % (key)
            return

    loginUin = int(para["loginUin"])
    ownerUin = int(para["ownerUin"])
    module     = deal_post_str(para["module"])
    urlName    = deal_post_str(para["urlName"])

    # 3. check validation
    if len(module) == 0:
        fill_error_code(res, "empty_module_enName")
        return

    if len(urlName) == 0:
        fill_error_code(res, "empty_module_urlName")
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
            obj_url = session_api.query(
                TableAtlasModuleUrl
            ).filter(
                TableAtlasModuleUrl.module  == module,
                TableAtlasModuleUrl.urlName == urlName
            ).first()

            if obj_url is None:
                fill_error_code(res, "invalid_urlName")
            else:
                res["data"]["urlDetail"] = obj_url.to_json()

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
