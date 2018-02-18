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
