### 云图模块 接口设计 ###

**01. 创建模块**

```text
请求地址 : http://atlas.yapi:8666/atlas/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.atlas.createModule",
        "para"          : {
            "loginUin"  : 调用者的userUin,
            "ownerUin"  : 调用者的ownerUin,
            "module"    : "模块英文名",
            "zhName"    : "模块中文名",
            "managers"  : [ 负责人1的uin, 负责人2的uin, ... ]
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "moduleDetail" : {
            "module"   : "vpc",
            "zhName"   : "私有网络",
            "addTime"  : "2018-02-25 15:16:00",
            "modTime"  : "2018-02-25 15:16:00"
        }
    }
}
```

**02. 修改模块的中文备注名**

```text
请求地址 : http://atlas.yapi:8666/atlas/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.atlas.renameModule",
        "para"          : {
            "loginUin"  : 调用者的userUin,
            "ownerUin"  : 调用者的ownerUin,
            "module"    : "模块英文名",
            "zhName"    : "模块中文名"
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "moduleDetail" : {
            "module"   : "vpc",
            "zhName"   : "私有网络",
            "addTime"  : "2018-02-25 15:16:00",
            "modTime"  : "2018-02-25 15:16:00"
        }
    }
}
```

**03. 查询模块列表**

```text
请求地址 : http://atlas.yapi:8666/atlas/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.atlas.getModuleList",
        "para"          : {
            "loginUin"  : 调用者的userUin,
            "ownerUin"  : 调用者的ownerUin,
            "pageId"    : (可选)第几页(整数, 从1开始),
            "pageSize"  : (可选)要几条(整数),
            "keyword"   : (可选)关键字匹配
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "totalNum"  : 总共多少条数据(整数, 不单单是这页上的, 而是全部的),
        "moduleList": [
            {
                "module"   : "vpc",
                "zhName"   : "私有网络",
                "addTime"  : "2018-02-25 15:16:00",
                "modTime"  : "2018-02-25 15:16:00"
            },
            ...
            ...
        ]
    }
}
```

**04. 查询单个模块的基本详情**

```text
请求地址 : http://atlas.yapi:8666/atlas/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.atlas.getModuleDetail",
        "para"          : {
            "loginUin"  : 调用者的userUin,
            "ownerUin"  : 调用者的ownerUin,
            "module"    : "模块英文名"
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "moduleDetail" : {
            "module"   : "vpc",
            "zhName"   : "私有网络",
            "addTime"  : "2018-02-25 15:16:00",
            "modTime"  : "2018-02-25 15:16:00"
        }
    }
}
```

**05. 查询单个模块的负责人列表**

```text
请求地址 : http://atlas.yapi:8666/atlas/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.atlas.getModuleManagers",
        "para"          : {
            "loginUin"  : 调用者的userUin,
            "ownerUin"  : 调用者的ownerUin,
            "module"    : 模块英文名
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "userList"  : [
            {
                "ownerUin"   : 909619400,
                "userUin"    : 909619752,
                "userName"   : "武安君",
                "userRemark" : "以武安天下"
            },
            ...
            ...
        ]
    }
}
```

**06. 为单个模块增加/删除若干个负责人**

```text
请求地址 : http://atlas.yapi:8666/atlas/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.atlas.updateModuleManagers",
        "para"          : {
            "loginUin"  : 调用者的userUin,
            "ownerUin"  : 调用者的ownerUin,
            "module"    : 模块英文名,
            "opMode"    : 操作模式(整数, 1-增加, 2-移除),
            "managers"  : [ 用户1的uin, 用户2的uin, ... ]
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "batchRes"  : [
            {
                "module"    : 模块英文名,
                "userUin"   : 某个用户的uin,
                "opCode"    : 是否成功(整数, 0-成功, 反之失败),
                "opMessage" : 失败原因
            },
            ...
            ...
        ]
    }
}
```

**07. 创建线上地址**

