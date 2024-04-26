#!/bin/bash
# take 1 argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 <start|stop|restart|status>"
    exit 1
fi

# if argument is stop or restart, kill all algosys processes
if [ $1 == "stop" ] || [ $1 == "restart" ]; then
    pkill -f "algosys "
    sleep 2
    if pgrep -f "algosys " > /dev/null; then
        pgrep -fla "algosys " | awk '{print $1, $4, "not stopped"}'
        exit 1
    else
        echo "algosys stopped"
    fi
    [ -f nohup.out ] && mv nohup.out nohup.out.old
fi

# if argument is start or restart, start all algosys processes
if [ $1 == "start" ] || [ $1 == "restart" ]; then
    nohup algosys scheduler start < /dev/null > algosys.log 2>&1 &
    nohup algosys ib start < /dev/null > algosys.log 2>&1 &
    # wait for scheduler/ib to finish launching before starting web
    sleep 3
    nohup algosys web start < /dev/null > algosys.log 2>&1 &
    sleep 1
    pgrep -fla "algosys " | awk '{print $1, $4, "started"}'
fi

# if argument is status, print which algosys processes are running
if [ $1 == "status" ]; then
    if pgrep -f "algosys " > /dev/null; then
        echo "algosys is running"
        pgrep -fla "algosys " | awk '{print $1, $4}'
    else
        echo "algosys is not running"
    fi
fi

# check if run in docker
if [ -f /.dockerenv ]; then
    # Wait for any process to exit
    wait -n
    # Exit with status of process that exited first
    exit $?
fi