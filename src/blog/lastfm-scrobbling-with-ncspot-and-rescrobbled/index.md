---
file_content: {{> ../article}}
file_extension: .html
title: Last.FM scrobbling with ncspot and rescrobbled
source: blog/lastfm-scrobbling-with-ncspot-and-rescrobbled/index.md
root: ../../
datetime: 2022-03-16
---

# so jk its actually after u put ur key in u log in then it makes a .config/rescrobbled/session file with a secret thingy then it doesnt ask again

[Rescrobbled](https://github.com/InputUsername/rescrobbled) is a daemon written in Rust which works by using the [MPRIS](https://wiki.archlinux.org/title/MPRIS) D-Bus interface to detect currently playing songs so they can be scrobbled to a [Last.fm](https://www.last.fm/) (or [ListenBrainz](https://listenbrainz.org/)) compatible service.

This can be used with Spotify's official client or something like [ncspot](https://github.com/hrkfdn/ncspot).

## ncspot

`ncspot` ([source](https://github.com/hrkfdn/ncspot)) is a lightweight [ncurses](https://invisible-island.net/ncurses/) Spotify terminal client written in Rust using `librespot`. It is less intuitive than Spotify's native electron app but consumes much less memory.


Installing it on Debian is very straightforward. Extract the binary from [hrkfdn/ncspot/releases](https://github.com/hrkfdn/ncspot/releases) to `/usr/local/bin/ncspot`, then open a terminal and run `ncspot`. The first run will prompt for credentials to a Spotify premium account.

### configuration

You will probably want volume normalization.

`~/.config/ncspot/config.toml`
```
volnorm = true
```
The rest of the configuration is documented at [hrkfdn/ncspot#configuration](https://github.com/hrkfdn/ncspot#configuration).

## rescrobbled

The [rescrobbled binaries](https://github.com/InputUsername/rescrobbled/releases) on GitHub were compiled with a version of `glib` that my Debian system did not have, so I had to compile from source.
Compiling is straightforward if `cargo` ([docs](https://doc.rust-lang.org/cargo/)) is installed.

First, install the dev dependencies.

```
sudo apt install libdbus-1-dev pkg-config libssl-dev
```

Then, compile and install rescrobbled using `cargo`.

```
cargo install rescrobbled
```

To use rescrobbled with Last.Fm, get an API account at [www.last.fm/api/account/create](https://www.last.fm/api/account/create). Only the `Application name` field is required, the rest of the fields can be left blank.

Submit the form, then copy the details of the new API account to the rescrobbled configuration.

`~/.config/rescrobbled/config.toml`
```
lastfm-key = "API key"
lastfm-secret = "Shared secret"
```

After this, consider creating a `systemd` unit file  so rescrobbled can run as a daemon in the background when the computer starts.

`~/.config/systemd/user/rescrobbled.service` ([source](https://github.com/InputUsername/rescrobbled/blob/master/rescrobbled.service))
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

Also consider configuring rescrobbled to avoid scrobbling potentially unwanted media that plays on the computer, like videos from a web browser. This can be accomplished by configuring the whitelist.

`~/.config/rescrobbled/config.toml`
```
player-whitelist = [ "ncspot" ]
```

The rescrobbled [README](https://github.com/InputUsername/rescrobbled/blob/master/README.md) also suggests using `playerctl` ([source](https://github.com/altdesktop/playerctl)) to determine a player's name for the whitelist.
```
sudo apt install playerctl
```
```
playerctl --list-all
```
