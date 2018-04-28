#!/bin/sh

# --------------------------------------------------
# env

echo "export LANG=zh_CN.UTF-8" >> /etc/profile
source /etc/profile

# --------------------------------------------------
# crontab

sed -i "/session    required   pam_loginuid.so/c\#session    required   pam_loginuid.so" /etc/pam.d/crond

(crontab -l; echo "0 * * * * (find /data/nginx/log                -type f -mtime +10 | xargs rm -f)") | crontab
(crontab -l; echo "0 * * * * (find /data/release/log/yapi/account -type f -mtime +10 | xargs rm -f)") | crontab
(crontab -l; echo "0 * * * * (find /data/release/log/yapi/atlas   -type f -mtime +10 | xargs rm -f)") | crontab
(crontab -l; echo "0 * * * * (find /data/release/log/yapi/cloud   -type f -mtime +10 | xargs rm -f)") | crontab
(crontab -l; echo "0 * * * * (find /data/release/log/yapi/grant   -type f -mtime +10 | xargs rm -f)") | crontab
(crontab -l; echo "0 * * * * (find /data/release/log/yapi/secret  -type f -mtime +10 | xargs rm -f)") | crontab
(crontab -l; echo "0 * * * * (find /data/release/log/yapi/swoole  -type f -mtime +10 | xargs rm -f)") | crontab

# --------------------------------------------------
# start

nginx
cd /data/release/py_proj && ./shell/api_start.sh
