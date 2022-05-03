FROM griffinht/inline-website as build

WORKDIR /usr/src

COPY src src

RUN inline-website.py --output build src

FROM scratch

COPY --from=build /usr/src/build/ /griffinht.com/
