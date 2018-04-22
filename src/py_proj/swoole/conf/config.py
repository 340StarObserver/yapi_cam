# -*- coding: utf-8 -*-

CONF_LOG = {
    "path"     : "/data/release/log/yapi/swoole/",
    "when"     : "D",
    "interval" : 1,
    "backup"   : 3,
    "encode"   : "utf-8",
    "switch"   : True
}

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

CONF_METHOD = {
    "yapi.swoole.auth"  : "AuthController"
}

CONF_CONSTANT = {
    "timeWindow"        : 600
}

CONF_CODE = {
    "success"           : ( 0   , "swoole : ok"                           ),
    "unknown"           : ( 4101, "swoole : unknown error"                ),
    "invalid_method"    : ( 4102, "swoole : invalid interfaceName"        ),
    "para_miss"         : ( 4103, "swoole : miss parameter"               ),
    "para_error"        : ( 4104, "swoole : para parse error"             ),
    "para_empty"        : ( 4105, "swoole : empty parameter"              ),
    "sql_error"         : ( 4106, "swoole : exec sql error"               ),
    "invalid_resource"  : ( 4107, "swoole : invalid resource format"      ),
    "invalid_condition" : ( 4108, "swoole : invalid condition format"     ),
    "invalid_secretId"  : ( 4200, "swoole : no such secretId or disabled" ),
    "signature_expired" : ( 4300, "swoole : signature expired"            ),
    "signature_wrong"   : ( 4400, "swoole : signature wrong"              ),
    "access_denied"     : ( 4500, "swoole : access denied"                )
}
