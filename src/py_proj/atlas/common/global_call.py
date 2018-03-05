# -*- coding: utf-8 -*-

""" 需要调用其他服务, 均在该文件中定义 """

import json
import urllib2

from atlas.conf.conf_common   import CONF_LOG
from atlas.conf.conf_common   import CONF_URL
from atlas.common.global_tool import create_eventid
from atlas.common.global_tool import create_timestamp


# ----------------------------------------
# send common request

def call_service(url, data, logger):
    # 1. encode data
    data = json.dumps(data).encode("utf-8")

    # 2. log request
    if  logger is not None and CONF_LOG["save_request"] is True:
        logger.debug("call service url  : %s" % (url))
        logger.debug("call service data : %s" % (data))

    # 3. send request
    req = urllib2.Request(url, data)
    req.add_header("Content-Type"  , "application/json; charset=utf-8")
    req.add_header("Content-Length", len(data))
    res = urllib2.urlopen(req)

    # 4. log response
    res = res.read()

    if  logger is not None and CONF_LOG["save_respond"] is True:
        logger.debug("call service res  : %s" % (res))

    # 5. return
    return json.loads(res)


# ----------------------------------------
# get user info

def call_service_getUserDetail(userUinList, logger):
    req_url  = CONF_URL["getUserDetail"]
    req_data = {
        "version"       : "1.0",
        "componentName" : "yapi.account",
        "eventId"       : create_eventid(),
        "timestamp"     : create_timestamp(),
        "interface"     : {
            "interfaceName" : "yapi.account.getUserDetail",
            "para"          : {
                "userUinList" : userUinList
            }
        }
    }
    return call_service(req_url, req_data, logger)
