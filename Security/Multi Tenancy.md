- Múltiplos interessados acessando o mesmo cluster
- usar RBAC pra limitar quais recursos os usuários podem manipular
- usar namespaces
- usar network policies

- Control Plane
	 - Namespace
	 - Access Control - RBAC ABAC
	 - Quotas - limita os recursos computacionais utilizados por um namespace

- Data Plane
	- NetWork Isolation - Network Policy
	- Storage Isolation - StorageClass
	- Node Isolation - Taints e Tolerations

- Definir `PriorityClass` para definir quais pods têm mais prioridade que outros. No Pod, usar a opção `spec.priorityClassName`

## Quality of Service

- Separa os pods em categorias usando os limites e requests de recursos
- São três tipos:
	- Guaranteed - Quanto os requests e limits são os mesmos
	- Burstable - Quando o limit é maior que o request
	- BestEffort - Não é configurado request nem limits

## DNS
- É possível limitar a resolução de DNS por namespace usandoa a opção `fallthrough in-namespace` do CoreDNS


Pop to pod encryption
 - Usar service mesh
 - Cilium
 - Calico IPSEC