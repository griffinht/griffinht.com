Rescrobbled is a daemon written in Rust which works by using the [MPRIS](https://wiki.archlinux.org/title/MPRIS) D-Bus interface to detect your songs, scrobbling them to a Last.fm (or ListenBrainz) compatible service.

This can be used with Spotify's official client, a web browser, or even something like ncspot.

## ncspot

[ncspot](https://github.com/hrkfdn/ncspot) is a lightweight ncurses Spotify terminal client written in Rust using `librespot`. It is less intuitive than Spotify's native electron app but consumes much less memory.


Installing it on Debian is very straightforward. Extract the binary from https://github.com/hrkfdn/ncspot/releases to `/usr/local/bin/ncspot`, then open a terminal and run `ncspot`. The first run will prompt for credentials to a Spotify premium account.

### configuration

You will probably want volume normalization.
`~/.config/ncspot/config.toml`
```
volnorm = true
```
The rest of the configuration is documented at [https://github.com/hrkfdn/ncspot#configuration].

## rescrobbled

The rescrobbled binaries on GitHub were compiled with a version of `glib` than my Debian system did not have, so I have to compile from source.
Compiling is straightforward if you already have `cargo` installed.
Get the dev dependencies.
`sudo apt install libdbus-1-dev pkg-config libssl-dev`
And compile and install with `cargo`
`cargo install rescrobbled`

To use rescrobbled with Last.Fm, get an API account at [https://www.last.fm/api/account/create]. Only the `Application name` field is required, the rest of the fields can be left blank.
Then, play the lastfm-key and lastfm-secret.
`~/.config/rescrobbled/config.toml`
```
lastfm-key = "xxx"
lastfm-secret = "xxx"
```

After this, consider creating a `systemd` unit file so rescrobbled can run as a daemon in the background when the computer starts.
`~/.config/systemd/user/rescrobbled.service`
```
[Unit]
Description=An MPRIS scrobbler
Documentation=https://github.com/InputUsername/rescrobbled
Wants=network-online.target
After=network-online.target

[Service]
ExecStart=%h/.cargo/bin/rescrobbled

[Install]
WantedBy=default.target
```
Enable this new unit file with `systemctl --user enable rescrobbled.service`.
Then, restart the computer or try `systemctl --user start rescrobbled.service`.

Also consider configuring rescrobbled to avoid scrobbling everything that plays on the computer by only whitelisting music players.
`~/.config/rescrobbled/config.toml`
```
player-whitelist = [ "ncspot" ]
```
