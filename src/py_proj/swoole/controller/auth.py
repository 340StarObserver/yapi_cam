# -*- coding: utf-8 -*-

import time
import traceback

from swoole.conf.config            import CONF_CONSTANT
from swoole.controller.base        import BaseController

from swoole.common.global_tool     import deal_post_str
from swoole.common.global_tool     import fill_error_code

from swoole.model.model_sql        import querySecret
from swoole.model.model_sql        import queryStrategys
from swoole.model.model_signature  import calcSignature
from swoole.model.model_permission import matchStrategys


class AuthController(BaseController):
    def __init__(self, para, res, logger):
        super(AuthController, self).__init__(para, res, logger)

    def verifyInput(self):
        for k in ["header", "content"]:
            if k not in self.para:
                fill_error_code(self.res, "para_miss", "miss parameter(%s)" % (k))
                return False

        for k in ["mode", "resource", "condition", "keyList"]:
            if k not in self.para["header"]:
                fill_error_code(self.res, "para_miss", "miss parameter(%s)" % (k))
                return False

        for k in ["module", "action", "reqTime", "reqNonce", "reqRegion", "secretId", "signature", "params"]:
            if k not in self.para["content"]:
                fill_error_code(self.res, "para_miss", "miss parameter(%s)" % (k))
                return False

        if not isinstance(self.para["header"]["resource"], list):
            fill_error_code(self.res, "invalid_resource")
            return False

        if not isinstance(self.para["header"]["condition"], list):
            fill_error_code(self.res, "invalid_condition")
            return False

        self.para["header"]["mode"] = int(self.para["header"]["mode"])
        self.para["header"]["resource"]   = list(self.para["header"]["resource"])
        self.para["header"]["condition"]  = list(self.para["header"]["condition"])
        self.para["header"]["keyList"]    = list(self.para["header"]["keyList"])

        self.para["content"]["reqTime"]   = int(self.para["content"]["reqTime"])
        self.para["content"]["reqNonce"]  = int(self.para["content"]["reqNonce"])
        self.para["content"]["params"]    = dict(self.para["content"]["params"])
        self.para["content"]["module"]    = deal_post_str(self.para["content"]["module"])
        self.para["content"]["action"]    = deal_post_str(self.para["content"]["action"])
        self.para["content"]["reqRegion"] = deal_post_str(self.para["content"]["reqRegion"])
        self.para["content"]["secretId"]  = deal_post_str(self.para["content"]["secretId"])
        self.para["content"]["signature"] = deal_post_str(self.para["content"]["signature"])

        if len(self.para["header"]["keyList"]) == 0:
            fill_error_code(self.res, "para_empty", "empty keyList")
            return False

        if len(self.para["content"]["module"]) == 0:
            fill_error_code(self.res, "para_empty", "empty module")
            return False

        if len(self.para["content"]["action"]) == 0:
            fill_error_code(self.res, "para_empty", "empty action")
            return False

        if len(self.para["content"]["reqRegion"]) == 0:
            fill_error_code(self.res, "para_empty", "empty reqRegion")
            return False

        if len(self.para["content"]["secretId"]) == 0:
            fill_error_code(self.res, "para_empty", "empty secretId")
            return False

        if len(self.para["content"]["signature"]) == 0:
            fill_error_code(self.res, "para_empty", "empty signature")
            return False

        return True


    def needCheckExpired(self):
        return 1 - ((self.para["header"]["mode"] & 4) >> 2)

    def needCheckSignature(self):
        return 1 - ((self.para["header"]["mode"] & 2) >> 1)

    def needCheckPermission(self):
        return 1 - (self.para["header"]["mode"] & 1)


    def identify(self):
        """ 获取身份 """
        secret = querySecret(self.para["content"]["secretId"])

        if secret is None:
            fill_error_code(self.res, "invalid_secretId")
            return False

        self.secretKey = secret["secretKey"]

        self.res["data"]["userUin"]  = secret["userUin"]
        self.res["data"]["ownerUin"] = secret["ownerUin"]
        self.res["data"]["appId"]    = secret["appId"]

        return True


    def checkExpired(self):
        """ 校验时间窗口 """
        time_req = self.para["content"]["reqTime"]
        time_now = int(time.time())

        if abs(time_req - time_now) > CONF_CONSTANT["timeWindow"]:
            fill_error_code(self.res, "signature_expired")
            return False

        return True


    def checkSignature(self):
        """ 校验数据签名 """
        sig = calcSignature(
            content   = self.para["content"],
            keyList   = self.para["header"]["keyList"],
            secretKey = self.secretKey
        )

        if sig != self.para["content"]["signature"]:
            fill_error_code(self.res, "signature_wrong")
            return False

        return True


    def checkPermission(self):
        """ 校验策略权限 """
        strategyRules = queryStrategys(
            userUin   = self.res["data"]["userUin"],
            ownerUin  = self.res["data"]["ownerUin"]
        )

        access = matchStrategys(
            strategyRules = strategyRules,
            module    = self.para["content"]["module"],
            action    = self.para["content"]["action"],
            resource  = self.para["header"]["resource"],
            condition = self.para["header"]["condition"],
            logger    = self.logger
        )

        if not access:
            fill_error_code(self.res, "access_denied")
            return False

        return True


    def handler(self):
        if not self.verifyInput():
            return

        if not self.identify():
            return

        if self.needCheckExpired() and not self.checkExpired():
            return

        if self.needCheckSignature() and not self.checkSignature():
            return

        if self.needCheckPermission() and not self.checkPermission():
            return
