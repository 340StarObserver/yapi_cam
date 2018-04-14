# -*- coding: utf-8 -*-

import json
import traceback

from grant.common.global_db     import DB_SESSION_AUTH
from grant.common.global_tool   import fill_error_code
from grant.common.global_tool   import deal_post_str

from grant.table.table_strategy import TableGrantStrategyInfo
from grant.table.table_strategy import TableGrantStrategyRelated

from grant.controller.base      import BaseController

class ListStrategyController(BaseController):
    def __init__(self, para, res, logger):
        super(ListStrategyController, self).__init__(para, res, logger)

    def verify(self):
        if "ownerUin" not in self.para:
            fill_error_code(self.res, "para_miss", "miss parameter(ownerUin)")
            return False
        else:
            self.para["ownerUin"] = int(self.para["ownerUin"])

        return True

    def related_strategy_by_user(self, userUin):
        sql_data = self.session_auth.query(
            TableGrantStrategyRelated.strategyId
        ).filter(
            TableGrantStrategyRelated.userUin == userUin
        ).all()

        user_list = []

        for item in sql_data:
            user_list.append(item[0])

        return tuple(user_list)

    def related_strategy_by_group(self, groupId):
        sql_data = self.session_auth.query(
            TableGrantStrategyRelated.strategyId
        ).filter(
            TableGrantStrategyRelated.groupId == groupId
        ).all()

        group_list = []

        for item in sql_data:
            group_list.append(item[0])

        return tuple(group_list)

    def query_strategy(self):
        # init sql
        sql = self.session_auth.query(
            TableGrantStrategyInfo.strategyId,
            TableGrantStrategyInfo.ownerUin,
            TableGrantStrategyInfo.strategyType,
            TableGrantStrategyInfo.strategyName,
            TableGrantStrategyInfo.strategyRemark
        ).filter(
            TableGrantStrategyInfo.ownerUin == self.para["ownerUin"]
        )

        # add conditions
        if "strategyName" in self.para:
            strategyName = deal_post_str(self.para["strategyName"])
            if len(strategyName) != 0:
                sql = sql.filter(TableGrantStrategyInfo.strategyName.like("%" + strategyName + "%"))

        if "strategyType" in self.para:
            sql = sql.filter(TableGrantStrategyInfo.strategyType == int(self.para["strategyType"]))

        if "userUin" in self.para:
            sql = sql.filter(
                TableGrantStrategyInfo.strategyId.in_(
                    self.related_strategy_by_user(int(self.para["userUin"]))
                )
            )
        
        if "groupId" in self.para:
            sql = sql.filter(
                TableGrantStrategyInfo.strategyId.in_(
                    self.related_strategy_by_group(int(self.para["groupId"]))
                )
            )

        # get total number
        self.res["data"]["totalNum"] = sql.count()
        self.res["data"]["strategyList"] = []

        # page query
        if  "pageId"   in self.para and int(self.para["pageId"])   > 0 and \
            "pageSize" in self.para and int(self.para["pageSize"]) > 0:
            pageId   = int(self.para["pageId"])
            pageSize = int(self.para["pageSize"])
            sql = sql.limit(pageSize).offset((pageId - 1) * pageSize)

        sql_data = sql.all()

        for item in sql_data:
            self.res["data"]["strategyList"].append({
                "strategyId"     : item[0],
                "ownerUin"       : item[1],
                "strategyType"   : item[2],
                "strategyName"   : item[3],
                "strategyRemark" : item[4]
            })

    def handler(self):
        session_mark = False

        try:
            self.session_auth = DB_SESSION_AUTH

            if self.verify():
                self.query_strategy()

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
