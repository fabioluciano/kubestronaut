# Cilium

> **Certificações**: CKS (Network Policies), CKA (Networking)

## Conceitos Fundamentais

### O que é Cilium?

Cilium é uma solução de networking, observabilidade e segurança para Kubernetes baseada em **eBPF** (extended Berkeley Packet Filter). Fornece funcionalidades avançadas que vão além das NetworkPolicies nativas do Kubernetes.

```admonish info title="Por que Cilium?"
- Usa eBPF para processamento de pacotes no kernel (alta performance)
- Suporta políticas L3/L4 (IP/porta) e L7 (HTTP, gRPC, Kafka)
- Criptografia transparente pod-to-pod (WireGuard/IPsec)
- Observabilidade profunda com Hubble
- Substitui kube-proxy com melhor performance
```

### Arquitetura do Cilium

| Componente | Descrição |
|------------|-----------|
| **cilium-agent** | DaemonSet em cada node, gerencia eBPF programs |
| **cilium-operator** | Deployment para tarefas cluster-wide |
| **Hubble** | Observabilidade de rede (opcional) |
| **Hubble Relay** | Agrega dados de todos os nodes |
| **Hubble UI** | Interface gráfica para visualização |

### Cilium vs NetworkPolicy Nativa

| Funcionalidade | NetworkPolicy K8s | Cilium |
|----------------|-------------------|--------|
| **L3/L4** | ✅ | ✅ |
| **L7 (HTTP, gRPC)** | ❌ | ✅ |
| **FQDN/DNS** | ❌ | ✅ |
| **Criptografia** | ❌ | ✅ (WireGuard/IPsec) |
| **Cluster Mesh** | ❌ | ✅ |
| **Observabilidade** | ❌ | ✅ (Hubble) |
| **Egress Gateway** | ❌ | ✅ |

---

## Instalação

### Via Helm (Recomendado)

```bash
# Adicionar repo
helm repo add cilium https://helm.cilium.io/
helm repo update

# Instalar com configurações padrão
helm install cilium cilium/cilium --version 1.15.0 \
  --namespace kube-system

# Instalar com Hubble habilitado
helm install cilium cilium/cilium --version 1.15.0 \
  --namespace kube-system \
  --set hubble.relay.enabled=true \
  --set hubble.ui.enabled=true

# Instalar substituindo kube-proxy
helm install cilium cilium/cilium --version 1.15.0 \
  --namespace kube-system \
  --set kubeProxyReplacement=true
```

### Valores Helm para Cilium

```yaml
{{#include ../assets/cilium/cilium.yaml}}
```

### Verificar Instalação

```bash
# Status do Cilium
kubectl -n kube-system get pods -l k8s-app=cilium

# Status detalhado
kubectl exec -ti -n kube-system cilium-xxxxx -- cilium status

# Health check
kubectl exec -ti -n kube-system cilium-xxxxx -- cilium-health status

# Verificar conectividade
cilium connectivity test
```

---

## Comandos Essenciais

### cilium CLI

```bash
# Instalar CLI
curl -L --remote-name-all https://github.com/cilium/cilium-cli/releases/latest/download/cilium-linux-amd64.tar.gz
tar xzvf cilium-linux-amd64.tar.gz
sudo mv cilium /usr/local/bin/

# Status do cluster
cilium status

# Teste de conectividade completo
cilium connectivity test

# Ver endpoints
cilium endpoint list

# Ver identities
cilium identity list
```

### Comandos no cilium-agent

```shell
# Status geral
kubectl exec -ti -n kube-system cilium-xxxxx -- cilium-dbg status

# Health dos nodes
kubectl exec -ti -n kube-system cilium-xxxxx -- cilium-health status

# Listar endpoints
kubectl exec -ti -n kube-system cilium-xxxxx -- cilium-dbg endpoint list

# Ver políticas aplicadas
kubectl exec -ti -n kube-system cilium-xxxxx -- cilium-dbg policy get

# Monitor de tráfego em tempo real
kubectl exec -ti -n kube-system cilium-xxxxx -- cilium-dbg monitor
```

---

## CiliumNetworkPolicy

### Estrutura Básica

```yaml
{{#include ../assets/cilium/ciliumnetworkpolicy-basic.yaml}}
```

### CiliumNetworkPolicy vs NetworkPolicy

```yaml
# NetworkPolicy nativa (L3/L4 apenas)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy

# CiliumNetworkPolicy (L3/L4/L7)
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy

# CiliumClusterwideNetworkPolicy (cluster-scoped)
apiVersion: cilium.io/v2
kind: CiliumClusterwideNetworkPolicy
```

---

## Políticas L3/L4

### Default Deny

```yaml
{{#include ../assets/cilium/ciliumnetworkpolicy-default-deny.yaml}}
```

### Isolate Namespace

```yaml
{{#include ../assets/cilium/ciliumnetworkpolicy-isolate-namespace.yaml}}
```

