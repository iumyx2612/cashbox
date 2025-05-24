# Using a slim version for a smaller base image
FROM python:3.12-slim-bullseye

RUN apt-get update \
    && apt-get install libmagic1 swig wget -y \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip 

# copy cores/requirements.txt to /app/requirements.txt
COPY cores/requirements.txt /app/requirements.txt

# install requirements
RUN pip install --no-cache-dir -r /app/requirements.txt --timeout 200

WORKDIR /app

COPY cores/ /app/
