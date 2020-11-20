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
    if [ -f crac_server.pid ]; then
        CRAC_SERVER_PID=`cat crac_server.pid`
        if [ ! -z "$CRAC_SERVER_PID" ]; then
            kill -9 $CRAC_SERVER_PID
            rm crac_server.pid
        fi
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
if [ -f crac_server.pid ]; then
    CRAC_SERVER_PID=`cat crac_server.pid`
    if [ ! -z "$CRAC_SERVER_PID" ]; then
        kill -9 $CRAC_SERVER_PID
        rm crac_server.pid
    fi
fi

# check if app is still running
PS_EXEC=1
until [ "$PS_EXEC" = "2" ]; do
    # run crac server
    python server.py -m > /dev/null 2>&1 &
    
    # save pid file
    echo $! > crac_server.pid
    
    sleep 5
    
    echo "Controllo se il server si è avviato, altrimenti rilancio"
    PS_EXEC=`ps -fA | grep "ython server" | wc -l | column -t`
done

# wait for server listening at the port
NCR=1
until [ "$NCR" = "0" ]; do
    echo "Aspetto che il server sia in ascolto sulla porta 3030"
    nc -z -w5 localhost 3030
    NCR=$?
done

# run crac client
python client.py > /dev/null 2>&1 &
