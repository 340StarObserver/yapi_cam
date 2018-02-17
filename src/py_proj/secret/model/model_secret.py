# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, DateTime, Text, Integer
from sqlalchemy.dialects.mysql import BIGINT

from secret.common import global_db

class TableSecretKey(global_db.DB_BASE_AUTH):
    __tablename__ = "t_secret"

    secretId     = Column(String(40), nullable = False, primary_key = True)
    secretKey    = Column(String(40), nullable = False)
    userUin      = Column(BIGINT(unsigned = True), nullable = False)
    status       = Column(Integer , nullable = False)
    addTime      = Column(DateTime, nullable = False)
    modTime      = Column(DateTime, nullable = False)
    secretRemark = Column(Text, default = None)

    def __init__(self, secretId, secretKey, userUin, status, addTime, modTime, secretRemark):
        self.secretId     = secretId
        self.secretKey    = secretKey
        self.userUin      = userUin
        self.status       = status
        self.addTime      = addTime
        self.modTime      = modTime
        self.secretRemark = secretRemark

    def to_json(self):
        return {
            "secretId"     : self.secretId,
            "secretKey"    : self.secretKey,
            "userUin"      : self.userUin,
            "status"       : self.status,
            "addTime"      : str(self.addTime),
            "modTime"      : str(self.modTime),
            "secretRemark" : self.secretRemark
        }
