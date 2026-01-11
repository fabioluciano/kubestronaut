# KCNA - Kubernetes and Cloud Native Associate

## Visão Geral do Exame

### Informações do Exame

| Aspecto | Detalhes |
|---------|----------|
| **Duração** | 90 minutos |
| **Formato** | Múltipla escolha |
| **Questões** | ~60 questões |
| **Nota mínima** | 75% |
| **Validade** | 3 anos |
| **Retake** | 1 retake gratuito |
| **Proctored** | Sim, online |

### Distribuição do Currículo

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title DOMÍNIOS DO KCNA

card "Kubernetes Fundamentals" as kf #lightgray
card "Container Orchestration" as co #lightgray
card "Cloud Native Architecture" as cna #lightgray
card "Cloud Native Observability" as cno #lightgray
card "Application Delivery" as ad #lightgray

note right of kf : 46%
note right of co : 22%
note right of cna : 16%
note right of cno : 8%
note right of ad : 8%

@enduml
```

---

## Domínio 1: Kubernetes Fundamentals (46%)

### 1.1 Recursos Kubernetes

#### Pods

```plaintext
Pod = Menor unidade deployável no Kubernetes
    = 1 ou mais containers compartilhando:
      - Network namespace (mesmo IP)
      - Storage (volumes)
      - Lifecycle
```

#### Workloads

| Recurso | Propósito | Casos de Uso |
|---------|-----------|--------------|
| **Deployment** | Apps stateless | Web servers, APIs |
| **StatefulSet** | Apps stateful | Databases, caches |
| **DaemonSet** | 1 pod por node | Logging, monitoring |
| **Job** | Execução única | Migrations, backups |
| **CronJob** | Execução agendada | Reports, cleanup |

#### Services

| Tipo | Descrição |
|------|-----------|
| **ClusterIP** | IP interno do cluster (default) |
| **NodePort** | Expõe em porta do node (30000-32767) |
| **LoadBalancer** | Load balancer externo (cloud) |
| **ExternalName** | Alias DNS para serviço externo |

### 1.2 Arquitetura Kubernetes

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title ARQUITETURA K8S

rectangle "CONTROL PLANE" {
  component "kube-apiserver\n(API Gateway)" as api
  component "etcd\n(Key-Value DB)" as etcd
  component "kube-scheduler\n(Pod Placement)" as sched
  component "controller-mgr\n(Controllers)" as ctrl
}

rectangle "WORKER NODES" {
  component "kubelet\n(Node Agent)" as kubelet
  component "kube-proxy\n(Network Rules)" as proxy
  component "Container Runtime\n(CRI)" as cri
}

api <--> kubelet

@enduml
```

### 1.3 API e Kubectl

```bash
# Formato de recursos
<api-group>/<version>/<resource>

# Exemplos
apps/v1/deployments
v1/pods                    # Core API (sem grupo)
networking.k8s.io/v1/ingresses

# Explorar API
kubectl api-resources      # Listar todos recursos
kubectl api-versions       # Listar versões de API
kubectl explain pod.spec   # Documentação inline
```

### 1.4 RBAC

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title RBAC

rectangle "WHO (Subject)" {
  card "User" as u
  card "Group" as g
  card "ServiceAccount" as sa
}

rectangle "WHAT (Rules)" {
  card "Role" as r
  card "ClusterRole" as cr
}

rectangle "BINDING" {
  card "RoleBinding" as rb
  card "ClusterRoleBinding" as crb
}

u --> rb
g --> rb
sa --> rb
r --> rb
cr --> crb

note bottom
  Role/RoleBinding = Namespace scope
  ClusterRole/ClusterRoleBinding = Cluster scope
end note

@enduml
```

---

## Domínio 2: Container Orchestration (22%)

### 2.1 Conceitos de Containers

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title CONTAINERS vs VIRTUAL MACHINES

rectangle "VM" {
  card "App + Libs" as vm_app
  card "Guest OS" as vm_os
  card "Hypervisor" as vm_hyp
  card "Host OS" as vm_host
  card "Hardware" as vm_hw
  
  vm_app -[hidden]down- vm_os
  vm_os -[hidden]down- vm_hyp
  vm_hyp -[hidden]down- vm_host
  vm_host -[hidden]down- vm_hw
}

rectangle "Container" {
  card "App + Libs" as c_app
  card "Container Runtime" as c_rt
  card "Host OS" as c_host
  card "Hardware" as c_hw
  
  c_app -[hidden]down- c_rt
  c_rt -[hidden]down- c_host
  c_host -[hidden]down- c_hw
}

note bottom of VM
  • Mais pesado
  • Isolamento total
  • GB de tamanho
  • Minutos para iniciar
end note

note bottom of Container
  • Mais leve
  • Compartilha kernel
  • MB de tamanho
  • Segundos para iniciar
end note

@enduml
```

### 2.2 Padrões de Interface (CxI)

