Docker images can be pinned to a specific digest in the form of a SHA256 hash by specifying it in the image reference ([source](https://docs.docker.com/engine/reference/builder/#syntax)).

#### Image reference syntax

Without digest
```
docker pull nginx:latest
```

With digest

```
docker pull nginx:latest@sha256:61face6bf030edce7ef6d7dd66fe452298d6f5f7ce032afdd01683ef02b2b841
```

The digest of a Docker image can be found by navigating to the `Tags` section of an image on the [Docker Hub](https://hub.docker.com/search?q=), then opening a specific tag.

The digest looks something like `sha256:61face6bf030edce7ef6d7dd66fe452298d6f5f7ce032afdd01683ef02b2b841`

#### Architecture

The digest is architecture specific and using the wrong architecture may cause an error message.

```
standard_init_linux.go:228: exec user process caused: exec format error
```

Use the `OS/ARCH` dropdown to pull the correct architecture. This is likely `linux/amd64`.

#### Read more

[Digests in Docker](https://www.mikenewswanger.com/posts/2020/docker-image-digests/)
