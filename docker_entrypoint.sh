#!/bin/bash

curl --retry 5 --retry-connrefused http://postgres:5432
socat TCP4-LISTEN:5432,fork,reuseaddr TCP4:postgres:5432 &

if [[ ! -f "/data/.data_loaded" ]]; then
    python load_data.py saves/*.ck2 && date +"%s" > /data/.data_loaded
fi

tail -f /dev/null
