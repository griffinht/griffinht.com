FROM python:alpine as build

WORKDIR /usr/src

COPY scripts/install.sh scripts/install.sh
RUN ./scripts/install.sh

COPY . .
RUN ./scripts/build.py --output build src

FROM scratch

COPY --from=build /usr/src/build/ /griffinht.com/
