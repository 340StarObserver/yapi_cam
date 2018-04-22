### 接入模块设计 ###

#### 一. 接入接口 ####

```text
请求地址 : http://cloud.yapi/cloud/interface

请求参数 :
{
    "module"    : 模块名,
    "action"    : 接口名,
    "reqTime"   : 秒级请求时间戳,
    "reqNonce"  : 噪声随机数,
    "reqRegion" : 请求地域名,
    "secretId"  : 签名密钥ID,
    "signature" : 签名,
    "params"    : 用户的业务参数（JSON结构体）
}

返回参数 :
{
    "code"      : 错误码,
    "codeDesc"  : 错误码描述简写,
    "message"   : 错误详情,
    "data"      : 业务返回（JSON结构体）
}
```

#### 二. 设计要点 - 频次控制 ####

每个接口都有下面这样的一个五元组 :

| isRate | minRate | curFrequency | timeLastZero | timeLastCall |
| ------ | ------- | ------------ | ------------ | ------------ |
| 是否限频 | 分钟频限 | 这轮累计频次 | 上轮清零时间 | 最近一次调用时间 |

伪代码如下 :

```python
if 开启全局统计频次 :
    curFrequency += 1
    timeLastCall = 当前时间
    
    if isRate and curFrequency > minRate and timeLastCall - timeLastZero < 60:
        限制访问
    
    if timeLastCall - timeLastZero >= 60:
        timeLastZero = timeLastCall

放通访问
```

#### 三. 设计要点 - 调用鉴权服务  ####

鉴权接口协议 见于 "07-swoole.md"，关注三个参数的取值 :

**mode**
时间窗口的校验 和 数据签名的校验 是肯定需要的，权限策略的校验 根据 接口配置数据中的isAuth字段来决定。所以，当 isAuth = 1 则 mode = 0；当 isAuth = 0 则 mode = 1。

**resource**
数据来源是 接入模块协议入参中的 params，计算方式是 接口配置数据中的 funcResource字段。

**condition**
数据来源是 接入模块协议入参中的 params，计算方式是 接口配置数据中的 funcCondition字段。

#### 四. 设计要点 - 调用后台业务 ####

各后台业务的协议不尽相同，故需要下列关注四点 :

**转发地址如何确定**
若后台业务接口关联的后端地址，其类型是 "单地址"，则其urlAddress字段就直接是转发地址。若是 "多地址"，则把 urlAddress字段 当做代码来动态执行。

**入参协议如何转换**
若请求接口配置数据中的 funcReq字段 是空的，则入参就直接是 接入模块 收到的 params字段。反之，把 funcReq字段 当做代码来动态执行。

**返回数据如何转换**
若请求接口配置数据中的 funcRsp字段 是空的，则返回数据就直接是 后台业务的返回。反之，把 funcRsp字段 当做代码来动态执行。

**错误码处理**
根据 上一步，即 <返回数据如何转换> 得到的转换后的返回，去错误码表中查出对应的记录，进行统一转换。
