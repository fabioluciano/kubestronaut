# Namespace

> **Certificacoes**: CKA (8%), CKAD (10%), KCNA (5%), CKS (5%)

## Conceitos Fundamentais

### O que sao Namespaces

Namespaces sao uma forma de dividir recursos de um cluster em **ambientes virtuais isolados**. Funcionam como "pastas" logicas que permitem organizar e isolar recursos, aplicar cotas e controlar acesso.

```plantuml,format=png
../assets/diagrams/general/namespace-namespaces-conceito-1.puml
```

### Namespaces Padrao do Kubernetes

O Kubernetes cria automaticamente alguns namespaces:

```plantuml,format=png
../assets/diagrams/general/namespace-namespaces-padrao-1.puml
```

| Namespace | Descricao | Uso |
|-----------|-----------|-----|
| `default` | Namespace padrao para recursos sem namespace especificado | Recursos do usuario (nao recomendado para producao) |
| `kube-system` | Componentes internos do Kubernetes | API Server, Controller Manager, Scheduler, CoreDNS |
| `kube-public` | Recursos publicos, legiveis por todos | cluster-info ConfigMap |
| `kube-node-lease` | Objetos Lease para heartbeat de nodes | Lease de cada node para deteccao de falhas |

```admonish warning title="Importante para o Exame"
- NUNCA delete os namespaces `kube-system`, `kube-public` ou `kube-node-lease`
- Recursos sem namespace especificado vao para `default`
- Em producao, SEMPRE especifique o namespace
```

## Casos de Uso

### Multi-tenancy

```plantuml,format=png
../assets/diagrams/general/namespace-multi-tenancy-com-namespaces-1.puml
```

### Ambientes de Desenvolvimento

```plantuml,format=png
../assets/diagrams/general/namespace-ambientes-por-namespace-1.puml
```

## Exemplos Praticos

### Namespace Basico

```yaml
../assets/namespace/namespace-basico.yaml}}
```

### Namespace com ResourceQuota e LimitRange

```yaml
../assets/namespace/namespace-com-quotas-e-limits.yaml}}
```

### Deployment em Namespace Especifico

```yaml
../assets/namespace/deployment-em-namespace.yaml}}
```

### Comunicacao entre Namespaces

```yaml
../assets/namespace/pod-acesso-outro-namespace.yaml}}
```

### NetworkPolicy para Isolar Namespace

```yaml
../assets/namespace/networkpolicy-deny-other-namespaces.yaml}}
```

### RBAC por Namespace

```yaml
../assets/namespace/rbac-namespace.yaml}}
```

## DNS entre Namespaces

O Kubernetes DNS permite comunicacao entre namespaces usando FQDN (Fully Qualified Domain Name):

```plantuml,format=png
../assets/diagrams/general/namespace-dns-entre-namespaces-1.puml
```

| Contexto | Formato DNS | Exemplo |
|----------|-------------|---------|
| Mesmo namespace | `<service>` | `mysql` |
| Outro namespace | `<service>.<namespace>` | `mysql.database` |
| FQDN completo | `<service>.<namespace>.svc.cluster.local` | `mysql.database.svc.cluster.local` |

## Comandos Uteis

### Gerenciamento de Namespaces

```bash
# Criar namespace (imperativo)
kubectl create namespace development
kubectl create ns staging  # Alias

# Criar namespace (declarativo)
kubectl apply -f namespace.yaml

# Listar namespaces
kubectl get namespaces
kubectl get ns

# Descrever namespace
kubectl describe namespace kube-system

# Ver detalhes em YAML
kubectl get namespace default -o yaml

# Deletar namespace (CUIDADO: deleta TODOS recursos)
kubectl delete namespace development
```

### Trabalhando com Namespaces

```bash
# Listar recursos em namespace especifico
kubectl get pods -n kube-system
kubectl get all -n production

# Listar recursos em TODOS namespaces
kubectl get pods --all-namespaces
kubectl get pods -A  # Alias

# Criar recurso em namespace especifico
kubectl run nginx --image=nginx -n development
kubectl create deployment web --image=nginx -n staging

# Aplicar YAML em namespace especifico
kubectl apply -f deployment.yaml -n production

# Mudar namespace padrao do contexto
kubectl config set-context --current --namespace=development

# Ver namespace atual
kubectl config view --minify | grep namespace

# Criar alias para namespace (util no exame)
alias kn='kubectl config set-context --current --namespace'
kn production  # Muda para production
```

### ResourceQuota e LimitRange

```bash
# Ver quotas de um namespace
kubectl get resourcequota -n team-a
kubectl describe resourcequota -n team-a

# Ver limit ranges
kubectl get limitrange -n team-a
kubectl describe limitrange -n team-a

# Ver consumo atual vs quota
kubectl describe namespace team-a
```

## Recursos por Escopo

