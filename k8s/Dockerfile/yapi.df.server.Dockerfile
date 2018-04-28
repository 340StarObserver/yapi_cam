FROM mydocker.io:5000/centos7_base:0.4.6

# docker build -t mydocker.io:5000/yapi-server:v1.0 -f yapi.df.server.Dockerfile .

# --------------------------------------------------
# dependence

RUN yum -y install gcc;          \
    yum -y install gcc-c++;      \
    yum -y install python-devel; \
    yum -y install mysql;        \
    yum -y install mysql-devel;  \
    yum -y install nginx;

# --------------------------------------------------
# code

ADD yapi.code.server/py_proj.tar.gz   /data/release/
ADD yapi.code.server/server_start.sh  /data/
ADD yapi.code.server/server_health.sh /data/

RUN chown -R root:root /data/release/py_proj; \
    chown root:root /data/server_start.sh;    \
    chown root:root /data/server_health.sh;   \
    chmod 755 /data/release/py_proj/shell/*;  \
    mkdir -p /data/release/log/yapi/account;  \
    mkdir -p /data/release/log/yapi/atlas;    \
    mkdir -p /data/release/log/yapi/cloud;    \
    mkdir -p /data/release/log/yapi/grant;    \
    mkdir -p /data/release/log/yapi/secret;   \
    mkdir -p /data/release/log/yapi/swoole;   \
    mkdir -p /data/nginx/log;                 \
    mkdir -p /data/nginx/pid;                 \
    chown -R nginx:nginx /data/nginx;

# --------------------------------------------------
# config

RUN ln -sf /data/config/yapi/server/nginx.conf             /etc/nginx/nginx.conf;                             \
    ln -sf /data/config/yapi/server/module_conf.ini        /data/release/py_proj/conf/module_conf.ini;        \
    ln -sf /data/config/yapi/server/uwsgi_py_web.ini       /data/release/py_proj/conf/uwsgi_py_web.ini;       \
    ln -sf /data/config/yapi/server/account_conf_code.py   /data/release/py_proj/account/conf/conf_code.py;   \
    ln -sf /data/config/yapi/server/account_conf_common.py /data/release/py_proj/account/conf/conf_common.py; \
    ln -sf /data/config/yapi/server/account_conf_method.py /data/release/py_proj/account/conf/conf_method.py; \
    ln -sf /data/config/yapi/server/atlas_conf_code.py     /data/release/py_proj/atlas/conf/conf_code.py;     \
    ln -sf /data/config/yapi/server/atlas_conf_common.py   /data/release/py_proj/atlas/conf/conf_common.py;   \
    ln -sf /data/config/yapi/server/atlas_conf_method.py   /data/release/py_proj/atlas/conf/conf_method.py;   \
    ln -sf /data/config/yapi/server/grant_conf_base.py     /data/release/py_proj/grant/conf/conf_base.py;     \
    ln -sf /data/config/yapi/server/grant_conf_code.py     /data/release/py_proj/grant/conf/conf_code.py;     \
    ln -sf /data/config/yapi/server/grant_conf_method.py   /data/release/py_proj/grant/conf/conf_method.py;   \
    ln -sf /data/config/yapi/server/secret_conf_code.py    /data/release/py_proj/secret/conf/conf_code.py;    \
    ln -sf /data/config/yapi/server/secret_conf_common.py  /data/release/py_proj/secret/conf/conf_common.py;  \
    ln -sf /data/config/yapi/server/secret_conf_method.py  /data/release/py_proj/secret/conf/conf_method.py;  \
    ln -sf /data/config/yapi/server/swoole_config.py       /data/release/py_proj/swoole/conf/config.py;       \
    ln -sf /data/config/yapi/server/cloud_config.py        /data/release/py_proj/cloud/conf/config.py;

EXPOSE 80
