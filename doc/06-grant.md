### 授权模块设计 ###

#### 一. 策略 ####

```text
库名 : db_auth
表名 : t_strategy
主键 : strategyId
索引 : ownerUin

strategyId        bigint  unsigned    not null    策略编号( 自增 )
ownerUin          bigint  unsigned    not null    所属租户的根账号
strategyType      int(11) unsigned    not null    策略类型
strategyName      varchar(255)        not null    策略名字
strategyRemark    text            default null    策略备注
strategyRule      text                not null    策略规则

关于策略类型 :
0 : 普通类型
1 : 根账号的预设策略（所属的根账号，这个根账号不必绑定该策略，即可生效）
2 : 子账号的预设策略（下属的子账号，那些子账号不必绑定该策略，即可生效）
```

关于策略规则字段，举个例子来详加说明。

```json
[
    {
        "effect"    : "allow",
        "action"    : [ "cbs:ListBucketObjects" ],
        "resource"  : [
            "yapi:gz:cbs:bucketId/aaa",
            "yapi:gz:cbs:bucketId/bbb"
        ],
        "condition" : [
            {
                "condKey"   : "customLabel",
                "condType"  : "oneIn",
                "condValue" : [ "labelA", "labelB", "labelC" ]
            }
        ]
    },
    {
        "effect"    : "deny",
        "action"    : [ "lb:*" ],
        "resource"  : [ "*" ],
        "condition" : [ "*" ]
    }
]
```

**effect**  
规则生效方式。allow（允许） 或者 deny（拒绝）。

**action**  
接口列表数组。内部每个元素都是 模块:接口 的形式，模块 和 接口 都可以用 * 来通配。

**resource**  
资源标签数组。可以自定义格式，但是不变的是，它是用冒号隔开的。如果冒号隔开的某一项有'/'号，则'/'号左侧的是键，右侧的是值，值可以用 * 通配。

**condition**  
复杂条件数组。数组中的每个子对象，都由条件字段，条件类型，条件值构成。支持的条件类型有 oneIn（只要一项属于），allIn（每一项都要属于），gt（大于），ge（大于等于），lt（小于），le（小于等于），eq（等于），neq（不等于）。

#### 二. 策略 ~ 用户，用户组 绑定关系 ####

```text
库名 : db_auth
表名 : r_related_strategy
主键 : (strategyId, userUin, groupId)
索引 : userUin
索引 : groupId

strategyId        bigint  unsigned    not null    策略编号
userUin           bigint  unsigned    not null    子账号
groupId           bigint  unsinged    not null    用户组编号

当 userUin == 0, groupId != 0, 表示用户组关联该策略
当 userUin != 0, groupId == 0, 表示用户关联该策略
```

#### 三. 接口设计 ####

**01. 策略规则中支持的条件运算符**

```text
请求地址 : http://grant.yapi/grant/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.grant",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.grant.getConditionOpList",
        "para"          : {
            "loginUin"  : 调用者的userUin,
            "ownerUin"  : 调用者的ownerUin
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.grant",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "opList"    : [
            {
                "opType" : "oneIn",
                "opName" : "存在属于"
            },
            ...
            ...
        ]
    }
}
```

**02. 创建策略**

```text
请求地址 : http://grant.yapi/grant/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.grant",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.grant.createStrategy",
        "para"          : {
            "loginUin"       : 调用者的userUin,
            "ownerUin"       : 调用者的ownerUin,
            "strategyType"   : 策略类型( 整数, 0-普通, 1-根账号预设, 2-子账号预设 ),
            "strategyName"   : 策略名字,
            "strategyRemark" : 策略备注,
            "strategyRule"   : 策略规则( json对象, 注意不是json字符串 )
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.grant",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "strategyDetail" : {
            "strategyId"     : 策略编号,
            "ownerUin"       : 所属租户的根账号,
            "strategyType"   : 策略类型,
            "strategyName"   : 策略名字,
            "strategyRemark" : 策略备注,
            "strategyRule"   : 策略规则
        }
    }
}
```

**03. 更新策略**

```text
请求地址 : http://grant.yapi/grant/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.grant",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.grant.updateStrategy",
        "para"          : {
            "loginUin"       : 调用者的userUin,
            "ownerUin"       : 调用者的ownerUin,
            "strategyId"     : 策略编号,
            "strategyType"   : 策略类型( 整数, 0-普通, 1-根账号预设, 2-子账号预设 ),
            "strategyName"   : 策略名字,
            "strategyRemark" : 策略备注,
            "strategyRule"   : 策略规则( json对象, 注意不是json字符串 )
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.grant",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "strategyDetail" : {
            "strategyId"     : 策略编号,
            "ownerUin"       : 所属租户的根账号,
            "strategyType"   : 策略类型,
            "strategyName"   : 策略名字,
            "strategyRemark" : 策略备注,
            "strategyRule"   : 策略规则
        }
    }
}
```

