### 鉴权模块设计  ###

#### 一. 鉴权接口  ####

```text
请求地址 : http://swoole.yapi/swoole/interface

请求参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.swoole",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.swoole.auth",
        "para"          : {
            "header"    : {
                "mode"      : 鉴权模式（整数）,
                "resource"  : 资源声明（列表）,
                "condition" : 条件声明（列表）,
                "keyList"   : 签名字段（列表）
            },
            "content"   : {   // 云API收到的参数
                "module"    : 模块名,
                "action"    : 接口名,
                "reqTime"   : 秒级请求时间戳,
                "reqNonce"  : 噪声随机数,
                "reqRegion" : 请求地域名,
                "secretId"  : 签名密钥ID,
                "signature" : 签名,
                "params"    : 用户的业务参数（JSON结构体）
            }
        }
    }
}

返回参数 :
{
    "version"       : "1.0",
    "componentName" : "yapi.swoole",
    "eventId"       : 123456789,
    "timestamp"     : 1445599887,
    "returnCode"    : 0,
    "returnMessage" : "ok",
    "data"          : {
        "userUin"   : 用户子账号,
        "ownerUin"  : 用户根账号,
        "appId"     : 用户appId
    }
}
```

**入参-mode**
- 0 : 时间窗口-1, 签名校验-1, 权限校验-1
- 1 : 时间窗口-1, 签名校验-1, 权限校验-0
- 2 : 时间窗口-1, 签名校验-0, 权限校验-1
- 3 : 时间窗口-1, 签名校验-0, 权限校验-0
- 4 : 时间窗口-0, 签名校验-1, 权限校验-1
- 5 : 时间窗口-0, 签名校验-1, 权限校验-0
- 6 : 时间窗口-0, 签名校验-0, 权限校验-1
- 7 : 时间窗口-0, 签名校验-0, 权限校验-0

**入参-resource**
形如 [ "yapi:gz:cbs:bucketId/aaa", "yapi:gz:cbs:bucketId/bbb" ]

**入参-condition**
形如 [ { "condKey"  : "customLabel", "condValue" : [ "labelA", "labelB", "labelC" ] } ]

**入参-keyList**
形如 [ "module", "action", "reqTime", "reqNonce", "reqRegion", "secretId", "params" ]

#### 二. 时间窗口 ####

swoole的配置文件中需要有一个时间窗口的参数，要求 | reqTime - 当前时间戳 | ≤ 时间窗口，可以一定程度上抵御重放攻击。

#### 三. 签名校验 ####

```text
S1. 先处理 params结构体 :
    转成JSON字符串，转的时候要递归地按照字段名排序

S2. 计算签名原文本 :
    根据keyList，从content中提取出所需的键值对
    将得到的键值对，按照字段名排序，得到 k=v 的数组
    将数组中的元素，用 &符号 连接

S3. 根据 secretId 查出 :
    secretKey 用作计算签名
    userUin   备用，鉴权成功返回
    ownerUin  备用，鉴权成功返回
    appId     备用，鉴权成功返回

S4. 计算数据签名 :
    基于签名原文本，以 secretKey 为盐，用 sha256 方式计算哈希
    对哈希值做一次base64编码

//  若算出来的数据签名，与入参中的 signature 一致，则认为签名校验通过
```

#### 四. 权限校验 ####

**4-1. 查出用户关联的所有策略**

```sql
假设用户的 :
userUin  = 909619752
ownerUin = 909619400

select
    strategyId, strategyRule from t_strategy
where strategyId in (
    select strategyId from r_related_strategy where userUin = 909619752 
    union all
    select
        r_related_strategy.strategyId
    from
        r_related_strategy, r_user_group
    where
        r_user_group.userUin = 909619752 and
        r_related_strategy.groupId = r_user_group.groupId
)
union all
select
    strategyId, strategyRule from t_strategy
where
    ownerUin = 909619752 and strategyType = 1
union all
select
    strategyId, strategyRule from t_strategy
where ownerUin = 909619400 and strategyType = 2

// 然后，在应用层，根据strategyId，做去重
```

**4-2. 策略之间的优先级**

```text
策略按照粒度来划分，有 精确类的（比如 vpc:CreateVpc），模糊类的（比如 vpc:*）
策略按照效果来划分，有 允许，拒绝

优先级为 :
精确拒绝 > 精确允许 > 模糊拒绝 > 模糊允许

设置四个变量（初始化为零） :
r1 是否存在精确拒绝
r2 是否存在精确允许
r3 是否存在模糊拒绝
r4 是否存在模糊允许

遍历 <步骤4-1> 得到的策略，逐个匹配，最终鉴权结果 = !r1 && (r2 || (!r3 && r4))
```
