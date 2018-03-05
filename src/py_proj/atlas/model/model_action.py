# -*- coding: utf-8 -*-

import time

from sqlalchemy import Column, String, DateTime, Text, Integer
from sqlalchemy.dialects.mysql import BIGINT

from atlas.common import global_db


class TableAtlasAction(global_db.DB_BASE_API):
    __tablename__ = "t_action"

    module        = Column(String(255), nullable = False, primary_key = True)
    action        = Column(String(255), nullable = False, primary_key = True)
    actionName    = Column(String(255), nullable = False)
    addTime       = Column(DateTime   , nullable = False)
    modTime       = Column(DateTime   , nullable = False)
    urlName       = Column(String(255), nullable = False)
    isAuth        = Column(Integer    , nullable = False)
    funcReq       = Column(Text, default = None)
    funcRsp       = Column(Text, default = None)
    funcResource  = Column(Text, default = None)
    funcCondition = Column(Text, default = None)

    def __init__(self, module, action, actionName, addTime, modTime, urlName, isAuth, funcReq, funcRsp, funcResource, funcCondition):
        self.module        = module
        self.action        = action
        self.actionName    = actionName
        self.addTime       = addTime
        self.modTime       = modTime
        self.urlName       = urlName
        self.isAuth        = isAuth
        self.funcReq       = funcReq
        self.funcRsp       = funcRsp
        self.funcResource  = funcResource
        self.funcCondition = funcCondition

    def to_json(self):
        return {
            "module"        : self.module,
            "action"        : self.action,
            "actionName"    : self.actionName,
            "addTime"       : str(self.addTime),
            "modTime"       : str(self.modTime),
            "urlName"       : self.urlName,
            "isAuth"        : self.isAuth,
            "funcReq"       : self.funcReq,
            "funcRsp"       : self.funcRsp,
            "funcResource"  : self.funcResource,
            "funcCondition" : self.funcCondition
        }


class TableAtlasActionRate(global_db.DB_BASE_LOG):
    __tablename__ = "t_action_rate"

    module       = Column(String(255), nullable = False, primary_key = True)
    action       = Column(String(255), nullable = False, primary_key = True)
    isRate       = Column(Integer    , nullable = False)
    minRate      = Column(Integer    , nullable = False)
    curFrequency = Column(Integer    , nullable = False, default = 0)
    timeLastZero = Column(BIGINT(unsigned = True), nullable = False)
    timeLastCall = Column(BIGINT(unsigned = True), nullable = False)

    def __init__(self, module, action, isRate, minRate, timeLastZero, timeLastCall):
        self.module       = module
        self.action       = action
        self.isRate       = isRate
        self.minRate      = minRate
        self.timeLastZero = timeLastZero
        self.timeLastCall = timeLastCall

    def to_json(self):
        return {
            "module"       : self.module,
            "action"       : self.action,
            "isRate"       : self.isRate,
            "minRate"      : self.minRate,
            "curFrequency" : self.curFrequency,
            "timeLastZero" : time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.timeLastZero)),
            "timeLastCall" : time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.timeLastCall))
        }


class TableAtlasActionLog(global_db.DB_BASE_LOG):
    __tablename__ = "t_action_log"

    reqId       = Column(String(255)            , nullable = False, primary_key = True)
    reqTime     = Column(BIGINT(unsigned = True), nullable = False)
    module      = Column(String(255)            , nullable = False)
    action      = Column(String(255)            , nullable = False)
    reqNonce    = Column(BIGINT(unsigned = True), default = None)
    userUin     = Column(BIGINT(unsigned = True), default = None)
    reqIp       = Column(String(255), default = None)
    reqRegion   = Column(String(255), default = None)
    receiveData = Column(Text       , default = None)
    returnData  = Column(Text       , default = None)
    returnCode  = Column(Integer    , default = None)
    camUrl      = Column(String(255), default = None)
    camAk       = Column(String(255), default = None)
    camReq      = Column(Text       , default = None)
    camRsp      = Column(Text       , default = None)
    svrUrl      = Column(String(255), default = None)
    svrReq      = Column(Text       , default = None)
    svrRsp      = Column(Text       , default = None)

    def __init__(self, reqId, reqTime, reqIp, reqRegion, reqNonce, module, action, userUin, receiveData, returnData, returnCode, camUrl, camAk, camReq, camRsp, svrUrl, svrReq, svrRsp):
        self.reqId       = reqId
        self.reqTime     = reqTime
        self.reqIp       = reqIp
        self.reqRegion   = reqRegion
        self.reqNonce    = reqNonce
        self.module      = module
        self.action      = action
        self.userUin     = userUin
        self.receiveData = receiveData
        self.returnData  = returnData
        self.returnCode  = returnCode
        self.camUrl      = camUrl
        self.camAk       = camAk
        self.camReq      = camReq
        self.camRsp      = camRsp
        self.svrUrl      = svrUrl
        self.svrReq      = svrReq
        self.svrRsp      = svrRsp

    def to_json(self):
        return {
            "reqId"       : self.reqId,
            "reqTime"     : time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.reqTime)),
            "reqIp"       : self.reqIp,
            "reqRegion"   : self.reqRegion,
            "reqNonce"    : self.reqNonce,
            "module"      : self.module,
            "action"      : self.action,
            "userUin"     : self.userUin,
            "receiveData" : self.receiveData,
            "returnData"  : self.returnData,
            "returnCode"  : self.returnCode,
            "camUrl"      : self.camUrl,
            "camAk"       : self.camAk,
            "camReq"      : self.camReq,
            "camRsp"      : self.camRsp,
            "svrUrl"      : self.svrUrl,
            "svrReq"      : self.svrReq,
            "svrRsp"      : self.svrRsp
        }
