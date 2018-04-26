# -*- coding: utf-8 -*-

from cloud.conf.config import CONF_SWOOLE

def camRequestData(reqData, isAuth, funcResource, funcCondition):
    """ 构造鉴权协议入参 """
    paramDict = reqData["params"]

    camResource  = []
    camCondition = []

    if funcResource:
        exec funcResource

    if funcCondition:
        exec funcCondition

    return {
        "version"       : "1.0",
        "componentName" : "yapi.swoole",
        "eventId"       : reqData["reqNonce"],
        "timestamp"     : reqData["reqTime"],
        "interface"     : {
            "interfaceName" : "yapi.swoole.auth",
            "para"          : {
                "content"   : reqData,
                "header"    : {
                    "mode"      : 1 - isAuth,
                    "resource"  : camResource,
                    "condition" : camCondition,
                    "keyList"   : CONF_SWOOLE["sigField"]
                }
            }
        }
    }
