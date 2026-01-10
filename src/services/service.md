# Service

<span class="badge badge-ckad">CKAD</span> <span class="badge badge-cka">CKA</span>

---

## O que é um Service?

```admonish info title="Service"
Service é uma abstração que define um conjunto lógico de Pods e uma política de acesso a eles. Permite expor aplicações de forma estável, independente do ciclo de vida dos Pods.
```

### Características Principais

| Aspecto | Descrição |
|---------|-----------|
| **IP Estável** | Cada Service recebe um ClusterIP fixo |
| **DNS** | Acessível via `<service>.<namespace>.svc.cluster.local` |
| **Load Balancing** | Distribui requisições entre Pods (round-robin) |
| **Descoberta** | Via DNS ou variáveis de ambiente |

### Arquitetura

```
          ┌─────────────┐
          │   Client    │
          └──────┬──────┘
                 │
          ┌──────▼──────┐
          │   Service   │ ← ClusterIP: 10.96.0.100
          │  (selector) │
          └──────┬──────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
┌───▼───┐   ┌───▼───┐   ┌───▼───┐
│ Pod 1 │   │ Pod 2 │   │ Pod 3 │
│ :8080 │   │ :8080 │   │ :8080 │
└───────┘   └───────┘   └───────┘
```

---

## Tipos de Service

| Tipo | Descrição | Use Case |
|------|-----------|----------|
| `ClusterIP` | Acesso interno ao cluster (padrão) | Comunicação entre microservices |
| `NodePort` | Expõe porta em todos os nodes (30000-32767) | Acesso externo simples |
| `LoadBalancer` | Cria load balancer externo (cloud) | Produção em cloud |
| `ExternalName` | CNAME para serviço externo | Integração com serviços externos |

### ClusterIP (Padrão)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: ClusterIP  # Padrão, pode ser omitido
  selector:
    app: my-app
  ports:
    - port: 80        # Porta do Service
      targetPort: 8080 # Porta do container
```

### NodePort

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-nodeport
spec:
  type: NodePort
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8080
      nodePort: 30080  # Opcional (30000-32767)
```

```admonish note title="NodePort"
- Todos os nodes respondem na mesma porta
- Cria automaticamente um ClusterIP
- Porta entre 30000-32767
```

### LoadBalancer

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-loadbalancer
spec:
  type: LoadBalancer
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8080
```

```admonish warning title="LoadBalancer"
Requer integração com cloud provider (AWS, GCP, Azure) ou MetalLB em bare-metal.
```

### ExternalName

```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-db
spec:
  type: ExternalName
  externalName: database.example.com
```

---

## Headless Service

```admonish tip title="Headless Service"
Service com `clusterIP: None` retorna os IPs dos Pods diretamente via DNS, sem load balancing.
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: headless-service
spec:
  clusterIP: None  # Headless
  selector:
    app: my-stateful-app
  ports:
    - port: 80
```

**Use cases:**
- StatefulSets (cada Pod precisa de DNS único)
- Service discovery direto para Pods
- Quando cliente precisa conhecer todos os Pods

---

## Descoberta de Services

### Via DNS (Recomendado)

```bash
# Formato completo
<service>.<namespace>.svc.cluster.local

# Mesmo namespace (simplificado)
<service>

# Exemplo
curl http://my-service.default.svc.cluster.local:80
curl http://my-service:80
```

### Via Variáveis de Ambiente

```bash
# Variáveis injetadas automaticamente
# (apenas para services criados ANTES do Pod)

MY_SERVICE_SERVICE_HOST=10.96.0.100
MY_SERVICE_SERVICE_PORT=80
```

---

## Múltiplas Portas

```yaml
apiVersion: v1
kind: Service
metadata:
  name: multi-port
spec:
  selector:
    app: my-app
  ports:
    - name: http    # Nome obrigatório com múltiplas portas
      port: 80
      targetPort: 8080
    - name: https
      port: 443
      targetPort: 8443
```

---

## Comandos Úteis

```bash
# Criar service via expose
kubectl expose pod my-pod --port=80 --target-port=8080

# Criar service para deployment
kubectl expose deployment my-deploy --port=80 --type=NodePort

# Listar services
kubectl get svc

# Detalhes do service
kubectl describe svc my-service

# Ver endpoints associados
kubectl get endpoints my-service

# Testar DNS do service
kubectl run -ti --rm debug --image=busybox -- nslookup my-service
```

### Verificar Ranges de IP

```bash
# Range de IPs dos Services
kubectl cluster-info dump | grep service-cluster-ip-range

# CIDR dos Pods
kubectl cluster-info dump | grep cluster-cidr
```

---

## Troubleshooting

### Service não conecta aos Pods

```bash
# 1. Verificar selector
kubectl get svc my-service -o yaml | grep -A5 selector

# 2. Verificar labels dos Pods
kubectl get pods --show-labels

# 3. Verificar endpoints
kubectl get endpoints my-service
# Se vazio → selector não bate com labels

# 4. Verificar se Pods estão Ready
kubectl get pods -l app=my-app
```

### Testar conectividade

```bash
# De dentro do cluster
kubectl run -ti --rm debug --image=nicolaka/netshoot -- curl http://my-service:80

# DNS resolve?
kubectl run -ti --rm debug --image=busybox -- nslookup my-service.default.svc.cluster.local
```

---

## Dicas para os Exames

```admonish tip title="Dicas CKA/CKAD"
1. **ClusterIP é padrão**: Não precisa especificar `type`
2. **NodePort range**: 30000-32767
3. **kubectl expose**: Forma rápida de criar services
4. **Endpoints vazios**: Problema de selector/labels
5. **Headless**: Use para StatefulSets
```

---

## Referências

- [Endpoints](endpoint.md) - Mapeamento Service → Pods
- [Ingress](../networking/ingress.md) - Roteamento HTTP/HTTPS
- [DNS](../networking/dns.md) - Resolução de nomes
