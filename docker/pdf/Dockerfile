FROM ubuntu:latest

SHELL ["/bin/bash", "-c"]

RUN apt-get update \
&& apt-get -y install curl python3-pip unzip poppler-utils

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
&& unzip awscliv2.zip \
&& ./aws/install

RUN pip3 install pdf2image boto3 pathlib Pillow natsort

COPY ./app /opt/app

RUN chmod -R 755 /opt/app