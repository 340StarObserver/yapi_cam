# -*- coding: utf-8 -*-

# ----------------------------------------
# About log

CONF_LOG = {
    "path"     : "/data/release/log/yapi/grant/",
    "when"     : "D",
    "interval" : 1,
    "backup"   : 3,
    "encode"   : "utf-8",
    "switch"   : True
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
    "recycle" : 3600,
    "size"    : 5
}

# ----------------------------------------
# About supported op in strategy rule

CONF_CONDITION_OP = {
    "oneIn" : u"至少存在一个属于",
    "allIn" : u"全部属于",
    "gt"    : u"大于",
    "ge"    : u"大于等于",
    "lt"    : u"小于",
    "le"    : u"小于等于",
    "eq"    : u"等于",
    "neq"   : u"不等于"
}

# ----------------------------------------
# About constant mode

MODE_STRATEGY_TYPE_COMMON  = 0
MODE_STRATEGY_TYPE_OWNER   = 1
MODE_STRATEGY_TYPE_SUB     = 2

MODE_RELATED_USER_WITHOUT  = 0
MODE_RELATED_USER_WITH     = 1

MODE_RELATED_GROUP_WITHOUT = 0
MODE_RELATED_GROUP_WITH    = 1

MODE_STRATEGY_BIND         = 1
MODE_STRATEGY_UNBIND       = 2
