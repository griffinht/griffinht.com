FROM python as build

WORKDIR /usr/src

COPY . .
RUN pip install asyncinotify chevron pyyaml && ./scripts/build.py --output build src

FROM scratch

COPY --from=build /usr/src/build/ /griffinht.com/
