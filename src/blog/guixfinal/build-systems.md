WHATCH THIS VIDEO
https://www.youtube.com/watch?v=VjKbZFMZr6I





The build systems in Guix may seem opaque and confusing, especially so someone not used to the gnu build system todo link

Starting from an example where guix shell --container share
Then migrating nginx configuration to regular things idk

what if i wanted to install a file somewhere?
check out each phase its not so tricky! give examples of how to modify each phase

patching shell scripts
shebang
https://stackoverflow.com/questions/53116226/what-is-the-recommended-posix-sh-shebang
which shell is it?

```sh
#!/usr/bin/env sh

echo $SHELL
```

works
```sh
#!/bin/sh

echo $SHELL
```

guix shell -- /bin/sh fails??

checking runtime path/library load




what if i wanted to delete a build phase (delete multiple)
or modifyt one
or add one?
https://github.com/pjotrp/guix-notes/blob/master/HACKING.org#renaming-and-moving-files


don't worry, you dont need to use gnu autotools in order to use gnu build system
make install:
    env

check out what copy build system does and reiimplement as make install




But what if I want to configure my scripts at runtime like nginx docker does
Sure! you'll need to add envsubst
