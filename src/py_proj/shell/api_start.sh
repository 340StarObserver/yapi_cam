#!/bin/bash
path=/data/release/py_proj
cd ${path}
${path}/shell/uwsgi ${path}/conf/uwsgi_py_web.ini
