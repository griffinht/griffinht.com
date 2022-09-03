projects
=======

2022
---------

**Scribbleshare** (12/2020 - 5/2021)

:   1. test
    2. test2
    3. test3


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
