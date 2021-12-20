FROM node as build

WORKDIR /usr/src
# see .dockerignore
COPY . .
RUN make

FROM scratch

COPY --from=build /usr/src/build/ /griffinht.com/
