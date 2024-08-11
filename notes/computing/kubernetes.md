this page is my teaching of kubernets
NOT my learnings







# security
temp) im planning on deploying some workloads to my kubernets cluster but they are completely separate from the existing stuff on the cluster - i never want any network traffic to cross or any volumes or other dat to be shared - how can i ensure they dont mix?                                                                                                                                                                         0
To ensure that your new workloads remain completely isolated from the existing workloads on your Kubernetes cluster, you can use several Kubernetes features and best practices. Here are the steps you can take:

### 1. Namespace Isolation
Namespaces are a key feature in Kubernetes to logically divide a cluster's resources for different applications or teams.

- **Create separate namespaces** for your workloads. This will provide a basic level of isolation.

  ```bash
  kubectl create namespace new-workloads
  kubectl create namespace existing-workloads
  ```

### 2. Network Policies
Network Policies are used to control the communication (ingress and egress) between different pods, services, and namespaces.

- **Define Network Policies** to restrict traffic between namespaces so that the new workloads cannot communicate with the old ones.

  Example Network Policy to deny all ingress traffic for a namespace:

  ```yaml
  apiVersion: networking.k8s.io/v1
  kind: NetworkPolicy
  metadata:
    name: deny-all-ingress
    namespace: new-workloads
  spec:
    podSelector: {}
    policyTypes:
    - Ingress
  ```

  Example Network Policy to deny all egress traffic for a namespace:

  ```yaml
  apiVersion: networking.k8s.io/v1
  kind: NetworkPolicy
  metadata:
    name: deny-all-egress
    namespace: new-workloads
  spec:
    podSelector: {}
    policyTypes:
    - Egress
  ```

  Ensure to apply Network Policies that deny traffic between the `new-workloads` and `existing-workloads` namespaces.

### 3. Resource Quotas and Limits
To avoid misuse of resources and to limit the impact of one set of workloads on another, you can use ResourceQuotas and LimitRanges.

- **Set Resource Quotas** for each namespace.

  ```yaml
  apiVersion: v1
  kind: ResourceQuota
  metadata:
    name: resource-quota
    namespace: new-workloads
  spec:
    hard:
      requests.cpu: "10"
      requests.memory: "20Gi"
      limits.cpu: "20"
      limits.memory: "40Gi"
  ```

### 4. RBAC (Role-Based Access Control)
Control access to resources within the cluster by assigning roles and bindings that limit users to specific namespaces.

- **Create Roles and RoleBindings** for your namespaces as needed.

  Example RoleBinding:

  ```yaml
  apiVersion: rbac.authorization.k8s.io/v1
  kind: RoleBinding
  metadata:
    name: read-only-binding
    namespace: new-workloads
  subjects:
  - kind: User
    name: "your-username"
    apiGroup: rbac.authorization.k8s.io
  roleRef:
    kind: Role
    name: read-only
    apiGroup: rbac.authorization.k8s.io
  ```

### 5. Storage Classes and Persistent Volume Claims
Ensure that the Persistent Volume Claims (PVCs) and Persistent Volumes (PVs) used by the new workloads are not shared with the existing ones.

- **Define separate Storage Classes** if needed and ensure **PVCs are namespaced**, which they are by default.

### 6. Resource Labels and Selectors
Use labels and selectors to scope resources and avoid unintended overlaps.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  namespace: new-workloads
  labels:
    app: my-app
spec:
  selector:
    matchLabels:
      app: my-app
