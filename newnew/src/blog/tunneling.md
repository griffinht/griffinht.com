Today I wanted to expose an NFS server I had set up on my NAS to a client. I could have wrangled with the built in layer 7 authentication methods which NFS provides, but this could get messy and insecure. Instead, I wanted to rely on something else

wireguard is great, but it is default open. When I connect two machines together via WireGuard, they will by default share all the services running on all their ports with each other - the client to the server and the server to the client! Additionally, if one machine has IP forwarding enabled (`net.ipv4.ip_forward=1`), then the other machine will be able to access everything the remote machine has access to!

This can be great for certain use cases. What if you want to access all the services running on a server from a remote machine? What about an entire LAN, or the whole internet? This is the classic use case of a VPN, which lends itself perfectly to something like WireGuard. This is how I connect my remote VPS to my homelab server. The connection allows the two machines to communicate as if they were physically connected to the same LAN. todo link to this setup. That's how I expose all the prometheus metric exporters on my remote VPS to my Prometheus server on my homelab. todo write post about status.griffinht.com

Compare this to a reverse proxy or SSH tunnel, where things are default closed.

How can I add access controls to WireGuard? What if I have a server and I only want to expose a service on a specific port to a remote machine? I could implement my own access controls using firewall rules, but this can get messy, especially when using Docker which mangles `iptables`.

features
mfa, audit logs, acls, user management

VPN
WireGuard - double pubkey auth, no ACL
zerotier
tailscale/headscale
    https://blog.patshead.com/2022/10/is-it-time-for-you-to-set-up-tailscale-acls.html
openziti/zrok?????/
netmaker
netbird
    https://docs.netbird.io/how-to/manage-network-access
yggraddsil
https://news.ycombinator.com/item?id=37142388


Tunnel
https://github.com/anderspitman/awesome-tunneling
cloudflare tunnels
    https://orth.uk/ssh-over-cloudflare
ssh
pagekite
ngrok


reverse proxy
nginx
ssh?




# use case: single service


# use case: many services

let's say i have a prometheus node exporter, ssh daemon and some other adminstrative things i want to expose all of which to an admin server

WireGuard is perfect!

But let's say I don't want to expose every single service - in this scenario my NAS has sensitive data, so I don't want to expose everything to the Prometheus server.

