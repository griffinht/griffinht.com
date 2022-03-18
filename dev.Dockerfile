FROM python:alpine

WORKDIR /app

COPY scripts/ scripts/
RUN ./scripts/install.sh

ENTRYPOINT ["sh", "-c", "rm -rf build/* && ./scripts/build.py --output build src && ./scripts/build.py --watch --output build src"]
