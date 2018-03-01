### 账号模块 接口设计 ###

**01. 批量查询账户详情**

```text
请求地址 : http://account.yapi:8666/account/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.account",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.account.getUserDetail",
        "para"          : {
            "userUinList" : [ userUin1, userUin2, ... ]
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.account",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "userUin1"  : {
            "userUin"    : 909619752,
            "ownerUin"   : 909619400,
            "appId"      : 1251568418,
            "userName"   : "武安君",
            "userRemark" : "以武安天下",
            "userPhone"  : 13912345678,
            "userEmail"  : "xxx@qq.com",
            "addTime"    : "2018-01-01 00:00:00",
            "modTime"    : "2018-02-02 00:00:00"
        },
        "userUin2"  : {
            ...
            ...
        },
        ...
        ...
    }
}
```

**02. 子账户列表**

```text
请求地址 : http://account.yapi:8666/account/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.account",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.account.getSubAccountList",
        "para"          : {
            "pageId"    : 第几页,
            "pageSize"  : 要几条,
            "ownerUin"  : 根账号uin,
            "keyword"   : (可选)关键字
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.account",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "totalNum"  : 满足条件的总数,
        "userList"  : [
            {
                "userUin"    : 909619752,
                "ownerUin"   : 909619400,
                "appId"      : 1251568418,
                "userName"   : "武安君",
                "userRemark" : "以武安天下",
                "userPhone"  : 13912345678,
                "userEmail"  : "xxx@qq.com",
                "addTime"    : "2018-01-01 00:00:00",
                "modTime"    : "2018-02-02 00:00:00"
            },
            ...
            ...
        ]
    }
}
```

**03. 创建用户组**

```text
请求地址 : http://account.yapi:8666/account/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.account",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.account.createUserGroup",
        "para"          : {
            "loginUin"    : 调用者的userUin,
            "ownerUin"    : 调用者的ownerUin,
            "groupName"   : 用户组名,
            "groupRemark" : 用户组备注
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.account",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "userGroupDetail" : {
            "groupId"     : 用户组ID,
            "ownerUin"    : 创建者的ownerUin,
            "groupName"   : 用户组名,
            "groupRemark" : 用户组备注,
            "groupNum"    : 用户组内人数,
            "addTime"     : 创建时间,
            "modTime"     : 更新时间
        }
    }
}
```

**04. 编辑用户组基本信息**

```text
请求地址 : http://account.yapi:8666/account/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.account",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.account.updateUserGroup",
        "para"          : {
            "loginUin"    : 调用者的userUin,
            "ownerUin"    : 调用者的ownerUin,
            "groupId"     : 用户组的ID,
            "groupName"   : 用户组的新名字,
            "groupRemark" : 用户组的新备注,
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.account",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "userGroupDetail" : {
            "groupId"     : 用户组ID,
            "ownerUin"    : 创建者的ownerUin,
            "groupName"   : 用户组名,
            "groupRemark" : 用户组备注,
            "groupNum"    : 用户组内人数,
            "addTime"     : 创建时间,
            "modTime"     : 更新时间
        }
    }
}
```

**05. 批量绑定/解绑用户和用户组**

```text
请求地址 : http://account.yapi:8666/account/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.account",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.account.bindUserGroup",
        "para"          : {
            "loginUin"    : 调用者的userUin,
            "ownerUin"    : 调用者的ownerUin,
            "opMode"      : 操作模式(整数, 1-绑定, 2-解绑),
            "opList"      : [
                {
                    "groupId" : 某用户组ID,
                    "userUin" : 某用户的userUin
                },
                ...
                ...
            ]
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.account",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "batchRes"  : [
            {
                "groupId"   : 某用户组ID,
                "userUin"   : 某用户的userUin,
                "opCode"    : 是否成功(整数, 0-成功, 反之失败),
                "opMessage" : 失败原因
            },
            ...
            ...
        ]
    }
}
```

**06. 批量删除用户组**

```text
请求地址 : http://account.yapi:8666/account/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.account",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.account.deleteUserGroup",
        "para"          : {
            "loginUin"    : 调用者的userUin,
            "ownerUin"    : 调用者的ownerUin,
            "groupIdList" : [ groupId1, groupId2, ... ]
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.account",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "batchRes"  : [
            {
                "groupId"   : 某用户组ID,
                "opCode"    : 是否成功(整数, 0-成功, 反之失败),
                "opMessage" : 失败原因
            },
            ...
            ...
        ]
    }
}
```

**07. 当前租户下的用户组列表**

```text
请求地址 : http://account.yapi:8666/account/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.account",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.account.getUserGroupList",
        "para"          : {
            "loginUin"    : 调用者的userUin,
            "ownerUin"    : 调用者的ownerUin,
            "pageId"      : (可选)第几页, 若不填则取所有,
            "pageSize"    : (可选)要几条, 若不填则取所有,
            "keyword"     : (可选)关键字,
            "userUin"     : (可选)指定用户, 可用来查某个用户关联的用户组
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.account",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "totalNum"      : 满足条件的总数,
        "userGroupList" : [
            {
                "groupId"     : 用户组ID,
                "ownerUin"    : 创建者的ownerUin,
                "groupName"   : 用户组名,
                "groupRemark" : 用户组备注,
                "groupNum"    : 用户组内人数,
                "addTime"     : 创建时间,
                "modTime"     : 更新时间
            },
            ...
            ...
        ]
    }
}
```

**08. 查看某个用户组内的成员**

```text
请求地址 : http://account.yapi:8666/account/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.account",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.account.getGroupMemberList",
        "para"          : {
            "groupId"   : 用户组ID,
            "pageId"    : (可选)第几页, 若不填则取所有,
            "pageSize"  : (可选)要几条, 若不填则取所有
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.account",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "totalNum"  : 满足条件的总数,
        "userList"  : [
            {
                "userUin"    : 909619752,
                "ownerUin"   : 909619400,
                "appId"      : 1251568418,
                "userName"   : "武安君",
                "userRemark" : "以武安天下",
                "userPhone"  : 13912345678,
                "userEmail"  : "xxx@qq.com",
                "addTime"    : "2018-01-01 00:00:00",
                "modTime"    : "2018-02-02 00:00:00"
            },
            ...
            ...
        ]
    }
}
```
