# -*- coding: utf-8 -*-

from grant.conf.conf_base     import MODE_STRATEGY_TYPE_COMMON
from grant.conf.conf_base     import MODE_STRATEGY_TYPE_OWNER
from grant.conf.conf_base     import MODE_STRATEGY_TYPE_SUB
from grant.conf.conf_base     import CONF_CONDITION_OP
from grant.conf.conf_code     import CONF_CODE
from grant.common.global_tool import fill_error_code
from grant.common.global_tool import deal_post_str


def valid_strategy_info(para, res, logger):
    for k in ["strategyType", "strategyName", "strategyRemark", "strategyRule"]:
        if k not in para:
            fill_error_code(res, "para_miss", "miss parameter(%s)" % (k))
            return False

    para["strategyType"]   = int(para["strategyType"])
    para["strategyName"]   = deal_post_str(para["strategyName"])
    para["strategyRemark"] = deal_post_str(para["strategyRemark"])

    if para["strategyType"] != MODE_STRATEGY_TYPE_COMMON and para["strategyType"] != MODE_STRATEGY_TYPE_OWNER and para["strategyType"] != MODE_STRATEGY_TYPE_SUB:
        fill_error_code(res, "mode_strategy_type")
        return False

    if len(para["strategyName"]) == 0:
        fill_error_code(res, "empty_strategy_name")
        return False

    if not valid_strategy_rule(para["strategyRule"], logger):
        fill_error_code(res, "invalid_strategy_rule")
        return False

    return True


def valid_strategy_rule(strategyRule, logger):
    if not isinstance(strategyRule, list):
        return False

    for item in strategyRule:
        if "effect" not in item:
            return False

        if "action" not in item:
            return False

        if "resource" not in item:
            return False

        if "condition" not in item:
            return False

        if item["effect"] != "allow" and item["effect"] != "deny":
            return False

        if not isinstance(item["action"], list):
            return False

        for one_action in item["action"]:
            if len(one_action.split(":")) != 2:
                return False

        if not isinstance(item["resource"], list):
            return False

        if not isinstance(item["condition"], list):
            return False

        for one_condition in item["condition"]:
            if one_condition != "*":
                if not isinstance(one_condition, dict):
                    return False

                if "condKey" not in one_condition:
                    return False

                if "condType" not in one_condition:
                    return False

                if "condValue" not in one_condition:
                    return False

                if one_condition["condType"] not in CONF_CONDITION_OP:
                    return False

    return True
