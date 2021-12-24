<<<<<<< HEAD
FROM node as build

WORKDIR /usr/src
# see .dockerignore
COPY . .
RUN make

FROM scratch

COPY --from=build /usr/src/build/ /griffinht.com/
=======
FROM scratch

COPY /src/ /griffinht.com/
>>>>>>> 715cf1fe0a6fceacdf7b74bb904c811cd0e60741
