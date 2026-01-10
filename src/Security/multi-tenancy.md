# Multi-Tenancy

## Conceitos Fundamentais

### O que é Multi-Tenancy?

Multi-tenancy é a prática de compartilhar um cluster Kubernetes entre múltiplos usuários, times ou aplicações (tenants), mantendo isolamento e segurança.

```plantuml,format=png
!include ../assets/diagrams/security/multi-tenancy-modelos-de-multi-tenancy-1.puml
```

### Camadas de Isolamento

```plantuml,format=png
!include ../assets/diagrams/security/multi-tenancy-camadas-de-isolamento-1.puml
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
!include ../assets/diagrams/security/multi-tenancy-classes-de-qos-1.puml
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
!include ../assets/diagrams/security/multi-tenancy-opções-de-criptografia-pod-to-pod-1.puml
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
!include ../assets/diagrams/security/multi-tenancy-dicas-cks-multi-tenancy-1.puml
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
