FROM toolbelt/mustache as build

USER root

WORKDIR /usr/src

COPY src src
COPY build.sh .
RUN ./build.sh

FROM scratch

COPY --from=build /usr/src/build/ /griffinht.com/
