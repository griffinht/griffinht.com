```
nc nl2sh-2.cha.hackpack.club 41716                                                                                                                                                                                                                                                                                                                                                                                               09:34:21 
[ctfuser@LLM:~]$ list the current director ycontents
Translation:  ls
ctfuser
flag.txt
notes.txt
[ctfuser@LLM:~]$ print the notes.txt
Translation:  cat notes.txt
Welcome back to the natural language shell

The developers were just here... they left one of their debugging script around

How unsecure
[ctfuser@LLM:~]$ print flag.txt
flag.txt: Permission denied

[ctfuser@LLM:~]$ do ls with lh flags
Translation:  ls -lh
total 12K
drwxr-xr-x 2 ctfuser ctfuser 4.0K Apr 12 22:04 ctfuser
-rw-rw-r-- 1 root    root      30 Apr  9 13:56 flag.txt
-rw-rw-r-- 1 root    root     138 Apr  9 13:56 notes.txt
[ctfuser@LLM:~]$ list the ctfuser directory
Translation:  ls /home/ctfuser
[ctfuser@LLM:~]$ list the ctfuser dire with hidden files
Translation:  ls -a
.
..
ctfuser
flag.txt
notes.txt
[ctfuser@LLM:~]$ list the directory ctfuser with hidden files
Translation:  ls -a ctfuser 
.
..
.bash_logout
.bashrc
.profile
[ctfuser@LLM:~]$ who is the current user
Translation:  echo $USER

[ctfuser@LLM:~]$ list the bin directory with lh flas
Translation:  ls -la /bin
total 5412
drwxr-xr-x 1 root root    4096 Apr  9 21:56 .
drwxr-xr-x 1 root root    4096 Apr 12 22:04 ..
-rwxr-xr-x 1 root root 1183448 Feb 25  2020 bash
-rwxr-xr-x 3 root root   39144 Sep  5  2019 bunzip2
-rwxr-xr-x 3 root root   39144 Sep  5  2019 bzcat
lrwxrwxrwx 1 root root       6 Sep  5  2019 bzcmp -> bzdiff
-rwxr-xr-x 1 root root    2227 Sep  5  2019 bzdiff
lrwxrwxrwx 1 root root       6 Sep  5  2019 bzegrep -> bzgrep
-rwxr-xr-x 1 root root    4877 Sep  4  2019 bzexe
lrwxrwxrwx 1 root root       6 Sep  5  2019 bzfgrep -> bzgrep
-rwxr-xr-x 1 root root    3775 Sep  5  2019 bzgrep
-rwxr-xr-x 3 root root   39144 Sep  5  2019 bzip2
-rwxr-xr-x 1 root root   18584 Sep  5  2019 bzip2recover
lrwxrwxrwx 1 root root       6 Sep  5  2019 bzless -> bzmore
-rwxr-xr-x 1 root root    1297 Sep  5  2019 bzmore
-rwxr-xr-x 1 root root   43416 Sep  5  2019 cat
-rwxr-xr-x 1 root root   72024 Sep  5  2019 chgrp
-rwxr-xr-x 1 root root   63864 Sep  5  2019 chmod
-rwxr-xr-x 1 root root   72024 Sep  5  2019 chown
-rwxr-xr-x 1 root root  153976 Sep  5  2019 cp
-rwxr-xr-x 1 root root  129816 Jul 18  2019 dash
-rwxr-xr-x 1 root root  108920 Sep  5  2019 date
-rwxr-xr-x 1 root root   80256 Sep  5  2019 dd
-rwxr-xr-x 1 root root   93128 Sep  5  2019 df
-rwxr-xr-x 1 root root  142144 Sep  5  2019 dir
-rwxr-xr-x 1 root root   84440 Apr  2  2020 dmesg
lrwxrwxrwx 1 root root       8 Nov  7  2019 dnsdomainname -> hostname
lrwxrwxrwx 1 root root       8 Nov  7  2019 domainname -> hostname
-rwxr-xr-x 1 root root   39256 Sep  5  2019 echo
-rwxr-xr-x 1 root root      28 Jan 29  2020 egrep
-rwxr-xr-x 1 root root   39256 Sep  5  2019 false
-rwxr-xr-x 1 root root      28 Jan 29  2020 fgrep
-rwxr-xr-x 1 root root   73128 Apr  2  2020 findmnt
-rwxr-xr-x 1 root root  199136 Jan 29  2020 grep
-rwxr-xr-x 2 root root    2346 Dec 13  2019 gunzip
-rwxr-xr-x 1 root root    6376 Dec 13  2019 gzexe
-rwxr-xr-x 1 root root   97496 Dec 13  2019 gzip
-rwxr-xr-x 1 root root   26856 Nov  7  2019 hostname
-rwxr-xr-x 1 root root   30952 Feb 27  2020 kill
-rwxr-xr-x 1 root root   76160 Sep  5  2019 ln
-rwxr-xr-x 1 root root   57104 Apr 16  2020 login
-rwxr-xr-x 1 root root  142144 Sep  5  2019 ls
-rwxr-xr-x 1 root root  133352 Apr  2  2020 lsblk
-rwxr-xr-x 1 root root   88408 Sep  5  2019 mkdir
-rwxr-xr-x 1 root root   72024 Sep  5  2019 mknod
-rwxr-xr-x 1 root root   47448 Sep  5  2019 mktemp
-rwx------ 1 root root   43160 Apr  2  2020 more
-rwsr-xr-x 1 root root   55528 Apr  2  2020 mount
-rwxr-xr-x 1 root root   14568 Apr  2  2020 mountpoint
-rwxr-xr-x 1 root root  149888 Sep  5  2019 mv
lrwxrwxrwx 1 root root       8 Nov  7  2019 nisdomainname -> hostname
lrwxrwxrwx 1 root root      14 Feb 13  2020 pidof -> /sbin/killall5
-rwxr-xr-x 1 root root  137688 Feb 27  2020 ps
-rwxr-xr-x 1 root root   43352 Sep  5  2019 pwd
lrwxrwxrwx 1 root root       4 Feb 25  2020 rbash -> bash
-rwxr-xr-x 1 root root   51544 Sep  5  2019 readlink
-rwxr-xr-x 1 root root   72056 Sep  5  2019 rm
-rwxr-xr-x 1 root root   47448 Sep  5  2019 rmdir
-rwxr-xr-x 1 root root   27144 Dec  7  2019 run-parts
-rwxr-xr-x 1 root root  121288 Dec 22  2018 sed
lrwxrwxrwx 1 root root       4 Apr  9 21:56 sh -> dash
-rwxr-xr-x 1 root root   39256 Sep  5  2019 sleep
-rwxr-xr-x 1 root root   84344 Sep  5  2019 stty
-rwsr-xr-x 1 root root   67816 Apr  2  2020 su
-rwxr-xr-x 1 root root   39256 Sep  5  2019 sync
-rwxr-xr-x 1 root root  448112 Mar 14  2020 tar
-rwxr-xr-x 1 root root   14360 Dec  7  2019 tempfile
-rwx------ 1 root root  100728 Sep  5  2019 touch
-rwxr-xr-x 1 root root   39256 Sep  5  2019 true
-rwsr-xr-x 1 root root   39144 Apr  2  2020 umount
-rwxr-xr-x 1 root root   39288 Sep  5  2019 uname
-rwxr-xr-x 2 root root    2346 Dec 13  2019 uncompress
-rwxr-xr-x 1 root root  142144 Sep  5  2019 vdir
-rwxr-xr-x 1 root root   35048 Apr  2  2020 wdctl
-rwx------ 1 root root     946 Dec  7  2019 which
lrwxrwxrwx 1 root root       8 Nov  7  2019 ypdomainname -> hostname
-rwxr-xr-x 1 root root    1984 Dec 13  2019 zcat
-rwxr-xr-x 1 root root    1678 Dec 13  2019 zcmp
-rwxr-xr-x 1 root root    5880 Dec 13  2019 zdiff
-rwxr-xr-x 1 root root      29 Dec 13  2019 zegrep
-rwxr-xr-x 1 root root      29 Dec 13  2019 zfgrep
-rwxr-xr-x 1 root root    2081 Dec 13  2019 zforce
-rwxr-xr-x 1 root root    7585 Dec 13  2019 zgrep
-rwxr-xr-x 1 root root    2206 Dec 13  2019 zless
-rwxr-xr-x 1 root root    1842 Dec 13  2019 zmore
-rwxr-xr-x 1 root root    4553 Dec 13  2019 znew
```
