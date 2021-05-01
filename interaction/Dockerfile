from ubuntu:20.04
#FROM python:3.8-alpine


#ENV TERM linux

run apt-get -qq update && apt-get install -qq --no-install-recommends netcat gcc libc-dev libffi-dev make python3-pip

#run apk update && apk add --no-cache netcat-openbsd bash
#run apk add gcc
#run apk add libc-dev
#run apk add libffi-dev
#run apk add make
COPY requirements.txt /
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt

#run apt-get install -qq --no-install-recommends vim

COPY exploit.py /
COPY check1.py /

