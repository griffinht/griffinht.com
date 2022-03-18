FROM python:alpine as build

WORKDIR /usr/src

COPY . .
RUN ./scripts/build.py --output build src

FROM scratch

COPY --from=build /usr/src/build/ /griffinht.com/
