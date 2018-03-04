# -*- coding: utf-8 -*-

import sys
import datetime
import traceback

from sqlalchemy import or_

from account.conf   import conf_code
from account.common import global_db
from account.common import global_tool

from account.model.model_user  import TableAccountUser
from account.model.model_user  import TableAccountAppId
from account.model.model_group import TableAccountGroupInfo
from account.model.model_group import TableAccountGroupMember


# --------------------------------------------------
# constant variables

USER_GROUP_BIND   = 1
USER_GROUP_UNBIND = 2


# --------------------------------------------------
# following are some CGIs

def cgi_createUserGroup(para, res):
    # 1. prepare a logger
    logger = global_tool.get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    for key in ["loginUin", "ownerUin", "groupName", "groupRemark"]:
        if key not in para:
            res["returnCode"]    = conf_code.CONF_CODE["para_miss"][0]
            res["returnMessage"] = "miss parameter(%s)" % (key)
            return

    loginUin    = int(para["loginUin"])
    ownerUin    = int(para["ownerUin"])
    groupName   = global_tool.deal_post_str(para["groupName"])
    groupRemark = global_tool.deal_post_str(para["groupRemark"])

    # 3. logic work
    session_mark = False
    try:
        session_auth = global_db.DB_SESSION_AUTH
        session_mark = True

        if session_auth.query(TableAccountUser).filter(TableAccountUser.userUin == ownerUin).first() is None:
            res["returnCode"]    = conf_code.CONF_CODE["invalid_owner_uin"][0]
            res["returnMessage"] = conf_code.CONF_CODE["invalid_owner_uin"][1]
        elif session_auth.query(TableAccountGroupInfo).filter(TableAccountGroupInfo.ownerUin == ownerUin, TableAccountGroupInfo.groupName == groupName).first() is not None:
            res["returnCode"]    = conf_code.CONF_CODE["invalid_group_name"][0]
            res["returnMessage"] = conf_code.CONF_CODE["invalid_group_name"][1]
        else:
            time_now  = datetime.datetime.now()
            obj_group = TableAccountGroupInfo(ownerUin, groupName, groupRemark, time_now, time_now)

            session_auth.add(obj_group)
            session_auth.flush()

            res["data"]["userGroupDetail"] = obj_group.to_json()

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


def cgi_updateUserGroup(para, res):
    # 1. prepare a logger
    logger = global_tool.get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    for key in ["loginUin", "ownerUin", "groupId", "groupName", "groupRemark"]:
        if key not in para:
            res["returnCode"]    = conf_code.CONF_CODE["para_miss"][0]
            res["returnMessage"] = "miss parameter(%s)" % (key)
            return

    loginUin    = int(para["loginUin"])
    ownerUin    = int(para["ownerUin"])
    groupId     = int(para["groupId"])
    groupName   = global_tool.deal_post_str(para["groupName"])
    groupRemark = global_tool.deal_post_str(para["groupRemark"])

    # 3. logic work
    session_mark = False
    try:
        session_auth = global_db.DB_SESSION_AUTH
        session_mark = True

        if session_auth.query(TableAccountUser).filter(TableAccountUser.userUin == ownerUin).first() is None:
            res["returnCode"]    = conf_code.CONF_CODE["invalid_owner_uin"][0]
            res["returnMessage"] = conf_code.CONF_CODE["invalid_owner_uin"][1]
        else:
            obj_group = session_auth.query(TableAccountGroupInfo).filter(TableAccountGroupInfo.groupId == groupId).first()

            if obj_group is None:
                res["returnCode"]    = conf_code.CONF_CODE["invalid_group_id"][0]
                res["returnMessage"] = conf_code.CONF_CODE["invalid_group_id"][1]
            elif session_auth.query(TableAccountGroupInfo).filter(
                    TableAccountGroupInfo.ownerUin  == ownerUin,
                    TableAccountGroupInfo.groupName == groupName,
                    TableAccountGroupInfo.groupId   != groupId
                ).first() is not None:
                res["returnCode"]    = conf_code.CONF_CODE["invalid_group_name"][0]
                res["returnMessage"] = conf_code.CONF_CODE["invalid_group_name"][1]
            else:
                obj_group.groupName   = groupName
                obj_group.groupRemark = groupRemark
                obj_group.modTime     = datetime.datetime.now()

                res["data"]["userGroupDetail"] = obj_group.to_json()

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


