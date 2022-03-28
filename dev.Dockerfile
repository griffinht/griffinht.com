FROM python:alpine

WORKDIR /app

COPY scripts/install.sh scripts/install.sh
RUN ./scripts/install.sh

ENTRYPOINT ["sh", "-c", "rm -rf build/* && ./scripts/build2.py --output build src && exit 0 && ./scripts/build.py --watch --output build src"]
