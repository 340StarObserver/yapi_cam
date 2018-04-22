# -*- coding: utf-8 -*-

import json
from sqlalchemy import text
from swoole.common.global_db import DB_ENGINE_AUTH

def _executeSql(sql):
    res  = DB_ENGINE_AUTH.execute(text(sql).execution_options(autocommit = True))
    data = []
    for row in res:
        data.append(row)
    return data

def querySecret(secretId):
    """ 获取密钥 """
    sql  = "select t_secret.secretId, t_secret.secretKey, t_secret.userUin, t_user.ownerUin, r_user_app.appId from t_secret, t_user, r_user_app where t_secret.secretId = '%s' and t_secret.status = 0 and t_secret.userUin = t_user.userUin and t_user.ownerUin = r_user_app.ownerUin limit 1" % (secretId)

    data = _executeSql(sql)

    if len(data) == 0:
        return None

    return {
        "secretId"  : data[0][0],
        "secretKey" : data[0][1],
        "userUin"   : data[0][2],
        "ownerUin"  : data[0][3],
        "appId"     : data[0][4]
    }

def queryStrategys(userUin, ownerUin):
    """ 获取某人关联的所有策略 """
    sql  = "select strategyId, strategyRule from t_strategy where strategyId in (select strategyId from r_related_strategy where userUin = %d union all select r_related_strategy.strategyId from r_related_strategy, r_user_group where r_user_group.userUin = %d and r_related_strategy.groupId = r_user_group.groupId) union all select strategyId, strategyRule from t_strategy where ownerUin = %d and strategyType = 1 union all select strategyId, strategyRule from t_strategy where ownerUin = %d and strategyType = 2" % (userUin, userUin, userUin, ownerUin)

    data = _executeSql(sql)

    temp = {}
    for row in data:
        temp[str(row[0])] = json.loads(row[1])

    res = []
    for k in temp:
        for rule in temp[k]:
            for action in rule["action"]:
                res.append({
                    "effect"    : rule["effect"],
                    "module"    : action.split(":")[0],
                    "action"    : action.split(":")[1],
                    "resource"  : rule["resource"],
                    "condition" : rule["condition"]
                })

    return res
