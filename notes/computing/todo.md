TMRW

# overall
k3s
docker compose
- docker is declarative linux sysadmin
	- chroot -> volumes
	- namespaces -> containers
- docker compose is declarative linux sysadmin
	- scp -> docker compose cp
	- networking/ip route/iptables -> docker networking
		- host networking - linux sysadmin route
		- port - linux sysadmin route?
- swarm abstracts linux
- kubernetes abtstracts linux
	- linux -> kubernernets

# volumes
host mounts

# config
volumes
config
dynamic
live reload
# workloads
## daemon set
docker compose for free!
## cron
postgres backup [[postgres]]
- dagster pipeline which outputs data?
cert renewal



management

linux
- DOCKER_HOST=ssh://
- ssh tunnel /var/unix/sock
kubectl


linux
- sshfs
compose
- docker compose cp caddy_config/Caddyfile caddy:/etc/caddy/Caddyfile
- docker compose exec caddy caddy reload --config /etc/caddy/Caddyfile
swarm
- config
kubernetes
- configmap







- get docker compose up
- deploy apps and serverless stuff


undistributed computing? ok! ssh + dns gets you all the way there!
don't do distributed computing at home kids

KUBERNETES IS THE ULTIMATE CLOUD OPERATING SYSTEM



KUBERNETES
- secrets, volumes, config
- deployment

KUBERNETES IS THE ULTIMATE PAAS - is it tho? isn't docker compose the ultimate paas? uhhhh
https://kamal-deploy.org/

how do you deploy your weekend project>
https://news.ycombinator.com/item?id=32781921
kubernetes on bare metal?


https://www.youtube.com/watch?v=tayQQ_D2Rxc
https://github.com/vagrant-libvirt/vagrant-libvirt

serverless - a cron job which runs on ur pc and just needs internet

mental model:
vps - public ip - dns
- load balancer - caddy

many vpses - many public ips - many dns
- kube external dns

hypervisor - many public ips - many dns
- kube external dns - could be AN INTERNAL DNS SERVER i guess??
https://xeiaso.net/


gainers
- miniflux
- obsidian
- notebooks

loss avoiders
- invidious (distraction free)

loss
- docker compose
- todo backlog - its infinite, how can i store it better - thats maintennce
- todo findnig hidden maintenence in your life? who talks abotu this stuff I need it!

current loss
- learning notebooks





containers
where am i running my software?
if its all on one host then maybe nix/guix are good? naw
docker compose is a really nice orchestraror for single nodes- alternatives? who else can work life docker compose?
[[workflow orchestrator]] with dagster + compose socket?!?!?!


compose
i think this server should run on this node so thats where i will deploy it
do you have the mental load to decide where your workloads will run? and set up networking and storage accordingly?

this is easy on a single vps
harder with more workloads but see stackoverflow

i want kubernetes to decide where my workload will run for me, and figure out all the networking for it


summary: you don't need distributed computing
overall: make sure to unbundle your deps - dont have compose files depend on resources from other compose files i.e networks
thats when you need to make use of tailscale and shit i think?? uhhh
i mean idk.. wellllllll

hmmm





[[centralized computing]]
nix/guix/systemd, compose, compose based paas, single node kubernetes!?!??!

[[distributed computing]]
kubernetes, swarm, (mesos/rancher/m)? paas = fly, containerless app run, etc