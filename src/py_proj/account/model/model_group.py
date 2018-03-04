# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, DateTime, Text, Integer
from sqlalchemy.dialects.mysql import BIGINT

from account.common import global_db

class TableAccountGroupInfo(global_db.DB_BASE_AUTH):
    __tablename__ = "t_group"

    groupId     = Column(BIGINT(unsigned = True), nullable = False, primary_key = True, autoincrement = True)
    ownerUin    = Column(BIGINT(unsigned = True), nullable = False)
    groupName   = Column(String(255), nullable = False)
    groupRemark = Column(Text, default = None)
    groupNum    = Column(BIGINT(unsigned = True), nullable = False, default = 0)
    addTime     = Column(DateTime, nullable = False)
    modTime     = Column(DateTime, nullable = False)

    def __init__(self, ownerUin, groupName, groupRemark, addTime, modTime):
        self.ownerUin    = ownerUin
        self.groupName   = groupName
        self.groupRemark = groupRemark
        self.addTime     = addTime
        self.modTime     = modTime

    def to_json(self):
        return {
            "groupId"     : self.groupId,
            "ownerUin"    : self.ownerUin,
            "groupName"   : self.groupName,
            "groupRemark" : self.groupRemark,
            "groupNum"    : self.groupNum,
            "addTime"     : str(self.addTime),
            "modTime"     : str(self.modTime)
        }

class TableAccountGroupMember(global_db.DB_BASE_AUTH):
    __tablename__ = "r_user_group"

    groupId = Column(BIGINT(unsigned = True), nullable = False, primary_key = True)
    userUin = Column(BIGINT(unsigned = True), nullable = False, primary_key = True)
    addTime = Column(DateTime, nullable = False)

    def __init__(self, groupId, userUin, addTime):
        self.groupId = groupId
        self.userUin = userUin
        self.addTime = addTime

    def to_json(self):
        return {
            "groupId" : self.groupId,
            "userUin" : self.userUin,
            "addTime" : str(self.addTime)
        }
