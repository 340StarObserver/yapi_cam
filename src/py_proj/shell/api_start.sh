#!/bin/bash
path=/data/release/py_proj
${path}/shell/uwsgi --ini ${path}/conf/uwsgi_py_web.ini
