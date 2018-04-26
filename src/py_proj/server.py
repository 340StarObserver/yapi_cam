# -*- coding: utf-8 -*-

import os
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

par_cwd = sys.path[0] + os.sep
lib_dir = par_cwd + "lib"
sys.path.insert(0, lib_dir)

reload(sys)

import flask
import json
import ConfigParser
import logging
from   logging.handlers import TimedRotatingFileHandler

app  = flask.Flask(__name__)
path = os.path.split(os.path.realpath(__file__))[0] + os.sep
moduleConfDict = {}

# --------------------------------------------------
# 读取各模块的开关配置
#
def initConf():
    try:
        config = ConfigParser.ConfigParser()
        with open(path + "conf" + os.sep + "module_conf.ini", "r") as db_conf_file:
            config.readfp(db_conf_file)

            if config.get("module", "secret") == "true":
                moduleConfDict["secret"] = True

            if config.get("module", "account") == "true":
                moduleConfDict["account"] = True

            if config.get("module", "atlas") == "true":
                moduleConfDict["atlas"] = True

            if config.get("module", "grant") == "true":
                moduleConfDict["grant"] = True

            if config.get("module", "swoole") == "true":
                moduleConfDict["swoole"] = True

            if config.get("module", "cloud") == "true":
                moduleConfDict["cloud"] = True

    except IOError, e:
        getServerlogger().exception("read module conf error")
        exit(1)
    except Exception, e:
        getServerlogger().exception("init module conf error")
        exit(1)

# --------------------------------------------------
# 日志 : 引入各模块是否成功
#
def getServerlogger():
    logger = logging.getLogger("server_init")
    if len(logger.handlers) == 0:
        logger.setLevel(logging.DEBUG)
        logPath = os.path.split(os.path.realpath(__file__))[0] + os.sep
        path_file_name = logPath + "server_init" + ".log"
        fh = TimedRotatingFileHandler(path_file_name, when = "D", interval = 1, backupCount = 3, encoding = "utf-8")
        formatter = logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger

# --------------------------------------------------
# 运行
getServerlogger().info("start server.......")
initConf()

# --------------------------------------------------
# 模块 : 密钥
if moduleConfDict.get("secret", False) == True:
    from secret.interface import process_secret_request
    getServerlogger().info("import secret")

@app.route("/secret/interface", methods = ["POST"])
def deal_secret():
    return process_secret_request()

# --------------------------------------------------
# 模块 : 账号
if moduleConfDict.get("account", False) == True:
    from account.interface import process_account_request
    getServerlogger().info("import account")

@app.route("/account/interface", methods = ["POST"])
def deal_account():
    return process_account_request()

# --------------------------------------------------
# 模块 : API Manager
if moduleConfDict.get("atlas", False) == True:
    from atlas.interface import process_atlas_request
    getServerlogger().info("import atlas")

@app.route("/atlas/interface", methods = ["POST"])
def deal_atlas():
    return process_atlas_request()

# --------------------------------------------------
# 模块 : 授权
if moduleConfDict.get("grant", False) == True:
    from grant.interface import process_grant_request
    getServerlogger().info("import grant")

@app.route("/grant/interface", methods = ["POST"])
def deal_grant():
    return process_grant_request()

# --------------------------------------------------
# 模块 : 鉴权
if moduleConfDict.get("swoole", False) == True:
    from swoole.interface import process_swoole_request
    getServerlogger().info("import swoole")

@app.route("/swoole/interface", methods = ["POST"])
def deal_swoole():
    return process_swoole_request()

# --------------------------------------------------
# 模块 : 接入
if moduleConfDict.get("cloud", False) == True:
    from cloud.interface import process_cloud_request
    getServerlogger().info("import cloud")

@app.route("/cloud/interface", methods = ["POST"])
def deal_cloud():
    return process_cloud_request()

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8666, debug = False)
