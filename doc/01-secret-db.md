### 密钥模块 数据设计 ###

**01. 账户**

```text
库名 : db_auth
表名 : t_user
主键 : userUin
索引 : ownerUin

userUin       bigint, unsigned,     not null    自己的uin
ownerUin      bigint, unsigned,     not null    所属的uin
userName      varchar(255)    ,     not null    用户名字
userRemark    text            , default null    用户备注
userPhone     bigint, unsigned, default null    用户手机
userEmail     varchar(255)    , default null    用户邮箱
addTime       datetime        ,     not null    创建时间
modTime       datetime        ,     not null    更新时间
```

**02. AppId**

```text
库名 : db_auth
表名 : r_user_app
主键 : ownerUin
索引 : unique(appId)

ownerUin      bigint, unsigned,     not null    所属的uin
appId         bigint, unsigned,     not null    AppId
```

**03. 用户组**

```text
库名 : db_auth
表名 : t_group
主键 : groupId
索引 : ownerUin, unique(groupName)

groupId       bigint, unsigned,     not null    组ID
ownerUin      bigint, unsigned,     not null    所属的uin
groupName     varchar(255)    ,     not null    组名字
groupRemark   text            , default null    组备注
groupNum      bigint, unsigned,     not null    组内用户数量
addTime       datetime        ,     not null    创建时间
modTime       datetime        ,     not null    更新时间
```

**04. 用户和用户组的关系**

```text
库名 : db_auth
表名 : r_user_group
主键 : (groupId, userUin)

groupId       bigint, unsigned,     not null    组ID
userUin       bigint, unsigned,     not null    用户的uin
addTime       datetime        ,     not null    加入时间
```

**05. 密钥表**

```text
库名 : db_auth
表名 : t_secret
主键 : secretId
索引 : userUin

secretId      char(40)  ,           not null    密钥ID
secretKey     char(40)  ,           not null    密钥KEY
userUin       bigint    , unsigned, not null    用户的uin
status        int(11)   , unsigned, not null    密钥状态
addTime       datetime  ,           not null
modTime       datetime  ,           not null
secretRemark  text      ,       default null

// status = 0  启用中
// status = 1  禁用中
// status = 2  已删除
```
