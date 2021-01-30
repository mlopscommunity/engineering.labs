#!/bin/bash

# Pass any parameters for mflow run as parameters to this script e.g.
# ./train-and-build.sh -P max_epochs=5 -P num_samples=15000

# build can be done in GH Actions
docker build -t englabs/trainer --build-arg GCP_CREDS_JSON_BASE64="$(cat gcp.json.b64)" -f ./Dockerfile-trainer .

JSON_FILE="$(uuidgen).json"
mlflow run . -P json_dump=/tmp/englab/$JSON_FILE -P model_name=BertModel "$@"

NAME=$(cat ${JSON_FILE} |jq -r '.name')
VERSION=$(cat ${JSON_FILE} |jq -r '.version')
MODEL_NAME=/${NAME}/$VERSION
MODEL_TAG=${NAME}-$VERSION

echo "MODEL_NAME: ${MODEL_NAME}"


docker build -t labs1-mlflow-torch:${MODEL_TAG} --build-arg GCP_CREDS_JSON_BASE64="$(cat gcp.json.b64)" --build-arg MODEL_NAME=${MODEL_NAME} -f ./Dockerfile-torchserve .

# This is much better done in GH Actions, just here to test out
cat gcp.json.b64 | base64 --decode > gcp.json
gcloud auth activate-service-account mlflow-storage@engineeringlab.iam.gserviceaccount.com  --key-file=./gcp.json
gcloud auth configure-docker
docker tag labs1-mlflow-torch:${MODEL_TAG} gcr.io/engineeringlab/labs1-mlflow-torch:${MODEL_TAG}
docker push gcr.io/engineeringlab/labs1-mlflow-torch:${MODEL_TAG}
