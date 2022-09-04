projects
=======

2022
---------

**Ednotes**

:   1. html
    2. css
    3. typescript
    4. docker

:   ednotes is a project

:   [source](https://griffinht.com/git/ednotes.git/)

2021
----------

**dockron**

:   1. rust
    2. docker

:   simple task scheduler/repeater

:   [source](https://griffinht.com/git/dockron.git/)

>

**ip-server** (9/2020 - 10/2020)

:   1. rust
    2. networking
    3. http
    4. docker

:   Toy Rust server and client CLI which returns the client's IPv4 or IPv6 address over HTTP/1.1, implemented with low level blocking networking with the Rust standard library

:   simple server that returns client ip addresss `docker run --rm stzups/ip-server -c griffinht.com:38234`

:   [source](https://griffinht.com/git/ip-server.git/)

:   [demo](http://griffinht.com:38234)

>

**Personal home lab** (7/2/2021 - present)

:   1. docker
    2. docker-compose
    3. shell
    4. wireguard
    5. nfs
    6. restic
    7. prometheus
    8. grafana
    9. nginx
    10. letsencrypt

:   Over 30 unique Docker images deployed via docker compose running on an old laptop

    * Hardware provisioning: collection of dash (sh) and Bourne again (bash) shell scripts written to remotely install and configure a fresh minimal Debian Bullseye install

    * Networking: Hairpin NAT setup with MikroTik RouterOS

    * Remote Access: wireguard VPN tunnel provides secure remote access

    * File server: accessible via NFS, SMB, WebDAV, or web interface (gossa), with automated cloud backups to Backblaze B2 using restic

    * Monitoring: metrics collected via Prometheus, visualized via Grafana

    * Password manager: personal instance of VaultWarden for syncing passwords across my devices

    * Web server: nginx with auto renewing LetsEncrypt SSL certificates via acme.sh

        * griffinht.com: public website with a small blog and a git repository (cgit)

        * hot.griffinht.com: my personal collection of several internal web interfaces for personal use secured by Authelia

            * Services: monitoring dashboards (Grafana), metasearch engine (SearXNG), RSS feed reader (Miniflux), speedtest (LibreSpeed), photo viewer (PhotoPrism), household ERP (Grocy), as well as various alternative frontends for popular services (LibReddit, Invidious, Nitter, Rimgo, Quetre, and Scribe)

>

**Scribbleshare** (12/2020 - 5/2021)

:   1. java
    2. netty
    3. websockets
    4. typescript
    5. docker
    6. web security
    7. sql
    8. nginx
    9. gradle


:   Full stack interactive web app written from the ground up featuring complete user authentication

:   **Java HTTP backend** built with Netty framework

    * user/password authentication hashed with BCrypt, resistant against timing attacks

    * ephemeral/persistent session management via HTTP cookies using SHA256 hashed session identifiers
    
    * **HTML/CSS/TypeScript frontend** served to web browser by **Java HTTP Backend** via HTTP

        * lightweight

            * no external NPM dependencies

            * bundled/minified via rollup.js to static HTML/CSS/JavaScript (ES6)

        * built and served by backend via Dockerfile image

:   4k SLOC **Java WebSocket backend** used to synchronize whiteboard drawing between web clients in real time

    * custom binary protocol with hand-written serializers/deserializers

:   [source](https://griffinht.com/git/scribbleshare.git/)

>

**home-fastled-controller** (2/2020 - 3/2020)

:   programmed an arduino using the FastLED library to control several custom soldered strips of individually addressable RGB led strips with various patterns.

>

**Strawberryizer** (8/2020 - 9/2020)

:   1. c++
    2. dlib
    3. opencv
    4. winsock

:   Simple C++ program which uses dlib and OpenCV to perform facial recognition to overlay a strawberry image on a subject's face

>

**Tanks** (3/2020 - 8/2020)

:   Java server with fully custom HTTP/1.1 and WebSocket server implementations using blocking Java sockets with no external dependencies

:   2D real time multiplayer browser game where each client controls a tank which they may shoot and destroy other tanks

>

**truck cake thrower game**

:   1. html
    2. css
    3. javascript

:   ljkdhsfg

>



**SpaceGame**

:   1. c++
    2. direct3d
    3. win32

:   sdf

>

**Tanks**

:   1. java
    2. http
    3. websockets
    4. javascript

:   kljsdfg

>

**Minecraft Generator**

:   1. javascript

:   Originally hosted on https://lemonpickles.net/generator, then https://stzups.net/generator

:   [reddit](https://www.reddit.com/r/Minecraft/comments/6bznqx/remember_111_chat_limit_is_op_i_made_a_copypaste/) [forum](https://hypixel.net/threads/forge-1-8-9-256chat-mod-v1-1b-now-actually-starts-up-edition.1959635/#post-14848866)

**ball game**

**fakevirus**

**the random game**
