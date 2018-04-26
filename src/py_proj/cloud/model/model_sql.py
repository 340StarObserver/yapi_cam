# -*- coding: utf-8 -*-

import json
import traceback

from sqlalchemy import and_

from cloud.conf.config        import CONF_SWOOLE

from cloud.common.global_db   import DB_SESSION_API
from cloud.common.global_db   import DB_SESSION_LOG

from cloud.table.table_module import TableCloudModuleUrl
from cloud.table.table_module import TableCloudModuleCode
from cloud.table.table_action import TableCloudAction
from cloud.table.table_action import TableCloudActionLog
from cloud.table.table_action import TableCloudActionRate


def queryActionDetail(module, action, logger):
    """ 获取接口详情 """
    res = None
    session_mark = False

    try:
        session_api  = DB_SESSION_API
        session_mark = True

        obj = session_api.query(
            TableCloudAction.module,
            TableCloudAction.action,
            TableCloudAction.urlName,
            TableCloudModuleUrl.urlType,
            TableCloudModuleUrl.urlAddress,
            TableCloudAction.isAuth,
            TableCloudAction.funcReq,
            TableCloudAction.funcRsp,
            TableCloudAction.funcResource,
            TableCloudAction.funcCondition
        ).join(
            TableCloudModuleUrl,
            and_(
                TableCloudAction.module  == TableCloudModuleUrl.module,
                TableCloudAction.urlName == TableCloudModuleUrl.urlName
            )
        ).filter(
            TableCloudAction.module == module,
            TableCloudAction.action == action
        ).first()

        if obj:
            res = {
                "module"        : obj[0],
                "action"        : obj[1],
                "urlName"       : obj[2],
                "urlType"       : obj[3],
                "urlAddress"    : obj[4],
                "isAuth"        : obj[5],
                "funcReq"       : obj[6],
                "funcRsp"       : obj[7],
                "funcResource"  : obj[8],
                "funcCondition" : obj[9]
            }

        session_api.commit()

    except Exception, e:
        if session_mark:
            session_api.rollback()

        if logger:
            logger.error(traceback.format_exc())

    finally:
        if session_mark:
            session_api.close()

    return res


def beyondRateLimit(module, action, reqTime, logger):
    """ 判断是否超过频次限制 """
    res = False
    session_mark = False

    try:
        session_log  = DB_SESSION_LOG
        session_mark = True

        obj = session_log.query(
            TableCloudActionRate
        ).filter(
            TableCloudActionRate.module == module,
            TableCloudActionRate.action == action
        ).first()

        if obj:
            obj.curFrequency += 1
            obj.timeLastCall = reqTime

            if obj.timeLastCall - obj.timeLastZero > 60:
                obj.curFrequency = 1
                obj.timeLastZero = obj.timeLastCall
            elif obj.isRate and obj.curFrequency > obj.minRate:
                res = True

        session_log.commit()

    except Exception, e:
        if session_mark:
            session_log.rollback()

        if logger:
            logger.error(traceback.format_exc())

    finally:
        if session_mark:
            session_log.close()

    return res


def writeLog(reqData, rspData, auditData, logger):
    """ 审计日志 """
    session_mark = False

    try:
        session_log  = DB_SESSION_LOG
        session_mark = True

        if "camReq" in auditData:
            camReq = json.dumps(auditData["camReq"]).encode("utf-8")
        else:
            camReq = None

        if "camRsp" in auditData:
            camRsp = json.dumps(auditData["camRsp"]).encode("utf-8")
        else:
            camRsp = None

        if "svrReq" in auditData:
            svrReq = json.dumps(auditData["svrReq"]).encode("utf-8")
        else:
            svrReq = None

        if "svrRsp" in auditData:
            svrRsp = json.dumps(auditData["svrRsp"]).encode("utf-8")
        else:
            svrRsp = None

        obj = TableCloudActionLog(
            reqId       = reqData["reqId"],
            reqTime     = reqData["reqTime"],
            reqIp       = reqData["reqIp"],
            reqRegion   = reqData["reqRegion"],
            reqNonce    = reqData["reqNonce"],
            module      = reqData["module"],
            action      = reqData["action"],
            userUin     = reqData["params"].get("loginUin", None),
            receiveData = json.dumps(reqData).encode("utf-8"),
            returnData  = json.dumps(rspData).encode("utf-8"),
            returnCode  = rspData["code"],
            camUrl      = auditData.get("camUrl", CONF_SWOOLE["url"]),
            camAk       = reqData["secretId"],
            camReq      = camReq,
            camRsp      = camRsp,
            svrUrl      = auditData.get("svrUrl", None),
            svrReq      = svrReq,
            svrRsp      = svrRsp
        )

        session_log.add(obj)
        session_log.commit()

    except Exception, e:
        if session_mark:
            session_log.rollback()

        if logger:
            logger.error(traceback.format_exc())

    finally:
        if session_mark:
            session_log.close()


def queryErrorCode(module, code, logger):
    """ 获取对应的错误码 """
    res = None
    session_mark = False

    try:
        session_api  = DB_SESSION_API
        session_mark = True

        obj = session_api.query(
            TableCloudModuleCode
        ).filter(
            TableCloudModuleCode.module == module,
            TableCloudModuleCode.code   == code
        ).first()

        if obj:
            res = obj.to_json()

        session_api.commit()

    except Exception, e:
        if session_mark:
            session_api.rollback()

        if logger:
            logger.error(traceback.format_exc())

    finally:
        if session_mark:
            session_api.close()

    return res
