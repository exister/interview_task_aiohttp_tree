#!/usr/bin/env bash

set -e

DO_CONNECTION_CHECK=${DO_CONNECTION_CHECK:-true}

if [ "${DO_CONNECTION_CHECK}" = true ]; then
    for link in $(env | grep _LINK= | cut -d = -f 2 | sort | uniq)
    do
        ./wait-for-it.sh ${link}
    done
fi

LOG_LEVEL='DEBUG'

if [ "$1" == 'runserver' ]; then
    exec gosu unprivileged python app.py
fi

exec "$@"
