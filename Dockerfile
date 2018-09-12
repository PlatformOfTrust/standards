FROM frolvlad/alpine-python3

RUN apk add --update --no-cache \
    python3-dev \
    build-base \
    linux-headers

ADD . /src
WORKDIR /src

RUN chmod +x build.sh && chmod +x docker-run.sh && chmod +x setup.sh && ./setup.sh

RUN apk del \
    python-dev \
    build-base \
    linux-headers

