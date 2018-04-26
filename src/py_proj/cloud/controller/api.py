# -*- coding: utf-8 -*-

from cloud.conf.config        import CONF_SWOOLE
from cloud.conf.config        import CONF_SWITCH

from cloud.common.global_tool import fill_error_code
from cloud.common.global_tool import deal_post_str
from cloud.common.global_tool import call_service

from cloud.model.model_sql    import queryActionDetail
from cloud.model.model_sql    import beyondRateLimit
from cloud.model.model_sql    import writeLog
from cloud.model.model_sql    import queryErrorCode
from cloud.model.model_cam    import camRequestData
from cloud.model.model_svr    import svrRequestUrl
from cloud.model.model_svr    import svrRequestData
from cloud.model.model_svr    import svrRespondData
from cloud.model.model_svr    import svrErrorCode


class ApiController(object):
    def __init__(self, para, res, logger):
        self.para   = para
        self.res    = res
        self.logger = logger
        self.audit  = {}

    def verifyInput(self):
        for k in CONF_SWOOLE["sigField"]:
            if k not in self.para:
                fill_error_code(self.res, "para_miss", "miss parameter(%s)" % (k))
                return False

        if "signature" not in self.para:
            fill_error_code(self.res, "para_miss", "miss parameter(signature)")
            return False

        self.para["module"]    = deal_post_str(self.para["module"])
        self.para["action"]    = deal_post_str(self.para["action"])
        self.para["reqRegion"] = deal_post_str(self.para["reqRegion"])
        self.para["secretId"]  = deal_post_str(self.para["secretId"])
        self.para["signature"] = deal_post_str(self.para["signature"])
        self.para["reqTime"]   = int(self.para["reqTime"])
        self.para["reqNonce"]  = int(self.para["reqNonce"])
        self.para["params"]    = dict(self.para["params"])

        if len(self.para["module"]) == 0:
            fill_error_code(self.res, "para_empty", "empty parameter(module)")
            return False

        if len(self.para["action"]) == 0:
            fill_error_code(self.res, "para_empty", "empty parameter(action)")
            return False

        if len(self.para["reqRegion"]) == 0:
            fill_error_code(self.res, "para_empty", "empty parameter(reqRegion)")
            return False

        if len(self.para["secretId"]) == 0:
            fill_error_code(self.res, "para_empty", "empty parameter(secretId)")
            return False

        if len(self.para["signature"]) == 0:
            fill_error_code(self.res, "para_empty", "empty parameter(signature)")
            return False

        return True

    def report(self):
        writeLog(self.para, self.res, self.audit, self.logger)

    def handler(self):
        # 1. 获取接口详情
        action = queryActionDetail(self.para["module"], self.para["action"], self.logger)

        if not action:
            fill_error_code(self.res, "invalid_action")
            return

        # 2. 访问频次控制
        if CONF_SWITCH["rate_analyse"] and beyondRateLimit(self.para["module"], self.para["action"], self.para["reqTime"], self.logger):
            fill_error_code(self.res, "rate_limit")
            return

        # 3. 调用鉴权服务
        self.audit["camUrl"] = CONF_SWOOLE["url"]

        self.audit["camReq"] = camRequestData(
            reqData       = self.para,
            isAuth        = action["isAuth"],
            funcResource  = action["funcResource"],
            funcCondition = action["funcCondition"]
        )

        self.audit["camRsp"] = call_service(
            url    = self.audit["camUrl"],
            data   = self.audit["camReq"],
            logger = self.logger
        )

        self.para["params"]["region"]    = self.para["reqRegion"]
        self.para["params"]["timestamp"] = self.para["reqTime"]
        self.para["params"]["loginUin"]  = self.audit["camRsp"]["data"].get("userUin", None)
        self.para["params"]["ownerUin"]  = self.audit["camRsp"]["data"].get("ownerUin", None)
        self.para["params"]["appId"]     = self.audit["camRsp"]["data"].get("appId", None)

        if self.audit["camRsp"]["returnCode"]:
            self.res["code"]     = self.audit["camRsp"]["returnCode"]
            self.res["codeDesc"] = self.audit["camRsp"]["returnMessage"]
            self.res["message"]  = self.audit["camRsp"]["returnMessage"]
            return

        # 4. 调用后端业务
        self.audit["svrUrl"] = svrRequestUrl(self.para, action["urlType"], action["urlAddress"])
        self.audit["svrReq"] = svrRequestData(self.para, action["funcReq"])
        self.audit["svrRsp"] = call_service(self.audit["svrUrl"], self.audit["svrReq"], self.logger)

        rspData = svrRespondData(self.audit["svrRsp"], action["funcRsp"])

        self.res["code"]     = rspData["code"]
        self.res["codeDesc"] = ""
        self.res["message"]  = rspData["message"]
        self.res["data"]     = rspData["data"]

        if self.res["code"]:
            codeDetail = queryErrorCode(self.para["module"], self.res["code"], self.logger)

            if not codeDetail:
                fill_error_code(self.res, "invalid_code")
                return

            rspData = svrErrorCode(self.res, codeDetail)

            self.res["code"]     = rspData["code"]
            self.res["codeDesc"] = rspData["codeDesc"]
            self.res["message"]  = rspData["message"]
            self.res["data"]     = rspData["data"]