### Backend Ingress

```yaml
{{#include ../assets/cilium/ciliumnetworkpolicy-backend-ingress.yaml}}
```

### Frontend Egress

```yaml
{{#include ../assets/cilium/ciliumnetworkpolicy-frontend-egress.yaml}}
```

### Egress Deny

```yaml
{{#include ../assets/cilium/ciliumnetworkpolicy-egress-deny.yaml}}
```

### Deny ICMP

```yaml
{{#include ../assets/cilium/ciliumnetworkpolicy-deny-icmp.yaml}}
```

---

## Políticas L7 (Application Layer)

### Policy HTTP L7

```yaml
{{#include ../assets/cilium/ciliumnetworkpolicy-basic.yaml}}
```


---

### Default Deny

```yaml
{{#include ../assets/cilium/ciliumnetworkpolicy-default-deny.yaml}}
```


---

### Policy HTTP L7

```yaml
{{#include ../assets/cilium/ciliumnetworkpolicy-l7-http.yaml}}
```


---

### Policy com FQDN

```yaml
{{#include ../assets/cilium/ciliumnetworkpolicy-fqdn.yaml}}
```

---

### Valores Helm para Cilium

```yaml
{{#include ../assets/cilium/cilium.yaml}}
```

---

### Allow DNS e HTTPS

```yaml
{{#include ../assets/cilium/ciliumnetworkpolicy-allow-dns-https.yaml}}
```

---

### Backend Ingress

```yaml
{{#include ../assets/cilium/ciliumnetworkpolicy-backend-ingress.yaml}}
```

---

### Deny ICMP

```yaml
{{#include ../assets/cilium/ciliumnetworkpolicy-deny-icmp.yaml}}
```

---

### Egress Deny

```yaml
{{#include ../assets/cilium/ciliumnetworkpolicy-egress-deny.yaml}}
```

---

### Frontend Egress

```yaml
{{#include ../assets/cilium/ciliumnetworkpolicy-frontend-egress.yaml}}
```

---

### Isolate Namespace

```yaml
{{#include ../assets/cilium/ciliumnetworkpolicy-isolate-namespace.yaml}}
```

---

### Encryption com WireGuard (Helm)

```yaml
{{#include ../assets/cilium/helm-encryption-wireguard.yaml}}
```

---

## Hubble (Observabilidade)

### Habilitar Hubble

```bash
# Via Helm upgrade
helm upgrade cilium cilium/cilium \
  --namespace kube-system \
  --reuse-values \
  --set hubble.relay.enabled=true \
  --set hubble.ui.enabled=true

# Verificar
kubectl get pods -n kube-system -l k8s-app=hubble-relay
kubectl get pods -n kube-system -l k8s-app=hubble-ui
```

### hubble CLI

```bash
# Port-forward para o relay
kubectl port-forward -n kube-system svc/hubble-relay 4245:80 &

# Ver fluxos em tempo real
hubble observe

# Filtrar por namespace
hubble observe --namespace production

# Ver apenas drops (tráfego bloqueado)
hubble observe --verdict DROPPED

# Ver fluxos HTTP
hubble observe --protocol http
```

---

## Criptografia de Rede

### WireGuard (Recomendado)

```bash
# Habilitar via Helm
helm upgrade cilium cilium/cilium \
  --namespace kube-system \
  --reuse-values \
  --set encryption.enabled=true \
  --set encryption.type=wireguard

# Verificar status
kubectl exec -ti -n kube-system cilium-xxxxx -- cilium-dbg encrypt status
```

---

## Troubleshooting

### Verificar Status

```bash
# Status geral
cilium status

# Ver logs do agent
kubectl logs -n kube-system -l k8s-app=cilium --tail=100

# Monitor de tráfego bloqueado
kubectl exec -ti -n kube-system cilium-xxxxx -- cilium-dbg monitor --type drop
```

```admonish failure title="Pods não conseguem se comunicar"
1. Verificar se Cilium está healthy: `cilium status`
2. Verificar se há policies bloqueando: `hubble observe --verdict DROPPED`
3. Verificar endpoints: `cilium endpoint list`
```

---

## Dicas para o Exame CKS

```admonish tip title="Dicas CKS - Cilium"
1. **CiliumNetworkPolicy vs NetworkPolicy**: Saiba quando usar cada uma
2. **L7 policies**: Cilium permite filtrar por HTTP method/path
3. **FQDN policies**: Permite egress por domínio DNS
4. **Hubble**: Use para debugar tráfego bloqueado
5. **Default deny**: Sempre comece isolando e depois permita
```

---

## Referências

- [Cilium Documentation](https://docs.cilium.io/)
- [CiliumNetworkPolicy Reference](https://docs.cilium.io/en/stable/network/kubernetes/policy/)
- [Network Policy](network-policy.md) - NetworkPolicies nativas do Kubernetes
