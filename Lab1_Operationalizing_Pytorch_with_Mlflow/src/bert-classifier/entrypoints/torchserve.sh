#!/bin/bash
set -e

if [[ "$1" = "serve" ]]; then
    shift 1
    torchserve --start --ts-config ${MLFLOW_HOME}/config.properties
else
    eval "$@"
fi

# prevent docker exit
tail -f /dev/null