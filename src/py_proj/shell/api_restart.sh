#!/bin/bash
path=/data/release/py_proj/shell
bash ${path}/stop_api.sh 1
sleep 2
bash ${path}/start_api.sh
