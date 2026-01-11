# NetworkPolicy

## Conceitos Fundamentais

### O que é NetworkPolicy?

NetworkPolicy é um recurso do Kubernetes que controla o tráfego de rede entre Pods no cluster. Por padrão, todos os Pods podem se comunicar livremente - NetworkPolicies implementam segmentação de rede (microsegmentação).

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam defaultTextAlignment center
skinparam rectangle {
  roundCorner 10
}

title COMPORTAMENTO PADRÃO

rectangle "SEM NetworkPolicy" {
  rectangle "Pod A" as PA1
  rectangle "Pod B" as PB1
  rectangle "Pod C" as PC1
  
  PA1 <--> PB1
  PB1 <--> PC1
  PA1 <--> PC1
  
  note bottom of PB1 : Todos se comunicam livremente
}

rectangle "COM NetworkPolicy" {
  rectangle "Pod A\n(frontend)" as PA2
  rectangle "Pod B\n(backend)" as PB2
  rectangle "Pod C\n(database)" as PC2
  
  PA2 --> PB2 : permitido
  PB2 ..> PC2 : bloqueado
  
  note bottom of PB2 : Tráfego controlado por políticas
}
@enduml
```

### Pré-requisitos

```plantuml,format=png
@startuml
skinparam monochrome true

map "CNI COMPATÍVEIS" as cni {
  Compatíveis => Calico, Cilium, Weave Net, Antrea, Romana
  NÃO suportam => Flannel (padrão em alguns clusters)
}

note bottom of cni
  ⚠️ **ATENÇÃO**
  NetworkPolicy sem CNI compatível:
  O recurso é criado mas NÃO é aplicado!
end note
@enduml
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
@startuml
skinparam monochrome true

object "policyTypes: [Ingress]" as p1 {
  Ingress = Apenas tráfego definido nas regras
  Egress = Todo tráfego permitido (não restrito)
}

object "policyTypes: [Egress]" as p2 {
  Ingress = Todo tráfego permitido (não restrito)
  Egress = Apenas tráfego definido nas regras
}

object "policyTypes: [Ingress, Egress]" as p3 {
  Ingress = Apenas tráfego definido nas regras
  Egress = Apenas tráfego definido nas regras
}

object "Sem policyTypes definido" as p4 {
  "Se houver ingress rules" = Ingress restrito
  "Se houver egress rules" = Egress restrito
}

p1 -[hidden]-> p2
p2 -[hidden]-> p3
p3 -[hidden]-> p4
@enduml
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
@startuml
skinparam monochrome true

title ⚠️ CUIDADO COM A SINTAXE

rectangle "OU lógico (dois itens)" {
  note as N1
    from:
      - podSelector: {...}
      - namespaceSelector: {...}
  end note
}

rectangle "E lógico (um item)" {
  note as N2
    from:
      - podSelector: {...}
        namespaceSelector: {...}
  end note
}
@enduml
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
@startuml
skinparam monochrome true

title MÚLTIPLAS NETWORKPOLICIES

rectangle "Pod" as pod
rectangle "Policy A\n(permite porta 80)" as pA
rectangle "Policy B\n(permite porta 443)" as pB

pA --> pod
pB --> pod

note bottom of pod
  **Resultado: permite porta 80 E 443**
  
  Se múltiplas NetworkPolicies selecionam o mesmo Pod:
  • Regras são ADITIVAS (união)
  • Tráfego é permitido se QUALQUER policy permite
  • NÃO há ordem de precedência
end note
@enduml
```

---

## Dicas para os Exames

```plantuml,format=png
@startuml
skinparam monochrome true

map "DICAS CKA/CKS - NETWORKPOLICY" as dicas {
  Padrão => Sem NetworkPolicy = tudo permitido
  podSelector: {} => Seleciona TODOS os pods do namespace
}

note bottom of dicas
  **Seletores críticos:**
  • podSelector - mesmo namespace
  • namespaceSelector - outros namespaces
  • ipBlock - IPs externos

  **Cuidado com sintaxe AND vs OR:**
  from:
    - pod: A
    - ns: B    → POD A **OU** NS B (itens separados)

  from:
    - pod: A
      ns: B    → POD A **E** NS B (mesmo item)

  **Default deny egress quebra DNS!**
  Lembre de liberar porta 53 UDP/TCP para kube-dns

  **CIDR:**
  • 0.0.0.0/0 = todos os IPs
  • x.x.x.x/32 = um único IP
end note
@enduml
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
