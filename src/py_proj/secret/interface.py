# -*- coding: utf-8 -*-

import json
import flask
import traceback

from secret.conf   import conf_code
from secret.conf   import conf_common
from secret.conf   import conf_method
from secret.common import global_tool

from secret.cgi.cgi_secret import *

def process_secret_request():
    # 1. get request parameters
    para_str  = flask.request.get_data()
    para_dict = json.loads(para_str)

    # 2. get logger
    if "interface" in para_dict and "interfaceName" in para_dict["interface"] and para_dict["interface"]["interfaceName"] in conf_method.CONF_METHOD:
        logger_name = conf_method.CONF_METHOD[para_dict["interface"]["interfaceName"]]
    else:
        logger_name = "error_method"

    logger = global_tool.get_logger(logger_name)
    logger.debug('-------------------- process beg --------------------')

    if conf_common.CONF_LOG["save_request"] is True:
        logger.debug("request : %s" % (para_str))

    # 3. init respond struct
    res = {
        "version"       : para_dict.get("version"      , "1.0"),
        "componentName" : para_dict.get("componentName", "yapi.secret"),
        "eventId"       : para_dict.get("eventId"      , global_tool.create_eventid()),
        "timestamp"     : para_dict.get("timestamp"    , global_tool.create_timestamp()),
        "returnCode"    : conf_code.CONF_CODE["success"][0],
        "returnMessage" : conf_code.CONF_CODE["success"][1],
        "data"          : {}
    }

    # 4. process
    try:
        if logger_name == "error_method":
            res["returnCode"]    = conf_code.CONF_CODE["invalid_method"][0]
            res["returnMessage"] = conf_code.CONF_CODE["invalid_method"][1]
        else:
            eval(logger_name)(
                para = para_dict.get("interface", {}).get("para", {}),
                res  = res
            )

    except KeyError, e:
        res["returnCode"]    = conf_code.CONF_CODE["para_error"][0]
        res["returnMessage"] = traceback.format_exc()
    except ValueError, e:
        res["returnCode"]    = conf_code.CONF_CODE["para_error"][0]
        res["returnMessage"] = traceback.format_exc()
    except NameError, e:
        res["returnCode"]    = conf_code.CONF_CODE["invalid_method"][0]
        res["returnMessage"] = traceback.format_exc()
    except Exception, e:
        res["returnCode"]    = conf_code.CONF_CODE["unknown"][0]
        res["returnMessage"] = traceback.format_exc()
    finally:
        res = json.dumps(res).encode("utf-8")

    # 5. write log
    if conf_common.CONF_LOG["save_respond"] is True:
        logger.debug("respond : %s" % (res))

    logger.debug('-------------------- process end --------------------')
    logger.debug('')

    # 6. return
    return res
