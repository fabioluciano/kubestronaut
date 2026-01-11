# Multi-Tenancy

## Conceitos Fundamentais

### O que é Multi-Tenancy?

Multi-tenancy é a prática de compartilhar um cluster Kubernetes entre múltiplos usuários, times ou aplicações (tenants), mantendo isolamento e segurança.

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title MODELOS DE MULTI-TENANCY

map "SOFT MULTI-TENANCY" as soft {
  Tenants => Times da mesma organização
  Confiança => Entre tenants
  Isolamento => Por namespaces
  Complexidade => Mais simples de implementar
}

map "HARD MULTI-TENANCY" as hard {
  Tenants => Não confiam uns nos outros
  Escopo => Pode incluir clientes externos
  Isolamento => Rigoroso em todas as camadas
  Complexidade => Requer mais configuração
}

@enduml
```

### Camadas de Isolamento

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title CAMADAS DE ISOLAMENTO

package "CONTROL PLANE ISOLATION" {
  [Namespaces] as ns
  note right of ns : separação lógica
  [RBAC] as rbac
  note right of rbac : controle de acesso
  [ResourceQuotas] as rq
  note right of rq : limites de recursos
  [LimitRanges] as lr
  note right of lr : defaults e limites por pod
}

package "DATA PLANE ISOLATION" {
  [NetworkPolicy] as np
  note right of np : isolamento de rede
  [Storage] as st
  note right of st : StorageClass por tenant
  [Node Isolation] as ni
  note right of ni : taints/tolerations, nodeSelector
}

package "RUNTIME ISOLATION" {
  [Pod Security] as ps
  note right of ps : PSA/PSS
  [RuntimeClass] as rc
  note right of rc : gVisor, Kata
  [Seccomp/AppArmor] as sa
}

@enduml
```

---

## Control Plane Isolation

### Namespaces

```yaml
{{#include ../assets/security/multi-tenancy/namespaces.yaml}}
```

### RBAC por Tenant

```yaml
{{#include ../assets/security/multi-tenancy/rbac-tenant.yaml}}
```

### ResourceQuota por Tenant

```yaml
{{#include ../assets/security/multi-tenancy/resource-quota.yaml}}
```

### LimitRange por Tenant

```yaml
{{#include ../assets/security/multi-tenancy/limit-range.yaml}}
```

---

## Data Plane Isolation

### NetworkPolicy por Tenant

```yaml
{{#include ../assets/security/multi-tenancy/network-policy.yaml}}
```

### StorageClass por Tenant

```yaml
{{#include ../assets/security/multi-tenancy/storage-class-tenant.yaml}}
```

### Node Isolation (Dedicated Nodes)

```bash
# Taint nodes para tenant específico
kubectl taint nodes node-1 tenant=team-a:NoSchedule
kubectl label nodes node-1 tenant=team-a
```

```yaml
{{#include ../assets/security/multi-tenancy/pod-node-isolation.yaml}}
```

---

## Quality of Service (QoS)

### Classes de QoS

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title CLASSES DE QoS

map "GUARANTEED (Prioridade Alta)" as guaranteed {
  Recursos => requests == limits para CPU e memória
  Eviction => Último a ser evicted
}

map "BURSTABLE (Prioridade Média)" as burstable {
  Recursos => requests < limits
  Eviction => Evicted após BestEffort
}

map "BESTEFFORT (Prioridade Baixa)" as besteffort {
  Recursos => Sem requests nem limits
  Eviction => Primeiro a ser evicted
}

@enduml
```

### Exemplos de QoS

```yaml
{{#include ../assets/security/multi-tenancy/qos-pods.yaml}}
```

### Verificar QoS

```bash
kubectl get pod <pod-name> -o jsonpath='{.status.qosClass}'
```

---

## PriorityClass

### Criar PriorityClass

```yaml
{{#include ../assets/security/multi-tenancy/priority-class.yaml}}
```

### Usar PriorityClass

```yaml
{{#include ../assets/security/multi-tenancy/pod-priority.yaml}}
```

---

## DNS Isolation

### Limitar Resolução DNS por Namespace

```yaml
{{#include ../assets/security/multi-tenancy/coredns-config.yaml}}
```

---

## Pod-to-Pod Encryption

### Opções de Criptografia

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title OPÇÕES DE CRIPTOGRAFIA POD-TO-POD

map "1. SERVICE MESH (Istio, Linkerd)" as mesh {
  Recurso => mTLS automático entre pods
  Desvantagem => Mais overhead
}

map "2. CILIUM (WireGuard)" as cilium {
  Recurso => Criptografia transparente
  Vantagem => Performance melhor que IPsec
}

map "3. CALICO (IPsec/WireGuard)" as calico {
  Recurso => Suporta ambos IPsec e WireGuard
}

map "4. WEAVE NET" as weave {
  Recurso => Criptografia sleeve mode
}

@enduml
```

### Cilium com WireGuard

```bash
# Instalar Cilium com encryption
helm install cilium cilium/cilium \
  --namespace kube-system \
  --set encryption.enabled=true \
  --set encryption.type=wireguard
```

---

## Dicas para o Exame CKS

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title DICAS CKS - MULTI-TENANCY

map "CAMADAS DE ISOLAMENTO" as camadas {
  Control Plane => Namespace, RBAC, Quotas
  Data Plane => NetworkPolicy, Storage, Nodes
  Runtime => PSA, RuntimeClass, Seccomp
}

map "QoS Classes (ordem de eviction)" as qos {
  1 => BestEffort (primeiro)
  2 => Burstable
  3 => Guaranteed (último)
}

map "Definições QoS" as defqos {
  Guaranteed => requests == limits
  Burstable => requests < limits
  BestEffort => sem resources
}

map "PriorityClass" as priority {
  value => maior = prioridade maior
  preemption => pode evictar pods de menor prioridade
}

note as N1
  **NetworkPolicy default deny:**
  spec:
    podSelector: {}
    policyTypes: [Ingress, Egress]
end note

@enduml
```

---

## Referências

- [Namespace](fundamentals/namespace.md)
- [RBAC](rbac.md)
- [ResourceQuota](../configuration/resource-quota.md)
- [LimitRange](../configuration/limit-range.md)
- [NetworkPolicy](network-policy.md)
- [Pod Security Admission](pod-security-admission.md)
- [RuntimeClass](runtime-classes.md)
