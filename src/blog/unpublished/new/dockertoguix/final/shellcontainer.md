docker exec equivalent?

try something nsenter
https://guix.gnu.org/en/blog/2017/running-system-services-in-containers/
sudo nsenter --all --target 303630 --preserve-credentials /bin/sh

using nsenter with regular docker/podman
using nsenter without root
