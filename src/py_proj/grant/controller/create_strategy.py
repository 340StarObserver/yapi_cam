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


class CreateStrategyController(BaseController):
    def __init__(self, para, res, logger):
        super(CreateStrategyController, self).__init__(para, res, logger)

    def handler(self):
        # 1. if miss uin
        if "ownerUin" not in self.para:
            fill_error_code(self.res, "para_miss", "miss parameter(ownerUin)")
            return

        self.para["ownerUin"] = int(self.para["ownerUin"])

        # 2. if invalid strategy info
        if not valid_strategy_info(self.para, self.res, self.logger):
            return

        # 3. logic work
        session_mark = False

        try:
            session_auth = DB_SESSION_AUTH

            if session_auth.query(TableGrantUser).filter(TableGrantUser.userUin == self.para["ownerUin"]).first() is None:
                fill_error_code(self.res, "invalid_owner_uin")

            else:
                obj_strategy = TableGrantStrategyInfo(
                    self.para["ownerUin"],
                    self.para["strategyType"],
                    self.para["strategyName"],
                    self.para["strategyRemark"],
                    json.dumps(self.para["strategyRule"]).encode("utf-8")
                )
                session_auth.add(obj_strategy)
                session_auth.flush()
                self.res["data"]["strategyDetail"] = obj_strategy.to_json()

            session_auth.commit()

        except Exception, e:
            if session_mark is True:
                session_auth.rollback()

            traceback_str = traceback.format_exc()
            fill_error_code(self.res, "sql_error", traceback_str)

            if self.logger:
                self.logger.error(traceback_str)

        finally:
            if session_mark is True:
                session_auth.close()
