# -*- coding: utf-8 -*-

import json
import traceback

from grant.conf.conf_code       import CONF_CODE
from grant.conf.conf_base       import MODE_STRATEGY_BIND
from grant.conf.conf_base       import MODE_STRATEGY_UNBIND

from grant.common.global_db     import DB_SESSION_AUTH
from grant.common.global_tool   import fill_error_code

from grant.table.table_user     import TableGrantUser
from grant.table.table_group    import TableGrantGroupInfo
from grant.table.table_strategy import TableGrantStrategyInfo
from grant.table.table_strategy import TableGrantStrategyRelated

from grant.controller.base      import BaseController


class BindUserStrategyController(BaseController):
    def __init__(self, para, res, logger):
        super(BindUserStrategyController, self).__init__(para, res, logger)

    def verify(self):
        if "ownerUin" not in self.para:
            fill_error_code(self.res, "para_miss", "miss parameter(ownerUin)")
            return False

        self.para["ownerUin"] = int(self.para["ownerUin"])

        if self.session_auth.query(TableGrantUser).filter(TableGrantUser.userUin == self.para["ownerUin"]).first() is None:
            fill_error_code(self.res, "invalid_owner_uin")
            return False

        if "bindMode" not in self.para:
            fill_error_code(self.res, "para_miss", "miss parameter(bindMode)")
            return False

        self.para["bindMode"] = int(self.para["bindMode"])

        if self.para["bindMode"] != MODE_STRATEGY_BIND and self.para["bindMode"] != MODE_STRATEGY_UNBIND:
            fill_error_code(self.res, "mode_related_bind")
            return False

        self.para["bindList"] = list(self.para["bindList"])

        n = len(self.para["bindList"])
        i = 0
        while i < n:
            self.para["bindList"][i]["strategyId"] = int(self.para["bindList"][i]["strategyId"])
            self.para["bindList"][i]["userUin"]    = int(self.para["bindList"][i]["userUin"])
            i += 1

        f = lambda x, y : x if y in x else x + [y]
        self.para["bindList"] = reduce(f, [[], ] + self.para["bindList"])

        return True

    def bind(self, strategyId, userUin):
        res = {
            "strategyId" : strategyId,
            "userUin"    : userUin,
            "opCode"     : CONF_CODE["success"][0],
            "opMessage"  : CONF_CODE["success"][1]
        }

        obj_strategy = self.session_auth.query(
            TableGrantStrategyInfo
        ).filter(
            TableGrantStrategyInfo.strategyId == strategyId
        ).first()

        obj_user = self.session_auth.query(
            TableGrantUser
        ).filter(
            TableGrantUser.userUin == userUin
        ).first()

        obj_bind = self.session_auth.query(
            TableGrantStrategyRelated
        ).filter(
            TableGrantStrategyRelated.strategyId == strategyId,
            TableGrantStrategyRelated.userUin    == userUin,
            TableGrantStrategyRelated.groupId    == 0
        ).first()

        if obj_strategy is None:
            res["opCode"]    = CONF_CODE["invalid_strategy_id"][0]
            res["opMessage"] = CONF_CODE["invalid_strategy_id"][1]
            return res

        if obj_strategy.ownerUin != self.para["ownerUin"]:
            res["opCode"]    = CONF_CODE["permission_strategy"][0]
            res["opMessage"] = CONF_CODE["permission_strategy"][1]
            return res

        if obj_user is None:
            res["opCode"]    = CONF_CODE["invalid_user_uin"][0]
            res["opMessage"] = CONF_CODE["invalid_user_uin"][1]
            return res

        if obj_user.ownerUin != self.para["ownerUin"]:
            res["opCode"]    = CONF_CODE["permission_user"][0]
            res["opMessage"] = CONF_CODE["permission_user"][1]
            return res

        if self.para["bindMode"] == MODE_STRATEGY_BIND:
            if obj_bind is not None:
                res["opCode"]    = CONF_CODE["bind_user_already"][0]
                res["opMessage"] = CONF_CODE["bind_user_already"][1]
            else:
                self.session_auth.add(TableGrantStrategyRelated(strategyId, userUin, 0))
        else:
            if obj_bind is None:
                res["opCode"]    = CONF_CODE["bind_user_not"][0]
                res["opMessage"] = CONF_CODE["bind_user_not"][1]
            else:
                self.session_auth.delete(obj_bind)

        return res

    def handler(self):
        session_mark = False

        try:
            self.session_auth = DB_SESSION_AUTH

            if self.verify():
                self.res["data"]["batchRes"] = []
                
                for item in self.para["bindList"]:
                    self.res["data"]["batchRes"].append(self.bind(item["strategyId"], item["userUin"]))

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