```text
请求地址 : http://atlas.yapi:8666/atlas/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.atlas.createModuleUrl",
        "para"          : {
            "loginUin"  : 调用者的userUin,
            "ownerUin"  : 调用者的ownerUin,
            "module"    : 模块英文名,
            "urlName"   : 线上地址的别名,
            "urlType"   : 地址类型(整数, 1-单地址, 2-多地址),
            "urlAddress": url地址(单地址下为一个url地址, 多地址下为一段py代码)
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "urlDetail" : {
            "module"     : 模块英文名，
            "urlName"    : 线上地址的别名,
            "urlType"    : 地址类型,
            "urlAddress" : url地址,
            "addTime"    : 创建时间(形如 "2018-01-01 00:00:00"),
            "modTime"    : 更新时间(形如 "2018-01-01 00:00:00")
        }
    }
}
```

**08. 修改线上地址**

```text
请求地址 : http://atlas.yapi:8666/atlas/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.atlas.updateModuleUrl",
        "para"          : {
            "loginUin"  : 调用者的userUin,
            "ownerUin"  : 调用者的ownerUin,
            "module"    : 模块英文名,
            "urlName"   : 线上地址的别名,
            "urlType"   : 地址类型,
            "urlAddress": url地址
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "urlDetail" : {
            "module"     : 模块英文名，
            "urlName"    : 线上地址的别名,
            "urlType"    : 地址类型,
            "urlAddress" : url地址,
            "addTime"    : 创建时间(形如 "2018-01-01 00:00:00"),
            "modTime"    : 更新时间(形如 "2018-01-01 00:00:00")
        }
    }
}
```

**09. 查询某个模块下的线上地址**

```text
请求地址 : http://atlas.yapi:8666/atlas/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.atlas.getModuleUrlList",
        "para"          : {
            "loginUin"  : 调用者的userUin,
            "ownerUin"  : 调用者的ownerUin,
            "module"    : (必填)模块英文名,
            "urlName"   : (选填)按线上地址的别名进行模糊匹配的关键词,
            "urlType"   : (选填)地址类型(整数, 不填-全部, 0-全部, 1-单地址, 2-多地址),
            "pageId"    : (选填)第几页,
            "pageSize"  : (选填)要几条
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "totalNum"      : 满足条件的总数,
        "moduleUrlList" : [
            {
                "module"     : 模块英文名，
                "urlName"    : 线上地址的别名,
                "urlType"    : 地址类型,
                "urlAddress" : url地址,
                "addTime"    : 创建时间,
                "modTime"    : 更新时间
            },
            ...
            ...
        ]
    }
}
```

**10. 查询单个线上地址的详情**

```text
请求地址 : http://atlas.yapi:8666/atlas/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.atlas.getModuleUrlDetail",
        "para"          : {
            "loginUin"  : 调用者的userUin,
            "ownerUin"  : 调用者的ownerUin,
            "module"    : 模块英文名,
            "urlName"   : 线上地址的别名
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "urlDetail" : {
            "module"     : 模块英文名，
            "urlName"    : 线上地址的别名,
            "urlType"    : 地址类型,
            "urlAddress" : url地址,
            "addTime"    : 创建时间,
            "modTime"    : 更新时间
        }
    }
}
```

**11. 创建模块错误码**

```text
请求地址 : http://atlas.yapi:8666/atlas/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.atlas.createModuleErrorCode",
        "para"          : {
            "loginUin"     : 调用者的userUin,
            "ownerUin"     : 调用者的ownerUin,
            "module"       : 模块英文名,
            "code"         : 错误码(整数),
            "codeType"     : 错误大类(整数),
            "codeDesc"     : 错误码的英文简写,
            "showSvrError" : 是否展示后端错误信息(整数, 0-否, 1-是),
            "message"      : 错误信息
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "errorCodeDetail" : {
            "module"       : 模块英文名,
            "code"         : 错误码(整数),
            "codeType"     : 错误大类(整数),
            "codeDesc"     : 错误码的英文简写,
            "showSvrError" : 是否展示后端错误信息(整数, 0-否, 1-是),
            "message"      : 错误信息
        }
    }
}
```

**12. 删除模块错误码**

