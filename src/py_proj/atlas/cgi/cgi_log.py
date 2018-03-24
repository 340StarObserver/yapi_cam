# -*- coding: utf-8 -*-

import sys
import time
import datetime
import traceback

from atlas.conf.conf_code     import *
from atlas.common.global_db   import *
from atlas.common.global_call import *
from atlas.common.global_tool import *

from atlas.model.model_action import TableAtlasActionRate
from atlas.model.model_action import TableAtlasActionLog

# --------------------------------------------------
# constant variables

MODE_RATE_QUERY_ALL             = 0
MODE_RATE_QUERY_NOTLIMIT        = 1
MODE_RATE_QUERY_LIMIT_NOTBEYOND = 2
MODE_RATE_QUERY_LIMIT_BEYOND    = 3

MODE_ACTION_RATE_CLOSE = 0
MODE_ACTION_RATE_OPEN  = 1

# --------------------------------------------------
# following are some CGIs

def cgi_getActionRate(para, res):
    # 1. prepare a logger
    logger = get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    module = deal_post_str(para.get("module", ""))
    action = deal_post_str(para.get("action", ""))
    rateMode = int(para.get("rateMode", MODE_RATE_QUERY_ALL))

    if len(module) == 0:
        fill_error_code(res, "empty_module_enName")
        return

    # 3. logic work
    session_mark = False
    try:
        session_log  = DB_SESSION_LOG
        session_mark = True

        # init a sql
        sql = session_log.query(TableAtlasActionRate).filter(TableAtlasActionRate.module == module)

        # add condition
        if len(action) != 0:
            sql = sql.filter(TableAtlasActionRate.action.like("%" + action + "%"))

        if rateMode == MODE_RATE_QUERY_NOTLIMIT:
            sql = sql.filter(TableAtlasActionRate.isRate == MODE_ACTION_RATE_CLOSE)
        elif rateMode == MODE_RATE_QUERY_LIMIT_NOTBEYOND:
            sql = sql.filter(
                TableAtlasActionRate.isRate == MODE_ACTION_RATE_OPEN,
                TableAtlasActionRate.curFrequency <= TableAtlasActionRate.minRate
            )
        elif rateMode == MODE_RATE_QUERY_LIMIT_BEYOND:
            sql = sql.filter(
                TableAtlasActionRate.isRate == MODE_ACTION_RATE_OPEN,
                TableAtlasActionRate.curFrequency > TableAtlasActionRate.minRate
            )

        # sort
        sql = sql.order_by(TableAtlasActionRate.curFrequency.desc())

        # get total count
        res["data"]["totalNum"] = sql.count()
        res["data"]["actionRateList"] = []

        # page query
        if  "pageId"   in para and int(para["pageId"])   > 0 and \
            "pageSize" in para and int(para["pageSize"]) > 0:
            pageId   = int(para["pageId"])
            pageSize = int(para["pageSize"])
            sql = sql.limit(pageSize).offset((pageId - 1) * pageSize)

        obj_rate_list = sql.all()

        for obj_rate in obj_rate_list:
            res["data"]["actionRateList"].append(obj_rate.to_json())

        session_log.commit()

    except Exception, e:
        if session_mark is True:
            session_log.rollback()

        traceback_str = traceback.format_exc()
        res["returnCode"]    = CONF_CODE["sql_error"][0]
        res["returnMessage"] = traceback_str

        logger.error(traceback_str)

    finally:
        if session_mark is True:
            session_log.close()


