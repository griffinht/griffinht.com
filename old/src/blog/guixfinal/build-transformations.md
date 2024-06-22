http://futurile.net/2023/12/05/guix-package-transformations/

### Using the Guix REPL

1. Start the Guix REPL:

```shell
guix repl
```

2. Load the required modules and define your custom package:

```scheme
(use-modules (gnu packages)
             (guix packages)
             (guix transforms))

(define custom-package
  (package
    (inherit (specification->package "existing-package-name"))
    (arguments
     (substitute-keyword-arguments (package-arguments (specification->package "existing-package-name"))
       ((#:configure-flags flags)
        `("--your-custom-flag" ,@flags))))))

;; Now you can build your custom package
(build-package custom-package)
```

Please replace `"existing-package-name"` with the actual name of the package and `--your-custom-flag` with your desired configure flag.

### Using a Manifest File

1. Create a file

temp）lets say existing package already has some configure flags in a list how can i simply add one to that list does thi accomplish that
Apologies for any confusion earlier. If you want to simply add a custom `configure` flag to an existing list of flags for a given package, you will want to make use of the `package` inheritance and `substitute-keyword-arguments` function to modify the `arguments` field of the package definition.

Here is a more detailed example, showing how you could add a custom flag with Guix's Scheme API, specifically in a case where the existing package already has some configure flags:

```scheme
(use-modules (guix packages) (guix utils) (guix git-download) (guix build-system gnu))

(define original-package ; Replace with the original package name
  ;; Assuming we get the original package from the collection of packages
  ;; This could be (gnu packages xxx) where xxx is the package module
  (specification->package "original-package-name"))

(define custom-package
  (package
    (inherit original-package)
    (name "custom-package-name") ; Optional: give a new name to your custom-package
    (arguments
      ;; We modify existing 'arguments' field
      (substitute-keyword-arguments (package-arguments original-package)
        ((#:configure-flags existing-flags)
         ;; Append your custom flag to the existing list of flags
         (cons "--your-custom-flag" existing-flags))))))

;; Now you can build custom-package
(use-modules (guix))
(package->derivation %store custom-package)
```



wow! thats how we can build in the repl! epic!



Today I was using `nginx` as a web server, and I wanted to use the `auth_request` directive.

Turns out the `auth_request` directive is part of the [`ngx_http_auth_request_module`](https://nginx.org/en/docs/http/ngx_http_auth_request_module.html).

Too bad the Guix packagers decided not to include my module in their build of `nginx`. I know from experience that the [official `nginx` Docker image]() does come with this module compiled, so I guess I will have to abandon Guix and use that instead.

Just kidding! I'll make my own `nginx`! Package transformation options to the rescue!

```sh
$ guix shell nginx --with-configure-flag=nginx=--with-http_auth_request_module
```

To make this declarative, I can define what I just did in a manifest file (todo link to docs)


## original manifest

I can generate a simple manifest for the unmodified `nginx` with `guix shell --export-manifest`

```sh
$ guix shell nginx --export-manifest
```

`manifest.scm`
```scheme
(specifications->manifest (list "nginx"))
```

## modified manifest

I don't recall the syntax for adding a package transformation like this to a manifest file, so I will let `guix shell --export-manifest` do the work

```sh
$ guix shell nginx --with-configure-flag=nginx=--with-http_auth_request_module --export-manifest
```

`manifest.scm`
```
(use-modules (guix transformations))

(define transform1
  (options->transformation
    '((with-configure-flag
        .
        "nginx=--with-http_auth_request_module"))))

(packages->manifest
  (list (transform1 (specification->package "nginx"))))
```

I can then pass this manifest to `guix shell` (or many other Guix commands):

```sh
$ guix shell --manifest=manifest.scm
```

That's it!

## updating the package

Looks like our `nginx` package is running version v2.blah. I'd like to update to a more recent version - todo

# the docker way

this seems to be non trivial with docker - for example, this user was trying to add brotli
brotli is a dynamic module - different procedure! find an example with a static module
https://github.com/nginxinc/docker-nginx/issues/332

# the debian way

how can I do this in debian?

# the gentoo way?

these package transformations seem like they might be awfully similar to Gentoo's USE flags - are they? idk




todo email futurile person telling them how i used configure flags with nginx
