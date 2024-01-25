I write a fair bit of shell scripts. These scripts can begin to get complicated, and my main testing method is to run the script. It can be very frustrating for something to break in the middle of the script execution, This is especially an issue when my scripts are not **indeptoment**

```sh
touch file
```

Every time I run this script I have to launch the program, then clean up after it. If 

# Static analysis

Thankfully `shellcheck` is an excellent static anlysis tool for shell scripts, and using it has saved me so much pain and anguish. I like to use it within `bash-language-server`, which integrates feedback from `shellcheck` right in my text editor (Neovim).

todo screenshot?

# Debugging

Why is there not a debugger for shell scripts? I'd love to be able to go line by line, stepping in and out of function calls, and being able to pause on errors and see a stack trace and local variables. Looking online

Do I really want this? Actually, no. What I want is a way to run my scripts interactively, without having to go through the "write" --"compile"-- "execute" lifecycle. This is the root of my problems - I want to 



# Interactive evaluation/execution

As it turns out, the "bash debugger" I have been looking for this entire time already exists, hidden right under my nose. As it turns out, the "bash debugger" tool is widely available, and integrates with nearly any workflow. I don't even have to find a barely maintained debug adapter implementation!

The "bash debugger" tool I want is called "bash". It is a shell interpreter which is installed on most unix systems (and even Windows!).

`bash` provides us a REPL

Unfortunately, the REPL is only useful for typing in commands. Actual shell scripts belong in files, and the commands we type in to our shells and the commands that are executed by our shell scripts are unrelated - or are they?

What if we copy-pasted the code from our shell scripts in to a REPL (a bash bourne again shell shell)? Let's take an example shell script.

```sh
#!/bin/sh

bruh
bruh2
bruh3
```

There is an obvious problem. Let's debug this interactively
This manual copy pasting is getting tiring - what if there was a way to automate the process of selecting text from the buffer and sending it to the REPL? `vim-slime` to the rescue!

Now how can I check the value of "$response"?
echo "$response"
I can type this into my editor and send it, or just type straight in to the REPL - whichever is easier.


> note that there are many different ways to accomplish - emacs has SLIME (and has had SLIME for the past 500 years), vim has had vim-slime for the past 15 years ish (see the blog post!), even VSCode is (finally) getting some support for interactive programming

This also brings

Another feature I like to have is a way to see documentation about symbols. This is usually provided by the language server. Basically, if my cursor is on a symbol and I press `K`, then I want to execute `help symbol` and show the result in my editor. todo

On the Neovim side, plugins like `Conjure` provide an even more rich interface to the REPL - syntax aware text selection with Tree-sitter, automatic documentation information, blah blah blah

# python (long running server)

developing a server? changing a specific endpoint?
Development workflow is this: start the server, change something, restart the server, test it
test driven development: write a test, mock the dependencies, turns out you had to mock the entire server, start the server (automated), test it (automated)
    Maybe add some hot-module reload (HMR) magic to make things slightly more bearable
interactive development: start the server, change something, test it

There is something to be said about the kind of code TDD produces veruss interactive programming. Arcane functions, idk - code looks different when it was written with a different workflow todo find that hn thread about unreadable lisp idk 

Python? Javascript? todo make a javascript repl, Even things you wouldn't normally consider to be a REPL - id like to make a repl out of everything - sysctl, blah blah blah idk

Python debugger? why would I even want that??
here I am interactively developing a python server
this involves long running python code which blocks - normally this would be an issue with a REPL as when the server is running I wouldn't be able to evaluate anything
what if we ran the server on a thread? then w

now instead of restarting the python program (control+c then ./script.py) I can just reevalute the buffer and maintain all the existing state!
debugging error? idk

# javascript

JavaScript is indeed an interactive programming language, and I bet you already have extensive experience using the JavaScript REPL right in your browser! Open your devtools and open the console - that's a REPL! How can we use this? how can we develop with this?

here is an example of a long running

here is another example of someone programming a gui in racket
GUI programming is notorious for having lots of state - imagine developing ta submenu which requires opening two other menus with a specific set of values - every change to the submenu would require the program to be restarted, and the submenu would have to be reoponed manually. Before I knew about interactive programming, I figured that GUIs were tedious and annoying

# chatgpt



I'd like to bring the REPL everywhere. I use `sway`, which is a tiling window manager configured by a selection of shell scripts. `sway` provides a interface to run configuration commands while it is running, which allows the changes to be seen instantly. My current workflow with `sway` is to edit then reload the entire editor. This hides errors and is kind of slow - every reload takes a second or two and causes things to kind of freeze up temporarilty. This occurs every time, even when I only wanted to change a color or something.
