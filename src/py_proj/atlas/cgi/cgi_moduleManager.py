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
