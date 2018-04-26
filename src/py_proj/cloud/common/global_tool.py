# -*- coding: utf-8 -*-

import json
import time
import uuid
import flask
import random
import urllib2
import hashlib

import logging
from   logging.handlers import TimedRotatingFileHandler

from cloud.conf.config import CONF_LOG
from cloud.conf.config import CONF_CODE


def fill_error_code(res, error_key, error_msg = None):
    res["code"] = CONF_CODE[error_key][0]

    if error_msg is None:
        res["codeDesc"] = CONF_CODE[error_key][1]
    else:
        res["codeDesc"] = "cloud : " + error_msg

    res["message"] = res["codeDesc"]


def deal_post_str(para):
    if para is not None:
        return unicode(para).strip(" ").encode("utf-8")
    return ""


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


def get_client_ip():
    default_ip = "127.0.0.1"
    client_ip  = default_ip

    try:
        client_ip = flask.request.remote_addr
    except:
        pass

    if client_ip == default_ip:
        try:
            client_ip = flask.request.headers.get("X-Forwarded-For", default_ip).split(",")[0]
        except:
            pass

    return client_ip


def create_request_id(post_data_str):
    seed_str = "0123456789&()abcdefghijklmnopqrstuvwxyz+-_.[]ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    seed_len = len(seed_str)
    
    random_str = ""
    i = 0
    while i < 64:
        random_str += seed_str[random.randint(0, seed_len - 1)]
        i += 1

    base_str = "%s_%s_%s" % (str(post_data_str), str(uuid.uuid1()), random_str)
    return hashlib.sha512(base_str).hexdigest()


def call_service(url, data, logger):
    data = json.dumps(data).encode("utf-8")

    if logger:
        logger.debug("call url : %s" % (url))
        logger.debug("call req : %s" % (data))

    req = urllib2.Request(url, data)
    req.add_header("Content-Type"  , "application/json; charset=utf-8")
    req.add_header("Content-Length", len(data))
    res = urllib2.urlopen(req)
    res = res.read()

    if logger:
        logger.debug("call rsp : %s" % (res))

    return json.loads(res)
