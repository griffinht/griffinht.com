#!/bin/sh

url="https://guix.griffinht.com"

# entrypoint can't be overridden interestingly
container="$(docker create guix)"
docker start "$container"
build() {
    cmd="$1"
    docker exec -it "$container" /run/current-system/profile/bin/bash --login -c "guix build --substitute-urls='$url' $cmd"
}

# wait for bootup
while ! build ''; do
    echo retrying in 1 second...
    sleep 1
done

echo connected
# todo remove
docker exec -it "$container" /run/current-system/profile/bin/bash --login -c "echo https 443/tcp > /etc/services"
time docker exec -it "$container" /run/current-system/profile/bin/bash --login -c "guix build --substitute-urls='$url' build sway"
docker rm --force "$container"
