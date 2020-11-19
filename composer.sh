#! /bin/bash

while getopts o:s:a: option
do
case "${option}"
in
o) OS=${OPTARG};; # mac
s) SERVICE=${OPTARG};; # start, stop, build, logs, restart
a) APP=${OPTARG};; # crac_server, crac_client
esac
done

if [ "$SERVICE" = "stop" ]; then
docker-compose stop $APP
if [ "$OS" = "mac" ]; then
osascript -e 'quit app "XQuartz"'
fi
exit 0
elif [ "$SERVICE" = "logs" ]; then
docker-compose logs -f --tail=250 $APP
exit 0
elif [ "$SERVICE" = "restart" ]; then
docker-compose restart $APP
exit 0
fi

if [ "$OS" = "mac" ]; then
open -a XQuartz
fi

export IP=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
export DISPLAY=$IP:0
xhost + $IP

if [ "$SERVICE" = "build" ]; then
docker-compose up -d --build $APP
else
docker-compose up -d $APP
fi