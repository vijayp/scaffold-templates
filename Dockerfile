FROM python:3.8

# Create app directory
WORKDIR /app

RUN apt-get -y update && apt-get -y upgrade && apt-get -y install nodejs

# Install app dependencies
COPY Makefile py ./

RUN make setup

EXPOSE 5000
CMD cd py && . venv/bin/activate && python3 ____PROGRAM_webserver.py
