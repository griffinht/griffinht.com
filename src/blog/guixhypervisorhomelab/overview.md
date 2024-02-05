the system people:
    systemd is good! just apt install and edit some configs!

the container people:
    no more system! put the whole system in a container!
    creates issues when you are duplicating services
        5 different nginxes becaues each one is isolated
        wiregurad: its so tightly integrated in the system that a container is silly (not really but idk)


debian -> guix system
    wireguard (used to be container but guix made it so easy)
    nginx + ssl (used to be container but guix made it so easy)
    file share/nfs/sambda (used to be container but guix made it so easy)
    docker daemon

container -> guix pack
    cgit?



each of these steps are independent!
todo do both each way! idk




todo compare nginx on debian vs guix
    quickly testing config changes? edit a file and reload vs guix deploy - slow! dev times matter!
    lose the ability to copy/share config from online
        some things have escape hatches
        to be fair this is most systems, each have their own flavor of configuration files and locations
        guix will freeze sometimess - very disappointing
        i think its because some services dont want to restart or something?
        somtimes services need to be manually restarted
        containers really are amazing - i am in favor of moving things off the system
            exceptions:
                ssh (for remote admin only)
                wireguard (why cant i find a docker thing that makes it easy? actually i should idk)
then compare nginx in a Dockerfile vs guix pack 
    show local dev!
