# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, DateTime, Text, Integer
from sqlalchemy.dialects.mysql import BIGINT

from atlas.common import global_db


class TableAtlasModule(global_db.DB_BASE_API):
    __tablename__ = "t_module"

    module  = Column(String(255), nullable = False, primary_key = True)
    zhName  = Column(String(255), nullable = False)
    addTime = Column(DateTime   , nullable = False)
    modTime = Column(DateTime   , nullable = False)

    def __init__(self, module, zhName, addTime, modTime):
        self.module  = module
        self.zhName  = zhName
        self.addTime = addTime
        self.modTime = modTime

    def to_json(self):
        return {
            "module"  : self.module,
            "zhName"  : self.zhName,
            "addTime" : str(self.addTime),
            "modTime" : str(self.modTime)
        }


class TableAtlasModuleManager(global_db.DB_BASE_API):
    __tablename__ = "t_module_manager"

    module  = Column(String(255),             nullable = False, primary_key = True)
    userUin = Column(BIGINT(unsigned = True), nullable = False, primary_key = True)

    def __init__(self, module, userUin):
        self.module  = module
        self.userUin = userUin

    def to_json(self):
        return {
            "module"  : self.module,
            "userUin" : self.userUin
        }


class TableAtlasModuleUrl(global_db.DB_BASE_API):
    __tablename__ = "t_module_url"

    module     = Column(String(255), nullable = False, primary_key = True)
    urlName    = Column(String(255), nullable = False, primary_key = True)
    urlType    = Column(Integer    , nullable = False)
    urlAddress = Column(Text       , nullable = False)
    addTime    = Column(DateTime   , nullable = False)
    modTime    = Column(DateTime   , nullable = False)

    def __init__(self, module, urlName, urlType, urlAddress, addTime, modTime):
        self.module     = module
        self.urlName    = urlName
        self.urlType    = urlType
        self.urlAddress = urlAddress
        self.addTime    = addTime
        self.modTime    = modTime

    def to_json(self):
        return {
            "module"     : self.module,
            "urlName"    : self.urlName,
            "urlType"    : self.urlType,
            "urlAddress" : self.urlAddress,
            "addTime"    : self.addTime,
            "modTime"    : self.modTime
        }


class TableAtlasModuleCode(global_db.DB_BASE_API):
    __tablename__ = "t_module_errorcode"

    module       = Column(String(255), nullable = False, primary_key = True)
    code         = Column(Integer    , nullable = False, primary_key = True)
    showSvrError = Column(Integer    , nullable = False)
    codeDesc     = Column(String(255), nullable = False)
    message      = Column(Text       , nullable = False)

    def __init__(self, module, code, showSvrError, codeDesc, message):
        self.module       = module
        self.code         = code
        self.showSvrError = showSvrError
        self.codeDesc     = codeDesc
        self.message      = message

    def to_json(self):
        return {
            "module"       : self.module,
            "code"         : self.code,
            "showSvrError" : self.showSvrError,
            "codeDesc"     : self.codeDesc,
            "message"      : self.message
        }
