- É uma aplicação opensource que fornece e assegura conectividade de rede entre pods
- Por padrão usa criptografia de pod para pod



```shell
kubectl exec -ti -n kube-system cilium-4jm25 -- cilium-dbg status
```

```shell
kubectl exec -ti -n kube-system cilium-4jm25 -- cilium-health status
```

```yaml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "l3-egress-rule"
spec:
  endpointSelector:
    matchLabels:
      role: frontend
  egress:
  - toEndpoints:
    - matchLabels:
        role: backend

```


```yaml
# cks7262:~/8_p1.yaml
apiVersion: "cilium.io/v2"kind: CiliumNetworkPolicy
metadata:
	name: p1
	namespace: team-orange
spec:
	endpointSelector:
		matchLabels:
			type: messenger
	egressDeny:
		- toEndpoints:
			- matchLabels:
				type: database # we use the label of the Pods behind the Service "database"
```

```yaml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
	name: p2
	namespace: team-orange
spec:
	endpointSelector:
		matchLabels:
			type: transmitter # we use the label of the Pods behind Deployment "transmitter"
	egressDeny:
	- toEndpoints:
		- matchLabels:
			type: database
	  icmps:
		- fields:
			- type: 8
			  family: IPv4
			- type: EchoRequest
			  family: IPv6
```

```yaml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
	name: p3
	namespace: team-orange
spec:
	endpointSelector:
		- matchLabels:
			type: database
	egress:
		- toEndpoints:
			- matchLabels:
				type: messenger
		authentication:
			mode: "required" # Enable Mutual Authentication
```