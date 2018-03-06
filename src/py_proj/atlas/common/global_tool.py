# -*- coding: utf-8 -*-

""" 工具函数 """

import time
import random
import logging
from logging.handlers import TimedRotatingFileHandler

from atlas.conf import conf_code
from atlas.conf import conf_common

from atlas.model.model_module import TableAtlasModule
from atlas.model.model_module import TableAtlasModuleManager
from atlas.model.model_module import TableAtlasModuleUrl
from atlas.model.model_module import TableAtlasModuleCode
from atlas.model.model_action import TableAtlasAction

# ----------------------------------------
# fill error code
#
def fill_error_code(res, error_key):
    res["returnCode"]    = conf_code.CONF_CODE[error_key][0]
    res["returnMessage"] = conf_code.CONF_CODE[error_key][1]

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

# ----------------------------------------
# judge whether already exist such a module
#
def judge_exist_module(session_api, module):
    if session_api.query(TableAtlasModule).filter(TableAtlasModule.module == module).first() is None:
        return False
    return True

# ----------------------------------------
# judge whether already exist such a module manager
#
def judge_exist_moduleManager(session_api, module, userUin):
    if session_api.query(TableAtlasModuleManager).filter(TableAtlasModuleManager.module == module, TableAtlasModuleManager.userUin == userUin).first() is None:
        return False
    return True

# ----------------------------------------
# judge whether already exist such a module error code
#
def judge_exist_moduleCode(session_api, module, code):
    if session_api.query(TableAtlasModuleCode).filter(TableAtlasModuleCode.module == module, TableAtlasModuleCode.code == code).first() is None:
        return False
    return True

# ----------------------------------------
# judge whether already exist such a module online address
#
def judge_exist_moduleUrl(session_api, module, urlName):
    if session_api.query(TableAtlasModuleUrl).filter(TableAtlasModuleUrl.module == module, TableAtlasModuleUrl.urlName == urlName).first() is None:
        return False
    return True

# ----------------------------------------
# judge whether already exist such a action
#
def judge_exist_action(session_api, module, action):
    if session_api.query(TableAtlasAction).filter(TableAtlasAction.module == module, TableAtlasAction.action == action).first() is None:
        return False
    return True
