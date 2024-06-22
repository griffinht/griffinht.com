todo what does this mean This is the declarative counterpart of text-file. 

Notice how I mentioned `local-file` returns an object *representing* the file. Evaluating the expression `(local-file "example")` will perform no file I/O, nor will it check if the `example` file exists. This is similar to how in Java, the `File` object represents a file, and instantiating a file with `new File("file_name")` does not read the file or check that it exists. todo 

> new to `guix repl`? check out section [9.13 Invoking `guix repl`](https://guix.gnu.org/manual/en/html_node/Invoking-guix-repl.html) from the manual

Here is an example:

```sh
$ guix repl
GNU Guile 3.0.9
Copyright (C) 1995-2023 Free Software Foundation, Inc.

Guile comes with ABSOLUTELY NO WARRANTY; for details type `,show w'.
This program is free software, and you are welcome to redistribute it
under certain conditions; type `,show c' for details.

Enter `,help' for help.
scheme@(guix-user)> (local-file "example")
;;; <stdin>:1:1: warning: possibly unbound variable `local-file'
ice-9/boot-9.scm:1685:16: In procedure raise-exception:
error: local-file: unbound variable

Entering a new prompt.  Type `,bt' for a backtrace or `,q' to continue.
scheme@(guix-user) [1]> ,q
scheme@(guix-user)> (use-modules (guix gexp))
scheme@(guix-user)> (local-file "example")
$1 = #<<local-file> file: "example" absolute: #<promise #<procedure 1280680 at <unknown port>:4:0 ()>> name: "example" recursive?: #f select?: #<procedure true (file stat)>>
```

The `local-file` procedure is defined in the `(guix gexp`) module, so I had to import it with `(use-modules (guix gexp))`.

What did the `local-file` procedure evaluate to exactly? I know it evaluates to a "file-like" object, but what is that?





How can we expand a gexp? By passing to the `gexp->derivation` procedure.



# CODE STAGING
Compare this *code staging* to shell scripts.

Host
`example`
```
this is an example file
```

Host and build
`pipe`
```sh
mkpipe pipe
```

Host
```sh
cat example
```

Embedding build code in the host:
```sh
echo 'cat example' > pipe
eval < pipe
```

sdfasdf
`plain-file` would be like this:
```sh
echo 'echo this is a fake file' > pipe
eval < pipe
```



Defining the
