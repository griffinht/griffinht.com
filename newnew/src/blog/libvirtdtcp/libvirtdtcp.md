https://wiki.libvirt.org/Libvirt_daemon_is_not_listening_on_tcp_ports_although_configured_to.html
# Connecting to libvirt remotely via TCP

This guide assumes `systemd` will not be used.



- note that libvirt can't auto spawn daemons? idk!


## Client configuration

By default, tools such as `virsh` will attempt to connect to the local system. We want to configure them to connect to a remote server which will be set up later. We will accomplish this by modifying the libvirt connection URI.

## Connection URI [docs](https://libvirt.org/uri.html)

https://libvirt.org/uri.html#tcp-transport

We want to use `tcp` transport. We could use `tls`, but this would require managing TLS certificates [docs](https://wiki.libvirt.org/TLSSetup.html). This is unnecessary if the network is trusted. Personally, I will be having `libvirtd` bind to a WireGuard network interface to only allow remote access via WireGuard todo.

```
virsh --connect tcp://hostname/session
error: failed to connect to the hypervisor
error: Cannot read CA certificate '/etc/pki/CA/cacert.pem': No such file or directory
```

Per the [wiki](https://wiki.libvirt.org/Failed_to_connect_to_the_hypervisor.html#cannot-read-ca-certificate), we need to add `qemu` to our connection URI.


```
virsh --connect qemu+tcp://hostname/session
error: failed to connect to the hypervisor
error: unable to connect to server at 'hostname:16509': Connection refused
```

It works! Now we need to start `libvirtd` on the server.

## Server configuration

## `libvirt/libvirtd.conf` reference

I initially had trouble finding this elusive configuration file. It is frequently mentioned across various libvirt documentation pages, but the only reference I could find was this GitHub gist:

https://gist.github.com/rmohr/355404d84bc27d639927f585a95a85ed

The full documentation is available here, on the [Remote support](https://libvirt.org/remote.html) page of the libvirt documentation.

The configuration file is here:

```
$ libvirtd --listen
2024-05-04 16:10:24.116+0000: 30547: info : libvirt version: 8.6.0
2024-05-04 16:10:24.116+0000: 30547: info : hostname: hypervisor
2024-05-04 16:10:24.116+0000: 30547: error : virNetTLSContextCheckCertFile:105 : Cannot read CA certificate '/etc/pki/CA/cacert.pem': No such file or directory
```

`~/.config/libvirtd/libvirtd.conf`
```
listen_tls = 0
```
```
$ libvirtd --listen
2024-05-04 16:19:03.552+0000: 30608: info : libvirt version: 8.6.0
2024-05-04 16:19:03.552+0000: 30608: info : hostname: hypervisor
```

This works, but a look at `ss -tupln` will reveal that the daemon did not actually listen on any TCP port.

We need to also configure the daemon to listen via TCP:

`~/.config/libvirtd/libvirtd.conf`
```
listen_tcp = 1
```

This works. The default port is 16509 and the default interface is `0.0.0.0`. Both of these can be configured as follows:

`~/.config/libvirtd/libvirtd.conf`
```
tcp_port = "16509"
listen_addr = "0.0.0.0"
```

Interestingly, the `listen_addr` does not appear to be documented with all the other options on the [Remote support](https://libvirt.org/remote.html) page.

## Connecting to the server via the client

```
virsh --connect qemu+tcp://hostname/session
error: failed to connect to the hypervisor
error: authentication failed: Failed to start SASL negotiation: -1 (SASL(-1): generic failure: GSSAPI Error: No credentials were s
```

By default, `libvirtd` uses SASL authentication. This can be disabled with the `auth_tcp` option. Other values for this option are documented here

`~/.config/libvirtd/libvirtd.conf`
```
auth_tcp = "none"
```

Don't forget to restart the daemon to pick up the new config changes (or send a SIGHUP signal i think?), and everything should work (probably).

# Caveats

Attempting to open the graphical console in `virt-manager` yields the following error:
```
Error connecting to graphical console:
Guest is on a remote host with transport 'tcp' but is only configured to listen locally. To connect remotely you will need to change the guest's listen address.
```

# TLDR

todo link to libvirt config file locations

`~/.config/libvirtd/libvirtd.conf`
```
listen_tls = 0 # default: 1
listen_tcp = 1 # default: 0
#listen_addr = "0.0.0.0"
#tls_port = "16509"
auth_tcp = "none" # default: SASL
```

I'm still not quite sure where all of these options are documented, but this seems to work so :shrug:
