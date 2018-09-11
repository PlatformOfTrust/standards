FROM frolvlad/alpine-oraclejdk8

ADD . /src
WORKDIR /src

RUN wget https://github.com/dgarijo/Widoco/releases/download/v1.4.5/widoco-1.4.5-jar-with-dependencies.jar -O /src/widoco.jar