| Interface | Descrição | Exemplos |
|-----------|-----------|----------|
| **CRI** | Container Runtime Interface | containerd, CRI-O |
| **CNI** | Container Network Interface | Calico, Cilium, Flannel |
| **CSI** | Container Storage Interface | AWS EBS, GCE PD |
| **SMI** | Service Mesh Interface | Linkerd, Istio |

### 2.3 OCI - Open Container Initiative

```plaintext
OCI define padrões para:

1. Runtime Specification (runtime-spec)
   - Como executar containers
   - runc é a implementação de referência

2. Image Specification (image-spec)
   - Formato de imagens de container
   - Layers, config, manifest

3. Distribution Specification (distribution-spec)
   - Como distribuir imagens
   - Registry API
```

### 2.4 Container Runtimes

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title HIERARQUIA DE RUNTIMES

rectangle "High-Level Runtime (CRI)" {
  component "containerd" as containerd
  component "CRI-O" as crio
}

rectangle "Low-Level Runtime (OCI)" {
  component "runc\n(processo isolado)" as runc
  component "kata-containers\n(microVM)" as kata
  component "gVisor\n(sandbox)" as gvisor
}

containerd --> runc
containerd --> kata
crio --> runc
crio --> gvisor

@enduml
```

---

## Domínio 3: Cloud Native Architecture (16%)

### 3.1 Características Cloud Native

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title 12-FACTOR APP (Resumo)

card "1. Codebase" as f1
card "2. Dependencies" as f2
card "3. Config" as f3
card "4. Backing Services" as f4
card "5. Build/Release/Run" as f5
card "6. Processes" as f6
card "7. Port Binding" as f7
card "8. Concurrency" as f8
card "9. Disposability" as f9
card "10. Dev/Prod Parity" as f10
card "11. Logs" as f11
card "12. Admin Processes" as f12

note right of f1 : Um repo, múltiplos deploys
note right of f2 : Declarar e isolar dependências
note right of f3 : Configuração via ambiente
note right of f4 : Tratar como recursos anexados
note right of f5 : Separar estágios estritamente
note right of f6 : Executar como processos stateless
note right of f7 : Exportar serviços via porta
note right of f8 : Escalar via modelo de processo
note right of f9 : Maximizar robustez
note right of f10 : Manter ambientes similares
note right of f11 : Tratar como event streams
note right of f12 : Rodar admin tasks como one-offs

@enduml
```

### 3.2 Microservices vs Monolith

| Aspecto | Monolith | Microservices |
|---------|----------|---------------|
| **Deploy** | Tudo junto | Independente |
| **Escala** | Vertical | Horizontal |
| **Tecnologia** | Única stack | Polyglot |
| **Complexidade** | Baixa inicial | Alta inicial |
| **Falhas** | Cascata | Isoladas |

### 3.3 Autoscaling

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title TIPOS DE AUTOSCALING

rectangle "Horizontal Pod Autoscaler (HPA)" {
  note as n1
    Ajusta número de réplicas baseado em métricas
    Exemplo: CPU > 80% → adiciona pods
  end note
}

rectangle "Vertical Pod Autoscaler (VPA)" {
  note as n2
    Ajusta recursos (CPU/memória) dos pods
    Exemplo: Aumenta requests/limits automaticamente
  end note
}

rectangle "Cluster Autoscaler" {
  note as n3
    Ajusta número de nodes no cluster
    Exemplo: Pods pending → adiciona nodes
  end note
}

@enduml
```

### 3.4 Serverless

```plaintext
Serverless no Kubernetes:

• Knative - Plataforma serverless para K8s
  - Serving: Auto-scaling (inclusive scale-to-zero)
  - Eventing: Event-driven architecture

• OpenFaaS - Functions as a Service
• Kubeless - Funções serverless nativas

Características:
- Scale to zero quando ocioso
- Pay-per-use
- Event-driven
```

---

## Domínio 4: Cloud Native Observability (8%)

### 4.1 Os Três Pilares

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title TRÊS PILARES DA OBSERVABILIDADE

rectangle "MÉTRICAS" {
  card "Números agregados" as m
  note bottom of m
    Prometheus
    Grafana
  end note
}

rectangle "LOGS" {
  card "Eventos discretos" as l
  note bottom of l
    Fluentd
    Loki
    Elasticsearch
  end note
}

rectangle "TRACES" {
  card "Requests end-to-end" as t
  note bottom of t
    Jaeger
    Zipkin
    Tempo
  end note
}

@enduml
```

### 4.2 Prometheus

```plaintext
Prometheus (CNCF Graduated):

• Time-series database para métricas
• Pull-based model (scraping)
• PromQL para queries
• AlertManager para alertas

Tipos de métricas:
- Counter: Só incrementa (requests totais)
- Gauge: Pode subir/descer (temperatura)
- Histogram: Distribuição (latência)
- Summary: Similar histogram, calculado client-side
```

### 4.3 OpenTelemetry

