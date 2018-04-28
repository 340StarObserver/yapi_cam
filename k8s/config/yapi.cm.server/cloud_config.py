# -*- coding: utf-8 -*-

CONF_LOG = {
    "path"     : "/data/release/log/yapi/cloud/",
    "when"     : "D",
    "interval" : 1,
    "backup"   : 3,
    "encode"   : "utf-8",
    "switch"   : True
}

CONF_DB_API = {
    "host"     : "master.mysql",
    "port"     : 3306,
    "user"     : "mysql_user",
    "pass"     : "mysql_passwd",
    "dbname"   : "db_yapi_data",
    "encode"   : "utf8",
    "recycle"  : 3600,
    "size"     : 5
}

CONF_DB_LOG = {
    "host"     : "master.mysql",
    "port"     : 3306,
    "user"     : "mysql_user",
    "pass"     : "mysql_passwd",
    "dbname"   : "db_yapi_log",
    "encode"   : "utf8",
    "recycle"  : 3600,
    "size"     : 5
}

CONF_SWITCH = {
    "rate_analyse" : True
}

CONF_SWOOLE = {
    "url"      : "http://swoole.yapi/swoole/interface",
    "sigField" : ["module", "action", "reqTime", "reqNonce", "reqRegion", "secretId", "params"]
}

CONF_CODE = {
    "success"        : ( 0   , "cloud : ok"                   ),
    "unknown"        : ( 3100, "cloud : unknown error"        ),
    "invalid_code"   : ( 3200, "cloud : error code not found" ),
    "para_miss"      : ( 4001, "cloud : miss parameter"       ),
    "para_error"     : ( 4002, "cloud : para parse error"     ),
    "para_empty"     : ( 4003, "cloud : empty parameter"      ),
    "invalid_action" : ( 4004, "cloud : action not found"     ),
    "rate_limit"     : ( 4100, "cloud : beyond rate limit"    )
}
