# -*- coding: utf-8 -*-

# ----------------------------------------
# About error code
CONF_CODE = {
    "success"               : ( 0   , "ok"                                    ),
    "unknown"               : ( 101 , "unknown error"                         ),
    "invalid_method"        : ( 102 , "invalid interfaceName"                 ),
    "para_miss"             : ( 103 , "miss parameter"                        ),
    "para_error"            : ( 104 , "para parse error"                      ),
    "sql_error"             : ( 105 , "exec sql error"                        ),
    "invalid_user_uin"      : ( 1001, "no such userUin"                       ),
    "invalid_owner_uin"     : ( 1002, "no such ownerUin"                      ),
    "invalid_group_id"      : ( 1003, "no such group"                         ),
    "invalid_group_name"    : ( 1101, "duplicate groupName of the ownerUin"   ),
    "invalid_bind_mode"     : ( 1201, "opMode can only be 1-bind or 2-unbind" ),
    "user_in_group_not"     : ( 1202, "user not in group"                     ),
    "user_in_group_already" : ( 1203, "user already in group"                 ),
    "owner_not_match_user"  : ( 1204, "userUin is not of the ownerUin"        ),
    "owner_not_match_group" : ( 1205, "group is not of the ownerUin"          )
}