```text
请求地址 : http://atlas.yapi:8666/atlas/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.atlas.deleteModuleErrorCode",
        "para"          : {
            "loginUin"      : 调用者的userUin,
            "ownerUin"      : 调用者的ownerUin,
            "errorCodeList" : [
                {
                    "module": 模块英文名,
                    "code"  : 错误码
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
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "batchRes"  : [
            {
                "module"    : 模块英文名,
                "code"      : 错误码,
                "opCode"    : 是否成功(整数， 0-成功, 反之失败),
                "opMessage" : 失败原因
            },
            ...
            ...
        ]
    }
}
```

**13. 修改模块错误码**

```text
请求地址 : http://atlas.yapi:8666/atlas/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.atlas.updateModuleErrorCode",
        "para"          : {
            "loginUin"     : 调用者的userUin,
            "ownerUin"     : 调用者的ownerUin,
            "module"       : 模块英文名,
            "code"         : 错误码(整数),
            "codeType"     : 错误大类(整数),
            "codeDesc"     : 错误码的英文简写,
            "showSvrError" : 是否展示后端错误信息(整数, 0-否, 1-是),
            "message"      : 错误信息
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "errorCodeDetail" : {
            "module"       : 模块英文名,
            "code"         : 错误码(整数),
            "codeType"     : 错误大类(整数),
            "codeDesc"     : 错误码的英文简写,
            "showSvrError" : 是否展示后端错误信息(整数, 0-否, 1-是),
            "message"      : 错误信息
        }
    }
}
```

**14. 查询某个模块下的错误码**

```text
请求地址 : http://atlas.yapi:8666/atlas/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.atlas.getModuleErrorCodeList",
        "para"          : {
            "loginUin"     : 调用者的userUin,
            "ownerUin"     : 调用者的ownerUin,
            "module"       : (必填)模块英文名,
            "code"         : (选填)指定错误码(整数),
            "codeType"     : (选填)错误大类(整数),
            "showSvrError" : (选填)是否展示后端错误信息(整数, 不填-全部, 0-不展示, 1-展示),
            "keyword"      : (选填)关键字匹配,
            "pageId"       : (选填)第几页,
            "pageSize"     : (选填)要几条
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "totalNum"      : 满足条件的总数,
        "errorCodeList" : [
            {
                "module"       : 模块英文名,
                "code"         : 错误码(整数),
                "codeType"     : 错误大类(整数),
                "codeDesc"     : 错误码的英文简写,
                "showSvrError" : 是否展示后端错误信息(整数, 0-否, 1-是),
                "message"      : 错误信息
            },
            ...
            ...
        ]
    }
}
```

**15. 创建接口**

```text
请求地址 : http://atlas.yapi:8666/atlas/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.atlas.createAction",
        "para"          : {
            "loginUin"      : 调用者的userUin,
            "ownerUin"      : 调用者的ownerUin,
            "module"        : 模块英文名,
            "action"        : 接口英文名,
            "actionName"    : 接口中文名,
            "urlName"       : 线上地址的别名,
            "isAuth"        : 是否进行鉴权(整数, 0-否, 1-是),
            "isRate"        : 是否限制频次(整数, 0-否, 1-是),
            "minRate"       : 每分钟限制多少次(整数, isRate = 0 则该字段可不填),
            "funcReq"       : (选填)python代码(将调用方的参数转换为后端业务所需的格式),
            "funcRsp"       : (选填)python代码(将后端业务的返回转换为对调用方来说是统一的格式),
            "funcResource"  : (选填)python代码(构造鉴权资源),
            "funcCondition" : (选填)python代码(构造鉴权条件)
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "actionDetail" : {
            "module"        : 模块英文名,
            "action"        : 接口英文名,
            "actionName"    : 接口中文名,
            "urlName"       : 线上地址的别名,
            "addTime"       : 创建时间,
            "modTime"       : 更新时间,
            "isAuth"        : 是否进行鉴权(整数, 0-否, 1-是),
            "isRate"        : 是否限制频次(整数, 0-否, 1-是),
            "minRate"       : 每分钟限制多少次(整数, isRate = 0 则该字段可不填),
            "funcReq"       : python代码(将调用方的参数转换为后端业务所需的格式),
            "funcRsp"       : python代码(将后端业务的返回转换为对调用方来说是统一的格式),
            "funcResource"  : python代码(构造鉴权资源),
            "funcCondition" : python代码(构造鉴权条件)
        }
    }
}
```

