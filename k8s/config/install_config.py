# -*- coding: utf-8 -*-

import sys
import logging
import subprocess

logfile = "config_install.log"

cm_arr = [
    ("yapi.cm.supervisord", "yapi.cm.supervisord/"),
    ("yapi.cm.server"     , "yapi.cm.server/"     )
]

namespace = "yapi"

is_delete_existed = True


def run_shell(cmd):
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE, shell = True, stderr = subprocess.STDOUT)
    logger.debug("running : %s" % cmd)
    out, err = p.communicate()
    return p.returncode, out


def getlogger(name):
    logger = logging.getLogger(name)
    if len(logger.handlers) == 0:
        logger.setLevel(logging.DEBUG)
        path_file_name = sys.path[0] + "/" + logfile
        fh = logging.FileHandler(path_file_name, encoding = "utf-8")
        formatter = logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        if name != "file":
            console = logging.StreamHandler()
            console.setLevel(logging.DEBUG)
            formatter = logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s")
            console.setFormatter(formatter)
            logger.addHandler(console)
    return logger


logger = getlogger("default")
file_logger = getlogger("file")


def check_if_existed(cm_name, namespace):
    (status, output) = run_shell("kubectl get cm " + cm_name + " -n " + namespace)
    result = (status, output)
    return result


def create_cm(cm_name, folder, namespace):
    folder = sys.path[0] + "/" + folder
    (status, output) = run_shell("kubectl create cm " + cm_name + " --from-file=" + folder + " -n " + namespace)
    result = (status, output)
    return result


def delete_cm(cm_name, namespace):
    (status, output) = run_shell("kubectl delete cm " + cm_name + " -n " + namespace)
    result = (status, output)
    return result


def get_cm(cm_name, namespace):
    (status, output) = run_shell("kubectl get cm " + cm_name + " -n " + namespace + " -o yaml")
    result = (status, output)
    return result


def main():
    succ_num = 0
    for cm in cm_arr:
        is_exist = check_if_existed(cm[0], namespace)
        if is_exist[0] == 0:
            if not is_delete_existed:
                logger.info("cm %s existed.pass..." % (cm[0]))
                continue
            g_ret = get_cm(cm[0], namespace)
            if g_ret[0] == 0:
                file_logger.info("get cm %s namespace %s before delete,yaml:\n%s" % (cm[0], namespace, g_ret[1]))
            else:
                logger.error("get cm for backup error!exit!")
                exit(1)
            d_ret = delete_cm(cm[0], namespace)
            if d_ret[0] != 0:
                logger.error("delete cm %s error.status:%s,output:%s" % (cm[0], d_ret[0], d_ret[1]))
                exit(1)
            else:
                logger.info("delete cm success.")
        c_ret = create_cm(cm[0], cm[1], namespace)
        if c_ret[0] != 0:
            logger.error("create cm %s error.status:%s,output:%s" % (cm[0], c_ret[0], c_ret[1]))
            exit(1)
        else:
            logger.info("create cm %s success" % (cm[0]))
            succ_num += 1
    if succ_num == len(cm_arr):
        logger.info("install config done.all success.....")
    else:
        logger.error("install config done.there is %d cm failed !!!!!!!" % (succ_num))
        exit(1)


if __name__ == "__main__":
    main()