**04. 批量删除策略**

```text
请求地址 : http://grant.yapi/grant/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.grant",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.grant.deleteStrategy",
        "para"          : {
            "loginUin"       : 调用者的userUin,
            "ownerUin"       : 调用者的ownerUin,
            "strategyIdList" : [ 策略编号1, 策略编号2, ... ]
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.grant",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "batchRes"  : [
            {
                "strategyId" : 策略编号,
                "opCode"     : 是否成功(整数, 0-成功, 反之失败),
                "opMessage"  : 失败原因
            }
        ]
    }
}
```

**05. 查询单个策略的详情**

```text
请求地址 : http://grant.yapi/grant/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.grant",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.grant.getStrategyDetail",
        "para"          : {
            "loginUin"  : 调用者的userUin,
            "ownerUin"  : 调用者的ownerUin,
            "strategyId": 策略编号
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.grant",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "strategyDetail" : {
            "strategyId"     : 策略编号,
            "ownerUin"       : 所属租户的根账号,
            "strategyType"   : 策略类型,
            "strategyName"   : 策略名字,
            "strategyRemark" : 策略备注,
            "strategyRule"   : 策略规则
        }
    }
}
```

**06. 查看单个策略所关联的用户和用户组**

```text
请求地址 : http://grant.yapi/grant/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.grant",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.grant.getStrategyRelated",
        "para"          : {
            "loginUin"     : 调用者的userUin,
            "ownerUin"     : 调用者的ownerUin,
            "strategyId"   : 策略编号,
            "relatedUser"  : 是否返回关联的用户( 整数, 0-否, 1-是 ),
            "relatedGroup" : 是否返回关联的用户组( 整数, 0-否, 1-是 )
        }
    }
}

relatedUser  = 1, 返回中 userList  才存在
relatedGroup = 1, 返回中 groupList 才存在

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.grant",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "userList"  : [
            {
                "userUin"   : 用户子账号,
                "userName"  : 用户名字,
                "ownerUin"  : 所属租户的根账号,
                "appId"     : 所属租户
            },
            ...
            ...
        ],
        "groupList" : [
            {
                "groupId"   : 用户组编号,
                "groupName" : 用户组名字,
                "ownerUin"  : 所属租户的根账号
            },
            ...
            ...
        ]
    }
}
```

**07. 查询策略列表**

```text
请求地址 : http://grant.yapi/grant/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.grant",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.grant.getStrategyList",
        "para"          : {
            "loginUin"     : 调用者的userUin,
            "ownerUin"     : 调用者的ownerUin,
            "strategyName" : (可选)策略名的模糊匹配,
            "strategyType" : (可选)策略类型( 整数, 0-普通, 1-根账号预设, 2-子账号预设 ),
            "userUin"      : (可选)指定子账号，可用于筛选出某个用户关联的策略,
            "groupId"      : (可选)指定用户组，可用于筛选出某个用户组关联的策略,
            "pageId"       : (可选)第几页,
            "pageSize"     : (可选)要几条
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.grant",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "totalNum"     : 满足条件的总数,
        "strategyList" : [
            {
                "strategyId"     : 策略编号,
                "ownerUin"       : 所属租户的根账号,
                "strategyType"   : 策略类型,
                "strategyName"   : 策略名字,
                "strategyRemark" : 策略备注
            },
            ...
            ...
        ]
    }
}
```

**08. 批量 绑定/解绑 用户和策略**

```text
请求地址 : http://grant.yapi/grant/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.grant",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.grant.bindUserStrategy",
        "para"          : {
            "loginUin"  : 调用者的userUin,
            "ownerUin"  : 调用者的ownerUin,
            "bindMode"  : 绑定方式( 整数, 1-绑定, 2-解绑 ),
            "bindList"  : [
                {
                    "strategyId" : 策略编号,
                    "userUin"    : 子账号
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
    "componentName" : "yapi.grant",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "batchRes"  : [
            {
                "strategyId" : 策略编号,
                "userUin"    : 子账号,
                "opCode"     : 是否成功(整数, 0-成功, 反之失败),
                "opMessage"  : 失败原因
            }
        ]
    }
}
```

**09. 批量 绑定/解绑 用户组和策略**

```text
请求地址 : http://grant.yapi/grant/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.grant",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.grant.bindGroupStrategy",
        "para"          : {
            "loginUin"  : 调用者的userUin,
            "ownerUin"  : 调用者的ownerUin,
            "bindMode"  : 绑定方式( 整数, 1-绑定, 2-解绑 ),
            "bindList"  : [
                {
                    "strategyId" : 策略编号,
                    "groupId"    : 用户组编号
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
    "componentName" : "yapi.grant",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "batchRes"  : [
            {
                "strategyId" : 策略编号,
                "groupId"    : 用户组编号,
                "opCode"     : 是否成功(整数, 0-成功, 反之失败),
                "opMessage"  : 失败原因
            }
        ]
    }
}
```
