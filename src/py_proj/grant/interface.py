# -*- coding: utf-8 -*-

import json
import flask
import traceback

from grant.conf.conf_base     import CONF_LOG
from grant.conf.conf_code     import CONF_CODE
from grant.conf.conf_method   import CONF_METHOD
from grant.common.global_tool import *

from grant.controller.base                  import BaseController
from grant.controller.get_condition_op_list import ConditionOpListController
from grant.controller.create_strategy       import CreateStrategyController
from grant.controller.update_strategy       import UpdateStrategyController
from grant.controller.delete_strategy       import DeleteStrategyController
from grant.controller.detail_strategy       import DetailStrategyController
from grant.controller.bind_strategy         import BindUserStrategyController
from grant.controller.bind_strategy         import BindGroupStrategyController
from grant.controller.related_strategy      import StrategyRelatedController
from grant.controller.list_strategy         import ListStrategyController

def process_grant_request():
    # 1. get request parameters
    para_str  = flask.request.get_data()
    para_dict = json.loads(para_str)

    # 2. init respond struct
    res = {
        "version"       : para_dict.get("version"      , "1.0"),
        "componentName" : para_dict.get("componentName", "yapi.grant"),
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
        logger.debug("-------------------- process --------------------")
        logger.debug("request : %s" % (para_str))
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
            logger.debug("respond : %s" % (res))

    # 6. return
    return res
