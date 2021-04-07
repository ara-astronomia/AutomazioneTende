#!/bin/bash

# enable job control
set -m

while getopts s:a:p: option; do
case "${option}"
in
    s) SERVICE=${OPTARG};; # start, stop, logs
    a) APP=${OPTARG};; # server, client
    p) ARG=${OPTARG};; # -m -s
esac; done

# retrieve environmental variables
source .env
export $(grep --regexp ^[A-Z] .env | cut -d= -f1)

if [ -z "$SERVER_PORT" ]; then
    SERVER_PORT=`cat config.ini | grep "port = " | cut -d " " -f 3`
fi

if [ -z "$SERVER_IP" ]; then
    SERVER_IP=`cat config.ini | grep -e "^ip = " | cut -d " " -f 3`
fi

echo ip: $SERVER_IP
echo porta: $SERVER_PORT

if [ "$SERVICE" = "stop" ]; then
    if [ -f crac_server.pid ]; then
        CRAC_SERVER_PID=`cat crac_server.pid`
        if [ ! -z "$CRAC_SERVER_PID" ]; then
            kill -9 $CRAC_SERVER_PID
            rm crac_server.pid
        fi
    fi
    echo "CRaC server spento, bye"
    exit 0
elif [ "$SERVICE" = "logs" ]; then
    if [ ! "$APP" ]; then
        APP=*
    fi
    tail -f -n250 $APP.log
    exit 0
fi

if [ ! "$APP" ] || [ "$APP" == "server" ]; then
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
    COUNTER=0
    until [ "$PS_EXEC" = "2" ]; do
        ((COUNTER++))
        if [ "$COUNTER" = "10" ]; then
            echo "Non sono riuscito ad avviare il server dopo $COUNTER tentativi, esco"
            exit 1
        fi
        # run crac server
        python server.py $ARG > /dev/null 2>&1 &
        
        # save pid file
        echo $! > crac_server.pid
        
        sleep 5
        
        echo "$COUNTER - Controllo se il server si è avviato, altrimenti rilancio"
        PS_EXEC=`ps -fA | grep "ython server" | wc -l | column -t`
    done

    # wait for server listening at the port
    NCR=1

    until [ "$NCR" = "0" ]; do
        echo "Aspetto che il server sia in ascolto sulla porta $SERVER_PORT"
        nc -z -w5 localhost $SERVER_PORT
        NCR=$?
    done

    echo "CRaC server avviato!"
fi

# run crac client
if [ ! "$APP" ] || [ "$APP" == "client" ]; then
    # wait for server listening at the port
    COUNTER=0
    NCR=1
    until [ "$NCR" = "0" ]; do
        ((COUNTER++))
        if [ "$COUNTER" = "10" ]; then
            echo "Non sono riuscito a collegarmi al server dopo $COUNTER tentativi, esco"
            exit 1
        fi
        echo "$COUNTER - Aspetto che il server sia in ascolto sulla porta $SERVER_PORT"
        nc -z -w5 $SERVER_IP $SERVER_PORT
        NCR=$?
    done
    
    python client.py > /dev/null 2>&1 &

    echo "CRaC client avviato!"
fi
