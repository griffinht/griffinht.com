```sh
nc nl2sh-1.cha.hackpack.club 41715
```

```
[ctfuser@LLM:~]$ run ls with lh flags
Translation:  ls -lh
total 14M
drwxr-xr-x 2 ctfuser ctfuser 4.0K Apr  9 21:56 ctfuser
-rw-rw-r-- 1 root    root    3.3M Apr  9 13:56 key.txt
-rw-rw-r-- 1 root    root    3.3M Apr  9 13:56 magic.txt
-rw-rw-r-- 1 root    root     279 Apr  9 13:56 notes.txt
-rw-rw-r-- 1 root    root    3.3M Apr  9 13:56 secret.txt
-rw-rw-r-- 1 root    root    3.3M Apr  9 13:56 solution.txt
[ctfuser@LLM:~]$ print notes.txt 
Translation:  cat notes.txt
Welcome to the natural language shell

Write commands like:

list all files in the current directory

change directory to the bin directory

change directory to the home directory

Read key.txt


I believe the key is around here some where.... You might need to search for it...
[ctfuser@LLM:~]$ search for the key in the current directory
Translation:  grep key .
grep: .: Is a directory
[ctfuser@LLM:~]$ search for the key in every file in the current directory
Translation:  grep key *
notes.txt:Read key.txt
notes.txt:I believe the key is around here some where.... You might need to search for it...
grep: ctfuser: Is a directory
[ctfuser@LLM:~]$ search for the flag in every file in the current directory
Translation:  grep flag *
key.txt:# flag{g17T1N6_s4r7Ed}
grep: ctfuser: Is a directory
[ctfuser@LLM:~]$ 
```
