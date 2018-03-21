### 云图模块 数据设计 ###

**01. 模块**

```text
库名 : db_yapi_data
表名 : t_module
主键 : module
索引 : unique(zhName)

module        varchar(255)          not null    模块英文名
zhName        varchar(255)          not null    模块中文备注名
addTime       datetime              not null    创建时间
modTime       datetime              not null    更新时间
```

**02. 模块负责人**

```text
库名 : db_yapi_data
表名 : t_module_manager
主键 : (module, userUin)

module        varchar(255)          not null    模块英文名
userUin       bigint, unsigned      not null    负责人的uin
```

**03. 模块线上地址**

```text
库名 : db_yapi_data
表名 : t_module_url
主键 : (module, urlName)

module        varchar(255)          not null    模块英文名
urlName       varchar(255)          not null    该线上地址的别名
urlType       int(11)   , unsigned, not null    该线上地址的类型
urlAddress    text                  not null    url地址
addTime       datetime              not null    创建时间
modTime       datetime              not null    更新时间

// urlType = 1  单地址类型, urlAddress 形如 http://secret.yapi:8666/secret/interface
// urlType = 2  多地址类型, urlAddress 是一段python代码, 根据请求参数决定转发地址
```

**04. 模块错误码**

```text
库名 : db_yapi_data
表名 : t_module_errorcode
主键 : (module, code)

module        varchar(255)          not null    模块英文名
code          int(11)   , unsigned, not null    错误码数字
showSvrError  int(11)   , unsigned, not null    是否展示后端错误信息
codeType      int(11)   , unsigned, not null    错误大类
codeDesc      varchar(255)          not null    错误码英文简写
message       text                  not null    错误码详细信息

// codeType :
// 3000  后端返回格式错误
// 4000  用户错误
// 4100  频次超限
// 4200  签名密钥不存在
// 4300  签名过期
// 4400  签名错误
// 4500  权限不足
// 5000  后端错误
```

**05. 接口**

```text
库名 : db_yapi_data
表名 : t_action
主键 : (module, action)

module        varchar(255)          not null    模块英文名
action        varchar(255)          not null    接口英文名
actionName    varchar(255)          not null    接口中文名
addTime       datetime              not null    创建时间
modTime       datetime              not null    更新时间
urlName       varchar(255)          not null    线上地址的别名
isAuth        int(11)   , unsigned, not null    是否鉴权(0-否, 1-是)
funcReq       text              default null    python代码(将调用方的参数转换为后端业务所需的格式)
funcRsp       text              default null    python代码(将后端业务的返回转换为对调用方来说是统一的格式)
funcResource  text              default null    python代码(构造鉴权资源)
funcCondition text              default null    python代码(构造鉴权条件)
```

**06. 接口的频次控制**

```text
库名 : db_yapi_log
表名 : t_action_rate
主键 : (module, action)

module        varchar(255)          not null    模块英文名
action        varchar(255)          not null    接口英文名
isRate        int(11)   , unsigned, not null    是否进行频率限制(0-否, 1-是)
minRate       int(11)   , unsigned, not null    每分钟限制该接口被调用多少次
curFrequency  int(11)   , unsigned, not null    当前累计调用了多少次了
timeLastZero  bigint    , unsigned, not null    上次计数器清零的时间(秒级时间戳)
timeLastCall  bigint    , unsigned, not null    最近一次调用接口时间(秒级时间戳)
```

**07. 接口的调用日志**

```text
库名 : db_yapi_log
表名 : t_action_log
主键 : reqId
索引 : (reqTime, module)

reqId         varchar(255)          not null    请求ID
reqTime       bigint, unsigned,     not null    请求时间(秒级时间戳)
reqIp         varchar(255)    , default null    请求源IP
reqRegion     varchar(255)    , default null    请求区域
reqNonce      bigint, unsigned, default null    调用随机数
module        varchar(255)          not null    模块英文名
action        varchar(255)          not null    接口英文名
userUin       bigint, unsigned, default null    调用方的uin
receiveData   text            , default null    接收的调用方的请求参数
returnData    text            , default null    返回给调用方的数据
returnCode    int(11)         , default null    错误码
camUrl        varchar(255)    , default null    鉴权地址
camAk         varchar(255)    , default null    鉴权密钥
camReq        text            , default null    鉴权请求参数
camRsp        text            , default null    鉴权返回数据
svrUrl        varchar(255)    , default null    转发给后端服务的地址
svrReq        text            , default null    转发给后端服务的请求参数
svrRsp        text            , default null    接收自后端服务的返回数据
```
