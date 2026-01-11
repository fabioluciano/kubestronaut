# API Objects

```admonish info title="Certificações"
KCNA (18%), CKA (25%), CKAD (25%), CKS (10%)
```

## 📖 Conceitos Fundamentais

### O que são API Objects

API Objects são entidades persistentes no sistema Kubernetes que representam o estado do cluster. Tudo no Kubernetes é um objeto: Pods, Services, Deployments, Secrets, etc.

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title API OBJECTS - CONCEITO

note as N1
  API Object = Representação do estado no cluster
end note

rectangle "O que você DECLARA" {
  card "Quais workloads rodar (Pods, Deployments)" as w1
  card "Quais recursos usar (PV, ConfigMap, Secret)" as w2
  card "Como expor serviços (Service, Ingress)" as w3
  card "Políticas de segurança (NetworkPolicy, RBAC)" as w4
}

rectangle "O que o Kubernetes FAZ" {
  card "Persiste objetos no etcd" as k1
  card "Monitora estado atual vs desejado" as k2
  card "Reconcilia diferenças (control loop)" as k3
  card "Atualiza status dos objetos" as k4
}

@enduml
```

### Declarativo vs Imperativo

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title DECLARATIVO vs IMPERATIVO

rectangle "IMPERATIVO (como fazer)" {
  note as imp
    kubectl run nginx --image=nginx
    kubectl scale deployment nginx --replicas=3
    kubectl set image deployment/nginx nginx=nginx:1.21
  end note
}

rectangle "DECLARATIVO (o que quero)" {
  note as dec
    kubectl apply -f deployment.yaml
  end note
  
  note as yaml
    deployment.yaml:
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: nginx
    spec:
      replicas: 3
      template:
        spec:
          containers:
          - image: nginx:1.21
  end note
}

note as rec
  ✅ RECOMENDADO: Declarativo
  • Versionável (Git)
  • Reproduzível
  • Auditável
  • GitOps friendly
end note

@enduml
```

## 📋 Estrutura de um Object

### Campos Obrigatórios

Todo objeto Kubernetes DEVE ter estes campos:

```yaml
../assets/api-objects/pod-campos-obrigatorios.yaml}}
```

### Anatomia Completa

```yaml
../assets/api-objects/deployment-anatomia-completa.yaml}}
```

## 🏷️ Metadata

### Labels

Labels são pares key-value usados para **identificar** e **selecionar** objetos:

```yaml
../assets/api-objects/metadata-labels.yaml}}
```

**Convenções recomendadas** (app.kubernetes.io):

| Label | Descrição |
|-------|-----------|
| `app.kubernetes.io/name` | Nome da aplicação |
| `app.kubernetes.io/instance` | Nome único da instância |
| `app.kubernetes.io/version` | Versão da aplicação |
| `app.kubernetes.io/component` | Componente dentro da aplicação |
| `app.kubernetes.io/part-of` | Aplicação de maior nível |
| `app.kubernetes.io/managed-by` | Ferramenta que gerencia |

### Selectors

```yaml
../assets/api-objects/selectors.yaml}}
```

```bash
# Selecionar com kubectl
kubectl get pods -l app=nginx
kubectl get pods -l 'environment in (prod,staging)'
kubectl get pods -l 'app=nginx,tier!=backend'
kubectl get pods -l 'release'  # label existe
kubectl get pods -l '!deprecated'  # label não existe
```

### Annotations

Annotations armazenam **metadata não-identificadora**:

```yaml
../assets/api-objects/metadata-annotations.yaml}}
```

**Diferença Labels vs Annotations**:

| Aspecto | Labels | Annotations |
|---------|--------|-------------|
| **Propósito** | Identificar/Selecionar | Metadata adicional |
| **Uso em selectors** | ✅ Sim | ❌ Não |
| **Tamanho** | Limitado (63 chars) | Até 256KB |
| **Indexado no etcd** | ✅ Sim | ❌ Não |

## 📦 Tipos de Objetos

### Por Escopo

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title ESCOPO DOS OBJETOS

rectangle "NAMESPACE-SCOPED (isolados por namespace)" #lightblue {
  card "Pods" as p1
  card "Deployments, ReplicaSets, StatefulSets, DaemonSets" as p2
  card "Services, Endpoints" as p3
  card "ConfigMaps, Secrets" as p4
  card "PersistentVolumeClaims" as p5
  card "Jobs, CronJobs" as p6
  card "Roles, RoleBindings" as p7
  card "ServiceAccounts" as p8
  card "NetworkPolicies" as p9
  card "Ingresses" as p10
}

rectangle "CLUSTER-SCOPED (globais no cluster)" #lightyellow {
  card "Nodes" as c1
  card "Namespaces" as c2
  card "PersistentVolumes" as c3
  card "StorageClasses" as c4
  card "ClusterRoles, ClusterRoleBindings" as c5
  card "CustomResourceDefinitions (CRDs)" as c6
  card "PriorityClasses" as c7
}