```

### 7. Use Pod Security Policies and SecurityContext
Set security policies to enforce isolation for your pods.

- Define **Pod Security Policies** and ensure pods run with the least privilege.

  Example:

  ```yaml
  apiVersion: policy/v1beta1
  kind: PodSecurityPolicy
  metadata:
    name: restricted
  spec:
    privileged: false
    allowPrivilegeEscalation: false
    requiredDropCapabilities:
      - ALL
  ```

- Utilize the **SecurityContext** field in pod specifications to enforce security contexts.

  Example:

  ```yaml
  apiVersion: v1
  kind: Pod
  metadata:
    name: restricted-pod
    namespace: new-workloads
  spec:
    securityContext:
      runAsUser: 1000
      runAsGroup: 3000
      fsGroup: 2000
  ```

By combining these strategies, you can achieve a high level of isolation between your workloads, ensuring that they do not inadvertently share resources or network communication channels.

# todo
when kubectl apply, make sure nothing says configured because that would indicate change
side car container
- i want to be able to pop a sidecar pod in for debugging
	- ss -tupln
	- curl
	- maybe like a rich interactive curl? why can't i use the whole networking stack?
	- idk there should be a lot more stuff here
when is it time to split out service by microservice?
- oauth proxy - should it run in 
- are the problems you are having with oauth proxy because of orcherstration (kubernets) or app config (caddy!)
	- would debug service mesh really fix this? uhhhh
		- i feel like if it cant run without kube then you shouldnt be running it idk
	- i wanted to see which headers caddy was getting from oauth2 proxy
		- i could simulate the request from oauth2 proxy
		- i could make caddy log its requests
			- pita! i can barely understand caddy logs!
			- maybe that isn't what application logs are for...
		- i could put something in between caddy and oauth2 proxy
			- bingo! i think?
observability
- start using tools like honeycomb and axiom??
- https://play.honeycomb.io/sandbox/tours
- https://axiom.co/ (playground
- https://matthewsanabria.dev/posts/observability-companies-to-watch-in-2024/
cost analysis
- how much are my pods costing me????
- how can i optimize???

## workflow
https://xeiaso.net/vods/2024/gitea-k8s/
- todo watch more people deploy k9s
- dev workflow videos! amazing!
https://www.nomadproject.io/
- how is the workflow compared to kube? why does everything say it is nice and simple?

https://github.com/collabnix/kubelabs?tab=readme-ov-file

[[automated]] [[orchestrator]] 
[[distributed computing]] 

## [[tools]]
treasure trove of debugging tools! https://news.ycombinator.com/item?id=20774712
- https://github.com/vmware-archive/octant net viz
- observing kube resources!? https://github.com/pulumi/kubespy
- kubectx
	- https://github.com/danielfoehrKn/kubeswitch
https://blog.kubesimplify.com/10-things-you-might-not-know-about-k9s
- sanitize?
- pulses - install a metrics server
- kubectl-tree
k9s
- todo bench
- todo sanitize
logs
- kubetail - uselss?
- stern - yes!
	- todo improve this loop!
	- remember the loops! never hit more than 1 button to do shit!
kubectl diff https://kubernetes.io/docs/reference/kubectl/generated/kubectl_diff/

feedbkac loop
- https://superuser.com/questions/1433325/does-firefox-ignore-the-hosts-file-how-to-make-firefox-honor-the-hosts-file

- YESTERDAY YOU SPENT THE WHOLE DAY IN INNER FEEDBACK LOOPS
	- jvm reload
	- blah blah blah
- remember in docker compose we had a great way of nearly instantly reloading 
- lets do that here! lets use compose
	- rewrite caddy to compose
https://www.gitpod.io/blog/kubernetes-local-remote
- mock it with authelia
	- no mocks! mocks are a waste of time!
	- what if we just developed on prod!!
	- devspace, skaffold, tilt
	- bridge to kube (vscode)
		- kubefwd
			- kubefwd, bridge to kube (vscode)
			- 
		- https://www.getambassador.io/docs/telepresence/latest/quick-start
		- https://gefyra.dev/docs/getting-started-with-gefyra/
		- https://mirrord.dev/docs/overview/quick-start/
		- cringe https://www.architech.ca/articles/ditching-docker-compose-for-kubernetes
	- inner dev loop
		- https://www.getambassador.io/docs/telepresence/latest/concepts/devloop
	- signadot? https://doordash.engineering/2022/06/23/fast-feedback-loop-for-kubernetes-product-development-in-a-production-environment/

you don't need kubernetes
https://www.youtube.com/watch?v=H5sPGruv2yc






workload
- task
	- cronjob??
- service/daemon
	- daemonset???
	- idk?

misc:
service/loadbalancer/etc
- traefik with compose introduced me to those concepts PERFECTLY ahhhH!
- compare that workflow with docker!
	- DO BOTH REEEE

storage
- stateless
- cache
- persistent
- config
	- automates going in to persistent
	- so easy to vcs! compare to persistent writing scripts! this automates that!
- secrets?








1. running a pod - searxng
2. access it with port forward
	1. don't allow searxng to have network access?? idk
3. caddy -> volume
	1. editing the volume to manyally add the config
	2. https certs!
4. public ip on gke
	1. gcp reservered ip
	2. note it doesn't work on clusterip!
5. caddy -> config
	1. automates the volume
6. add searxng to caddy pod
	1. reverse proxy with 127.0.0.1
7. split searxng to other pod, then
8. pod - pod networking
	1. without service
		1. kubectl get ip
	2. with service - dns!
		1. ports and port selectors and stuff idk
9. caddy -> searxng
	1. services
		1. hey wait how come everyone can access everyone?
		2. network policy
10. caddy -> internet?
	1. idk
11. cleanup: jsonnet templating
12. gitops
	1. restart deployment? this is an antipattern!
	2. make all resources immutable!



gke
- how much is this joint costing me?!?!?

deloyments
- stern for logging
- rollout restart
	- i changed a secret lets go!q
	- https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/
	- when i rollout restart, how can i see the status???
- https://github.com/stakater/Reloader/
	- update a config map???

network policies
- use case
	- prevent searxng from accessing redlib
	- prevent database from accessing internet
- viz?
	- how can i see my network policies visually?
	- https://editor.networkpolicy.io/
	- https://networkpolicy.io/
	- https://artturik.github.io/network-policy-viewer/
- testing?
	- e2e tests? idk... how do i know my network policies are working?!?
- implementation
	- https://k0sproject.io/
	- minikube
		- minikube start --cni calico
		- https://minikube.sigs.k8s.io/docs/handbook/network_policy/
	- bruh



liveness/healthcechk???
