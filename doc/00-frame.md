### 云API & CAM 组件架构 ###

```text
module  |  description
--------|---------------
sdk     |  调用云API的SDK
cloud   |  云API服务模块
atlas   |  云API管理模块
secret  |  密钥模块
swoole  |  鉴权模块
grant   |  授权模块
```

模块之间的关系如图 :

<img src = "https://static-1256056882.cos.ap-guangzhou.myqcloud.com/yapi/yapi_frame.png">
