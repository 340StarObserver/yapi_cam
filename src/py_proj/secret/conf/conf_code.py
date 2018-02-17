# -*- coding: utf-8 -*-

# ----------------------------------------
# About error code
CONF_CODE = {
    "success"           : ( 0  , "ok"                        ),
    "unknown"           : ( 101, "unknown error"             ),
    "invalid_method"    : ( 102, "invalid interfaceName"     ),
    "para_miss"         : ( 103, "miss parameter"            ),
    "para_error"        : ( 104, "para parse error"          ),
    "sql_error"         : ( 105, "exec sql error"            ),
    "invalid_user_uin"  : ( 1001, "no such userUin"          ),
    "invalid_op_mode"   : ( 1101, "opMode can only be 0/1/2" ),
    "invalid_secret_id" : ( 1201, "no such secret"           )
}