class BindGroupStrategyController(BaseController):
    def __init__(self, para, res, logger):
        super(BindGroupStrategyController, self).__init__(para, res, logger)

    def verify(self):
        if "ownerUin" not in self.para:
            fill_error_code(self.res, "para_miss", "miss parameter(ownerUin)")
            return False

        self.para["ownerUin"] = int(self.para["ownerUin"])

        if self.session_auth.query(TableGrantUser).filter(TableGrantUser.userUin == self.para["ownerUin"]).first() is None:
            fill_error_code(self.res, "invalid_owner_uin")
            return False

        if "bindMode" not in self.para:
            fill_error_code(self.res, "para_miss", "miss parameter(bindMode)")
            return False

        self.para["bindMode"] = int(self.para["bindMode"])

        if self.para["bindMode"] != MODE_STRATEGY_BIND and self.para["bindMode"] != MODE_STRATEGY_UNBIND:
            fill_error_code(self.res, "mode_related_bind")
            return False

        self.para["bindList"] = list(self.para["bindList"])

        n = len(self.para["bindList"])
        i = 0
        while i < n:
            self.para["bindList"][i]["strategyId"] = int(self.para["bindList"][i]["strategyId"])
            self.para["bindList"][i]["groupId"]    = int(self.para["bindList"][i]["groupId"])
            i += 1

        f = lambda x, y : x if y in x else x + [y]
        self.para["bindList"] = reduce(f, [[], ] + self.para["bindList"])

        return True

    def bind(self, strategyId, groupId):
        res = {
            "strategyId" : strategyId,
            "groupId"    : groupId,
            "opCode"     : CONF_CODE["success"][0],
            "opMessage"  : CONF_CODE["success"][1]
        }

        obj_strategy = self.session_auth.query(
            TableGrantStrategyInfo
        ).filter(
            TableGrantStrategyInfo.strategyId == strategyId
        ).first()

        obj_group = self.session_auth.query(
            TableGrantGroupInfo
        ).filter(
            TableGrantGroupInfo.groupId == groupId
        ).first()

        obj_bind = self.session_auth.query(
            TableGrantStrategyRelated
        ).filter(
            TableGrantStrategyRelated.strategyId == strategyId,
            TableGrantStrategyRelated.userUin    == 0,
            TableGrantStrategyRelated.groupId    == groupId
        ).first()

        if obj_strategy is None:
            res["opCode"]    = CONF_CODE["invalid_strategy_id"][0]
            res["opMessage"] = CONF_CODE["invalid_strategy_id"][1]
            return res

        if obj_strategy.ownerUin != self.para["ownerUin"]:
            res["opCode"]    = CONF_CODE["permission_strategy"][0]
            res["opMessage"] = CONF_CODE["permission_strategy"][1]
            return res

        if obj_group is None:
            res["opCode"]    = CONF_CODE["invalid_group_id"][0]
            res["opMessage"] = CONF_CODE["invalid_group_id"][1]
            return res

        if obj_group.ownerUin != self.para["ownerUin"]:
            res["opCode"]    = CONF_CODE["permission_group"][0]
            res["opMessage"] = CONF_CODE["permission_group"][1]
            return res

        if self.para["bindMode"] == MODE_STRATEGY_BIND:
            if obj_bind is not None:
                res["opCode"]    = CONF_CODE["bind_group_already"][0]
                res["opMessage"] = CONF_CODE["bind_group_already"][1]
            else:
                self.session_auth.add(TableGrantStrategyRelated(strategyId, 0, groupId))
        else:
            if obj_bind is None:
                res["opCode"]    = CONF_CODE["bind_group_not"][0]
                res["opMessage"] = CONF_CODE["bind_group_not"][1]
            else:
                self.session_auth.delete(obj_bind)

        return res

    def handler(self):
        session_mark = False

        try:
            self.session_auth = DB_SESSION_AUTH

            if self.verify():
                self.res["data"]["batchRes"] = []
                
                for item in self.para["bindList"]:
                    self.res["data"]["batchRes"].append(self.bind(item["strategyId"], item["groupId"]))

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
