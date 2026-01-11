# Namespace

> **Certificacoes**: CKA (8%), CKAD (10%), KCNA (5%), CKS (5%)

## Conceitos Fundamentais

### O que sao Namespaces

Namespaces sao uma forma de dividir recursos de um cluster em **ambientes virtuais isolados**. Funcionam como "pastas" logicas que permitem organizar e isolar recursos, aplicar cotas e controlar acesso.

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title NAMESPACES - CONCEITO

note as N1
  Namespace = Ambiente virtual isolado dentro do cluster
end note

rectangle "Cluster Kubernetes" {
  rectangle "Namespace: default" #lightblue {
    card "Pod A" as pa
    card "Service A" as sa
  }

  rectangle "Namespace: production" #lightgreen {
    card "Pod B" as pb
    card "Service B" as sb
    card "ConfigMap B" as cb
  }

  rectangle "Namespace: development" #lightyellow {
    card "Pod C" as pc
    card "Service C" as sc
  }
}

note bottom
  - Recursos ISOLADOS por namespace
  - Mesmo nome pode existir em namespaces diferentes
  - Recursos cluster-scoped NAO pertencem a namespaces
end note

@enduml
```

### Namespaces Padrao do Kubernetes

O Kubernetes cria automaticamente alguns namespaces:

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title NAMESPACES PADRAO

rectangle "default" #lightblue {
  note as n1
    Namespace padrao para recursos
    sem namespace especificado
  end note
}

rectangle "kube-system" #lightcoral {
  note as n2
    Componentes do sistema Kubernetes:
    - kube-apiserver
    - kube-controller-manager
    - kube-scheduler
    - kube-proxy
    - CoreDNS
    - etcd (se em pod)
  end note
}

rectangle "kube-public" #lightgreen {
  note as n3
    Recursos publicos legiveis
    por todos (autenticados ou nao)
    Contem: cluster-info ConfigMap
  end note
}

rectangle "kube-node-lease" #lightyellow {
  note as n4
    Lease objects para heartbeat de nodes
    Melhora performance de deteccao
    de falhas de nodes
  end note
}

@enduml
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
@startuml
skinparam monochrome true
skinparam backgroundColor white

title MULTI-TENANCY COM NAMESPACES

rectangle "Cluster Kubernetes" {
  rectangle "Namespace: team-frontend" #lightblue {
    card "ResourceQuota: 4 CPU, 8Gi" as q1
    card "LimitRange" as l1
    card "NetworkPolicy" as n1
    card "RBAC: frontend-devs" as r1
  }

  rectangle "Namespace: team-backend" #lightgreen {
    card "ResourceQuota: 8 CPU, 16Gi" as q2
    card "LimitRange" as l2
    card "NetworkPolicy" as n2
    card "RBAC: backend-devs" as r2
  }

  rectangle "Namespace: team-data" #lightyellow {
    card "ResourceQuota: 16 CPU, 32Gi" as q3
    card "LimitRange" as l3
    card "NetworkPolicy" as n3
    card "RBAC: data-engineers" as r3
  }
}

@enduml
```

### Ambientes de Desenvolvimento

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title AMBIENTES POR NAMESPACE

rectangle "Cluster" {
  rectangle "development" #lightblue {
    card "app:dev"
    note right: Recursos limitados\nSem PodDisruptionBudget
  }

  rectangle "staging" #lightyellow {
    card "app:staging"
    note right: Configuracao similar a prod\nTestes de integracao
  }

  rectangle "production" #lightgreen {
    card "app:prod"
    note right: Recursos maiores\nNetworkPolicy restritiva\nRBAC rigoroso
  }
}

@enduml
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
@startuml
skinparam monochrome true
skinparam backgroundColor white

title DNS ENTRE NAMESPACES

rectangle "Namespace: frontend" #lightblue {
  card "Pod: web-app" as web
}

rectangle "Namespace: backend" #lightgreen {
  card "Service: api-service" as api
  note bottom of api
    FQDN: api-service.backend.svc.cluster.local
  end note
}

rectangle "Namespace: database" #lightyellow {
  card "Service: mysql" as db
  note bottom of db
    FQDN: mysql.database.svc.cluster.local
  end note
}

web --> api : api-service.backend
web --> db : mysql.database

note as N1
  Formato FQDN:
  <service>.<namespace>.svc.cluster.local

  Dentro do MESMO namespace:
  apenas <service>

  ENTRE namespaces:
  <service>.<namespace>
