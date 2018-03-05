# -*- coding: utf-8 -*-

""" 工具函数 """

import time
import random
import logging
from logging.handlers import TimedRotatingFileHandler

from atlas.conf import conf_common

# ----------------------------------------
# 处理请求参数中的字符串
#
def deal_post_str(para):
    if para is not None:
        return unicode(para).strip(" ").encode("utf-8")
    return ""

# ----------------------------------------
# 生成毫秒时间戳
#
def create_timestamp():
    return int(round(time.time() * 1000))

# ----------------------------------------
# 生成随机eventId
#
def create_eventid():
    return int('%d%d' % (int(round(time.time() * 1000)), random.randint(10000,99999)))

# ----------------------------------------
# 创建日志句柄
# ----------------------------------------
# @para f_name : 日志文件名( 每个接口有独立的日志文件 )
# ----------------------------------------
#
def get_logger(f_name):
    logger = logging.getLogger(f_name)
    if len(logger.handlers) == 0:
        logger.setLevel(logging.DEBUG)
        fh = TimedRotatingFileHandler(
            filename    = conf_common.CONF_LOG["path"] + f_name + ".log",
            when        = conf_common.CONF_LOG["when"],
            interval    = conf_common.CONF_LOG["interval"],
            encoding    = conf_common.CONF_LOG["encode"],
            backupCount = conf_common.CONF_LOG["backup"]
        )
        fh.setFormatter(logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s"))
        logger.addHandler(fh)
    return logger
