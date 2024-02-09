# ref
https://www.redhat.com/sysadmin/compose-podman-pods
https://developers.redhat.com/blog/2019/01/15/podman-managing-containers-pods#
https://www.undrground.org/2020/07/01/moving-from-docker-compose-to-podman-pods/
https://www.mavjs.org/post/podman-pods-instead-of-docker-compose/#fn:4


# compose to pods
i was using compose

compose rootless was buggin

podman compose is buggin

why not 

use podman pods

how to declaratively manage podman pods??

generate kubernetes pod, podman play!
https://mohitgoyal.co/2021/05/10/working-with-pods-with-podman-generate-and-podman-play/

plus i guess it would make me x closer to kubernetes - neat i suppose!


let's take a look at the generated yaml
ref: https://kubernetes.io/docs/concepts/workloads/pods/

its hard to read - let's reorganize

im also going to remove some cruft




https://github.com/containers/podman/pull/17950


# basics

## docker compose ls

podman pod ps

## docker compose ps (current project)

podman pod ps --filter name=mypod --ctr-names --ctr-status

podman ps --pod 

add `--filter pod=mypod` to only see one pod

add `--all` to see published ports and stuff

todo show published ports
im pretty sure there is a better way...

## docker compose up

doesnt work i dont think
podman kube play --replace --wait pod.yml

## docker compose up --detach

podman kube play --replace pod.yml

## docker compose up --down

podman kube play --down pod.yml
podman kube down

## custom built images

just specify, see docs

if you have modified an image definition you do need to add `--build` to `podman kube play` or else it won't automatically rebuild your changes.

# volumes

The docs state "Only three volume types are supported by kube play, the hostPath, emptyDir, and persistentVolumeClaim volume types."

That means we only have to worry about these three, compared to Kubernete's many? todo how many?

[kubernetes ref](https://kubernetes.io/docs/concepts/storage/volumes/)


## implicit volumes

certain docker images tend to declare their volumes with the VOLUME thing, which means I have to track them down and undo it blah blah

podman ignores this, which is exactly what I want! todo idk

# depends_on

# networking

## container to container
[docs](https://kubernetes.io/docs/concepts/workloads/pods/)
Within a Pod, containers share an IP address and port space, and can find each other via localhost. The containers in a Pod can also communicate with each other using standard inter-process communications like SystemV semaphores or POSIX shared memory. 

## host to container
publish

Imperative with `podman pod create` todo link docs

`podman pod create --publish ... todo`

Declarative as a Kubernetes Pod definition

`pod.yml`
```
    ports:
      - containerPort: 9091
        hostPort: 9091
```

todo what about doing it do 

## container to host
Containers within the Pod see the system hostname as being the same as the configured name for the Pod. There's more about this in the networking section.

```
python3 -m http.server
podman pod create alpine wget system:8080
<output>
```

## container to other pod
todo



show the graphs comparing pods vs regular!

this actually replicates what I have been trying to finangle with docker compose

compose:
    authelia:
    authelia_internal:
    blah blah:

pods:
    blah blah idk

authelia -> redis:6893
authelia -> localhost:6893
wowza!

## fine grained networking - no internet access

# todo configmap for configuration??

# templating

something i enjoyed doing with docker compose was using yaml templating to change certain parts of my config for local development. that allowed me to do things like fake secrets or blah blah

## variable substition

"AUTHELIA_SESSION_DOMAIN=${DOMAIN:-hot.localhost}"

# caveats
HEALTHCHECK is not supported for OCI image format and will be ignored. Must use `docker` format 

# continers vs pods vs deployments vs daemonset

`podman kube generate` doesn't only generate Kubernetes Pod definitions - it can also create [deployment](todo) and [daemonste](todo) configs.

# conclusion

I think I am going to stop using docker compose now thanks to `podman pod` and `podman kube play`. While the original issue I had with docker compose would have been trivial to fix, I am still glad I didn't fix it and instead tried to jumped ship. These newer tools feel much more modern and polished. This contrasts to the experience I had with `podman-compose` (link), which I found to be buggy and inactively maintained. I also like how I am one step closer to kubernetes without actually using any kubernetes - I think this is a big positive in terms of flexiblity of future deployments. I could deploy this stack on a full k8s cluster, or even a baby kind or k3s idk but this opens up all these options to me, where docker compose kept me entrapped within docker compose. This gets me closer to rolling deployments, high availability, blah blah blah

docker comopse would have required swarm or something which is probably dead in the water, and COMPOSE STILL DOESN'T HAVE SECRETS - but to be fair volumes are probably better anyways idk

not to mention the networking is soo much better i think?

and it makes it ridiculosly easy to deploy to a rootless podman host - check out my setup post on this
but what if i want to deploy to docker still? meh idk if i can todo
