FROM python as build

WORKDIR /usr/src

COPY src src
COPY scripts/ scripts/
RUN pip install asyncinotify chevron pyyaml && ./scripts/build.py --output build src

FROM scratch

COPY --from=build /usr/src/build/ /griffinht.com/
