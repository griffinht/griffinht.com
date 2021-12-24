<<<<<<< HEAD
default: init build
.PHONY: build # otherwise Make will relate the build target to the build output directory and won't run the build target

# install build dependencies
init:
	./init.sh
# spin up docker image of nginx at http://localhost:8080 and watch src/ to rebuild on changes
# you will probably also want to disable browser cache
develop: build
	./develop.sh
build:
	./build.sh
clean:
	rm -rf build
=======
default:
>>>>>>> 715cf1fe0a6fceacdf7b74bb904c811cd0e60741
docker:
	docker build --tag stzups/griffinht.com:latest .
