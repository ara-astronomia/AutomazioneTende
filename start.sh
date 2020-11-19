#!/bin/bash

# enable job control
set -m

while getopts s:a: option; do
case "${option}"
in
    s) SERVICE=${OPTARG};; # start, stop, logs
    a) APP=${OPTARG};; #crac_server, crac_client
esac; done

# retrieve environmental variables
source .env

if [ "$SERVICE" = "stop" ]; then
    CRAC_SERVER_PID=`cat crac_server.pid`
    if [ ! -z "$CRAC_SERVER_PID" ]; then
        kill -9 $CRAC_SERVER_PID
        rm crac_server.pid
    fi
    exit 0
elif [ "$SERVICE" = "logs" ]; then
    if [ ! "$APP" ]; then
        APP=*
    fi
    tail -f -n250 $APP.log
    exit 0
fi

# remove old crac server instance if any
CRAC_SERVER_PID=`cat crac_server.pid`
if [ ! -z "$CRAC_SERVER_PID" ]; then
    kill -9 $CRAC_SERVER_PID
    rm crac_server.pid
fi

# run crac server
python server.py -m > /dev/null 2>&1 &
#SR=$?
#echo "Risultato è $SR"
#if [ "$SR" = "1" ]; then
#    echo "Porta occupata, riprova"
#    exit 1
#fi

#until [ "$SR" = "0" ]; do
#    echo "Il risultato è $SR"
#    python server.py -m > /dev/null &
#    SR=$?
#done

# save pid file
echo $! > crac_server.pid

nc -z -v -w5 localhost 3030
NCR=$?
until [ "$NCR" = "0" ]; do
    echo "Il risultato è $NCR"
    nc -z -w5 localhost 3030
    NCR=$?
done

# run crac client
python client.py > /dev/null 2>&1 &
