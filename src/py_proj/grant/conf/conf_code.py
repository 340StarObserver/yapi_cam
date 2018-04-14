# -*- coding: utf-8 -*-

# ----------------------------------------
# About error code

CONF_CODE = {
    "success"               : ( 0   , "ok"                                   ),
    "unknown"               : ( 101 , "unknown error"                        ),
    "invalid_method"        : ( 102 , "invalid interfaceName"                ),
    "para_miss"             : ( 103 , "miss parameter"                       ),
    "para_error"            : ( 104 , "para parse error"                     ),
    "sql_error"             : ( 105 , "exec sql error"                       ),
    "permission_strategy"   : ( 1001, "strategy not belong to the ownerUin"  ),
    "permission_user"       : ( 1002, "userUin not belong to the ownerUin"   ),
    "permission_group"      : ( 1003, "userGroup not belong to the ownerUin" ),
    "invalid_user_uin"      : ( 1101, "no such userUin"                      ),
    "invalid_owner_uin"     : ( 1102, "no such ownerUin"                     ),
    "invalid_group_id"      : ( 1103, "no such userGroup"                    ),
    "invalid_strategy_id"   : ( 1104, "no such strategy"                     ),
    "invalid_strategy_rule" : ( 1105, "invalid strategy rule"                ),
    "empty_strategy_name"   : ( 1201, "strategyName can not be empty"        ),
    "mode_strategy_type"    : ( 1301, "strategyType can only be 0 / 1 / 2"   ),
    "mode_related_user"     : ( 1302, "relatedUser can only be 0 / 1"        ),
    "mode_related_group"    : ( 1303, "relatedGroup can only be 0 / 1"       ),
    "mode_related_bind"     : ( 1304, "bindMode can only be 1 / 2"           ),
    "bind_user_not"         : ( 1401, "the user not bind the strategy yet"   ),
    "bind_user_already"     : ( 1402, "the user already bind the strategy"   ),
    "bind_group_not"        : ( 1403, "the group not bind the strategy yet"  ),
    "bind_group_already"    : ( 1404, "the group already bind the strategy"  )
}
