#!/bin/sh

set -e

# todo -enable-kvm
"$(guix system vm system.scm --persistent --no-graphic)" \
    -nic 'user,model=virtio-net-pci,hostfwd=tcp::2222-:22' \
