# -*- coding: utf-8 -*-

import json

from sqlalchemy import Column, String, DateTime, Text, Integer
from sqlalchemy.dialects.mysql import BIGINT

from grant.common import global_db


class TableGrantStrategyInfo(global_db.DB_BASE_AUTH):
    __tablename__ = "t_strategy"

    strategyId     = Column(BIGINT(unsigned = True), nullable = False, primary_key = True, autoincrement = True)
    ownerUin       = Column(BIGINT(unsigned = True), nullable = False)
    strategyType   = Column(Integer, nullable = False, default = 0)
    strategyName   = Column(String(255), nullable = False)
    strategyRemark = Column(Text, default = None)
    strategyRule   = Column(Text, nullable = False)

    def __init__(self, ownerUin, strategyType, strategyName, strategyRemark, strategyRule):
        self.ownerUin       = ownerUin
        self.strategyType   = strategyType
        self.strategyName   = strategyName
        self.strategyRemark = strategyRemark
        self.strategyRule   = strategyRule

    def to_json(self):
        return {
            "strategyId"     : self.strategyId,
            "ownerUin"       : self.ownerUin,
            "strategyType"   : self.strategyType,
            "strategyName"   : self.strategyName,
            "strategyRemark" : self.strategyRemark,
            "strategyRule"   : json.loads(self.strategyRule)
        }


class TableGrantStrategyRelated(global_db.DB_BASE_AUTH):
    __tablename__ = "r_related_strategy"

    strategyId = Column(BIGINT(unsigned = True), nullable = False, primary_key = True)
    userUin    = Column(BIGINT(unsigned = True), nullable = False, primary_key = True)
    groupId    = Column(BIGINT(unsigned = True), nullable = False, primary_key = True)

    def __init__(self, strategyId, userUin, groupId):
        self.strategyId = strategyId
        self.userUin    = userUin
        self.groupId    = groupId

    def to_json(self):
        return {
            "strategyId" : self.strategyId,
            "userUin"    : self.userUin,
            "groupId"    : self.groupId
        }
