#!/bin/bash

mlflow run . -P json_dump=/tmp/englab/dump.json -P model_name=BertModel "$@"

: "${JSON_FILE:="dump.json"}"

NAME=$(cat ${JSON_FILE} |jq -r '.name')
VERSION=$(cat ${JSON_FILE} |jq -r '.version')
MODEL_NAME=/${NAME}/$VERSION
MODEL_TAG=${NAME}-$VERSION

echo "MODEL_NAME: ${MODEL_NAME}"


docker build -t labs1-mlflow-torch:${MODEL_TAG} --build-arg GCP_CREDS_JSON_BASE64="$(cat gcp.json.b64)" --build-arg MODEL_NAME=${MODEL_NAME} -f ./Dockerfile-torchserve .