**16. 修改接口**

```text
请求地址 : http://atlas.yapi:8666/atlas/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.atlas.updateAction",
        "para"          : {
            "loginUin"      : 调用者的userUin,
            "ownerUin"      : 调用者的ownerUin,
            "module"        : 模块英文名,
            "action"        : 接口英文名,
            "actionName"    : 接口中文名,
            "urlName"       : 线上地址的别名,
            "isAuth"        : 是否进行鉴权(整数, 0-否, 1-是),
            "isRate"        : 是否限制频次(整数, 0-否, 1-是),
            "minRate"       : 每分钟限制多少次(整数, isRate = 0 则该字段可不填),
            "funcReq"       : (选填)python代码(将调用方的参数转换为后端业务所需的格式),
            "funcRsp"       : (选填)python代码(将后端业务的返回转换为对调用方来说是统一的格式),
            "funcResource"  : (选填)python代码(构造鉴权资源),
            "funcCondition" : (选填)python代码(构造鉴权条件)
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "actionDetail" : {
            "module"        : 模块英文名,
            "action"        : 接口英文名,
            "actionName"    : 接口中文名,
            "urlName"       : 线上地址的别名,
            "addTime"       : 创建时间,
            "modTime"       : 更新时间,
            "isAuth"        : 是否进行鉴权(整数, 0-否, 1-是),
            "isRate"        : 是否限制频次(整数, 0-否, 1-是),
            "minRate"       : 每分钟限制多少次(整数, isRate = 0 则该字段可不填),
            "funcReq"       : python代码(将调用方的参数转换为后端业务所需的格式),
            "funcRsp"       : python代码(将后端业务的返回转换为对调用方来说是统一的格式),
            "funcResource"  : python代码(构造鉴权资源),
            "funcCondition" : python代码(构造鉴权条件)
        }
    }
}
```

**17. 查询接口列表**

```text
请求地址 : http://atlas.yapi:8666/atlas/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.atlas.getActionList",
        "para"          : {
            "loginUin"     : 调用者的userUin,
            "ownerUin"     : 调用者的ownerUin,
            "module"       : 模块英文名,
            "action"       : (选填)根据接口英文名进行模糊匹配,
            "actionName"   : (选填)根据接口中文名进行模糊匹配,
            "urlName"      : (选填)根据线上地址的别名进行模糊匹配,
            "modTimeRange" : (选填)根据更新时间范围进行筛选(格式形如 "2018-01-01:2018-02-01"),
            "pageId"       : (选填)第几页,
            "pageSize"     : (选填)要几条
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "totalNum"  : 满足条件的总数,
        "actionList": [
            {
                "module"     : 模块英文名,
                "action"     : 接口英文名,
                "actionName" : 接口中文名,
                "urlName"    : 线上地址的别名,
                "addTime"    : 创建时间,
                "modTime"    : 更新时间
            },
            ...
            ...
        ]
    }
}
```

**18. 查询单个接口的详情**

```text
请求地址 : http://atlas.yapi:8666/atlas/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.atlas.getActionDetail",
        "para"          : {
            "loginUin"  : 调用者的userUin,
            "ownerUin"  : 调用者的ownerUin,
            "module"    : 模块英文名,
            "action"    : 接口英文名
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "actionDetail" : {
            "module"        : 模块英文名,
            "action"        : 接口英文名,
            "actionName"    : 接口中文名,
            "addTime"       : 创建时间,
            "modTime"       : 更新时间,
            "urlName"       : 线上地址的别名,
            "urlType"       : 线上地址的类型,
            "urlAddress"    : 线上地址的url,
            "isAuth"        : 是否进行鉴权(整数, 0-否, 1-是),
            "isRate"        : 是否限制频次(整数, 0-否, 1-是),
            "minRate"       : 每分钟限制多少次(整数, isRate = 0 则该字段可不填),
            "funcReq"       : python代码(将调用方的参数转换为后端业务所需的格式),
            "funcRsp"       : python代码(将后端业务的返回转换为对调用方来说是统一的格式),
            "funcResource"  : python代码(构造鉴权资源),
            "funcCondition" : python代码(构造鉴权条件)
        }
    }
}
```

