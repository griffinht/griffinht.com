What dependencies does recrobbled require?
Ubuntu, and wahtever is in `libdbus-1-dev` and `dbus` todo link to those packages?

https://github.com/InputUsername/rescrobbled/blob/master/.github/workflows/ci.yml



Looks like we need `pkg-config`
todo chatgpt generated?

https://guix.gnu.org/manual/en/html_node/Invoking-guix-import.html#Invoking-guix-import
`guix import rescrobbled`
```
$ guix import crate rescrobbled > rescrobbled.scm
$ guix build -f todo
module not found
recursive import
```

``` sh
$ guix import --recursive rescrobbled
$ guix build -f todo
--- stderr
  pkg_config failed: Could not run `PKG_CONFIG_ALLOW_SYSTEM_CFLAGS="1" PKG_CONFIG_ALLOW_SYSTEM_LIBS="1" "pkg-config" "--libs" "--cflags" "dbus-1" "dbus-1 >= 1.6"`
  The pkg-config command could not be found.

  Most likely, you need to install a pkg-config package for your OS.
  Try `apt install pkg-config`, or `yum install pkg-config`,
  or `pkg install pkg-config`, or `apk add pkgconfig` depending on your distribution.

  If you've already installed it, ensure the pkg-config command is one of the
  directories in the PATH environment variable.

  If you did not expect this build to link to a pre-installed system library,
  then check documentation of the libdbus-sys crate for an option to
  build the library from source, or disable features or dependencies
  that require pkg-config.
  One possible solution is to check whether packages
  'libdbus-1-dev' and 'pkg-config' are installed:
  On Ubuntu:
  sudo apt install libdbus-1-dev pkg-config
  On Fedora:
  sudo dnf install dbus-devel pkgconf-pkg-config

  thread 'main' panicked at /tmp/guix-build-rust-rescrobbled-0.7.1.drv-0/rescrobbled-0.7.1/guix-vendor/rust-libdbus-sys-0.2.5.tar.gz/build.rs:25:9:
  explicit panic
  note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

```sh
$ guix search pkg-config
name: pkg-config
version: 0.29.2
outputs:
+ out: everything
systems: x86_64-linux i686-linux
dependencies: 
location: gnu/packages/pkg-config.scm:39:2
homepage: https://www.freedesktop.org/wiki/Software/pkg-config
license: GPL 2+
synopsis: Helper tool used when compiling applications and libraries  
description: pkg-config is a helper tool used when compiling applications and libraries.  It helps you insert the correct compiler options on the command line
+ so an application can use gcc -o test test.c `pkg-config --libs --cflags glib-2.0` for instance, rather than hard-coding values on where to find glib (or
+ other libraries).  It is language-agnostic, so it can be used for defining the location of documentation tools, for instance.
relevance: 39
```

`rescrobbled.scm`
```scheme
(define-module (...)
               #:use-module (gnu packages pkg-config)
...
(define-public rust-rescrobbled-0.7
  (package
    (inputs (list pkg-config))
```

```sh
$ guix build -f todo
--- stderr
  pkg_config failed: `PKG_CONFIG_ALLOW_SYSTEM_CFLAGS="1" PKG_CONFIG_ALLOW_SYSTEM_LIBS="1" PKG_CONFIG_PATH="/gnu/store/gr0sy0m1mv36qv54idm6cn10l3mngshq-file-5.44/lib/pkgconfig:/gnu/store/6k1yys9wqrfn4y41ic1win8gpnimncwj-xz-5.2.8/lib/pkgconfig" "pkg-config" "--libs" "--cflags" "dbus-1" "dbus-1 >= 1.6"` did not exit successfully: exit status: 1
  error: could not find system library 'dbus-1' required by the 'libdbus-sys' crate

  --- stderr
  Package dbus-1 was not found in the pkg-config search path.
  Perhaps you should add the directory containing `dbus-1.pc'
  to the PKG_CONFIG_PATH environment variable
  No package 'dbus-1' found
  Package dbus-1 was not found in the pkg-config search path.
  Perhaps you should add the directory containing `dbus-1.pc'
  to the PKG_CONFIG_PATH environment variable
  No package 'dbus-1' found

  One possible solution is to check whether packages
  'libdbus-1-dev' and 'pkg-config' are installed:
  On Ubuntu:
  sudo apt install libdbus-1-dev pkg-config
  On Fedora:
  sudo dnf install dbus-devel pkgconf-pkg-config

  thread 'main' panicked at /tmp/guix-build-rust-rescrobbled-0.7.1.drv-0/rescrobbled-0.7.1/guix-vendor/rust-libdbus-sys-0.2.5.tar.gz/build.rs:25:9:
  explicit panic
  note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

todo add dbus
```sh
$ guix search dbus
...
```

`rescrobbled.scm`
```scheme
(define-public rust-rescrobbled-0.7
  (package
    (inputs (list pkg-config dbus))
```

```sh
$ guix build -f todo
  run pkg_config fail: `PKG_CONFIG_ALLOW_SYSTEM_CFLAGS="1" PKG_CONFIG_PATH="/gnu/store/b4gf6y18w69hlkp030napxr25hnbdgyf-dbus-1.14.0/lib/pkgconfig:/gnu/store/gr0sy0m1mv36qv54idm6cn10l3mngshq-file-5.44/lib/pkgconfig:/gnu/store/6k1yys9wqrfn4y41ic1win8gpnimncwj-xz-5.2.8/lib/pkgconfig" "pkg-config" "--libs" "--cflags" "openssl"` did not exit successfully: exit status: 1
  error: could not find system library 'openssl' required by the 'openssl-sys' crate

  --- stderr
  Package openssl was not found in the pkg-config search path.
  Perhaps you should add the directory containing `openssl.pc'
  to the PKG_CONFIG_PATH environment variable
  No package 'openssl' found


  --- stderr
  thread 'main' panicked at /tmp/guix-build-rust-rescrobbled-0.7.1.drv-0/rescrobbled-0.7.1/guix-vendor/rust-openssl-sys-0.9.93.tar.xz/build/find_normal.rs:190:5:


  Could not find directory of OpenSSL installation, and this `-sys` crate cannot
  proceed without this knowledge. If OpenSSL is installed and this crate had
  trouble finding it,  you can set the `OPENSSL_DIR` environment variable for the
  compilation process.

  Make sure you also have the development packages of openssl installed.
  For example, `libssl-dev` on Ubuntu or `openssl-devel` on Fedora.

  If you're in a situation where you think the directory *should* be found
  automatically, please open a bug at https://github.com/sfackler/rust-openssl
  and include information about your system as well as this message.

  $HOST = x86_64-unknown-linux-gnu
  $TARGET = x86_64-unknown-linux-gnu
  openssl-sys = 0.9.93


  note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

```sh
$ guix search openssl
name: openssl
version: 3.0.8
outputs:
+ doc: documentation
+ static: static libraries
+ out: everything else
systems: x86_64-linux i686-linux
dependencies: perl@5.36.0
location: gnu/packages/tls.scm:602:2
homepage: https://www.openssl.org/
license: ASL 2.0
synopsis: SSL/TLS implementation  
description: OpenSSL is an implementation of SSL/TLS.
relevance: 32
...
```

There are several different versions and outputs of `openssl`. Which one to choose? I would guess we might only need the static libraries, but I'm not quite sure. 

Let's look at the actual package definition. [`guix edit`](manual) will 

```sh
$ guix edit openssl
```

[`gnu/packages/tls`](todo link)
```scheme
(define-public openssl-3.0
  (package
    (inherit openssl-1.1)
    (version "3.0.8")
...
```

`rescrobbled.scm`
```scheme
(define-module (...)
               #:use-module (gnu packages tls)
...
(define-public rust-rescrobbled-0.7
  (package
    (inputs (list pkg-config dbus openssl-3.0)) ; todo pick specific output of openssl?
```


That was so much work! How come we can't just `cargo install`?

How does `cargo` get packages? But Guix also has binaries! But they are fully reproducible, read more
