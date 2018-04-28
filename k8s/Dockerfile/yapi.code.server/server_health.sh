#!/bin/sh

[ $(netstat -ltnp | grep nginx | grep 80 | wc -l) -eq 1 ] && [ $(netstat -ltnp | grep uwsgi | wc -l) -ge 2 ]
