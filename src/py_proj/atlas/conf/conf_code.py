# -*- coding: utf-8 -*-

# ----------------------------------------
# About error code
CONF_CODE = {
    "success"                  : ( 0   , "ok"                                      ),
    "unknown"                  : ( 101 , "unknown error"                           ),
    "invalid_method"           : ( 102 , "invalid interfaceName"                   ),
    "para_miss"                : ( 103 , "miss parameter"                          ),
    "para_error"               : ( 104 , "para parse error"                        ),
    "sql_error"                : ( 105 , "exec sql error"                          ),
    "module_permission"        : ( 1000, "module permission denied"                ),
    "invalid_user_uin"         : ( 1001, "no such userUin"                         ),
    "invalid_owner_uin"        : ( 1002, "no such ownerUin"                        ),
    "invalid_module"           : ( 1003, "no such module"                          ),
    "invalid_module_manager"   : ( 1004, "no such module manager"                  ),
    "invalid_urlName"          : ( 1005, "no such module online address"           ),
    "invalid_errorCode"        : ( 1006, "no such module error code"               ),
    "invalid_action"           : ( 1007, "no such module action"                   ),
    "empty_module_enName"      : ( 1101, "module enName can not be empty"          ),
    "empty_module_zhName"      : ( 1102, "module zhName can not be empty"          ),
    "empty_module_managers"    : ( 1103, "module managers can not be empty"        ),
    "empty_module_urlName"     : ( 1104, "module urlName can not be empty"         ),
    "empty_module_urlAddress"  : ( 1105, "module urlAddress can not be empty"      ),
    "empty_module_action"      : ( 1106, "module action can not be empty"          ),
    "empty_module_actionName"  : ( 1107, "module actionName can not be empty"      ),
    "duplicate_module_enName"  : ( 1201, "duplicate module enName"                 ),
    "duplicate_module_zhName"  : ( 1202, "duplicate module zhName"                 ),
    "duplicate_module_manager" : ( 1203, "duplicate module manager"                ),
    "duplicate_module_urlName" : ( 1204, "duplicate module urlName"                ),
    "duplicate_module_code"    : ( 1205, "duplicate module error code"             ),
    "duplicate_module_action"  : ( 1206, "duplicate module action"                 ),
    "mode_manager"             : ( 1301, "opMode can only be 1-add or 2-remove"    ),
    "mode_urlType"             : ( 1302, "urlType can only be 1-single or 2-multi" ),
    "mode_codeType"            : ( 1303, "unsupported error code type"             ),
    "mode_showSvrError"        : ( 1304, "showSvrError can only be 0-no or 1-yes"  ),
    "mode_isAuth"              : ( 1305, "isAuth can only be 0-no or 1-yes"        ),
    "mode_isRate"              : ( 1306, "isRate can only be 0-no or 1-yes"        )
}