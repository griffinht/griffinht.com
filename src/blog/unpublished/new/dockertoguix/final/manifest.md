Oops! --verbosity=10
Ooops! --keep-failed
--log-file
ls /tmp/guix
We see source and environment
in fact the guix manual has somwething about 


https://guix.gnu.org/manual/en/html_node/Debugging-Build-Failures.html



concatenate manifests
then just make everything one package


oops i accidentally used (list instead of '(
The astute reader may have noticed the quasi-quote and comma syntax in the argument field. Indeed, the build code in the package declaration should not be evaluated on the client side, but only when passed to the Guix daemon. This mechanism of passing code around two running processes is called code staging.



moving package definiotion out of manifest
```scheme
(concatenate-manifests
  (list
    (specifications->manifest
      (list "git"
            "openssh-sans-x"
            "bash" ; run our shell scripts todo use dash???
            "coreutils" ; stuff idk
            "shadow" ; useradd
            "which" ; which ssh
            "procps" ; ps, top - debug
            ))
    (packages->manifest
      (list (load "guix.scm")))))
```

compare (load) to (use-modules)

then debugging

    why install-path not working?

    guix build to debug

    why cant i find the file i just made?

input vs propagative vs native




****talk about how using gnu-build-system and patch-shebang and things will automatically fix everything
https://guix.gnu.org/manual/devel/en/html_node/Build-Phases.html
https://guix.gnu.org/en/blog/2018/a-packaging-tutorial-for-guix/



todo guix shell breaks cache
--rebuild-cache


let's find openssh-sans-x definition
guix edit openssh-sans-x




investigating what the file system looks like in the build
add --save-provenance to guix pack and check out the profile
this gives a profile
--localstatedir is interesting
--root???
ls $GUIX_ENVIRONMENT


--emulate-fhs as a workaroud


/bin/sh exists?





changing packages
start with (package (inherit oldpackager))
then start modifyinfg

but wait! do we really want to build from source? not really lol



all we want is to put a file at /etc/ssh_config well not really
"$(which sshd)" -f "$GUIX_ENVIRONMENT/etc/ssh/sshd_config" -D -e
this even works if guix environment isn't defined and we are on a normal system :))
what about on systems without guix environemtn?
or places that can't evalute an environemnt variable? static configs!
