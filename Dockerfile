FROM python:3.8

# Create app directory
WORKDIR /app

RUN apt-get -y update && apt-get -y upgrade && apt-get -y install nodejs

# Install app dependencies
COPY Makefile ./
COPY py ./py/
RUN find ./  
RUN make setup

EXPOSE 5000
CMD . venv/bin/activate && cd py && python3 ____PROGRAM_webserver.py
