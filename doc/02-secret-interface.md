### 密钥模块 接口设计 ###

**01. 创建密钥**

```text
请求地址 : http://secret.yapi:8666/secret/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.secret",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.secret.createSecret",
        "para"          : {
            "userUin"      : 909619752,
            "secretRemark" : "密钥备注( 非必要字段 )"
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.secret",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "secretDetail" : {
            "secretId"     : "AKIDVPlfVMWCt5WOXHu79JQEl25KWGv27Lrd",
            "secretKey"    : "VPlfVPUAt5WOXHu79JQEl25KWGv27Lrd",
            "userUin"      : 909619752,
            "status"       : 0,
            "addTime"      : "2018-02-16 19:36:00",
            "modTime"      : "2018-02-16 19:36:00",
            "secretRemark" : "密钥备注"
        }
    }
}

//  status = 0  启用中
//  status = 1  禁用中
//  status = 2  已删除
```

**02. 批量 删除/启用/禁用 密钥**

```text
请求地址 : http://secret.yapi:8666/secret/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.secret",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.secret.operateSecret",
        "para"          : {
            "secretIds" : [ secretId1, secretId2, ... ],
            "opMode"    : 操作类型( 整数, 0-启用, 1-禁用, 2-删除 )
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.secret",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "batchRes"  : [
            {
                "secretId"  : 密钥ID,
                "opCode"    : 是否成功( 整数, 0-成功, 反之失败 ),
                "opMessage" : 失败原因
            },
            ...
            ...
        ]
    }
}
```

**03. 修改单个密钥的备注**

```text
请求地址 : http://secret.yapi:8666/secret/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.secret",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.secret.remarkSecret",
        "para"          : {
            "secretId"     : 密钥ID,
            "secretRemark" : 密钥备注
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.secret",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {}
}
```

**04. 获取某人的密钥列表**

```text
请求地址 : http://secret.yapi:8666/secret/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.secret",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.secret.getSecretList",
        "para"          : {
            "userUin"   : 909619752,
            "showMode"  : 显示模式( 非必要字段, 整数, 1-显示secretKey, 反之不显示 )
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.secret",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "secretList": [
            {
                "secretId"     : "AKIDVPlfVMWCt5WOXHu79JQEl25KWGv27Lrd",
                "secretKey"    : "VPlfVPUAt5WOXHu79JQEl25KWGv27Lrd",
                "userUin"      : 909619752,
                "status"       : 0,
                "addTime"      : "2018-02-16 19:36:00",
                "modTime"      : "2018-02-16 19:36:00",
                "secretRemark" : "密钥备注"
            },
            ...
            ...
        ]
    }
}

//  showMode = 1, 返回中才会有secretKey字段
```

**05. 获取单个密钥的secretKey**

```text
请求地址 : http://secret.yapi:8666/secret/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.secret",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.secret.getSecretKey",
        "para"          : {
            "secretId"  : 密钥ID
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.secret",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "secretDetail" : {
            "secretId"     : "AKIDVPlfVMWCt5WOXHu79JQEl25KWGv27Lrd",
            "secretKey"    : "VPlfVPUAt5WOXHu79JQEl25KWGv27Lrd",
            "userUin"      : 909619752,
            "status"       : 0,
            "addTime"      : "2018-02-16 19:36:00",
            "modTime"      : "2018-02-16 19:36:00",
            "secretRemark" : "密钥备注"
        }
    }
}
```
