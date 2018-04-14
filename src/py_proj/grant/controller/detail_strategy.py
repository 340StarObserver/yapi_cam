# -*- coding: utf-8 -*-

import json
import traceback

from grant.common.global_db     import DB_SESSION_AUTH
from grant.common.global_tool   import fill_error_code

from grant.table.table_user     import TableGrantUser
from grant.table.table_strategy import TableGrantStrategyInfo

from grant.model.valid_strategy import valid_strategy_info
from grant.controller.base      import BaseController

class DetailStrategyController(BaseController):
    def __init__(self, para, res, logger):
        super(DetailStrategyController, self).__init__(para, res, logger)

    def verify(self):
        if "ownerUin" not in self.para:
            fill_error_code(self.res, "para_miss", "miss parameter(ownerUin)")
            return False

        if "strategyId" not in self.para:
            fill_error_code(self.res, "para_miss", "miss parameter(strategyId)")
            return False

        ownerUin   = int(self.para["ownerUin"])
        strategyId = int(self.para["strategyId"])

        self.obj_strategy = self.session_auth.query(
            TableGrantStrategyInfo
        ).filter(
            TableGrantStrategyInfo.strategyId == strategyId
        ).first()

        if self.obj_strategy is None:
            fill_error_code(self.res, "invalid_strategy_id")
            return False

        if self.obj_strategy.ownerUin != ownerUin:
            fill_error_code(self.res, "permission_strategy")
            return False

        return True

    def handler(self):
        session_mark = False

        try:
            self.session_auth = DB_SESSION_AUTH

            if self.verify():
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
