# -*- coding: utf-8 -*-

import json
import flask
import traceback

from cloud.conf.config        import CONF_LOG
from cloud.conf.config        import CONF_CODE

from cloud.common.global_tool import get_logger
from cloud.common.global_tool import deal_post_str
from cloud.common.global_tool import fill_error_code
from cloud.common.global_tool import get_client_ip
from cloud.common.global_tool import create_request_id

from cloud.controller.api     import ApiController

def process_cloud_request():
    # 1. get request parameters
    para_str  = flask.request.get_data()
    para_dict = json.loads(para_str)

    para_dict["reqId"] = create_request_id(para_str)
    para_dict["reqIp"] = get_client_ip()

    # 2. init respond struct
    res = {
        "code"     : CONF_CODE["success"][0],
        "codeDesc" : CONF_CODE["success"][1],
        "message"  : CONF_CODE["success"][1],
        "data"     : {}
    }

    # 3. get logger
    if CONF_LOG["switch"]:
        logger = get_logger("%s.%s" % (
            para_dict.get("module", "error"),
            para_dict.get("action", "error")
        ))

        logger.debug("-------------------- process --------------------")
        logger.debug("cloud req : %s" % (para_str))
    else:
        logger = None

    # 4. work
    try:
        controller = ApiController(para_dict, res, logger)
        
        if  controller.verifyInput():
            controller.handler()
            controller.report()
        
    except KeyError, e:
        fill_error_code(res, "para_error", traceback.format_exc())
    except ValueError, e:
        fill_error_code(res, "para_error", traceback.format_exc())
    except Exception, e:
        fill_error_code(res, "unknown", traceback.format_exc())
    finally:
        res = json.dumps(res).encode("utf-8")
        
        if logger:
            logger.debug("cloud rsp : %s" % (res))

    return res
