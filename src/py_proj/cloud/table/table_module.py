# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, DateTime, Text, Integer
from sqlalchemy.dialects.mysql import BIGINT

from cloud.common.global_db import DB_BASE_API
from cloud.common.global_db import DB_BASE_LOG

class TableCloudModuleUrl(DB_BASE_API):
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
            "addTime"    : str(self.addTime),
            "modTime"    : str(self.modTime)
        }

class TableCloudModuleCode(DB_BASE_API):
    __tablename__ = "t_module_errorcode"

    module       = Column(String(255), nullable = False, primary_key = True)
    code         = Column(Integer    , nullable = False, primary_key = True)
    showSvrError = Column(Integer    , nullable = False)
    codeType     = Column(Integer    , nullable = False)
    codeDesc     = Column(String(255), nullable = False)
    message      = Column(Text       , nullable = False)

    def __init__(self, module, code, showSvrError, codeType, codeDesc, message):
        self.module       = module
        self.code         = code
        self.showSvrError = showSvrError
        self.codeType     = codeType
        self.codeDesc     = codeDesc
        self.message      = message

    def to_json(self):
        return {
            "module"       : self.module,
            "code"         : self.code,
            "showSvrError" : self.showSvrError,
            "codeType"     : self.codeType,
            "codeDesc"     : self.codeDesc,
            "message"      : self.message
        }
