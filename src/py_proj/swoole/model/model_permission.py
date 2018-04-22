# -*- coding: utf-8 -*-

ACCESS_DEFAULT        = 0 # 未明确表态
ACCESS_EXTRACT_REFUSE = 1 # 精确拒绝
ACCESS_EXTRACT_ALLOW  = 2 # 精确允许
ACCESS_FUZZY_REFUSE   = 3 # 模糊拒绝
ACCESS_FUZZY_ALLOW    = 4 # 模糊允许


def _compareResource(require_resource_str, input_resource_str, logger):
    if require_resource_str == "*":
        return True

    require_resource_words = require_resource_str.split(":")
    input_resource_words   = input_resource_str.split(":")

    if len(require_resource_words) != len(input_resource_words):
        return False

    n = len(require_resource_words)
    i = 0
    while i < n:
        require_word = require_resource_words[i]
        input_word   = input_resource_words[i]

        if require_word.find("/") == -1:
            if require_word != input_word:
                return False
        elif input_word.find("/") == -1:
            return False
        else:
            require_k = require_word.split("/")[0]
            require_v = require_word.split("/")[1]
            input_k = input_word.split("/")[0]
            input_v = input_word.split("/")[1]

            if require_k != input_k or (require_v != "*" and require_v != input_v):
                return False

        i += 1

    return True


def _compareCondition(cond_type, require_v, input_v, logger):
    if cond_type == "oneIn":
        if not isinstance(require_v, list):
            require_v = [require_v]

        if not isinstance(input_v, list):
            input_v = [input_v]

        for one_v in input_v:
            if one_v in require_v:
                return True

        return False

    if cond_type == "allIn":
        if not isinstance(require_v, list):
            require_v = [require_v]

        if not isinstance(input_v, list):
            input_v = [input_v]

        for one_v in input_v:
            if one_v not in require_v:
                return False

        return True

    if cond_type == "gt":
        return input_v > require_v

    if cond_type == "ge":
        return input_v >= require_v

    if cond_type == "lt":
        return input_v < require_v

    if cond_type == "le":
        return input_v <= require_v

    if cond_type == "eq":
        return input_v == require_v

    if cond_type == "neq":
        return input_v != require_v

    return False


def _judgeResource(db_resource, resource, logger):
    """ 单条策略中的 资源要求 是否满足 """
    if "*" in db_resource:
        return True

    if len(resource) == 0:
        return False

    for resource_str in resource:
        mark = False

        for db_resource_str in db_resource:
            if _compareResource(db_resource_str, resource_str, logger):
                mark = True
                break

        if not mark:
            return False

    return True


def _judgeCondition(db_condition, condition, logger):
    """ 单条策略中的 条件要求 是否满足 """
    if "*" in db_condition:
        return True

    db_key_set = set()
    in_key_set = set()

    for item in db_condition:
        db_key_set.add(item["condKey"])

    for item in condition:
        in_key_set.add(item["condKey"])

    if len(db_key_set - in_key_set) != 0:
        return False

    for input_cond in condition:
        for require_cond in db_condition:
            if input_cond["condKey"] == require_cond["condKey"] and not _compareCondition(require_cond["condType"], require_cond["condValue"], input_cond["condValue"], logger):
                return False
    return True


def _matchOneStrategy(rule, module, action, resource, condition, logger):
    """ 计算单条策略的效果 """
    db_effect    = rule["effect"]
    db_module    = rule["module"]
    db_action    = rule["action"]
    db_resource  = rule["resource"]
    db_condition = rule["condition"]

    # 1. 校验接口级别
    if (db_module == "*" or db_module == module) and (db_action == "*" or db_action == action):
        if db_module == module and db_action == action:
            if db_effect == "deny":
                res = ACCESS_EXTRACT_REFUSE
            else:
                res = ACCESS_EXTRACT_ALLOW
        else:
            if db_effect == "deny":
                res = ACCESS_FUZZY_REFUSE
            else:
                res = ACCESS_FUZZY_ALLOW
    else:
        return ACCESS_DEFAULT

    # 2. 校验资源级别
    if not _judgeResource(db_resource, resource, logger):
        return ACCESS_DEFAULT

    # 3. 校验条件级别
    if not _judgeCondition(db_condition, condition, logger):
        return ACCESS_DEFAULT

    return res


def matchStrategys(strategyRules, module, action, resource, condition, logger):
    """ 根据某用户关联的所有策略，综合判断权限 """
    r1 = False
    r2 = False
    r3 = False
    r4 = False

    for rule in strategyRules:
        tmpRes = _matchOneStrategy(rule, module, action, resource, condition, logger)

        if tmpRes == ACCESS_EXTRACT_REFUSE:
            r1 = True
        elif tmpRes == ACCESS_EXTRACT_ALLOW:
            r2 = True
        elif tmpRes == ACCESS_FUZZY_REFUSE:
            r3 = True
        elif tmpRes == ACCESS_FUZZY_ALLOW:
            r4 = True

    return not r1 and (r2 or (not r3 and r4))
