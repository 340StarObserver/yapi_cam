#!/bin/bash
module=uwsgi_py_web
sig=SIGKILL
ps -ewf | grep -w $module | grep -v grep | awk '{print $2}' | xargs -i kill -s $sig {}
