#!/bin/sh
# 检查uwsgi服务是否开启
if lsof -i:8000|grep uwsgi;then
uwsgi --stop /home/admin/wuyanweb/wuyanweb/wuyanweb/uwsgi.pid
echo "uwsgi stop"
fi
if lsof -i:80|grep nginx;then
service nginx stop
echo "nginx stop"
fi