def _do_user_group_bind(session_auth, ownerUin, groupId, userUin):
    res = {
        "groupId"   : groupId,
        "userUin"   : userUin,
        "opCode"    : conf_code.CONF_CODE["success"][0],
        "opMessage" : conf_code.CONF_CODE["success"][1]
    }

    obj_group = session_auth.query(TableAccountGroupInfo).filter(TableAccountGroupInfo.groupId == groupId).first()

    if obj_group is None:
        res["opCode"]    = conf_code.CONF_CODE["invalid_group_id"][0]
        res["opMessage"] = conf_code.CONF_CODE["invalid_group_id"][1]
        return res

    if obj_group.ownerUin != ownerUin:
        res["opCode"]    = conf_code.CONF_CODE["owner_not_match_group"][0]
        res["opMessage"] = conf_code.CONF_CODE["owner_not_match_group"][1]
        return res

    obj_user = session_auth.query(TableAccountUser).filter(TableAccountUser.userUin == userUin).first()

    if obj_user is None:
        res["opCode"]    = conf_code.CONF_CODE["invalid_user_uin"][0]
        res["opMessage"] = conf_code.CONF_CODE["invalid_user_uin"][1]
        return res

    if obj_user.ownerUin != ownerUin:
        res["opCode"]    = conf_code.CONF_CODE["owner_not_match_user"][0]
        res["opMessage"] = conf_code.CONF_CODE["owner_not_match_user"][1]
        return res

    if session_auth.query(TableAccountGroupMember).filter(TableAccountGroupMember.groupId == groupId, TableAccountGroupMember.userUin == userUin).first() is not None:
        res["opCode"]    = conf_code.CONF_CODE["user_in_group_already"][0]
        res["opMessage"] = conf_code.CONF_CODE["user_in_group_already"][1]
        return res

    session_auth.add(TableAccountGroupMember(groupId, userUin, datetime.datetime.now()))
    obj_group.groupNum += 1

    return res


def _do_user_group_unbind(session_auth, ownerUin, groupId, userUin):
    res = {
        "groupId"   : groupId,
        "userUin"   : userUin,
        "opCode"    : conf_code.CONF_CODE["success"][0],
        "opMessage" : conf_code.CONF_CODE["success"][1]
    }

    obj_group = session_auth.query(TableAccountGroupInfo).filter(TableAccountGroupInfo.groupId == groupId).first()

    if obj_group is None:
        res["opCode"]    = conf_code.CONF_CODE["invalid_group_id"][0]
        res["opMessage"] = conf_code.CONF_CODE["invalid_group_id"][1]
        return res

    if obj_group.ownerUin != ownerUin:
        res["opCode"]    = conf_code.CONF_CODE["owner_not_match_group"][0]
        res["opMessage"] = conf_code.CONF_CODE["owner_not_match_group"][1]
        return res

    obj_user = session_auth.query(TableAccountUser).filter(TableAccountUser.userUin == userUin).first()

    if obj_user is None:
        res["opCode"]    = conf_code.CONF_CODE["invalid_user_uin"][0]
        res["opMessage"] = conf_code.CONF_CODE["invalid_user_uin"][1]
        return res

    if obj_user.ownerUin != ownerUin:
        res["opCode"]    = conf_code.CONF_CODE["owner_not_match_user"][0]
        res["opMessage"] = conf_code.CONF_CODE["owner_not_match_user"][1]
        return res

    obj = session_auth.query(TableAccountGroupMember).filter(TableAccountGroupMember.groupId == groupId, TableAccountGroupMember.userUin == userUin).first()

    if obj is None:
        res["opCode"]    = conf_code.CONF_CODE["user_in_group_not"][0]
        res["opMessage"] = conf_code.CONF_CODE["user_in_group_not"][1]
    else:
        session_auth.delete(obj)
        obj_group.groupNum -= 1

    return res


