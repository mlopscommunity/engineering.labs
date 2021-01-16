FROM python:3.8-alpine

COPY requirements.txt requirements.txt
RUN DEBIAN_FRONTEND=noninteractive && \
    pip install --progress-bar=off -U --no-cache-dir -r requirements.txt

COPY kaggle_creds/kaggle.json /root/.kaggle/kaggle.json
RUN chmod 600 /root/.kaggle/kaggle.json

RUN mkdir /project
WORKDIR /project
COPY data_loader.py .
