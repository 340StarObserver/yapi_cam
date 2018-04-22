# -*- coding: utf-8 -*-

import json
import flask
import traceback

from swoole.conf.config        import CONF_LOG
from swoole.conf.config        import CONF_CODE
from swoole.conf.config        import CONF_METHOD
from swoole.common.global_tool import *

from swoole.controller.base    import BaseController
from swoole.controller.auth    import AuthController

def process_swoole_request():
    # 1. get request parameters
    para_str  = flask.request.get_data()
    para_dict = json.loads(para_str)

    # 2. init respond struct
    res = {
        "version"       : para_dict.get("version"      , "1.0"),
        "componentName" : para_dict.get("componentName", "yapi.swoole"),
        "eventId"       : para_dict.get("eventId"      , create_eventid()),
        "timestamp"     : para_dict.get("timestamp"    , create_timestamp()),
        "returnCode"    : CONF_CODE["success"][0],
        "returnMessage" : CONF_CODE["success"][1],
        "data"          : {}
    }

    # 3. if interfaceName invalid
    if "interface" not in para_dict or "interfaceName" not in para_dict["interface"] or para_dict["interface"]["interfaceName"] not in CONF_METHOD:
        fill_error_code(res, "invalid_method")
        return json.dumps(res).encode("utf-8")

    # 4. get logger
    if CONF_LOG["switch"]:
        logger = get_logger(para_dict["interface"]["interfaceName"])
    else:
        logger = None

    # 5. work
    try:
        eval(CONF_METHOD[para_dict["interface"]["interfaceName"]])(
            para   = para_dict.get("interface", {}).get("para", {}),
            res    = res,
            logger = logger
        ).handler()

    except KeyError, e:
        fill_error_code(res, "para_error", traceback.format_exc())
    except ValueError, e:
        fill_error_code(res, "para_error", traceback.format_exc())
    except NameError, e:
        fill_error_code(res, "invalid_method", traceback.format_exc())
    except Exception, e:
        fill_error_code(res, "unknown", traceback.format_exc())
    finally:
        res = json.dumps(res).encode("utf-8")

        if logger:
            logger.debug("[%s][%s]" % (para_str, res))

    # 6. return
    return res
