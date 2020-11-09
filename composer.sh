#! /bin/bash

while getopts o:s: option
do
case "${option}"
in
o) OS=${OPTARG};;
s) SERVICE=${OPTARG};; # start, stop, build
esac
done

if [ "$SERVICE" = "stop" ]; then
docker-compose stop 
if [ "$OS" = "MAC" ]; then
osascript -e 'quit app "XQuartz"'
fi
exit 0
fi

if [ "$OS" = "MAC" ]; then
open -a XQuartz
fi

export IP=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
export DISPLAY=$IP:0
xhost + $IP

if [ "$SERVICE" = "build" ]; then
docker-compose up -d --build
else
docker-compose up -d 
fi