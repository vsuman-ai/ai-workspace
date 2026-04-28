FROM --platform=linux/amd64 python:3.10-slim-bookworm
RUN mkdir -p /root/.cache/pants
RUN mkdir -p /root/.cache/nce
