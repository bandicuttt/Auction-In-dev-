FROM python:3

ENV PYTHONUNBUFFERED 1
ENV PYTHONUNBUFFERED 1
SHELL [ "/bin/bash", "-c" ]
WORKDIR /app
COPY . /app
RUN pip install -r req.txt