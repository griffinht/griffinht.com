#!/bin/sh

set -e

# todo -enable-kvm
# todo guix system image type docker
# experimental and currently needs root see invoking guix system sectyino of the manual
# could also just produce a regular docker image and be fine
#sudo "$(guix system container system.scm)"
#sudo "$(guix system container system.scm)"

# todo why can't this disable compression? or set the iamge tag? check out the underlying code!
# --network not necessary if the only service is guix??
image="$(guix system image --network --image-type=docker system.scm)"
echo "$image"
#image_id="$(docker load < /gnu/store/16vsnpjvpd8a4b2nwairk6h6fnkwc9iq-docker-image.tar.gz)"
#docker run --rm -it "$image_id"
