# Gateway API

## Conceitos Fundamentais

### O que é Gateway API?

Gateway API é a evolução do Ingress no Kubernetes. Oferece uma forma mais expressiva, extensível e orientada a roles para gerenciar tráfego de entrada (e futuramente saída) no cluster.

```plantuml,format=png
!include ../assets/diagrams/networking/gateway-api-ingress-vs-gateway-api-1.puml
```

### Arquitetura e Recursos

```plantuml,format=png
!include ../assets/diagrams/networking/gateway-api-gateway-api-resources-1.puml
```

### Separação de Responsabilidades

```plantuml,format=png
!include ../assets/diagrams/networking/gateway-api-roles-separação-de-responsabilidades-1.puml
```

---

## Instalação

### Instalar CRDs

```bash
# Instalar versão estável (Standard channel)
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.0.0/standard-install.yaml

# Instalar versão experimental (com recursos adicionais)
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.0.0/experimental-install.yaml

# Verificar CRDs instalados
kubectl get crds | grep gateway
```

### Implementações Disponíveis

| Implementação | GatewayClass |
|--------------|--------------|
| NGINX Gateway Fabric | nginx |
| Istio | istio |
| Contour | contour |
| Traefik | traefik |
| Envoy Gateway | envoy |
| Kong | kong |
| HAProxy | haproxy |
| Cilium | cilium |

---

## GatewayClass

### O que é GatewayClass?

GatewayClass define qual controller/implementação gerenciará os Gateways. Similar ao conceito de StorageClass.

```yaml
{{#include ../assets/gateway-api/gatewayclass.yaml}}
```

### Listar GatewayClasses

```bash
kubectl get gatewayclass

# Output:
# NAME    CONTROLLER                                   ACCEPTED   AGE
# nginx   gateway.nginx.org/nginx-gateway-controller   True       5m
```

---

## Gateway

### Estrutura do Gateway

```yaml
{{#include ../assets/gateway-api/gateway.yaml}}
```

### allowedRoutes

```yaml
{{#include ../assets/gateway-api/allowed-routes.yaml}}
```

---

## HTTPRoute

### Estrutura Básica

```yaml
{{#include ../assets/gateway-api/httproute-basic.yaml}}
```

### Path Matching

```yaml
{{#include ../assets/gateway-api/path-matching.yaml}}
```

### Header Matching

```yaml
{{#include ../assets/gateway-api/header-matching.yaml}}
```

### Method Matching

```yaml
{{#include ../assets/gateway-api/method-matching.yaml}}
```

### Query Parameter Matching

```yaml
{{#include ../assets/gateway-api/query-param-matching.yaml}}
```

---

## Exemplos Práticos

### Exemplo 1: Roteamento por Path

```yaml
{{#include ../assets/gateway-api/path-routing.yaml}}
```

### Exemplo 2: Canary Deployment (Weight-based)

```yaml
{{#include ../assets/gateway-api/canary-route.yaml}}
```

### Exemplo 3: Header-based Routing (A/B Testing)

```yaml
{{#include ../assets/gateway-api/ab-testing-route.yaml}}
```

### Exemplo 4: Redirect e Rewrite

```yaml
{{#include ../assets/gateway-api/redirect-rewrite-route.yaml}}
```

---

## TCPRoute e outros Routes

### TCPRoute (para tráfego TCP/não-HTTP)

```yaml
{{#include ../assets/gateway-api/tcproute.yaml}}
```

### GRPCRoute

```yaml
{{#include ../assets/gateway-api/grpcroute.yaml}}
```

---

## Comandos Úteis

```bash
# Listar GatewayClasses
kubectl get gatewayclass

# Listar Gateways
kubectl get gateway -A

# Listar HTTPRoutes
kubectl get httproute -A

# Detalhes de um Gateway
kubectl describe gateway main-gateway -n gateway-system

# Ver status de uma HTTPRoute
kubectl get httproute app-route -o yaml

# Ver IP/hostname do Gateway
kubectl get gateway main-gateway -o jsonpath='{.status.addresses[0].value}'
```

---

## Troubleshooting

### Route Não Funciona

```bash
# 1. Verificar status do Gateway
kubectl describe gateway <gateway-name>
# Verificar Conditions: Accepted, Programmed

# 2. Verificar status da HTTPRoute
kubectl describe httproute <route-name>
# Verificar Parents e Conditions

# 3. Verificar se parentRef está correto
# - namespace correto
# - sectionName se especificado

# 4. Verificar allowedRoutes no Gateway
# - from: All/Same/Selector
# - namespaces permitidos
```

### Gateway Não Aceita Routes

```yaml
{{#include ../assets/gateway-api/troubleshooting-allowed-routes.yaml}}
```

```bash
# Adicionar label ao namespace
kubectl label namespace app-ns gateway-access=true
```

---

## Dicas para os Exames

```plantuml,format=png
!include ../assets/diagrams/networking/gateway-api-dicas-ckackad-gateway-api-1.puml
```

---

## Referências

- [Service](service.md)
- [Networking](./index.md)
- [DNS](dns.md)
- [TLS](../security/tls.md)