**19. 全服务列表**

```text
请求地址 : http://atlas.yapi:8666/atlas/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.atlas.getServiceApiList",
        "para"          : {
            "loginUin"  : 调用者的userUin,
            "ownerUin"  : 调用者的ownerUin
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "apiList"   : [
            {
                "moduleEnName" : 模块英文名,
                "moduleZhName" : 模块中文名,
                "actionList"   : [
                    {
                        "actionEnName" : 接口英文名,
                        "actionZhName" : 接口中文名
                    },
                    ...
                    ...
                ]
            },
            ...
            ...
        ]
    }
}
```

**20. 查看各接口的当前频率**

```text
请求地址 : http://atlas.yapi:8666/atlas/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.atlas.getActionRate",
        "para"          : {
            "loginUin"          : 调用者的userUin,
            "ownerUin"          : 调用者的ownerUin,
            "module"            : 模块英文名,
            "action"            : (选填)接口英文名,
            "isRate"            : (选填)是否限制频次(整数, 不填-全部, 0-不限制, 1-限制),
            "hasExceed"         : (选填)是否超过限制(整数, 不填-全部, 0-未超过, 1-超过),
            "minRateRange"      : (选填)限制频次范围     (形如 ":100" 或 "100:" 或 "100:200"),
            "curFrequencyRange" : (选填)这分钟内累计几次了(形如 ":100" 或 "100:" 或 "100:200"),
            "pageId"            : (选填)第几页,
            "pageSize"          : (选填)要几条
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "totalNum"       : 满足条件的总数,
        "actionRateList" : [
            {
                "module"       : 模块英文名,
                "action"       : 接口英文名,
                "isRate"       : 是否限制频次,
                "minRate"      : 每分钟限制多少次,
                "curFrequency" : 这分钟内累计几次了,
                "timeLastZero" : 计数器上次清零时间,
                "timeLastCall" : 最近一次调用该接口的时间
            },
            ...
            ...
        ]
    }
}
```

**21. 搜索调用日志**

```text
请求地址 : http://atlas.yapi:8666/atlas/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.atlas.getActionLogList",
        "para"          : {
            "module"     : 模块英文名,
            "action"     : (选填)接口英文名,
            "reqTime"    : (选填)请求时间范围(形如 "2018-01-01:2018-02-01"),
            "reqIp"      : (选填)请求源IP,
            "reqRegion"  : (选填)请求区域,
            "userUin"    : (选填)调用方的uin,
            "returnCode" : (选填)错误码,
            "pageId"     : (选填)第几页,
            "pageSize"   : (选填)要几条
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "actionLogList" : [
            {
                "reqId"      : 请求ID,
                "reqTime"    : 请求时间,
                "reqIp"      : 请求源IP,
                "regRegion"  : 请求区域,
                "module"     : 模块英文名,
                "action"     : 接口英文名,
                "userUin"    : 调用方的uin,
                "returnCode" : 错误码
            },
            ...
            ...
        ]
    }
}
```

**22. 查看某次调用的详情日志**

```text
请求地址 : http://atlas.yapi:8666/atlas/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.atlas.getActionLogDetail",
        "para"          : {
            "reqId"     : 请求ID
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "actionLogDetail" : {
            "reqId"       : 请求ID,
            "reqTime"     : 请求时间(秒级时间戳),
            "reqIp"       : 请求源IP,
            "reqRegion"   : 请求区域,
            "reqNonce"    : 调用随机数,
            "module"      : 模块英文名,
            "action"      : 接口英文名,
            "userUin"     : 调用方的uin,
            "receiveData" : 接收的调用方的请求参数,
            "returnData"  : 返回给调用方的数据,
            "returnCode"  : 错误码,
            "camUrl"      : 鉴权地址,
            "camAk"       : 鉴权密钥,
            "camReq"      : 鉴权请求参数,
            "camRsp"      : 鉴权返回数据,
            "svrUrl"      : 转发给后端服务的地址,
            "svrReq"      : 转发给后端服务的请求参数,
            "svrRsp"      : 接收自后端服务的返回数据
        }
    }
}
```