def cgi_getActionLogList(para, res):
    # 1. prepare a logger
    logger = get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    time_int = int(time.time())
    time_str = time.strftime("%Y-%m-%d", time.localtime(time_int))
    time_str = time_str + ":" + time_str

    reqTime  = deal_post_str(para.get("reqTime", time_str))
    reqTime  = reqTime.split(":")

    timeBeg  = int(time.mktime(time.strptime(reqTime[0] + " 00:00:00", "%Y-%m-%d %H:%M:%S")))
    timeEnd  = int(time.mktime(time.strptime(reqTime[1] + " 23:59:59", "%Y-%m-%d %H:%M:%S")))

    module    = deal_post_str(para.get("module"   , ""))
    action    = deal_post_str(para.get("action"   , ""))
    reqIp     = deal_post_str(para.get("reqIp"    , ""))
    reqRegion = deal_post_str(para.get("reqRegion", ""))

    pageId    = int(para.get("pageId"  , 1 ))
    pageSize  = int(para.get("pageSize", 10))

    if pageId <= 0:
        pageId = 1

    if pageSize <= 0:
        pageSize = 10

    # 3. logic work
    session_mark = False
    try:
        session_log  = DB_SESSION_LOG
        session_mark = True

        # init a sql
        sql = session_log.query(
            TableAtlasActionLog.reqId,
            TableAtlasActionLog.reqTime,
            TableAtlasActionLog.reqIp,
            TableAtlasActionLog.reqRegion,
            TableAtlasActionLog.module,
            TableAtlasActionLog.action,
            TableAtlasActionLog.userUin,
            TableAtlasActionLog.returnCode
        ).filter(
            TableAtlasActionLog.reqTime >= timeBeg,
            TableAtlasActionLog.reqTime <= timeEnd
        )

        # add condition
        if len(module) != 0:
            sql = sql.filter(TableAtlasActionLog.module == module)

        if len(action) != 0:
            sql = sql.filter(TableAtlasActionLog.action == action)

        if len(reqIp) != 0:
            sql = sql.filter(TableAtlasActionLog.reqIp == reqIp)

        if len(reqRegion) != 0:
            sql = sql.filter(TableAtlasActionLog.reqRegion == reqRegion)

        if "userUin" in para:
            sql = sql.filter(TableAtlasActionLog.userUin == int(para["userUin"]))

        if "returnCode" in para:
            sql = sql.filter(TableAtlasActionLog.returnCode == int(para["returnCode"]))

        # sort
        sql = sql.order_by(TableAtlasActionLog.reqTime.desc())

        # get total count
        res["data"]["totalNum"] = sql.count()
        res["data"]["actionLogList"] = []

        # page query
        sql = sql.limit(pageSize).offset((pageId - 1) * pageSize)

        obj_log_list = sql.all()

        for obj_log in obj_log_list:
            res["data"]["actionLogList"].append({
                "reqId"      : obj_log[0],
                "reqTime"    : time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(obj_log[1])),
                "reqIp"      : obj_log[2],
                "regRegion"  : obj_log[3],
                "module"     : obj_log[4],
                "action"     : obj_log[5],
                "userUin"    : obj_log[6],
                "returnCode" : obj_log[7]
            })

        session_log.commit()

    except Exception, e:
        if session_mark is True:
            session_log.rollback()

        traceback_str = traceback.format_exc()
        res["returnCode"]    = CONF_CODE["sql_error"][0]
        res["returnMessage"] = traceback_str

        logger.error(traceback_str)

    finally:
        if session_mark is True:
            session_log.close()


def cgi_getActionLogDetail(para, res):
    # 1. prepare a logger
    logger = get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    reqId = deal_post_str(para.get("reqId", ""))

    if len(reqId) == 0:
        fill_error_code(res, "invalid_log")
        return

    # 3. logic work
    session_mark = False
    try:
        session_log  = DB_SESSION_LOG
        session_mark = True

        obj_log = session_log.query(TableAtlasActionLog).filter(TableAtlasActionLog.reqId == reqId).first()

        if obj_log is None:
            fill_error_code(res, "invalid_log")
        else:
            res["data"]["actionLogDetail"] = obj_log.to_json()

        session_log.commit()

    except Exception, e:
        if session_mark is True:
            session_log.rollback()

        traceback_str = traceback.format_exc()
        res["returnCode"]    = CONF_CODE["sql_error"][0]
        res["returnMessage"] = traceback_str

        logger.error(traceback_str)

    finally:
        if session_mark is True:
            session_log.close()
