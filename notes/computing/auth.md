

overview
- https://www.ory.sh/oauth2-openid-connect-do-you-need-use-cases-examples/
- https://www.keycloak.org/docs/latest/securing_apps/
- https://www.authelia.com/overview/authorization/openid-connect-1.0/
- https://xpufx.com/posts/protecting-your-first-app-with-authentik/

relying parties
- https://oauth2-proxy.github.io/oauth2-proxy/configuration/providers/openid_connect?_highlight=oidc
- lowkey unmaintained :( https://github.com/vouch/vouch-proxy
- too specficic
	- https://github.com/nginxinc/nginx-openid-connect
	- nope! https://github.com/envoyproxy/envoy/issues/21982
	- NOPE! https://github.com/greenpau/caddy-security
	- nawwww https://www.haproxy.com/blog/using-haproxy-as-an-api-gateway-part-2-authentication
- yes! todo try with auth0??
	- https://docs.konghq.com/hub/kong-inc/openid-connect/
	- https://tyk.io/docs/basic-config-and-security/security/authentication-authorization/openid-connect/

# big big big
https://openid.net/developers/certified-openid-connect-implementations/
https://github.com/lastlogin-io/obligator?tab=readme-ov-file#comparison-is-the-thief-of-joy
https://news.ycombinator.com/item?id=37848793
https://news.ycombinator.com/item?id=37858095
https://news.ycombinator.com/item?id=34093857
https://news.ycombinator.com/item?id=18980737

auth0
- expensive??
- https://auth0.com/docs/authenticate/login/oidc-conformant-authentication
- https://auth0.com/docs/authenticate/login/oidc-conformant-authentication/oidc-adoption-auth-code-flow
fusionauth
- no free tier
- https://fusionauth.io/docs/lifecycle/authenticate-users/integrations/oidc/
workos
- sheeeesh
- no oidc connect
authress
- .0012/api call???
- no oidc connect
ory
- $70 expensive!
clerk
- $25 https://clerk.com/pricing
- oauth??? no web ui lol https://clerk.com/docs/advanced-usage/clerk-idp
zitadell
- wierd, requires first/last name? LMAO WHO CARS
- ?? yes? https://zitadel.com/docs/apis/openidoauth/endpoints
logto
- idp locked behind paywall
- run this!!
- yes! https://news.ycombinator.com/item?id=32031649
- https://logto.io/en/products/idp
- not self service https://docs.logto.io/docs/recipes/user-profile/#recap
https://stytch.com/
- nope https://forum.stytch.com/t/does-stytch-support-oidc-idp-provider/293
stack
- lmao https://stack-auth.com/pricing

code
supabase
firebase
supertokens

self hosted
- casdoor
- authentik
	- complex but yes lol
- keycloak
	- yes lol
- authelia
	- too small, doesnt support social sign in


TIME TO GO DEEP ON AUTH0
TIME BOX RESEARCH PHASE
# oathkeeper
https://github.com/lastlogin-io/obligator?tab=readme-ov-file#comparison-is-the-thief-of-joy
https://news.ycombinator.com/item?id=37848793
https://www.ory.sh/docs/oathkeeper
kong/nginx/envoy/aws api gateway??/
- act as policy decision point?
- https://github.com/gen1us2k/kong_showcase/blob/master/docker-compose.yml
- https://github.com/ory/kratos-selfservice-ui-node
- https://github.com/ory/examples/tree/master
- https://www.ory.sh/zero-trust-api-security-ory-tutorial/
- https://hackernoon.com/secure-microservices-with-kong-and-ory

# requirements
- authentication
	- openid connect provider
		- https://www.scottbrady91.com/openid-connect/openid-connect-overview
		- 
		- so i can integrate with oauth2 proxy/kong/tyk/whateva
		- must suppoort
			- self service - https://docs.logto.io/docs/recipes/user-profile/#recap
				- user management
				- email/pass/forget pass
				- social sign in
					- not authelia
				- account deletion!?? naw?
- authorization
	- detached from authentication!?!??