def cgi_bindUserGroup(para, res):
    # 1. prepare a logger
    logger = global_tool.get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    for key in ["loginUin", "ownerUin", "opMode", "opList"]:
        if key not in para:
            res["returnCode"]    = conf_code.CONF_CODE["para_miss"][0]
            res["returnMessage"] = "miss parameter(%s)" % (key)
            return

    loginUin = int(para["loginUin"])
    ownerUin = int(para["ownerUin"])
    opMode   = int(para["opMode"])
    
    if opMode != USER_GROUP_BIND and opMode != USER_GROUP_UNBIND:
        res["returnCode"]    = conf_code.CONF_CODE["invalid_bind_mode"][0]
        res["returnMessage"] = conf_code.CONF_CODE["invalid_bind_mode"][1]
        return

    opList = para["opList"]

    if not isinstance(opList, list):
        opList = [opList]

    n = len(opList)
    i = 0
    while i < n:
        opList[i]["groupId"] = int(opList[i]["groupId"])
        opList[i]["userUin"] = int(opList[i]["userUin"])
        i += 1

    # 3. logic work
    session_mark = False
    try:
        session_auth = global_db.DB_SESSION_AUTH
        session_mark = True

        if session_auth.query(TableAccountUser).filter(TableAccountUser.userUin == ownerUin).first() is None:
            res["returnCode"]    = conf_code.CONF_CODE["invalid_owner_uin"][0]
            res["returnMessage"] = conf_code.CONF_CODE["invalid_owner_uin"][1]
        else:
            res["data"]["batchRes"] = []

            for item in opList:
                if opMode == USER_GROUP_BIND:
                    opFunc = _do_user_group_bind
                else:
                    opFunc = _do_user_group_unbind

                res["data"]["batchRes"].append(opFunc(session_auth, ownerUin,
                    item["groupId"],
                    item["userUin"]
                ))

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


def _do_delete_group(session_auth, ownerUin, groupId):
    res = {
        "groupId"   : groupId,
        "opCode"    : conf_code.CONF_CODE["success"][0],
        "opMessage" : conf_code.CONF_CODE["success"][1]
    }

    obj_group = session_auth.query(TableAccountGroupInfo).filter(TableAccountGroupInfo.groupId == groupId).first()

    if obj_group is None:
        res["opCode"]    = conf_code.CONF_CODE["invalid_group_id"][0]
        res["opMessage"] = conf_code.CONF_CODE["invalid_group_id"][1]
        return res

    if obj_group.ownerUin != ownerUin:
        res["opCode"]    = conf_code.CONF_CODE["owner_not_match_group"][0]
        res["opMessage"] = conf_code.CONF_CODE["owner_not_match_group"][1]
        return res

    session_auth.delete(obj_group)
    session_auth.query(TableAccountGroupMember).filter(
        TableAccountGroupMember.groupId == groupId
    ).delete(
        synchronize_session = False
    )

    return res


def cgi_deleteUserGroup(para, res):
    # 1. prepare a logger
    logger = global_tool.get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    for key in ["loginUin", "ownerUin", "groupIdList"]:
        if key not in para:
            res["returnCode"]    = conf_code.CONF_CODE["para_miss"][0]
            res["returnMessage"] = "miss parameter(%s)" % (key)
            return

    loginUin = int(para["loginUin"])
    ownerUin = int(para["ownerUin"])

    groupIdList = para["groupIdList"]

    if not isinstance(groupIdList, list):
        groupIdList = [groupIdList]

    n = len(groupIdList)
    i = 0
    while i < n:
        groupIdList[i] = int(groupIdList[i])
        i += 1

    # 3. logic work
    session_mark = False
    try:
        session_auth = global_db.DB_SESSION_AUTH
        session_mark = True

        if session_auth.query(TableAccountUser).filter(TableAccountUser.userUin == ownerUin).first() is None:
            res["returnCode"]    = conf_code.CONF_CODE["invalid_owner_uin"][0]
            res["returnMessage"] = conf_code.CONF_CODE["invalid_owner_uin"][1]
        else:
            res["data"]["batchRes"] = []

            for groupId in groupIdList:
                res["data"]["batchRes"].append(_do_delete_group(session_auth, ownerUin, groupId))

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


