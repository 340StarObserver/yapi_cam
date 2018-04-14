# -*- coding: utf-8 -*-

from grant.conf.conf_base  import CONF_CONDITION_OP
from grant.controller.base import BaseController

class ConditionOpListController(BaseController):
    def __init__(self, para, res, logger):
        super(ConditionOpListController, self).__init__(para, res, logger)

    def handler(self):
        self.res["data"]["opList"] = []

        for k in CONF_CONDITION_OP:
            self.res["data"]["opList"].append({
                "opType" : k,
                "opName" : CONF_CONDITION_OP[k]
            })
