# NetworkPolicy

## Conceitos Fundamentais

### O que é NetworkPolicy?

NetworkPolicy é um recurso do Kubernetes que controla o tráfego de rede entre Pods no cluster. Por padrão, todos os Pods podem se comunicar livremente - NetworkPolicies implementam segmentação de rede (microsegmentação).

```plantuml,format=png
!include ../assets/diagrams/security/network-policy-comportamento-padrão-1.puml
```

### Pré-requisitos

```plantuml,format=png
!include ../assets/diagrams/security/network-policy-diagram-2-1.puml
```

### Direções de Tráfego

| Direção | Descrição |
|---------|-----------|
| **Ingress** | Tráfego ENTRANDO no Pod selecionado |
| **Egress** | Tráfego SAINDO do Pod selecionado |

---

## Estrutura do NetworkPolicy

### Estrutura Completa

```yaml
{{#include ../assets/network-policy/example-policy.yaml}}
```

### Comportamento dos PolicyTypes

```plantuml,format=png
!include ../assets/diagrams/security/network-policy-diagram-3-1.puml
```

---

## Seletores

### podSelector

Seleciona Pods por labels **no mesmo namespace** da NetworkPolicy.

```yaml
{{#include ../assets/network-policy/pod-selector-example.yaml}}
```

### namespaceSelector

Seleciona Pods de **outros namespaces**.

```yaml
{{#include ../assets/network-policy/namespace-selector-example.yaml}}
```

### Combinando podSelector e namespaceSelector

```yaml
{{#include ../assets/network-policy/combined-selectors-example.yaml}}
```

```plantuml,format=png
!include ../assets/diagrams/security/network-policy-cuidado-com-a-sintaxe-1.puml
```

### ipBlock

Seleciona por bloco de IP CIDR.

```yaml
{{#include ../assets/network-policy/ipblock-example.yaml}}
```

```plaintext
CIDR Notação:
• 0.0.0.0/0    - Todos os IPs
• 10.0.0.1/32  - Um único IP
• 10.0.0.0/24  - 256 IPs (10.0.0.0 - 10.0.0.255)
• 10.0.0.0/16  - 65536 IPs (10.0.0.0 - 10.0.255.255)
```

---

## Padrões Comuns

### Default Deny All (Ingress)

```yaml
{{#include ../assets/network-policy/default-deny-ingress.yaml}}
```


### Deny All

```yaml
{{#include ../assets/networkpolicy/netpol-deny-all-test.yaml}}
```
### Default Deny All (Egress)

```yaml
{{#include ../assets/network-policy/default-deny-egress.yaml}}
```

### Default Deny All (Ingress + Egress)

```yaml
{{#include ../assets/network-policy/default-deny-all.yaml}}
```

### Allow All (Ingress)

```yaml
{{#include ../assets/network-policy/allow-all-ingress.yaml}}
```


### Allow All

```yaml
{{#include ../assets/networkpolicy/netpol-allow-all-test.yaml}}
```
### Allow All (Egress)

```yaml
{{#include ../assets/network-policy/allow-all-egress.yaml}}
```

---

## Exemplos Práticos

### Exemplo 1: Frontend → Backend → Database

```yaml
{{#include ../assets/network-policy/frontend-backend-database.yaml}}
```

### Exemplo 2: Permitir DNS (Egress)

```yaml
{{#include ../assets/network-policy/allow-dns.yaml}}
```

### Exemplo 3: Cross-Namespace

```yaml
{{#include ../assets/network-policy/allow-monitoring.yaml}}
```

---

## Proteção de Metadata Cloud

### Bloquear Acesso ao Metadata Service

Na cloud (AWS, GCP, Azure), o endpoint de metadata (`169.254.169.254`) pode expor informações sensíveis se o Pod for comprometido.

```yaml
{{#include ../assets/network-policy/block-metadata-access.yaml}}
```

---

## Comandos kubectl

```bash
# Criar NetworkPolicy
kubectl apply -f network-policy.yaml

# Listar NetworkPolicies
kubectl get networkpolicies -A
kubectl get netpol -A  # Alias

# Detalhes
kubectl describe networkpolicy <name>

# Ver YAML
kubectl get networkpolicy <name> -o yaml

# Deletar
kubectl delete networkpolicy <name>
```

---

## Troubleshooting

### Verificar se CNI Suporta NetworkPolicy

```bash
# Verificar qual CNI está em uso
kubectl get pods -n kube-system | grep -E 'calico|cilium|weave'

# Se for flannel, NetworkPolicies NÃO funcionam!
```

### Testar Conectividade

```bash
# Pod temporário para teste
kubectl run test --rm -it --image=busybox -- /bin/sh

# Testar conexão de dentro do pod
wget -qO- --timeout=2 http://backend-svc:8080

# Testar DNS
nslookup backend-svc

# Testar porta específica
nc -zv backend-svc 8080
```

### Debug com Labels

```bash
# Ver labels dos Pods
kubectl get pods --show-labels

# Ver labels dos Namespaces
kubectl get namespaces --show-labels

# Adicionar label ao namespace (necessário para namespaceSelector)
kubectl label namespace production env=production
```

### Múltiplas Policies

```plantuml,format=png
!include ../assets/diagrams/security/network-policy-múltiplas-networkpolicies-1.puml
```

---

## Dicas para os Exames

```plantuml,format=png
!include ../assets/diagrams/security/network-policy-diagram-6-1.puml
```

---

## Referências

- [Networking](../networking/index.md)
- [DNS](../networking/dns.md)
- [Service](../networking/service.md)
- [Cilium](cilium.md)
- [Pod](../workloads/pod.md)


---

### Ingress Policy

```yaml
{{#include ../assets/networkpolicy/netpol-ingress-test.yaml}}
```


---

### Egress Policy

```yaml
{{#include ../assets/networkpolicy/netpol-egress-test.yaml}}
```


---

### Bloquear Metadata Service

```yaml
{{#include ../assets/networkpolicy/cks/block-metadata-retrieval.yaml}}
```
