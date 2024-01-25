first person current tense
Tree-sitter not Treesitter
Neovim not NeoVim

My site has been down for like 4 months. In that time I have began to expose myself to the wonders of Lisp and Scheme and Guile and [the REPL](find a link) and [conversational software development](https://oli.me.uk/conversational-software-development/). I would mostly attribute these discoveries to my choice to [use Guix to manage my home](todo blog), which I made at the end of 2022. This was also when I switched from the stock Debian Gnome 3 desktop environment to Sway, which is a tiling window manager. Suddenly I found myself with the need to [build and configure my own desktop environment](todo blog).

maybe i want to be more explicit with these links? it can be kind of 

Something I'd like to do is write a command line tool for syntax highlighting using treesitter. I have been exposed to the wonders of tree-sitter thanks to integrating it with my NeoVim setup. I'd now like to tree-sitter all the things, like replacing `python-pygments` with 

I actually don't think this exists right now - `tree-sitter-cli` is more of a development tool and doesn't work with compiled tree-sitter grammars (`*.so` files). This is an issue for using tree-sitter in production, probably for speed reason and the fact that tree-sitter grammars are distributed as `.so` files. Thus, the only reasonable 

# Tree-sitter in the wild
    
    todo move to other article

https://news.ycombinator.com/item?id=21675113
Why doesn't this tool exist already?

[Repology](https://repology.org/project/tree-sitter-markdown/versions) shows me how 

Where is Tree-sitter used? For now, it seems like mostly just GitHub and the powerful text editors.

## Code forges

It looks like the only code forge right now that uses tree-sitter for syntax highlighting source code previews is GitHub. GitLab looks like it uses.

[GitHub](https://github.com/) uses Tree-sitter ([source](https://tree-sitter.github.io/tree-sitter/syntax-highlighting)), which I think gives it the best syntax highlighting of all the code forges.

[GitLab](https://about.gitlab.com/), a "comprehensive AI-powered DevSecOps platform" (open source GitHub clone with all the enterprisey stuff), appears to maybe do it client side with Highlight.js, and a `python-pygments` liek Rouge idk [source](https://docs.gitlab.com/ee/user/project/highlighting.html)

todo srht
[old blog](https://drewdevault.com/2019/07/08/Announcing-annotations-for-sourcehut.html)

codeberg/forgego? dont they use forgego?

[`gitea`](https://about.gitea.com/)

[`gogs`](https://gogs.io/)

## Git web viewers

Software here is more geared towards viewing git repositories, 

[`cgit`](https://git.zx2c4.com/cgit/), a minimal git web viewer [I use](https://git.griffinht.com), . `cgit` seems to make integrating an extern

[`klaus`](https://github.com/jonashaag/klaus), another minimal git web viewer "that Just Works™" for 

## Emacs

https://archive.casouri.cc/note/2023/tree-sitter-in-emacs-29/index.html

## Neovim

Neovim bundles parsers for C, Lua, and VimScript ([:help treesitter](https://neovim.io/doc/user/treesitter)). Installing more parsers can be accomplished

Neovim solves the packaging problem with an entire plugin which can automatically download the Treesitter grammars https://github.com/nvim-treesitter/nvim-treesitter. This seems to essentially be an automated

The `nvim-treesitter` plugin is what I currently use to install treesitter grammars for neovim, but I'd like to migrate towards using Guix packages. I recently began packaging my Neovim plugins using Guix with great success ([blog](todo)), and would like to do the same with treesitter grammers. This would eliminate a package manager from my system (todo why would i want to do this)

## VSCode

nope :)
VSCode seems to be happy with language server
https://github.com/microsoft/vscode/issues/50140
https://marketplace.visualstudio.com/items?itemName=jeff-hykin.experimental-tree-sitter
https://github.com/georgewfraser/vscode-tree-sitter

I think VSCode is going the way of the LSP in terms of syntax highlighting in their editor. I think the main benefits of Tree-sitter are undermined in an environment which usually has a language server and doesn't make use of advanced code navigation features like Emacs or Neovim do.

## Helix

[Helix](https://helix-editor.com/) is a . Basically if Neovim and VSCode had a baby. I don't use it, but it seems really cool!

Helix appears to bundle Treesitter grammars with themselves with Nix ([source](https://github.com/helix-editor/helix/blob/master/grammars.nix)).

## AUR

## Alpine Linux

## GNU Guix

link to tropin's yt streams

## cargo? i think it does lol
https://codeberg.org/NomisIV/pandoc-tree-sitter-filter

## Nix?

I was surprised to see that Nix does not seem to package the Treesitter grammars. https://nixos.wiki/wiki/Treesitter

# Why not more packages?

Lack of demand? I think most uses of Treesitter right now comes from Emacs and Neovim power users are looking for improved syntax highlighting for their text editors. nvim-treesitter and 


I think that Treesitter really ought to be used anywhere we look at source code. Whether that be in a file browser, online, or in a text editor (or IDE), I think the only reason Treesitter isn't everywhere is a lack of integration.

Tree-sitter is also very new - support in Emacs and Neovim only really landed in the past year or two. That's when I discovered Tree-sitter, after getting tired of the ugly built-in regex-based syntax highlighting which came with Neovim by default. I don't think many people are aware of Tree-sitter - VSCode users appear to be content with their LSP syntax based highlighting, and idk





# haunting

David Thompson, the creator, has a great overview on the [project page](https://dthompson.us/projects/haunt.html).

[Awesome Haunt](https://awesome.haunt.page/) is a neat collection of sites made with Haunt. Check it out!

```sh
$ guix shell haunt --export-manifest > manifest.scm
```

# goals

try not to break old urls - I liked my old url conventions

/blog/example-title/blah

# deployment

Now that we have a pile of HTML, CSS, and other files, how can I host it?

Previously I had been self hosting with plain old `nginx`. However, I think this time I want to instead use Cloudflare's CDN and Backblaze B2 for free.

This comes with several tangible benefits. The largest benefit is the **lightning fast deploys™** enabled by simply pushing to an S3 bucket. Previously, I had been bundling the website files and `nginx` in an entire custom Docker image built from a `Dockerfile`. This meant that every website update required a rebuild of the Docker image, and a redeploy with `docker-compose`. This meant each deploy required a restart of the `nginx` container, resulting in a bit of downtime. The proper way would have been to have `nginx` serve website files from a Docker volume which I could modify as easily as pushing to the S3 bucket. actually lets do that todo

It's also nice to not have to worry about TLS termination, which I was previously handling with a brittle certbot setup deployed with `docker-compose`. `acme.sh` was kind of not great, but `go/lego` was a lot better, but still, one less moving piece

# redundancy

But what if Cloudflare goes down? Why must I force everyone viewing my website to go through the big evil CDN? Fear not, for I might also todo host nginx with alt dns record




# anyways 

after looking at haunt for a bit i began comparing it to [my design goals for `inline-website`](todo ideas.md) and realized i did not want haunt. instead i began to build the second iteration of `inline-website`. I wanted to build a powerful static site generation toolchain, not just a standalone generator. This led to me realizing treesitter was lacking many integrations on the terminal and in document conversion - pandoc, and i realized pandoc was going to the be ultimate tool in my toolchain. no more reinventing the wheel - i was going to support all the documents and have syntax highlighting for all of them.

the first issue was the dev tooling. Haunt has `haunt serve` and so do many other static site generators - useful for development. Where was the `serve exec haunt build` command? off i went to build it lol

agin i was rather tempted to write it in guile but i still dont know guile and python makes building this kind of thing so deliciously easy, plus it has a great repl!
