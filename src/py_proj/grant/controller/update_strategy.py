# -*- coding: utf-8 -*-

import json
import traceback

from grant.common.global_db     import DB_SESSION_AUTH
from grant.common.global_tool   import fill_error_code

from grant.table.table_user     import TableGrantUser
from grant.table.table_strategy import TableGrantStrategyInfo

from grant.model.valid_strategy import valid_strategy_info
from grant.controller.base      import BaseController

class UpdateStrategyController(BaseController):
    def __init__(self, para, res, logger):
        super(UpdateStrategyController, self).__init__(para, res, logger)

    def verify(self):
        # check ownerUin
        if "ownerUin" not in self.para:
            fill_error_code(self.res, "para_miss", "miss parameter(ownerUin)")
            return False

        self.para["ownerUin"] = int(self.para["ownerUin"])

        if self.session_auth.query(TableGrantUser).filter(TableGrantUser.userUin == self.para["ownerUin"]).first() is None:
            fill_error_code(self.res, "invalid_owner_uin")
            return False

        # check strategyId
        if "strategyId" not in self.para:
            fill_error_code(self.res, "para_miss", "miss parameter(strategyId)")
            return False

        self.para["strategyId"] = int(self.para["strategyId"])

        self.obj_strategy = self.session_auth.query(TableGrantStrategyInfo).filter(TableGrantStrategyInfo.strategyId == self.para["strategyId"]).first()

        if self.obj_strategy is None:
            fill_error_code(self.res, "invalid_strategy_id")
            return False

        if self.obj_strategy.ownerUin != self.para["ownerUin"]:
            fill_error_code(self.res, "permission_strategy")
            return False

        # check strategy info
        return valid_strategy_info(self.para, self.res, self.logger)

    def handler(self):
        session_mark = False

        try:
            self.session_auth = DB_SESSION_AUTH

            if self.verify():
                self.obj_strategy.strategyType   = self.para["strategyType"]
                self.obj_strategy.strategyName   = self.para["strategyName"]
                self.obj_strategy.strategyRemark = self.para["strategyRemark"]
                self.obj_strategy.strategyRule   = json.dumps(self.para["strategyRule"]).encode("utf-8")

                self.res["data"]["strategyDetail"] = self.obj_strategy.to_json()

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
