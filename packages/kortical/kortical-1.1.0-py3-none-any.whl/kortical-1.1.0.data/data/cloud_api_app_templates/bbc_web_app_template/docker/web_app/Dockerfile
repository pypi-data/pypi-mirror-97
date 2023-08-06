# syntax=docker/dockerfile:experimental
FROM alpine:3.7

ENV LANG=en_GB.UTF-8
ENV LC_ALL=en_GB.UTF-8

RUN addgroup -S korticalgroup && adduser -S kortical -G korticalgroup

ENV PYTHONUNBUFFERED=1
RUN apk add --no-cache bash
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

ADD requirements.txt /data/requirements.txt
ADD . /data/bbc_web_app_template
RUN chown -R kortical /data
ADD docker/web_app/run-cmd.sh /usr/local/bin/run-cmd.sh
RUN chmod +x /usr/local/bin/run-cmd.sh

RUN mkdir -p /opt/kortical-cloud/venvs && \
    chown -R kortical /opt/kortical-cloud

USER kortical

RUN --mount=type=cache,target=$HOME/.cache/pip --mount=type=ssh \
    python3 -m venv /opt/kortical-cloud/venvs/app-venv && \
    . /opt/kortical-cloud/venvs/app-venv/bin/activate && \
    pip install -r /data/requirements.txt
