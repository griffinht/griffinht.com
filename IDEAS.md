openai api gateway
treesitter cli

inline website

# explanation of `inline-website`

Before Haunt, I was using my own static site generator, `inline-website`. It is written in python and I mostly hate it now that I have been enlightened with Haunt. The reason I created `inline-website` was because I didn't like other static site generators like Hugo or Jekyll. They all started by introducing me to themes and special file structures and build systems I did not understand. The only functionality I wanted was a simple template feature and the ability to write my content in Markdown. To me, the most natural progression was this


Input:
```
src/index.md
src/image.png
src/blog/template.mustache
src/blog/my-example-post.md
```

`template.mustache`
```html
<html lang="en">
<head>
    <title>{{title}}</title>
</head>
<body>
    <header>
        <h1><a href="{{root}}index.html">griffinht.com</a> > <a href="../index.html">blog</a></h1>
    </header>
    <div class="spacer">
        <article>
            <h1>{{title}}</h1>
            <time datetime="{{datetime}}">{{datetime}}</time>
            (<a href="{{> ../../source}}">source</a>)
            {{{content}}}
        </article>
    </div>
</body>
</html>
```

`my-example-post.md`
```markdown
---
file_content: {{> ../article}}
file_extension: .html
title: My Awesome Example Post
datetime: 2022-04-24
---
Hello [todo](https://griffinht.com) demonstrate markdown features
[pic](pic.png) todo
todo escape code blocks?

```

The `---` block at the top of the markdown allows me to set variables which can be used by my template, like the title or the date of the blog post.

`file_content` and `file_extension` are the only "special" variables

`inline-website` will read Markdown (`.md`) files and . All other files are simply copied

`file_extension` tells `inline-website` to convert `my-example-post.md` to `my-example-post.html`

`content` is also special. It converts Markdown content from an `.md` file to HTML.

Output:
```
build/index.html
build/blog/my-example-post.html
build/blog/pic.png
```



# inline-website compiler

usage:
```
inline-website --extension=md < file.md?
inline-website --file file.md
inline-website --repl=md
```

https://files.dthompson.us/docs/haunt/latest/Readers.html#Readers
look at this madlad https://git.sr.ht/~jakob/blog/tree/master/item/haunt/jakob
https://jakob.space/blog/pushing-haunt-to-its-limits.html

## phase 1: readers

> markdown

`file.md`
```md
---
file_content: {{{content}}}
file_extension: html
---

## hello
```

> yaml

`file.yml`
```yml
file_content: {{{content}}}
file_extension: html
content: <h1>hello</h1>
```

> todo texinfo, skribe, whatever

## phase 2

`(internal representation)`
```yml
file: file
file_content: {{{content}}}
file_extension: html
content: <h1>hello</h1>
```

`file.html`
```html
{{{content}}}
```

## phase 3

    mustache templating todo support liquid

`(internal representation)`
```yml
file: file
file_content: <h1>hello</h1>
file_extension: html
```

`file.html`
```html
<h1>hello</h1>
```


# build system

executable build script and infinite recursion? virtual files!

executable build scripts everywhere, allows for support for any build system
    inline website might just be one of these systems

applies to everything in that directory and below? or maybe parent directory? idk
im leaning towards just not and letting some other build tool handle it
but also its nice to have a `inline-website serve` command to do everything which this would do so idk
    shouldn't this be an external existing tool? `http-serve --command='inline-website build {file}'`
    this could also then be a repl basically i think?

# --serve

```
http --command='inline-website -f {}'
```

# --watch

```
watch --command='inline-website -f {}'
    --debounce
```

way to specify dependencies? nah thats the job of the build tool




provide built in rss feeds, atom feeds, seo metadata
and an example blog theme?


haunt also provides tags and chronological ordering - that would be nice woulnd't it?




haunt vs inline-website

data as code: `haunt`
data as configuration: `inline-website`
data as code is data as configuration??
compare my projects page to david thompson's https://git.dthompson.us/blog/tree/projects.scm





I picked `mustache` because it had a nice Python package and it was handlebars? Looking now I think liquid also is neat todo

I didn't see why I needed to use `hugo new site quickstart` and add an Hugo theme via a Git module. This made my simple website feel more like a react app, where I "simply" `npx create-react-app` and am left with a mess of `node`, `npm`, hundreds of dependencies in `node_modules`, and what the heck is a `node_modules` and why does my JavaScript need a build phase and what even is the compiler?

That's where the name for `inline-website` came - no central configuration, and it works **inline**. The only "configuration" is `.mustache` templates, and those are "inline" - that is, they are right where I expect them to be, instead of a special magical configuration

Anyways, I think I mostly accomplished my goal with `inline-website` - the "configuration" is indeed "inline", and it makes sense in my brain. However, the original python script is a bit brittle and I haven't had the time to implement an RSS feed. (though I bet I could with some clever `mustache` templating). Onwards to Haunt!







it was this point that i realized I may be attempting to poorly reimplement portions of pandoc
time to pandoc

https://github.com/michaelstepner/pandoc-mustache/
https://pandoc.org/MANUAL#templates

i dont want a static site generator
i dont even want `inline-website`
i want some templating tools and a nice interactive build system
