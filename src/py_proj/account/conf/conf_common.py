# -*- coding: utf-8 -*-

# ----------------------------------------
# About log
CONF_LOG = {
    "path"         : "/data/release/log/yapi/account/",
    "when"         : "D",
    "interval"     : 1,
    "backup"       : 3,
    "encode"       : "utf-8",
    "save_request" : True,
    "save_respond" : True
}

# ----------------------------------------
# About database
CONF_DB_AUTH = {
    "host"    : "master.mysql",
    "port"    : 3306,
    "user"    : "mysql_user",
    "pass"    : "mysql_passwd",
    "dbname"  : "db_auth",
    "encode"  : "utf8",
    "recycle" : 3600
}