```plaintext
OpenTelemetry (CNCF Incubating):

• Padrão unificado para telemetria
• Combina OpenTracing + OpenCensus
• Suporta métricas, logs e traces
• SDKs para múltiplas linguagens
• Collector para processar e exportar dados
```

---

## Domínio 5: Application Delivery (8%)

### 5.1 GitOps

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title GITOPS

rectangle "Princípios" {
  card "1. Git como single source of truth" as p1
  card "2. Declarative configuration" as p2
  card "3. Automated sync (reconciliation)" as p3
  card "4. Continuous verification" as p4
}

rectangle "Fluxo" {
  actor "Dev" as dev
  component "Git" as git
  component "Cluster" as cluster
  
  dev --> git : push
  git <--> cluster : sync
  cluster --> git : reconcile
}

note bottom
  Ferramentas: ArgoCD, Flux
end note

@enduml
```

### 5.2 CI/CD

```plaintext
CI (Continuous Integration):
- Build automático
- Testes automáticos
- Merge frequente

CD (Continuous Delivery/Deployment):
- Deploy automatizado para staging
- Deployment: Push automático para produção
- Delivery: Aprovação manual antes de prod

Ferramentas:
- Jenkins, GitHub Actions, GitLab CI
- ArgoCD, Flux (GitOps)
- Tekton (cloud-native CI/CD)
```

### 5.3 Helm e Kustomize

| Ferramenta | Abordagem | Quando Usar |
|------------|-----------|-------------|
| **Helm** | Templates + Values | Apps complexas, charts públicos |
| **Kustomize** | Patches sobre base | Customização simples, nativo kubectl |

---

## CNCF - Cloud Native Computing Foundation

### Estágios de Projetos

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title CNCF PROJECT STAGES

rectangle "SANDBOX" as sandbox
rectangle "INCUBATING" as incubating
rectangle "GRADUATED" as graduated

sandbox --> incubating
incubating --> graduated

note bottom of sandbox
  • Projetos em estágio inicial
  • Revisão a cada 12 meses
  • Pode ser removido
end note

note bottom of incubating
  • Usado em produção por 3+ empresas
  • Comunidade ativa de contribuidores
  • Documentação e governança definidas
end note

note bottom of graduated
  • Maturidade comprovada
  • Adoção ampla
  • Votação do TOC
end note

@enduml
```

### Projetos Graduated Importantes

| Projeto | Função |
|---------|--------|
| **Kubernetes** | Orquestração de containers |
| **Prometheus** | Monitoramento e alertas |
| **Envoy** | Service proxy |
| **CoreDNS** | DNS para Kubernetes |
| **containerd** | Container runtime |
| **Helm** | Package manager |
| **Jaeger** | Distributed tracing |
| **Fluentd** | Logging |
| **Harbor** | Container registry |
| **etcd** | Key-value store |

---

## Papéis em Cloud Native

### SRE - Site Reliability Engineer

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title SLI / SLO / SLA

rectangle "SLI (Service Level Indicator)" {
  note as n1
    Métrica que mede aspecto do serviço
    Exemplo: Latência, Error Rate, Throughput
  end note
}

rectangle "SLO (Service Level Objective)" {
  note as n2
    Alvo/meta para o SLI
    Exemplo: Latência p99 < 200ms
  end note
}

rectangle "SLA (Service Level Agreement)" {
  note as n3
    Contrato com consequências
    Exemplo: 99.9% uptime ou créditos
  end note
}

note bottom
  Relação: SLI mede → SLO define meta → SLA formaliza contrato
end note

@enduml
```

### Outros Papéis

| Papel | Responsabilidade |
|-------|------------------|
| **Cloud Architect** | Design de infraestrutura cloud |
| **DevOps Engineer** | Ciclo de vida completo da aplicação |
| **Platform Engineer** | Plataforma interna de desenvolvimento |
| **Security Engineer** | Segurança em cloud |
| **DevSecOps** | DevOps + Segurança integrada |

---

## Dicas para o Exame

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title DICAS KCNA

card "1. Foco nos conceitos, não em comandos\n   É múltipla escolha, não prático" as d1
card "2. Conheça bem a arquitetura K8s\n   Componentes do control plane\n   Papel de cada componente" as d2
card "3. Memorize os projetos CNCF importantes\n   Graduated vs Incubating vs Sandbox\n   Qual problema cada projeto resolve" as d3
card "4. Entenda os padrões (CRI, CNI, CSI, OCI)\n   O que cada um padroniza" as d4
card "5. GitOps e CI/CD\n   Princípios do GitOps\n   Diferença entre CD e CI" as d5
card "6. Observabilidade\n   3 pilares: métricas, logs, traces\n   Prometheus, Jaeger, Fluentd" as d6

@enduml
```

---

## Referências

- [Arquitetura](fundamentals/arquitetura.md)
- [Observabilidade](../observability/observabilidade.md)
- [Helm](../tools/helm.md)
- [Kustomize](../tools/kustomize.md)
- [Containers](fundamentals/containers.md)
- [Docker](fundamentals/docker.md)
