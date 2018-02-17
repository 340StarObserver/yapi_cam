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
            else:
                moduleConfDict["secret"] = False

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
if moduleConfDict.get("secret") == True:
    from secret.interface import process_secret_request
    getServerlogger().info("import secret")
@app.route("/secret/interface", methods = ["POST"])
def deal_secret():
    return process_secret_request()


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8666, debug = True)
