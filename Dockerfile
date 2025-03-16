FROM python:3.12-slim

RUN apt-get update && apt-get install -y make

RUN pip install --upgrade pip && pip install uv

WORKDIR /code
COPY . /code/

RUN uv sync


CMD ["echo", "done"]