end note

@enduml
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
@startuml
skinparam monochrome true
skinparam backgroundColor white

title NAMESPACE-SCOPED vs CLUSTER-SCOPED

rectangle "NAMESPACE-SCOPED" #lightblue {
  card "Pod" as p1
  card "Deployment" as p2
  card "ReplicaSet" as p3
  card "StatefulSet" as p4
  card "DaemonSet" as p5
  card "Job / CronJob" as p6
  card "Service" as p7
  card "ConfigMap" as p8
  card "Secret" as p9
  card "PersistentVolumeClaim" as p10
  card "Role / RoleBinding" as p11
  card "ServiceAccount" as p12
  card "NetworkPolicy" as p13
  card "Ingress" as p14
  card "ResourceQuota" as p15
  card "LimitRange" as p16
}

rectangle "CLUSTER-SCOPED" #lightyellow {
  card "Node" as c1
  card "Namespace" as c2
  card "PersistentVolume" as c3
  card "StorageClass" as c4
  card "ClusterRole" as c5
  card "ClusterRoleBinding" as c6
  card "CustomResourceDefinition" as c7
  card "PriorityClass" as c8
  card "IngressClass" as c9
}

@enduml
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
@startuml
skinparam monochrome true
skinparam backgroundColor white

title RESOURCEQUOTA

rectangle "Namespace: team-a" {
  rectangle "ResourceQuota" #lightcoral {
    note as quota
      pods: 10
      requests.cpu: 4
      requests.memory: 8Gi
      limits.cpu: 8
      limits.memory: 16Gi
      persistentvolumeclaims: 5
      services.loadbalancers: 2
    end note
  }

  card "Pod 1\ncpu: 500m\nmem: 512Mi" as p1
  card "Pod 2\ncpu: 1\nmem: 1Gi" as p2
  card "Pod 3\ncpu: 500m\nmem: 512Mi" as p3

  note bottom
    Consumo atual:
    3/10 pods
    2/4 CPU requests
    2Gi/8Gi memory requests
  end note
}

@enduml
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
@startuml
skinparam monochrome true
skinparam backgroundColor white

title LIMITRANGE

rectangle "Namespace: team-a" {
  rectangle "LimitRange" #lightcoral {
    note as lr
      Container:
        default: cpu=500m, mem=512Mi
        defaultRequest: cpu=100m, mem=128Mi
        max: cpu=2, mem=2Gi
        min: cpu=50m, mem=64Mi
    end note
  }

  card "Pod sem recursos\n(recebe defaults)" as p1
  card "Pod com recursos\n(validado contra min/max)" as p2
}

@enduml
```

```yaml
../assets/limit-range/limitrange-resource-limits.yaml}}
```

## Troubleshooting

### Problemas Comuns

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title TROUBLESHOOTING - NAMESPACES

rectangle "Problema: Pod nao cria" #lightcoral {
  note as p1
    Causas:
    1. ResourceQuota excedida
    2. LimitRange violado
    3. Namespace em Terminating

    Solucao:
    kubectl describe ns <namespace>
    kubectl get resourcequota -n <ns>
    kubectl describe pod -n <ns>
  end note
}

rectangle "Problema: Service nao encontrado" #lightyellow {
  note as p2
    Causas:
    1. Service em namespace diferente
    2. DNS incorreto

    Solucao:
    Usar FQDN: service.namespace.svc
    kubectl get svc -A | grep <service>
  end note
}

rectangle "Problema: Namespace nao deleta" #lightgreen {
  note as p3
    Causas:
    1. Finalizers pendentes
    2. Recursos com finalizers

    Solucao:
    kubectl get ns <ns> -o yaml
    Verificar finalizers
    kubectl patch ns <ns> -p '{"metadata":{"finalizers":[]}}'
  end note
}

@enduml
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
@startuml
skinparam monochrome true
skinparam backgroundColor white

title BEST PRACTICES - NOMENCLATURA

rectangle "Padrao por Ambiente" #lightblue {
  card "development"
  card "staging"
  card "production"
}

rectangle "Padrao por Time" #lightgreen {
  card "team-frontend"
  card "team-backend"
  card "team-platform"
}

rectangle "Padrao por Projeto" #lightyellow {
  card "project-ecommerce"
  card "project-blog"
  card "project-api"
}

rectangle "Padrao Combinado" #lightcoral {
  card "frontend-production"
  card "backend-staging"
  card "api-development"
}

@enduml
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
