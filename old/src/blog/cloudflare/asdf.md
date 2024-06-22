# Cloudflare as a personal CDN for all your favorite repositories

First you will need to acquire a high performance server with excellent networking capabilities

Just kidding! Assuming you have a domain whose DNS is managed by Cloudflare, just add a CNAME record pointing to `ci.guix.gnu.org` and make sure it is set to Proxied (the orange cloud).

todo screenshot

Benchmarks


todo traceroute and ping and other net analyssi tools?

todo plug these in to a local https proxy to monitor traffic

# `docker` docker.io
also mention oci
https://devops.stackexchange.com/questions/2731/downloading-docker-images-from-docker-hub-without-using-docker

# `npm`
guix shell --container --network node -- npm init
I found a silly package called `bloater` from [https://gist.github.com/anvaka/8e8fa57c7ee1350e3491](https://gist.github.com/anvaka/8e8fa57c7ee1350e3491). It was near the top of the list of packages with the largest number of dependencies.
guix shell --container --network node -- npm install bloater
to be fair most time is taken by decompressing


# `cargo` crates.io
    uses cloudfront
    benchmarks
guix shell --container --network nss-certs curl rust rust:cargo -- cargo build
note that cargo appears to use an internal version of curl unless a system curl is installed. this is necessary for ssl certificates to work
cargo add bevy tokio hyper actix-web rocket diesel serde rust-crypto tensorflow
cargo build

# `guix` ci.gnu.guix.org
todo cuirass web caching? https://guix.griffinht.com/
https://guix.gnu.org/manual/en/html_node/Substitute-Authentication.html
https://issues.guix.gnu.org/46942
https://guix.gnu.org/en/blog/2021/substitutes-now-also-available-from-bordeauxguixgnuorg/

awesome guix subsistute server list

# `apt`
# `apk`
# `pip` pypi.org
I know PyTorch is a particularly large python package, so I'll try that.

``` sh
$ guix shell --container --network python-pip -- pip download torch
```
I already get pretty great download speeds here todo benchmark all the things!

```
CNAME files.pythonhosted.org
```

ssl error, ssl encryption change to full instead of full (strict)
i did this with a cluodflare configuration rule


```sh
$ curl https://pythonhosted.griffinht.com/
<html>
<head>
<title>Fastly error: unknown domain pythonhosted.griffinht.com</title>
</head>
<body>
<p>Fastly error: unknown domain: pythonhosted.griffinht.com. Please check that this domain has been added to a service.</p>
<p>Details: cache-pdk-kpdk1780054-PDK</p></body></html>
```

curl -I 'https://files.pythonhosted.org/packages/1e/86/477ec85bf1f122931f00a2f3889ed9322c091497415a563291ffc119dacc/torch-2.1.2-cp311-none-macosx_11_0_arwhl'

its fastly


manual configuration
auto configurtion

what if cloudflare goes down??
its dangerous to rely on one provder for the internet todo peep hn bashing cloudflare


is it really this easy?
i heard cloudflaRE WILL ban you
    note they removed section 2.8 official image
this feels like abuse?
    i think this approach actually greatly reduces strain on the overall internet

compare to that gaming.gg service thing

automatically doing this for everything?
why doesnt the internet work like this automatically

don't other people know about this?

