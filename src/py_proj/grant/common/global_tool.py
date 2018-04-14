# -*- coding: utf-8 -*-

import time
import random
import logging
from   logging.handlers import TimedRotatingFileHandler

from grant.conf.conf_base import CONF_LOG
from grant.conf.conf_code import CONF_CODE

def fill_error_code(res, error_key, error_msg = None):
    res["returnCode"] = CONF_CODE[error_key][0]
    if error_msg is None:
        res["returnMessage"] = CONF_CODE[error_key][1]
    else:
        res["returnMessage"] = error_msg

def deal_post_str(para):
    if para is not None:
        return unicode(para).strip(" ").encode("utf-8")
    return ""

def create_timestamp():
    return int(round(time.time() * 1000))

def create_eventid():
    return int("%d%d" % (int(round(time.time() * 1000)), random.randint(10000,99999)))

def get_logger(f_name):
    logger = logging.getLogger(f_name)
    if len(logger.handlers) == 0:
        logger.setLevel(logging.DEBUG)
        fh = TimedRotatingFileHandler(
            filename    = CONF_LOG["path"] + f_name + ".log",
            when        = CONF_LOG["when"],
            interval    = CONF_LOG["interval"],
            encoding    = CONF_LOG["encode"],
            backupCount = CONF_LOG["backup"]
        )
        fh.setFormatter(logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s"))
        logger.addHandler(fh)
    return logger
