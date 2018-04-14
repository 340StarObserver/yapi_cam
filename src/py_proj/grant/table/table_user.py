# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, DateTime, Text, Integer
from sqlalchemy.dialects.mysql import BIGINT

from grant.common import global_db


class TableGrantUser(global_db.DB_BASE_AUTH):
    __tablename__ = "t_user"

    userUin    = Column(BIGINT(unsigned = True), nullable = False, primary_key = True)
    ownerUin   = Column(BIGINT(unsigned = True), nullable = False)
    userName   = Column(String(255), nullable = False)
    userRemark = Column(Text, default = None)
    userPhone  = Column(BIGINT(unsigned = True), default = None)
    userEmail  = Column(String(255), default = None)
    addTime    = Column(DateTime, nullable = False)
    modTime    = Column(DateTime, nullable = False)

    def __init__(self, userUin, ownerUin, userName, userRemark, userPhone, userEmail, addTime, modTime):
        self.userUin    = userUin
        self.ownerUin   = ownerUin
        self.userName   = userName
        self.userRemark = userRemark
        self.userPhone  = userPhone
        self.userEmail  = userEmail
        self.addTime    = addTime
        self.modTime    = modTime

    def to_json(self):
        return {
            "userUin"    : self.userUin,
            "ownerUin"   : self.ownerUin,
            "userName"   : self.userName,
            "userRemark" : self.userRemark,
            "userPhone"  : self.userPhone,
            "userEmail"  : self.userEmail,
            "addTime"    : str(self.addTime),
            "modTime"    : str(self.modTime)
        }


class TableGrantAppId(global_db.DB_BASE_AUTH):
    __tablename__ = "r_user_app"

    ownerUin = Column(BIGINT(unsigned = True), nullable = False, primary_key = True)
    appId    = Column(BIGINT(unsigned = True), nullable = False)

    def __init__(self, ownerUin, appId):
        self.ownerUin = ownerUin
        self.appId    = appId

    def to_json(self):
        return {
            "ownerUin" : self.ownerUin,
            "appId"    : self.appId
        }
