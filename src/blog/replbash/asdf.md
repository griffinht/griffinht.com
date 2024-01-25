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

> note that there are many different ways to accomplish - emacs has SLIME (and has had SLIME for the past 500 years), vim has had vim-slime for the past 15 years ish (see the blog post!), even VSCode is (finally) getting some support for interactive programming

This also brings

Another feature I like to have is a way to see documentation about symbols. This is usually provided by the language server. Basically, if my cursor is on a symbol and I press `K`, then I want to execute `help symbol` and show the result in my editor. todo

On the Neovim side, plugins like `Conjure` provide an even more rich interface to the REPL - syntax aware text selection with Tree-sitter, automatic documentation information, blah blah blah

Python? Javascript? todo make a javascript repl, Even things you wouldn't normally consider to be a REPL - id like to make a repl out of everything - sysctl, blah blah blah idk

I'd like to bring the REPL everywhere. I use `sway`, which is a tiling window manager configured by a selection of shell scripts. `sway` provides a interface to run configuration commands while it is running, which allows the changes to be seen instantly. My current workflow with `sway` is to edit then reload the entire editor. This hides errors and is kind of slow - every reload takes a second or two and causes things to kind of freeze up temporarilty. This occurs every time, even when I only wanted to change a color or something.
