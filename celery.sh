#!/bin/bash

get_help ()
{
    echo
    echo -e "\033[34m\033[1mUsage: \033[0m"
    echo -e "\t ./celery.sh \033[32mCommand [process] [worker count]\033[0m"
    echo
    echo -e "\033[32mCommand:\033[0m"
    echo -e "\t debug: run celery in the current workspace not in the background"
    echo -e "\t start: to start celery in the background"
    echo -e "\t stop: stop celery"
    echo -e "\t restart: restart celery"
    echo -e "\t stopwait: ensure all currently executing tasks is completed then stop"
    echo -e "\t --help or -h: get help"
    echo
    echo -e "\033[95mConfig:\033[0m"
    echo -e "\t path of pidfile and logfile are in config/config.py or somefile else"
    echo -e "\t config.Celery = dict("
    echo -e "\t     pidfile= '~/data/celery/%n.pid',"
    echo -e "\t     logfile= '~/data/celery/%n%I.log'"
    echo -e "\t )"
}

APP="water.celery_job.main"
PROCESS=1
THREAD=500
argc=$#
if [ $argc -eq 0 ]
then
    get_help
else
    if [[ $1 = '--help' || $1 = '-h' ]]
    then
        get_help
    else
        if [ $1 = 'debug' ]
        then
            celery worker --concurrency=$THREAD -l info --app=$APP -P gevent
        else
            pidfile=`python get_celery_config.py pidfile`
            logfile=`python get_celery_config.py logfile`
            echo
            echo -e "\033[40m$1 celery process\033[0m"
            echo
            if [[ $argc -eq 2 || $argc -eq 3 ]]
            then
                PROCESS=$2
            fi
            if [ $argc -eq 3 ]
            then
                THREAD=$3
            fi
            cmd="celery multi $1 $PROCESS -l info --concurrency=$THREAD -P gevent --app=$APP --pidfile=$pidfile --logfile=$logfile"
            echo -e "\033[95m"$cmd"\033[0m"
            eval $cmd
        fi
    fi
fi
