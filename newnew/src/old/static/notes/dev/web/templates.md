https://nomadiq.hashnode.dev/reimagining-front-end-web-development-with-htmx-and-hyperscript
https://binaryigor.com/htmx-and-web-components-a-perfect-match.html
api response - success or error

try it! how can you make a cool interactive demo for all of these WITH THE SERVER SIDE???

REST API

Many developers know that a REST API looks like `POST /user`, `GET /user/{id}`, `GET /user?address=bruh`, `DELETE /user`

There is also the idea that a pure REST API returns HTML instead of data.

## api

todo define as an openapi schema

`/greet?name=hi`
`/greet?name=`

Let's use ChatGPT (via [aichat](https://github.com/sigoden/aichat)) to generate a list of banned names.

```sh
$ echo give a list of random names as json | aichat > banned_names.json
$ jq '.' < banned_names.json
```

```json
{
  "names": [
    "Aurora",
    "Nico",
    "Jasmine",
    "Mateo",
    "Sofia",
    "Caleb",
    "Luna",
    "Eli",
    "Isabella",
    "Diego"
  ]
}
```

This will be our list of banned names. If we try to greet a name on this list, then we will get an error.


server side

## CGI Script

`cgi-bin/test` (executable)
```sh
#!/bin/sh

echo 'Content-Type: text/html'
echo

# insecure, value should be escaped
#echo "hello $X_REQUEST_USER_TODO"
echo "hello $(escape "$X_REQUEST_USER_TODO")"
```

`python3 -m http.server --cgi`

## FastAPI

```sh
def bruh(user header):
    #return f

```js
element.replaceWith(await fetch("/api/test"))
```

htmx + server side
```html
<div hx-get "/api/test">loading...</div>
```

declarative
    mustache
    js ``

imperative
manual js creating elements
```
let element = document.createElement("p");
p.innerText = error;
e.replaceWIth(element)
```

manual js imperative with template

```
template.content.clone
// emphasize  
element.innerText = error
```
