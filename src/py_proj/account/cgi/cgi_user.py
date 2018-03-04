# -*- coding: utf-8 -*-

import sys
import datetime
import traceback

from sqlalchemy import or_

from account.conf   import conf_code
from account.common import global_db
from account.common import global_tool

from account.model.model_user import TableAccountUser
from account.model.model_user import TableAccountAppId


def cgi_getUserDetail(para, res):
    # 1. prepare a logger
    logger = global_tool.get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    userUinList = para.get("userUinList", [])

    if not isinstance(userUinList, list):
        userUinList = [userUinList]

    n = len(userUinList)
    i = 0
    while i < n:
        userUinList[i] = int(userUinList[i])
        i += 1

    # 3. logic work
    session_mark = False
    try:
        session_auth = global_db.DB_SESSION_AUTH
        session_mark = True

        obj_user_list = session_auth.query(
            TableAccountUser, TableAccountAppId
        ).join(
            TableAccountAppId, TableAccountUser.ownerUin == TableAccountAppId.ownerUin
        ).filter(
            TableAccountUser.userUin.in_(tuple(userUinList))
        ).all()

        for obj_user in obj_user_list:
            res["data"][str(obj_user[0].userUin)] = dict(obj_user[0].to_json(), **obj_user[1].to_json())

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


def cgi_getSubAccountList(para, res):
    # 1. prepare a logger
    logger = global_tool.get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    if "ownerUin" not in para:
        res["returnCode"]    = conf_code.CONF_CODE["para_miss"][0]
        res["returnMessage"] = "miss parameter(ownerUin)"
        return

    ownerUin = int(para["ownerUin"])
    pageId   = int(para.get("pageId"  , 1 ))
    pageSize = int(para.get("pageSize", 10))
    keyword  = global_tool.deal_post_str(para.get("keyword", ""))

    # 3. logic work
    session_mark = False
    try:
        session_auth = global_db.DB_SESSION_AUTH
        session_mark = True

        if session_auth.query(TableAccountUser).filter(TableAccountUser.userUin == ownerUin).first() is None:
            res["returnCode"]    = conf_code.CONF_CODE["invalid_owner_uin"][0]
            res["returnMessage"] = conf_code.CONF_CODE["invalid_owner_uin"][1]
        else:
            # create a sql
            sql = session_auth.query(
                TableAccountUser, TableAccountAppId
            ).join(
                TableAccountAppId, TableAccountUser.ownerUin == TableAccountAppId.ownerUin
            ).filter(
                TableAccountUser.ownerUin == ownerUin,
                TableAccountUser.userUin  != ownerUin
            )

            # add condition : keyword
            if len(keyword) != 0:
                sql = sql.filter(or_(
                    TableAccountUser.userName.like(  "%" + keyword + "%"),
                    TableAccountUser.userRemark.like("%" + keyword + "%")
                ))

            # get total number
            res["data"]["totalNum"] = sql.count()

            # page query
            obj_user_list = sql.limit(pageSize).offset((pageId - 1) * pageSize).all()

            res["data"]["userList"] = []
            for obj_user in obj_user_list:
                res["data"]["userList"].append(dict(obj_user[0].to_json(), **obj_user[1].to_json()))

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