def cgi_getUserGroupList(para, res):
    # 1. prepare a logger
    logger = global_tool.get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    for key in ["loginUin", "ownerUin"]:
        if key not in para:
            res["returnCode"]    = conf_code.CONF_CODE["para_miss"][0]
            res["returnMessage"] = "miss parameter(%s)" % (key)
            return

    loginUin = int(para["loginUin"])
    ownerUin = int(para["ownerUin"])

    # 3. logic work
    session_mark = False
    try:
        session_auth = global_db.DB_SESSION_AUTH
        session_mark = True

        # S1. init a sql
        sql = session_auth.query(TableAccountGroupInfo)

        # S2. add condtion : userUin
        if "userUin" in para:
            sql = sql.join(
                TableAccountGroupMember,
                TableAccountGroupInfo.groupId == TableAccountGroupMember.groupId
            ).filter(
                TableAccountGroupMember.userUin == int(para["userUin"])
            )

        # S3. add condtion : ownerUin
        sql = sql.filter(TableAccountGroupInfo.ownerUin == ownerUin)

        # S4. add condtion : keyword
        if "keyword" in para:
            keyword = global_tool.deal_post_str(para["keyword"])
            if len(keyword) != 0:
                sql = sql.filter(or_(
                    TableAccountGroupInfo.groupName.like(  "%" + keyword + "%"),
                    TableAccountGroupInfo.groupRemark.like("%" + keyword + "%")
                ))

        # S5. get total count
        res["data"]["totalNum"] = sql.count()

        # S6. page query
        if  "pageId"   in para and int(para["pageId"])   > 0 and \
            "pageSize" in para and int(para["pageSize"]) > 0:
            pageId   = int(para["pageId"])
            pageSize = int(para["pageSize"])
            sql = sql.limit(pageSize).offset((pageId - 1) * pageSize)

        group_list = sql.all()

        res["data"]["userGroupList"] = []
        for obj_group in group_list:
            res["data"]["userGroupList"].append(obj_group.to_json())

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


def cgi_getGroupMemberList(para, res):
    # 1. prepare a logger
    logger = global_tool.get_logger(sys._getframe().f_code.co_name)

    # 2. get parameters
    if "groupId" not in para:
        res["returnCode"]    = conf_code.CONF_CODE["para_miss"][0]
        res["returnMessage"] = "miss parameter(groupId)"
        return

    groupId = int(para["groupId"])

    # 3. logic work
    session_mark = False
    try:
        session_auth = global_db.DB_SESSION_AUTH
        session_mark = True

        if session_auth.query(TableAccountGroupInfo).filter(TableAccountGroupInfo.groupId == groupId).first() is None:
            res["returnCode"]    = conf_code.CONF_CODE["invalid_group_id"][0]
            res["returnMessage"] = conf_code.CONF_CODE["invalid_group_id"][1]
        else:
            # S1. init a sql
            sql = session_auth.query(
                TableAccountGroupMember,
                TableAccountUser,
                TableAccountAppId
            ).join(
                TableAccountUser,
                TableAccountGroupMember.userUin == TableAccountUser.userUin
            ).join(
                TableAccountAppId,
                TableAccountUser.ownerUin == TableAccountAppId.ownerUin
            ).filter(
                TableAccountGroupMember.groupId == groupId
            )

            # S2. get total count
            res["data"]["totalNum"] = sql.count()

            # S3. page query
            if  "pageId"   in para and int(para["pageId"])   > 0 and \
                "pageSize" in para and int(para["pageSize"]) > 0:
                pageId   = int(para["pageId"])
                pageSize = int(para["pageSize"])
                sql = sql.limit(pageSize).offset((pageId - 1) * pageSize)

            user_list = sql.all()

            res["data"]["userList"] = []
            for item in user_list:
                res["data"]["userList"].append(dict(item[1].to_json(), **item[2].to_json()))

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
