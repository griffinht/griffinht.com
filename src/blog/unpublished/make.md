TODO CHANGE TO GREETER OR FIND SOMETHING CUTE
DIVIDER PROGRAM?

`make` is a utility which can be used to make stuff.

I'd like to make an executable `helloworld` that says 'Hello world!' when executed. Let's try this!

```
$ ./helloworld

unknown command
```

lets use make to make this executable

```
$ make helloworld

make: *** No rule to make target 'helloworld'.  Stop.
```

make doesn't know how to make me my file called helloworld. Let's give it some help

`helloworld`

```
#!/usr/bin/env sh

echo Hello world!
```

now let's see if make know how to make this file

```
$ make helloworld
make: Nothing to be done for 'helloworld'.

$ ./helloworld
Hello world!
```

Success! `make` has made `helloworld`! Except `make` didn't do anything here - I made `helloworld` myself! `make` simply ensured that the `helloworld` file exists, which is what I wanted!

Testing that `helloworld` works

`helloworld`

todo change to c example

```
#!/usr/bin/env sh

echo Goodbye world!
```

```
$ make helloworld
todo c compiler output

$ ./helloworld
Goodbye world!
```

This didn't work! I wanted `make` to make me an executable that says 'Hello world!' when executed. Instead I got this!
Let's tell make to make sure `helloworld` outputs the correct text.

todo top of makefile is first by default
```
helloworld: helloworld.test
    touch '$@'

helloworld.test:
    ./helloworld | diff - <(echo Hello world!)
```

todo test with any greeting
add multiply tests, write a program that fails one

Here we are using the `diff` utility and some pipe redirection (todo link) to check if the output of `helloworld` matches the output of `echo Hello world!`

```
$ make helloworld
prorgam failed or whatever do this for real and make a git repo and publish it with example files
```

Let's make sure we clean up after ourselves by removing the temporary files we made.

```
clean:
    rm -f *.test
```

How can I learn more about `make`? Using it! I learned a lot from my plain text accounting journey or inline-website? Link blog posts to here



We want the tested version of helloworld, or helloworld.test even if we aren't running it
We could also express this as helloworld: helloworld.raw but this makes the build required to use makefile which is unneccessary
