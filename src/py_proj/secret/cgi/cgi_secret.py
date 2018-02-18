# -*- coding: utf-8 -*-

import sys
import uuid
import datetime
import traceback

from secret.conf   import conf_code
from secret.common import global_db
from secret.common import global_tool

from secret.model.model_user   import TableSecretUser
from secret.model.model_secret import TableSecretKey


# --------------------------------------------------
# constant variables

SECRET_SHOW_MODE = 1

SECRET_STATUS_ENABLE    = 0
SECRET_STATUS_DISENABLE = 1
SECRET_STATUS_DELETE    = 2


# --------------------------------------------------
# func to create a random secretKey

def _get_unique_id():
    id_dict = {
        "0": ["0", "g", "G", "W"],
        "1": ["1", "h", "H", "X"],
        "2": ["2", "i", "I", "Y"],
        "3": ["3", "j", "J", "Z"],
        "4": ["4", "k", "K", "4"],
        "5": ["5", "l", "L", "5"],
        "6": ["6", "m", "M", "6"],
        "7": ["7", "n", "N", "7"],
        "8": ["8", "o", "O", "8"],
        "9": ["9", "p", "P", "9"],
        "a": ["a", "q", "A", "Q"],
        "b": ["b", "r", "B", "R"],
        "c": ["c", "s", "C", "S"],
        "d": ["d", "t", "D", "T"],
        "e": ["e", "u", "E", "U"],
        "f": ["f", "v", "F", "V"]
    }

    id_idx = [
        3, 2, 1, 0, 3, 2, 3, 2, 1, 0, 3, 2, 3, 2, 1, 0,
        3, 2, 3, 2, 1, 0, 3, 2, 3, 2, 1, 0, 3, 2, 1, 0
    ]

    new_uuid = str(uuid.uuid1()).replace("-", "")
    new_uuid_ex = []

    i = 0
    while i < 32:
        old_char = new_uuid[i]
        new_char = id_dict[old_char][id_idx[i]]
        new_uuid_ex.append(new_char)
        i += 1

    return "".join(new_uuid_ex)

def _create_secret_id():
    return "AKID" + _get_unique_id()

def _create_secret_key():
    return _get_unique_id()


# --------------------------------------------------
# following are some CGIs

def cgi_createSecret(para, res):
    # 1. prepare a logger
    logger = global_tool.get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    if "userUin" not in para:
        res["returnCode"]    = conf_code.CONF_CODE["para_miss"][0]
        res["returnMessage"] = "miss parameter(userUin)"
        return

    userUin = int(para.get("userUin", 0))
    secretRemark = global_tool.deal_post_str(para.get("secretRemark", None))

    # 3. logic work
    session_mark = False
    try:
        session_auth = global_db.DB_SESSION_AUTH
        session_mark = True

        if session_auth.query(TableSecretUser).filter(TableSecretUser.userUin == userUin).first() is None:
            res["returnCode"]    = conf_code.CONF_CODE["invalid_user_uin"][0]
            res["returnMessage"] = conf_code.CONF_CODE["invalid_user_uin"][1]
        else:
            time_now   = datetime.datetime.now()
            obj_secret = TableSecretKey(
                secretId     = _create_secret_id(),
                secretKey    = _create_secret_key(),
                userUin      = userUin,
                status       = SECRET_STATUS_ENABLE,
                addTime      = time_now,
                modTime      = time_now,
                secretRemark = secretRemark
            )
            session_auth.add(obj_secret)
            res["data"]["secretDetail"] = obj_secret.to_json()

        session_auth.commit()

    except Exception, e:
        if session_mark is True:
            session_auth.rollback()

        traceback_str = traceback.format_exc()
        res["returnCode"]    = conf_code.CONF_CODE["sql_error"][0]
        res["returnMessage"] = traceback_str

        logger.error(traceback_str)

    finally:
        if session_mark is True:
            session_auth.close()


