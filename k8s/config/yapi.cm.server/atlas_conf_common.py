# -*- coding: utf-8 -*-

# ----------------------------------------
# About log
CONF_LOG = {
    "path"         : "/data/release/log/yapi/atlas/",
    "when"         : "D",
    "interval"     : 1,
    "backup"       : 3,
    "encode"       : "utf-8",
    "save_request" : True,
    "save_respond" : True
}

# ----------------------------------------
# About database
CONF_DB_API = {
    "host"    : "master.mysql",
    "port"    : 3306,
    "user"    : "mysql_user",
    "pass"    : "mysql_passwd",
    "dbname"  : "db_yapi_data",
    "encode"  : "utf8",
    "recycle" : 3600,
    "size"    : 5
}

CONF_DB_LOG = {
    "host"    : "master.mysql",
    "port"    : 3306,
    "user"    : "mysql_user",
    "pass"    : "mysql_passwd",
    "dbname"  : "db_yapi_log",
    "encode"  : "utf8",
    "recycle" : 3600,
    "size"    : 5
}

# ----------------------------------------
# About call other services
CONF_URL = {
    "getUserDetail" : "http://account.yapi/account/interface"
}
