adanh/webhook
    too limiting! i can't even pass binary files - only json or multipart form encoded :( and the config is annoying and bulky
    i want to run sh -c 'echo hello world'
    which looks like
If I wanted to write a hook which ran `sh -c 'echo hello world'`, then the config would look like this!

```yaml

```

This is way too verbose

Given these limitations I decided to write my own tool - a tool which could convert http requests to shell scripts! I even came up with a name, http2shell, but realized it sounded too much like a tool for HTTP/2 todo link to http2. Thus shell2http was born!

This tool would also be able to do what I have been trying to implement for a while - a tool to run a build script when a URL is visited, useful for frontend development. This feature already exists for various tools - Hugo, react, blah blah blah, but I wanted it for all tools!

wrote my own - what to call it? shell2http!
    i could build a reverse proxy with curl!
```yaml
proxy:
    catch-all: true
    command: curl
```

As it turns out, `shell2http` already exists! Here is the GitHub page - check out some of the [examples](https://github.com/msoap/shell2http#examples)!

I also noticed this tool supports CGI scripts
https://github.com/msoap/shell2http

cgi scripts - this is exactly what i need! and is built in to python!!!
