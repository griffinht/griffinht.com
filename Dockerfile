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
RUN lychee /build --no-progress --timeout 5 --exclude projects/html --offline 

# then check online
# linkedin excluded because of a very silly 999 status code
RUN lychee /build --no-progress --timeout 5 --exclude projects/html --exclude https://www.linkedin.com/in/griffinht

FROM scratch

COPY --from=build /usr/src/build/ /griffinht.com/