def _modify_secret_status(session_auth, secret_id, op_mode):
    res = {
        "secretId"  : secret_id,
        "opCode"    : conf_code.CONF_CODE["success"][0],
        "opMessage" : conf_code.CONF_CODE["success"][1]
    }

    obj_secret = session_auth.query(TableSecretKey).filter(TableSecretKey.secretId == secret_id).first()

    if obj_secret is None:
        res["opCode"]    = conf_code.CONF_CODE["invalid_secret_id"][0]
        res["opMessage"] = conf_code.CONF_CODE["invalid_secret_id"][1]
        return res

    if   op_mode == SECRET_STATUS_ENABLE:
        if int(obj_secret.status) == SECRET_STATUS_DISENABLE:
            obj_secret.status  = SECRET_STATUS_ENABLE
            obj_secret.modTime = datetime.datetime.now()
        else:
            res["opCode"]    = conf_code.CONF_CODE["invalid_secret_status_enable"][0]
            res["opMessage"] = conf_code.CONF_CODE["invalid_secret_status_enable"][1]
    elif op_mode == SECRET_STATUS_DISENABLE:
        if int(obj_secret.status) == SECRET_STATUS_ENABLE:
            obj_secret.status  = SECRET_STATUS_DISENABLE
            obj_secret.modTime = datetime.datetime.now()
        else:
            res["opCode"]    = conf_code.CONF_CODE["invalid_secret_status_disenable"][0]
            res["opMessage"] = conf_code.CONF_CODE["invalid_secret_status_disenable"][1]
    elif op_mode == SECRET_STATUS_DELETE:
        if int(obj_secret.status) == SECRET_STATUS_DISENABLE:
            obj_secret.status  = SECRET_STATUS_DELETE
            obj_secret.modTime = datetime.datetime.now()
        else:
            res["opCode"]    = conf_code.CONF_CODE["invalid_secret_status_delete"][0]
            res["opMessage"] = conf_code.CONF_CODE["invalid_secret_status_delete"][1]

    return res


def cgi_operateSecret(para, res):
    # 1. prepare a logger
    logger = global_tool.get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    if "opMode" not in para:
        res["returnCode"]    = conf_code.CONF_CODE["para_miss"][0]
        res["returnMessage"] = "miss parameter(opMode)"
        return

    if  int(para["opMode"]) != SECRET_STATUS_ENABLE    and \
        int(para["opMode"]) != SECRET_STATUS_DISENABLE and \
        int(para["opMode"]) != SECRET_STATUS_DELETE:
        res["returnCode"]    = conf_code.CONF_CODE["invalid_op_mode"][0]
        res["returnMessage"] = conf_code.CONF_CODE["invalid_op_mode"][1]
        return

    opMode = int(para.get("opMode", 0))
    secretIds  = para.get("secretIds", [])

    if not isinstance(secretIds, list):
        secretIds = [secretIds]

    n = len(secretIds)
    i = 0
    while i < n:
        secretIds[i] = global_tool.deal_post_str(secretIds[i])
        i += 1

    # 3. logic work
    session_mark = False
    try:
        session_auth = global_db.DB_SESSION_AUTH
        session_mark = True

        res["data"]["batchRes"] = []
        for secret_id in secretIds:
            res["data"]["batchRes"].append(_modify_secret_status(session_auth, secret_id, opMode))

        session_auth.commit()

    except Exception, e:
        if session_mark is True:
            session_auth.rollback()

        traceback_str = traceback.format_exc()
        res["returnCode"]    = conf_code.CONF_CODE["sql_error"][0]
        res["returnMessage"] = traceback_str

        logger.error(traceback_str)

    finally:
        if session_mark is True:
            session_auth.close()


