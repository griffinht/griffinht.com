default: docker
.PHONY: build # otherwise Make will relate the build target to the build output directory and won't run the build target

build:
	./build.sh
clean:
	rm -rf build
docker:
	docker build --tag stzups/griffinht.com:latest .
