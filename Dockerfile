FROM python:3.7-alpine

# Installing necessary components
RUN apk update
RUN apk add musl-dev build-base mariadb-dev linux-headers bash jpeg-dev zlib-dev
RUN python -m pip install --upgrade pip

COPY . /central-de-ajuda-rs/
WORKDIR /central-de-ajuda-rs/central_de_ajuda/

RUN pip install -r ../requirements.txt