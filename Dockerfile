FROM griffinht/inline-website as build

# todo why /usr/src instead of any other directory
WORKDIR /usr/src

COPY src src

RUN inline-website.py --output build src

# broken link checker
FROM lycheeverse/lychee

WORKDIR /build

COPY --from=build /usr/src/build .

# check offline
RUN lychee /build --offline 

# then check online
RUN lychee /build

FROM scratch

COPY --from=build /usr/src/build/ /griffinht.com/