```plantuml,format=png
../assets/diagrams/general/namespace-namespace-scoped-vs-cluster-scoped-1.puml
```

```bash
# Listar recursos namespace-scoped
kubectl api-resources --namespaced=true

# Listar recursos cluster-scoped
kubectl api-resources --namespaced=false
```

## ResourceQuota por Namespace

ResourceQuota limita o consumo agregado de recursos em um namespace:

```plantuml,format=png
../assets/diagrams/general/namespace-resourcequota-1.puml
```

### Tipos de Quotas

| Tipo | Recursos |
|------|----------|
| **Compute** | `requests.cpu`, `requests.memory`, `limits.cpu`, `limits.memory` |
| **Storage** | `requests.storage`, `persistentvolumeclaims` |
| **Object Count** | `pods`, `services`, `secrets`, `configmaps`, `deployments.apps` |
| **Scoped** | `count/pods` com `scopeSelector` (BestEffort, NotBestEffort, etc.) |

```yaml
../assets/resource-quota/resourcequota-compute-quota-1.yaml}}
```

## LimitRange por Namespace

LimitRange define limites padrao e restricoes para containers/pods individuais:

```plantuml,format=png
../assets/diagrams/general/namespace-limitrange-1.puml
```

```yaml
../assets/limit-range/limitrange-resource-limits.yaml}}
```

## Troubleshooting

### Problemas Comuns

```plantuml,format=png
../assets/diagrams/general/namespace-troubleshooting-namespaces-1.puml
```

### Comandos de Diagnostico

```bash
# Namespace em Terminating que nao deleta
kubectl get namespace stuck-ns -o yaml
# Verificar finalizers e recursos pendentes

# Forcar delecao (CUIDADO)
kubectl get namespace stuck-ns -o json | \
  jq '.spec.finalizers = []' | \
  kubectl replace --raw "/api/v1/namespaces/stuck-ns/finalize" -f -

# Verificar quota excedida
kubectl describe resourcequota -n team-a
# Olhar "Used" vs "Hard"

# Verificar porque pod nao cria
kubectl describe pod pending-pod -n team-a
# Procurar eventos relacionados a quota/limits

# Listar todos recursos em um namespace
kubectl api-resources --verbs=list --namespaced -o name | \
  xargs -n 1 kubectl get --show-kind --ignore-not-found -n team-a
```

## Dicas para o Exame

```admonish tip title="Dicas CKA/CKAD"
1. **Mude o namespace padrao** no inicio do exame se necessario:
   ```bash
   kubectl config set-context --current --namespace=<ns>
   ```

2. **Use -n ou --namespace** em TODOS comandos se nao mudou o padrao

3. **Verifique o namespace** da questao antes de comecar

4. **DNS entre namespaces**: `service.namespace` ou FQDN completo

5. **ResourceQuota bloqueia pods** sem requests/limits se quota de compute existe

6. **LimitRange aplica defaults** automaticamente
```

```admonish warning title="Armadilhas Comuns"
- Esquecer de especificar namespace
- Deletar namespace kube-system acidentalmente
- Nao perceber que ResourceQuota exige requests/limits
- Confundir Role (namespace) vs ClusterRole (cluster)
```

### Template Rapido

```yaml
../assets/namespace/template-namespace-com-quotas.yaml}}
```

## Best Practices

### Nomenclatura

```plantuml,format=png
../assets/diagrams/general/namespace-best-practices-nomenclatura-1.puml
```

### Organizacao Recomendada

```bash
# Namespaces de sistema (nao modificar)
kube-system
kube-public
kube-node-lease

# Namespaces de infraestrutura
monitoring     # Prometheus, Grafana
logging        # ELK, Loki
ingress        # Ingress controllers
cert-manager   # Certificados

# Namespaces de aplicacao
<app>-dev
<app>-staging
<app>-prod

# Ou por time
<team>-dev
<team>-staging
<team>-prod
```

## Referencias

### Links Internos
- [ResourceQuota](resource-quota.md)
- [LimitRange](limit-range.md)
- [NetworkPolicy](security/network-policy.md)
- [RBAC](security/rbac.md)
- [DNS](dns.md)
- [Metadata](fundamentals/metadata.md)

### Documentacao Oficial
- [Namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
- [Resource Quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/)
- [Limit Ranges](https://kubernetes.io/docs/concepts/policy/limit-range/)
- [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
- [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)

---

> **Resumo**: Namespaces dividem o cluster em ambientes virtuais isolados. Namespaces padrao: default, kube-system, kube-public, kube-node-lease. Use ResourceQuota para limitar recursos agregados e LimitRange para defaults/limites individuais. DNS entre namespaces: `service.namespace.svc.cluster.local`. RBAC e NetworkPolicy sao namespace-scoped. Sempre especifique o namespace em producao.
