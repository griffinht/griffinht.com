default: docker
.PHONY: build # otherwise Make will relate the build target to the build output directory and won't run the build target

clean:
	rm -r build
docker:
	docker build --tag griffinht/griffinht.com:latest .
