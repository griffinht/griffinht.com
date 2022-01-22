FROM node as build

RUN npm install html-minifier -g;

WORKDIR /usr/src
# see .dockerignore
COPY . .
RUN make build

FROM scratch

COPY --from=build /usr/src/build/ /griffinht.com/
