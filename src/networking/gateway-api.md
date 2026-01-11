# Gateway API

## Conceitos Fundamentais

### O que é Gateway API?

Gateway API é a evolução do Ingress no Kubernetes. Oferece uma forma mais expressiva, extensível e orientada a roles para gerenciar tráfego de entrada (e futuramente saída) no cluster.

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title INGRESS vs GATEWAY API

rectangle "INGRESS (Legado)" {
  card "✗ Apenas HTTP/HTTPS" as i1
  card "✗ Configuração monolítica" as i2
  card "✗ Extensibilidade via annotations" as i3
  card "✗ Um recurso (Ingress) para tudo" as i4
}

rectangle "GATEWAY API (Moderno)" {
  card "✓ HTTP, HTTPS, TCP, UDP, gRPC, TLS" as g1
  card "✓ Separação de responsabilidades (roles)" as g2
  card "✓ Extensível via CRDs nativos" as g3
  card "✓ Múltiplos recursos especializados" as g4
  card "✓ Portabilidade entre implementações" as g5
}

@enduml
```

### Arquitetura e Recursos

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title GATEWAY API RESOURCES

rectangle "GatewayClass (Cluster-scoped)" as gc {
  note as n1
    Define o "tipo" de Gateway (implementação)
    Gerenciado pelo Cluster Admin
  end note
}

rectangle "Gateway (Namespace-scoped)" as gw {
  note as n2
    Instância que escuta em portas/IPs
    Gerenciado pelo Cluster Admin/Platform Team
  end note
}

rectangle "HTTPRoute / TCPRoute / GRPCRoute / etc." as route {
  note as n3
    Define regras de roteamento
    Gerenciado pelo App Developer
  end note
}

rectangle "Service / Backend" as svc

gc --> gw
gw --> route
route --> svc

@enduml
```

### Separação de Responsabilidades

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title ROLES - SEPARAÇÃO DE RESPONSABILIDADES

rectangle "Infrastructure Provider" {
  note as n1
    Implementa e mantém o GatewayClass controller
    Ex: NGINX, Istio, Contour, Traefik
  end note
}

rectangle "Cluster Operator / Platform Admin" {
  note as n2
    Cria GatewayClass
    Cria Gateway (define listeners, TLS)
    Define quais namespaces podem usar o Gateway
  end note
}

rectangle "Application Developer" {
  note as n3
    Cria Routes (HTTPRoute, TCPRoute, etc)
    Define regras de roteamento para seus Services
    Não precisa entender infraestrutura
  end note
}

@enduml
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
@startuml
skinparam monochrome true
skinparam defaultFontName Monospaced

title DICAS CKA/CKAD - GATEWAY API

note as N1
  **Hierarquia:**
  GatewayClass → Gateway → HTTPRoute → Service

  **GatewayClass:** Define implementação (nginx, istio, etc)
  **Gateway:** Define listeners (portas, TLS)
  **HTTPRoute:** Define regras de roteamento

  **HTTPRoute.parentRefs:**
    - name: gateway-name
    - namespace: gateway-ns (se diferente)
    - sectionName: listener-name (opcional)

  **Path types:**
    • Exact - match exato
    • PathPrefix - prefixo (mais comum)

  **Weight para canary:**
  backendRefs:
    - name: v1, weight: 90
    - name: v2, weight: 10
end note

@enduml
```

---

## Referências

- [Service](service.md)
- [Networking](./index.md)
- [DNS](dns.md)
- [TLS](../security/tls.md)