def cgi_remarkSecret(para, res):
    # 1. prepare a logger
    logger = global_tool.get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    if "secretId" not in para:
        res["returnCode"]    = conf_code.CONF_CODE["para_miss"][0]
        res["returnMessage"] = "miss parameter(secretId)"
        return

    if "secretRemark" not in para:
        res["returnCode"]    = conf_code.CONF_CODE["para_miss"][0]
        res["returnMessage"] = "miss parameter(secretRemark)"
        return

    secretId     = global_tool.deal_post_str(para["secretId"])
    secretRemark = global_tool.deal_post_str(para["secretRemark"])

    # 3. logic work
    session_mark = False
    try:
        session_auth = global_db.DB_SESSION_AUTH
        session_mark = True

        obj_secret = session_auth.query(TableSecretKey).filter(TableSecretKey.secretId == secretId).first()

        if obj_secret is None:
            res["returnCode"]    = conf_code.CONF_CODE["invalid_secret_id"][0]
            res["returnMessage"] = conf_code.CONF_CODE["invalid_secret_id"][1]
        else:
            obj_secret.secretRemark = secretRemark
            obj_secret.modTime      = datetime.datetime.now()

        session_auth.commit()

    except Exception, e:
        if session_mark is True:
            session_auth.rollback()

        traceback_str = traceback.format_exc()
        res["returnCode"]    = conf_code.CONF_CODE["sql_error"][0]
        res["returnMessage"] = traceback_str

        logger.error(traceback_str)

    finally:
        if session_mark is True:
            session_auth.close()


def cgi_getSecretList(para, res):
    # 1. prepare a logger
    logger = global_tool.get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    if "userUin" not in para:
        res["returnCode"]    = conf_code.CONF_CODE["para_miss"][0]
        res["returnMessage"] = "miss parameter(userUin)"
        return

    userUin  = int(para.get("userUin" , 0))
    showMode = int(para.get("showMode", 0))

    # 3. logic work
    session_mark = False
    try:
        session_auth = global_db.DB_SESSION_AUTH
        session_mark = True

        secret_list = session_auth.query(TableSecretKey).filter(
            TableSecretKey.userUin == userUin,
            TableSecretKey.status  != SECRET_STATUS_DELETE
        ).all()

        res["data"]["secretList"] = []

        for obj_secret in secret_list:
            json_secret = obj_secret.to_json()
            if showMode != SECRET_SHOW_MODE and "secretKey" in json_secret:
                json_secret.pop("secretKey")
            res["data"]["secretList"].append(json_secret)

        session_auth.commit()

    except Exception, e:
        if session_mark is True:
            session_auth.rollback()

        traceback_str = traceback.format_exc()
        res["returnCode"]    = conf_code.CONF_CODE["sql_error"][0]
        res["returnMessage"] = traceback_str

        logger.error(traceback_str)

    finally:
        if session_mark is True:
            session_auth.close()


def cgi_getSecretKey(para, res):
    # 1. prepare a logger
    logger = global_tool.get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    if "secretId" not in para:
        res["returnCode"]    = conf_code.CONF_CODE["para_miss"][0]
        res["returnMessage"] = "miss parameter(secretId)"
        return

    secretId = global_tool.deal_post_str(para["secretId"])

    # 3. logic work
    session_mark = False
    try:
        session_auth = global_db.DB_SESSION_AUTH
        session_mark = True

        obj_secret = session_auth.query(TableSecretKey).filter(TableSecretKey.secretId == secretId).first()

        if obj_secret is None:
            res["returnCode"]    = conf_code.CONF_CODE["invalid_secret_id"][0]
            res["returnMessage"] = conf_code.CONF_CODE["invalid_secret_id"][1]
        else:
            res["data"]["secretDetail"] = obj_secret.to_json()

        session_auth.commit()

    except Exception, e:
        if session_mark is True:
            session_auth.rollback()

        traceback_str = traceback.format_exc()
        res["returnCode"]    = conf_code.CONF_CODE["sql_error"][0]
        res["returnMessage"] = traceback_str

        logger.error(traceback_str)

    finally:
        if session_mark is True:
            session_auth.close()
