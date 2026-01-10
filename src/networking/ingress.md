# Ingress

```admonish info title="Certificações"
CKAD (20%), CKA (20%)
```

## 📖 Conceitos

### O que é

Ingress é um objeto que gerencia acesso externo HTTP/HTTPS aos serviços do cluster. Funciona como um proxy reverso.

### Ingress vs Service

| Recurso | Propósito | Protocolos |
|---------|-----------|------------|
| **Service NodePort** | Expõe porta em cada node | TCP/UDP |
| **Service LoadBalancer** | LB do cloud provider | TCP/UDP |
| **Ingress** | Roteamento HTTP/HTTPS | HTTP/HTTPS |

### Componentes

- **Ingress Resource**: Objeto que define regras de roteamento
- **Ingress Controller**: Implementação que processa as regras (nginx, traefik, etc)

## 🔧 Ingress Controller

### Instalação (nginx)

```bash
# Instalar nginx ingress controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml

# Verificar instalação
kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx
```

### Verificar Controller

```bash
# Ver pods do controller
kubectl get pods -n ingress-nginx

# Ver service (IP externo)
kubectl get svc -n ingress-nginx

# Ver logs
kubectl logs -n ingress-nginx <pod-name>
```

## 📝 Ingress Resource

### Estrutura Básica

```yaml
{{#include ../assets/ingress/ingress-basic.yaml}}
```

### PathType

| Tipo | Comportamento |
|------|---------------|
| **Prefix** | Match por prefixo (`/app` match `/app`, `/app/v1`) |
| **Exact** | Match exato (`/app` só match `/app`) |
| **ImplementationSpecific** | Depende do controller |

## 💻 Exemplos Práticos

### Exemplo 1: Ingress Simples

```yaml
{{#include ../assets/ingress/ingress-simple.yaml}}
```

### Exemplo 2: Host-based Routing

```yaml
{{#include ../assets/ingress/ingress-host-based.yaml}}
```

### Exemplo 3: Path-based Routing

```yaml
{{#include ../assets/ingress/ingress-path-based.yaml}}
```

### Exemplo 4: Ingress com TLS

```yaml
{{#include ../assets/ingress/ingress-tls.yaml}}
```

```bash
# Criar secret TLS
kubectl create secret tls tls-secret \
  --cert=tls.crt \
  --key=tls.key
```

### Exemplo 5: Default Backend

```yaml
{{#include ../assets/ingress/ingress-default-backend.yaml}}
```

## 🔧 Annotations Comuns (nginx)

```yaml
{{#include ../assets/networking/ingress-example-1.yaml}}
```

## 🔧 Comandos Úteis

```bash
# Criar ingress via kubectl
kubectl create ingress my-ingress \
  --rule="app.example.com/=service:80" \
  --class=nginx

# Listar ingresses
kubectl get ingress

# Ver detalhes
kubectl describe ingress <name>

# Ver regras
kubectl get ingress <name> -o yaml

# Testar (se tiver IP do ingress)
curl -H "Host: app.example.com" http://<ingress-ip>/
```

## 🐛 Troubleshooting

### Problema: Ingress não funciona

```bash
# 1. Verificar se controller está rodando
kubectl get pods -n ingress-nginx

# 2. Verificar se ingress foi processado
kubectl describe ingress <name>

# 3. Verificar endpoints do service
kubectl get endpoints <service-name>

# 4. Ver logs do controller
kubectl logs -n ingress-nginx <controller-pod>
```

### Problema: 404 Not Found

**Causas comuns**:
- Service não existe
- Endpoints vazios (pods não matcham selector)
- Path incorreto

```bash
# Verificar service
kubectl get svc <service-name>
kubectl get endpoints <service-name>
```

### Problema: 503 Service Unavailable

**Causa**: Backend não disponível

```bash
# Verificar se pods estão rodando
kubectl get pods -l <label-selector>

# Verificar endpoints
kubectl get endpoints <service-name>
```

## 🎓 Dicas para o Exame

### Criação Rápida

```bash
# Via kubectl create
kubectl create ingress simple \
  --rule="host/path=service:port"

# Exemplo completo
kubectl create ingress app-ingress \
  --rule="app.example.com/*=app-service:80" \
  --class=nginx
```

### Lembrar

1. `ingressClassName` é obrigatório em versões novas
2. Service deve existir e ter endpoints
3. TLS requer secret do tipo `kubernetes.io/tls`
4. PathType é obrigatório

### YAML Mínimo

```yaml
{{#include ../assets/ingress/ingress-minimal.yaml}}
```

## 🔗 Referências

### Documentação
- [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [Ingress Controllers](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/)
- [nginx Ingress](https://kubernetes.github.io/ingress-nginx/)

### Arquivos Relacionados
- [Service](service.md) - Services do Kubernetes
- [TLS/Ingress](../security/ingress.md) - Ingress com TLS (segurança)
- [Gateway API](gateway-api.md) - Nova API de gateway
- [NetworkPolicy](../security/network-policy.md) - Políticas de rede
