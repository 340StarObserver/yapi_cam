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

#### 二. 频次控制 ####

每个接口都有下面这样的一个五元组 :

| isRate | minRate | curFrequency | timeLastZero | timeLastCall |
| ------ | ------- | ------------ | ------------ | ------------ |
| 是否限频 | 分钟频限 | 这轮累计频次 | 上轮清零时间 | 最近一次调用时间 |

流程图如下 :

<img src = "https://static-1256056882.cos.ap-guangzhou.myqcloud.com/yapi/yapi_rate.png">