@enduml
```

### Por Categoria

| Categoria | Objetos |
|-----------|---------|
| **Workloads** | Pod, Deployment, ReplicaSet, StatefulSet, DaemonSet, Job, CronJob |
| **Networking** | Service, Ingress, NetworkPolicy, Endpoints |
| **Storage** | PersistentVolume, PersistentVolumeClaim, StorageClass |
| **Configuration** | ConfigMap, Secret |
| **Security** | ServiceAccount, Role, RoleBinding, ClusterRole, ClusterRoleBinding |
| **Scheduling** | PriorityClass, LimitRange, ResourceQuota |

## 🔄 Ciclo de Vida

### Estados de um Pod

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title POD LIFECYCLE

[*] --> Pending
Pending --> Running
Pending --> Unschedulable
Running --> Succeeded : exit 0
Running --> Failed : exit != 0
Succeeded --> [*]
Failed --> [*]

note right of Pending
  Aceito, mas containers
  não criados
end note

note right of Running
  Pelo menos um
  container rodando
end note

note right of Succeeded
  Todos containers terminaram
  com sucesso (exit 0)
end note

note right of Failed
  Pelo menos um
  container falhou
end note

@enduml
```

### Owner References e Garbage Collection

```yaml
../assets/api-objects/owner-references.yaml}}
```

**Garbage Collection Policies**:

| Policy | Comportamento |
|--------|---------------|
| `Foreground` | Owner bloqueado até dependentes deletados |
| `Background` | Owner deletado imediatamente, dependentes em background |
| `Orphan` | Dependentes não são deletados |

```bash
# Deletar deployment mantendo ReplicaSets/Pods
kubectl delete deployment nginx --cascade=orphan

# Deletar deployment e todos dependentes (padrão)
kubectl delete deployment nginx
```

## 📋 Comandos Essenciais

```bash
# Criar objeto
kubectl apply -f object.yaml        # Declarativo (recomendado)
kubectl create -f object.yaml       # Imperativo

# Ler objeto
kubectl get pods
kubectl get pod nginx -o yaml       # YAML completo
kubectl get pod nginx -o json       # JSON
kubectl describe pod nginx          # Descrição legível

# Atualizar objeto
kubectl apply -f object.yaml        # Apply (merge)
kubectl replace -f object.yaml      # Replace (substitui tudo)
kubectl edit pod nginx              # Editar interativamente
kubectl patch pod nginx -p '{"spec":{"containers":[{"name":"nginx","image":"nginx:1.22"}]}}'

# Deletar objeto
kubectl delete pod nginx
kubectl delete -f object.yaml
kubectl delete pods --all           # Todos no namespace

# Labels
kubectl label pod nginx env=prod
kubectl label pod nginx env-        # Remove label
kubectl get pods -l env=prod

# Annotations
kubectl annotate pod nginx description="Web server"
kubectl annotate pod nginx description-

# Ver estrutura do objeto
kubectl explain pod
kubectl explain pod.spec.containers
kubectl explain pod --recursive
```

## 💡 Dicas para Exame

### Estrutura Básica

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title DICAS - API OBJECTS

rectangle "1️⃣ CAMPOS OBRIGATÓRIOS" {
  note as n1
    apiVersion, kind, metadata.name, spec
  end note
}

rectangle "2️⃣ DESCOBRIR apiVersion" {
  note as n2
    kubectl api-resources | grep <recurso>
  end note
}

rectangle "3️⃣ DESCOBRIR spec" {
  note as n3
    kubectl explain <recurso>.spec
  end note
}

rectangle "4️⃣ GERAR YAML" {
  note as n4
    kubectl create <recurso> ... --dry-run=client -o yaml
  end note
}

rectangle "5️⃣ VALIDAR ANTES DE APLICAR" {
  note as n5
    kubectl apply -f file.yaml --dry-run=server
  end note
}

rectangle "6️⃣ LABELS vs ANNOTATIONS" {
  note as n6
    Labels: para selecionar (app=nginx)
    Annotations: para metadata (description="...")
  end note
}

@enduml
```

### Selectors Rápidos

```bash
# Igualdade
kubectl get pods -l app=nginx

# Conjunto
kubectl get pods -l 'app in (nginx,apache)'

# Negação
kubectl get pods -l app!=nginx

# Existência
kubectl get pods -l release

# Múltiplos
kubectl get pods -l 'app=nginx,environment=prod'
```

## 📚 Referências

### Links Internos
- [API](api/api.md)
- [Metadata](fundamentals/metadata.md)
- [Namespace](fundamentals/namespace.md)
- [Pod](workloads/pod.md)
- [Deployment](workloads/deployment.md)
- [kubectl](tools/kubectl.md)

### Documentação Oficial
- [Understanding Kubernetes Objects](https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects/)
- [Labels and Selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)
- [Annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/)
- [Field Selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/field-selectors/)
- [Owners and Dependents](https://kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/)

---

> **Resumo**: API Objects são entidades persistentes que representam estado no Kubernetes. Campos obrigatórios: apiVersion, kind, metadata.name, spec. Labels são para identificação/seleção; Annotations para metadata adicional. Objetos podem ser namespace-scoped ou cluster-scoped. Owner References controlam garbage collection. Use `kubectl explain` para descobrir estrutura e `--dry-run=client -o yaml` para gerar YAML.
