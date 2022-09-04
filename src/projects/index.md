projects
=======

2022
---------

**inline-website** (2/2022 - 5/2022)

:   1. python
    2. mustache

:   static website generator python script with no special directory structure (all files are inline)

:   supports mustache templates, markdown, yml

:   [source](https://griffinht.com/git/inline-website.git/) [example (this page)](https://griffinht.com/git/griffinht.com.git/tree/src/projects)

>

**Ednotes** (1/2022 - 4/2022)

:   1. html
    2. css
    3. typescript
    4. docker

:   timestamp base interactive video note taking app

:   lightweight static frontend with no dependencies

:   [source](https://griffinht.com/git/ednotes.git/) todo demo

2021
----------

**ip-server** (11/2021 - 12/2021)

:   1. rust
    2. networking
    3. http
    4. docker

:   Toy Rust server and client CLI which returns the client's IPv4 or IPv6 address over HTTP/1.1, implemented with low level blocking networking with the Rust standard library

:   simple server that returns client ip addresss `docker run --rm stzups/ip-server -c griffinht.com:38234`

:   [source](https://griffinht.com/git/ip-server.git/)

:   [demo](http://griffinht.com:38234)

>

**dockron** (9/2021 - 11/2021)

:   1. rust
    2. docker

:   simple process scheduler/repeater, like cron but easy to use in Docker containers

:   [source](https://griffinht.com/git/dockron.git/)

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

**home-fastled-controller** (2/2020 - 3/2020)

:   1. arduino
    2. c
    3. fastled
    4. ws281018b
    5. soldering

:   programmed an arduino using the FastLED library to control several custom soldered strips of individually addressable RGB led strips with various patterns.

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


2020
-----------

**Debian (Linux)**

:   installed Debian on computer, used daily ever since then

>

**Strawberryizer** (8/2020 - 9/2020)

:   1. c++
    2. dlib
    3. opencv
    4. winsock

:   Simple C++ program which uses dlib and OpenCV to perform facial recognition to overlay a strawberry image on a subject's face

>

**truck cake thrower game** (5/2020 - 6/2020)

:   1. html
    2. css
    3. javascript

:   ljkdhsfg

>


**SpaceGame** (5/2020 - 7/2020)

:   1. c++
    2. direct3d
    3. win32

:   sdf

>

**Tanks** (3/2020 - 8/2020)

:   1. java
    2. blocking sockets
    2. http
    3. websockets
    4. javascript

:   Java server with fully custom HTTP/1.1 and WebSocket server implementations using blocking Java sockets with no external dependencies

:   2D real time multiplayer browser game where each client controls a tank which they may shoot and destroy other tanks

2019
-----------

**BeaconProtect** (9/2019 - 2/2020)

:   1. java
    2. maven
    3. git

:   minecraft bukkit plugin, my first big java project

2017
-------------------

**Minecraft Generator** (5/2017)

:   1. javascript

:   Originally hosted on https://lemonpickles.net/generator, then https://stzups.net/generator

:   [reddit](https://www.reddit.com/r/Minecraft/comments/6bznqx/remember_111_chat_limit_is_op_i_made_a_copypaste/) [forum](https://hypixel.net/threads/forge-1-8-9-256chat-mod-v1-1b-now-actually-starts-up-edition.1959635/#post-14848866)

**ball game**

**fakevirus**

**the random game**

2014
--------------

**CodeAcademy**

:   1. javascript
    2. html
    3. css

:   self taught javascript through free online course

2013
----------

**System Administrator**

:   1. dynamic ip

:   managed several instance of Minecraft servers for use by my friends and I

:   responsible for loading maps, keeping software running and up to date

**Windows 7**

:   minecraft

2011
--------------

**Windows Vista**

:   web games (monkeyquest)

2009
-----------------


**Windows XP**

:   experience with ms word, cd-rom games
