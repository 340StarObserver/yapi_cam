# -*- coding: utf-8 -*-

# ----------------------------------------
# About error code
CONF_CODE = {
    "success"                         : ( 0   , "ok"                                    ),
    "unknown"                         : ( 101 , "unknown error"                         ),
    "invalid_method"                  : ( 102 , "invalid interfaceName"                 ),
    "para_miss"                       : ( 103 , "miss parameter"                        ),
    "para_error"                      : ( 104 , "para parse error"                      ),
    "sql_error"                       : ( 105 , "exec sql error"                        ),
    "invalid_user_uin"                : ( 1001, "no such userUin"                       ),
    "invalid_op_mode"                 : ( 1101, "opMode can only be 0/1/2"              ),
    "invalid_secret_id"               : ( 1102, "no such secret"                        ),
    "invalid_secret_status_enable"    : ( 1103, "only disenabled secret can be enabled" ),
    "invalid_secret_status_disenable" : ( 1104, "only enabled secret can be disenabled" ),
    "invalid_secret_status_delete"    : ( 1105, "only disenabled secret can be deleted" )
}
