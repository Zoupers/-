#!/bin/sh
uwsgi --ini /home/admin/wuyanweb/wuyanweb/wuyanweb/uwsgi.ini
echo "uwsgi start"
service nginx start
echo "nginx start"
