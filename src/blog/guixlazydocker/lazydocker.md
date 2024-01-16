# Building from source with `go`

# Using the prebuilt binaries

Thankfully, `lazydocker` provides prebuilt binaries that we can use. Installation is as simple as picking the binary release from the [releases](https://github.com/jesseduffield/lazydocker/releases).

```sh
$ curl https://github.com/jesseduffield/lazydocker/releases/download/v0.23.1/lazydocker_0.23.1_Linux_x86_64.tar.gz -OL
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100 4396k  100 4396k    0     0  10.2M      0 --:--:-- --:--:-- --:--:-- 10.2M
$ tar -xf lazydocker_0.23.1_Linux_x86_64.tar.gz
$ ./lazydocker
```

Easy as pie.

# Guix: packaging prebuilt binaries

What if we wanted to automate the process of downloading these prebuilt binaries?

I'm going to write a package brief definition based on section [9.2 Defining Packages](https://guix.gnu.org/manual/en/html_node/Defining-Packages.html) of the manual.

`lazydocker.scm`
```scheme
(use-modules
  (guix packages))

(package
  (name "lazydocker")
  (version "0.23.1")
  (source (local-file "lazydocker_0.23.1_Linux_x86_64.tar.gz"))
  (build-system copy-build-system)
  (synposis "A simple terminal UI for docker, written in Go")
  (license mit)
  (home-page "https://github.com/jesseduffield/lazydocker/"))
```

https://guix.gnu.org/cookbook/en/html_node/Getting-Started.html
todo dont include all this boilerplate

`lazydocker.scm` is a Scheme file which evaluates to a `package`, as defined by 

`package` is a data type which represents a package recipe, per section [9.2.1 `package` reference](https://guix.gnu.org/manual/en/html_node/package-Reference.html) of the manual. The `package` data type is defined in the `(guix packages)` module ([source](todo). I have defined several fields for this data type, such as `name`, `version`, `source`, and more.

`source` is a "file-like" object. I'm using the `local-file` procedure to return an object representing the file we downloaded earlier via `curl`. In scheme, a procedure is basically a function which can be evaluated to return a result. For example: todo

> the following procedures return "file-like" objects: `local-file`, `plain-file`, `computed-file`, `program-file`, and `scheme-file` per section [9.12 G-Expressions](https://guix.gnu.org/manual/en/html_node/G_002dExpressions.html) of the manual. check out the `plain-file` procedure if you want to represent a file called `fake_file` with file contents `this is not a real file`: `(plain-file "fake_file" "this is not a real file")` todo how did i know to pass strings instead of objects or 'symbols

Want to learn more about all this stuff? tood link

I will explain what everything means soon. For now, let's try building it using `guix build`todo ref:
```sh
$ guix build -f lazydocker.scm
/lazydocker.scm:8:11: error: local-file: unbound variable
hint: Did you forget `(use-modules (guix gexp))'?
```

# todo pop this in a article?

todo how to get all the licenses? without reading the docs or reading the source?

Guix is complaining that `local-file` is an "unbound variable". What does that mean? [here](https://www.cs.cmu.edu/Groups/AI/html/r4rs/r4rs_5.html).

We are missing the `local-file` variable from the *environment*. We could fix this by evaluating `(define local-file "asdf")`, which would add `local-file` to the environment as a variable with the string value "asdf" string literal todo, but that isn't what we want.

The `(guix gexp)` module [source](todo source code) defines the `local-file` variable as a procedure which returns a "file-like" object given a path, which is what we were expecting.

The error "local-file: unbound variable" was caused by me forgetting to import the Guix module todo is this a guix module? or a scheme module? link to use-modules docs. I can fix it by appending `(guix gexp)` to the arguments of the `(use-modules)` procedure. todo what is (guix gexp) is it a symbol? what is guix?

```scheme
(use-modules
  (guix packages)
  (guix gexp))
```

Let's try again:

```sh
$ guix build -f lazydocker.scm
lazydocker.scm:5:0: error: (package (name "lazydocker") (version "0.23.1") (source (origin (uri "https://github.com/jesseduffield/lazydocker/releases/download/v0.23.1/lazydocker_0.23.1_Linux_x86_64.tar.gz") (method url-fetch) (sha256 (base32 "")))) (build-system copy-build-system) (synposis "A simple terminal UI for docker, written in Go") (license mit) (home-page "https://github.com/jesseduffield/lazydocker/")): extraneous field initializers (synposis)
```

Looks like I misspelled `synposis` as `synposis`, resulting in the "extraneous field initializers (synposis)" error message. Let's try again with the typo corrected:

```sh
$ guix build -f lazydocker.scm
 error: (package (name "lazydocker") (version "0.23.1") (source (origin (uri "https://github.com/jesseduffield/lazydocker/releases/download/v0.23.1/lazydocker_0.23.1_Linux_x86_64.tar.gz") (method url-fetch) (sha256 (base32 "")))) (build-system copy-build-system) (synopsis "A simple terminal UI for docker, written in Go") (license mit) (home-page "https://github.com/jesseduffield/lazydocker/")): missing field initializers (description)
```

I forget to define the `description` field of the `package` data type, resulting in the "missing field initializers (description)" error message. Let's fix that:

`lazydocker.scm`
```sh
(use-modules
  (guix packages)
  (guix download))

(package
  (name "lazydocker")
  (version "0.23.1")
  (source (local-file "lazydocker_0.23.1_Linux_x86_64.tar.gz"))
  (build-system copy-build-system)
  (synopsis "A simple terminal UI for docker, written in Go")
  (description "")
  (license mit)
  (home-page "https://github.com/jesseduffield/lazydocker/"))
```

I'm going to leave the description blank for now.

> the `description` field also supports Texinfo syntax! todo example?

For reference, the `package` data type defines the fields which show up in `guix search <query>` and `guix show <package>` [web version hello example](https://packages.guix.gnu.org/packages/hello/2.12.1/).

Most of these fields should look fairly straightforward. Compare this to a JSON definition:
todo show that guix build json thing?
I'm also using the `copy-build-system` here, which todo


Let's build:

```sh
$ guix build -f lazydocker.scm
lazydocker.scm:8:10: error: (build-content-hash #vu8() sha256): invalid content hash length
```
Guix has a much better way:

```sh
$ guix gc --delete /gnu/store/24cpfmqfck2kzq4yznxwhimxawrmvn84-lazydocker_0.23.1_Linux_x86_64.tar.gz
finding garbage collector roots...
removing stale link from `/var/guix/gcroots/auto/nv8x4cxd01gjxkz1kw8ghv6liqyz2bq7' to `/home/griffin/.cache/guix/profiles/xxaobt7czsacqyzdnnmfmiz3z7hpcxvcpu365hiq5qjlqqkxtxha'
[0 MiB] deleting '/gnu/store/24cpfmqfck2kzq4yznxwhimxawrmvn84-lazydocker_0.23.1_Linux_x86_64.tar.gz'
deleting `/gnu/store/trash'
deleting unused links...
note: currently hard linking saves 32106.59 MiB
```

todo talk about auto version updates by getting download from version



inspecting the build files guix build | xargs lf
moving files around
document all these pahses?
```
starting phase `validate-runpath'
validating RUNPATH of 1 binaries in "/gnu/store/ldzbbf9dayv8awxsbz08p2p0nrlpajjr-mitmproxy-10.20.0/bin"...
/gnu/store/ldzbbf9dayv8awxsbz08p2p0nrlpajjr-mitmproxy-10.20.0/bin/mitmdump: error: depends on 'libz.so.1', which cannot be found in RUNPATH ()
error: in phase 'validate-runpath': uncaught exception:
misc-error #f "RUNPATH validation failed" () #f 
phase `validate-runpath' failed after 0.0 seconds
Backtrace:
           8 (primitive-load "/gnu/store/k0cqlhvk7bdqyizri2n9c3wjq8m…")
In guix/build/gnu-build-system.scm:
    908:2  7 (gnu-build #:source _ #:outputs _ #:inputs _ #:phases . #)
In ice-9/boot-9.scm:
  1752:10  6 (with-exception-handler _ _ #:unwind? _ # _)
In srfi/srfi-1.scm:
    634:9  5 (for-each #<procedure 7ffff77b3440 at guix/build/gnu-b…> …)
In ice-9/boot-9.scm:
  1752:10  4 (with-exception-handler _ _ #:unwind? _ # _)
In guix/build/gnu-build-system.scm:
   929:23  3 (_)
   570:10  2 (validate-runpath #:validate-runpath? _ # _ #:outputs _)
In ice-9/boot-9.scm:
  1685:16  1 (raise-exception _ #:continuable? _)
  1685:16  0 (raise-exception _ #:continuable? _)

ice-9/boot-9.scm:1685:16: In procedure raise-exception:
RUNPATH validation failed
builder for `/gnu/store/hjxcill4vz2ppss601d67kivl9azgfad-mitmproxy-10.20.0.drv' failed with exit code 1
```
what if i wante dto ignore this phase and just use the system library! skip phase validate runpath
https://guix.gnu.org/manual/en/html_node/Build-Phases.html#phase_002dvalidate_002drunpath
`validate-runpath`
what if I can't find the Guix package and i just want to use my system package
```sh
$ ldd $(which mitmproxy)
	linux-vdso.so.1 (0x00007ffcdf7b3000)
	libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007f87bd26d000)
	libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007f87bd24e000)
	libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007f87bd249000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f87bd068000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f87bd280000)
```
looks like debian has everything we need
but this won't work everywhere - guix shell --container failed to load lib
where does debian get this stuff from? https://packages.debian.org/cgi-bin/search_contents.pl?word=libz.so.1&searchmode=searchfiles&case=insensitive&version=unstable&arch=i386%EF%BC%89%E3%80%82

(from guix build zlib, produces multiple outputs in the form of mutliple lines in stdout)
ls /gnu/store/ygm2rzg08w0w96h9587k3n2yvhndcqkn-zlib-1.2.13/lib

we added zlib but it still wont work! mitmproxy can't find the guix zlib
how does guix find packages in the first palce? with magical ldd stuff
    to fix: build from source or do some ld_libary hackery
LD_LIBRARY_PATH="$GUIX_ENVIRONMENT/lib" ldd $(which mitmproxy)

guix shell glibc -- ldd $(which mitmproxy) makes it use guix
talk about binary size

also mentuion how guix patches shebangs


what de hell is this? prop vs inputs vs nateive
Another example where propagated-inputs is useful is for languages that lack a facility to record the run-time search path akin to the RUNPATH of ELF files; this includes Guile, Python, Perl, and more. When packaging libraries written in those languages, ensure they can find library code they depend on at run time by listing run-time dependencies in propagated-inputs rather than inputs. 

copy-build-syustem . for all files
but also copies environment-variables which we dont want

# Guix: building from source `go`

> if we wanted to apply any custom patches to modify the source code, we would do that here with the `patches` field of the `origin` data type. neat!

# Guix: building from source with Guix

# Contribuiting to upstream

Now that we have a Guix package "the right way", we can contribute it to the official Guix channel.

todo lazygit!
