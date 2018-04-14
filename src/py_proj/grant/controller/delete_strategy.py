# -*- coding: utf-8 -*-

import json
import traceback

from grant.conf.conf_code       import CONF_CODE
from grant.common.global_db     import DB_SESSION_AUTH
from grant.common.global_tool   import fill_error_code

from grant.table.table_user     import TableGrantUser
from grant.table.table_strategy import TableGrantStrategyInfo

from grant.model.valid_strategy import valid_strategy_info
from grant.controller.base      import BaseController

class DeleteStrategyController(BaseController):
    def __init__(self, para, res, logger):
        super(DeleteStrategyController, self).__init__(para, res, logger)

    def verify(self):
        if "ownerUin" not in self.para:
            fill_error_code(self.res, "para_miss", "miss parameter(ownerUin)")
            return False

        self.para["ownerUin"] = int(self.para["ownerUin"])

        if self.session_auth.query(TableGrantUser).filter(TableGrantUser.userUin == self.para["ownerUin"]).first() is None:
            fill_error_code(self.res, "invalid_owner_uin")
            return False

        self.para["strategyIdList"] = list(self.para["strategyIdList"])

        n = len(self.para["strategyIdList"])
        i = 0
        while i < n:
            self.para["strategyIdList"][i] = int(self.para["strategyIdList"][i])
            i += 1

        return True

    def deleteStrategy(self, strategyId):
        res = {
            "strategyId" : strategyId,
            "opCode"     : CONF_CODE["success"][0],
            "opMessage"  : CONF_CODE["success"][1]
        }

        obj_strategy = self.session_auth.query(
            TableGrantStrategyInfo
        ).filter(
            TableGrantStrategyInfo.strategyId == strategyId
        ).first()

        if obj_strategy is None:
            res["opCode"]    = CONF_CODE["invalid_strategy_id"][0]
            res["opMessage"] = CONF_CODE["invalid_strategy_id"][1]
        elif obj_strategy.ownerUin != self.para["ownerUin"]:
            res["opCode"]    = CONF_CODE["permission_strategy"][0]
            res["opMessage"] = CONF_CODE["permission_strategy"][1]
        else:
            self.session_auth.delete(obj_strategy)

        return res


    def handler(self):
        session_mark = False

        try:
            self.session_auth = DB_SESSION_AUTH

            if self.verify():
                self.res["data"]["batchRes"] = []
                
                for strategyId in self.para["strategyIdList"]:
                    self.res["data"]["batchRes"].append(self.deleteStrategy(strategyId))

            self.session_auth.commit()

        except Exception, e:
            if session_mark is True:
                self.session_auth.rollback()

            traceback_str = traceback.format_exc()
            fill_error_code(self.res, "sql_error", traceback_str)

            if self.logger:
                self.logger.error(traceback_str)

        finally:
            if session_mark is True:
                self.session_auth.close()
