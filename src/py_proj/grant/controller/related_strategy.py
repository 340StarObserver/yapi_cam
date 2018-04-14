# -*- coding: utf-8 -*-

import json
import traceback

from grant.conf.conf_base       import MODE_RELATED_USER_WITH
from grant.conf.conf_base       import MODE_RELATED_USER_WITHOUT
from grant.conf.conf_base       import MODE_RELATED_GROUP_WITH
from grant.conf.conf_base       import MODE_RELATED_GROUP_WITHOUT

from grant.common.global_db     import DB_SESSION_AUTH
from grant.common.global_tool   import fill_error_code

from grant.table.table_user     import TableGrantUser
from grant.table.table_user     import TableGrantAppId
from grant.table.table_group    import TableGrantGroupInfo
from grant.table.table_strategy import TableGrantStrategyInfo
from grant.table.table_strategy import TableGrantStrategyRelated

from grant.controller.base      import BaseController

class StrategyRelatedController(BaseController):
    def __init__(self, para, res, logger):
        super(StrategyRelatedController, self).__init__(para, res, logger)

    def verify(self):
        for k in ["ownerUin", "strategyId"]:
            if k not in self.para:
                fill_error_code(self.res, "para_miss", "miss parameter(%s)" % (k))
                return False
            else:
                self.para[k] = int(self.para[k])

        self.para["relatedUser"]  = int(self.para.get("relatedUser" , MODE_RELATED_USER_WITHOUT ))
        self.para["relatedGroup"] = int(self.para.get("relatedGroup", MODE_RELATED_GROUP_WITHOUT))

        obj_owner = self.session_auth.query(TableGrantUser).filter(TableGrantUser.userUin == self.para["ownerUin"]).first()

        obj_strategy = self.session_auth.query(TableGrantStrategyInfo).filter(TableGrantStrategyInfo.strategyId == self.para["strategyId"]).first()

        if obj_owner is None:
            fill_error_code(self.res, "invalid_owner_uin")
            return False

        if obj_strategy is None:
            fill_error_code(self.res, "invalid_strategy_id")
            return False

        if obj_strategy.ownerUin != self.para["ownerUin"]:
            fill_error_code(self.res, "permission_strategy")
            return False

        return True

    def related_user(self):
        sql_data = self.session_auth.query(
            TableGrantStrategyRelated.userUin,
            TableGrantUser.userName,
            TableGrantUser.ownerUin,
            TableGrantAppId.appId
        ).join(
            TableGrantUser,
            TableGrantStrategyRelated.userUin == TableGrantUser.userUin
        ).join(
            TableGrantAppId,
            TableGrantUser.ownerUin == TableGrantAppId.ownerUin
        ).filter(
            TableGrantStrategyRelated.strategyId == self.para["strategyId"],
            TableGrantStrategyRelated.userUin != 0
        ).all()

        self.res["data"]["userList"] = []

        for item in sql_data:
            self.res["data"]["userList"].append({
                "userUin"  : item[0],
                "userName" : item[1],
                "ownerUin" : item[2],
                "appId"    : item[3]
            })

    def related_group(self):
        sql_data = self.session_auth.query(
            TableGrantStrategyRelated.groupId,
            TableGrantGroupInfo.groupName,
            TableGrantGroupInfo.ownerUin
        ).join(
            TableGrantGroupInfo,
            TableGrantStrategyRelated.groupId == TableGrantGroupInfo.groupId
        ).filter(
            TableGrantStrategyRelated.strategyId == self.para["strategyId"],
            TableGrantStrategyRelated.userUin == 0
        ).all()

        self.res["data"]["groupList"] = []

        for item in sql_data:
            self.res["data"]["groupList"].append({
                "groupId"   : item[0],
                "groupName" : item[1],
                "ownerUin"  : item[2]
            })

    def handler(self):
        session_mark = False

        try:
            self.session_auth = DB_SESSION_AUTH

            if self.verify():
                if self.para["relatedUser"] == MODE_RELATED_USER_WITH:
                    self.related_user()
                if self.para["relatedGroup"] == MODE_RELATED_GROUP_WITH:
                    self.related_group()

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
