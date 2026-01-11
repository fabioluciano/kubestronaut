# Cloud Native

```admonish info title="Certificações"
KCNA (16%)
```

## Conceitos Fundamentais

### O que é Cloud Native?

Cloud Native é uma abordagem para construir e executar aplicações que exploram ao máximo as vantagens do modelo de computação em nuvem.

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title PILARES CLOUD NATIVE

rectangle "Cloud Native" {
  card "Containers" as c
  card "Microservices" as m
  card "DevOps" as d
  card "CI/CD" as ci
}

note bottom
  Aplicações cloud native são:
  • Escaláveis
  • Resilientes
  • Gerenciáveis
  • Observáveis
end note

@enduml
```

### Definição da CNCF

A **Cloud Native Computing Foundation (CNCF)** define Cloud Native como:

> "Tecnologias cloud native capacitam organizações a construir e executar aplicações escaláveis em ambientes modernos e dinâmicos como nuvens públicas, privadas e híbridas. Containers, service meshes, microservices, infraestrutura imutável e APIs declarativas exemplificam essa abordagem."

---

## CNCF - Cloud Native Computing Foundation

### O que é a CNCF?

- Fundação open-source parte da Linux Foundation
- Hospeda projetos críticos como Kubernetes, Prometheus, Envoy
- Define padrões e promove adoção de tecnologias cloud native

### Estágios de Projetos CNCF

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title ESTÁGIOS DE PROJETOS CNCF

rectangle "SANDBOX" as sandbox #lightgray
rectangle "INCUBATING" as incubating #gray
rectangle "GRADUATED" as graduated #darkgray

sandbox --> incubating : Adoção crescente
incubating --> graduated : Maturidade comprovada

note bottom of sandbox
  • Projetos em estágio inicial
  • Experimental
  • Revisão anual
end note

note bottom of incubating
  • Usado em produção por 3+ empresas
  • Comunidade ativa
  • Governança definida
end note

note bottom of graduated
  • Maturidade comprovada
  • Adoção ampla
  • Seguro para produção
end note

@enduml
```

### Projetos Graduated (Memorizar para KCNA)

| Projeto | Função | Categoria |
|---------|--------|-----------|
| **Kubernetes** | Orquestração de containers | Orchestration |
| **Prometheus** | Monitoramento e métricas | Observability |
| **Envoy** | Service proxy | Service Mesh |
| **CoreDNS** | DNS para clusters | Networking |
| **containerd** | Container runtime | Runtime |
| **Helm** | Package manager | App Definition |
| **Jaeger** | Distributed tracing | Observability |
| **Fluentd** | Logging | Observability |
| **Harbor** | Container registry | Registry |
| **etcd** | Key-value store | Database |
| **Argo** | GitOps/Workflows | CI/CD |
| **Flux** | GitOps | CI/CD |

### Projetos Incubating Importantes

| Projeto | Função |
|---------|--------|
| **OpenTelemetry** | Telemetria unificada |
| **Linkerd** | Service mesh |
| **gRPC** | RPC framework |
| **NATS** | Messaging |
| **Falco** | Runtime security |
| **Keda** | Event-driven autoscaling |

---

## 12-Factor App

Metodologia para construir aplicações SaaS modernas. Essencial para KCNA.

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title 12-FACTOR APP

card "1. Codebase\nUm repo, múltiplos deploys" as f1
card "2. Dependencies\nDeclarar e isolar" as f2
card "3. Config\nArmazenar no ambiente" as f3
card "4. Backing Services\nTratar como recursos" as f4
card "5. Build/Release/Run\nSeparar estágios" as f5
card "6. Processes\nExecutar stateless" as f6
card "7. Port Binding\nExportar via porta" as f7
card "8. Concurrency\nEscalar via processos" as f8
card "9. Disposability\nInício rápido, shutdown graceful" as f9
card "10. Dev/Prod Parity\nManter similares" as f10
card "11. Logs\nTratar como streams" as f11
card "12. Admin Processes\nRodar como one-offs" as f12

@enduml
```

### Mapeamento para Kubernetes

| Factor | Implementação no Kubernetes |
|--------|----------------------------|
| **1. Codebase** | Container image versionada |
| **2. Dependencies** | Dockerfile com todas deps |
| **3. Config** | ConfigMaps e Secrets |
| **4. Backing Services** | Services externos via DNS |
| **5. Build/Release/Run** | CI/CD pipeline |
| **6. Processes** | Pods stateless |
| **7. Port Binding** | containerPort + Service |
| **8. Concurrency** | HPA, replicas |
| **9. Disposability** | Probes, graceful shutdown |
| **10. Dev/Prod Parity** | Namespaces, Helm values |
| **11. Logs** | stdout/stderr → Fluentd |
| **12. Admin** | Jobs, kubectl exec |

---

## Microservices

### Microservices vs Monolith

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title MONOLITH vs MICROSERVICES

rectangle "MONOLITH" {
  rectangle "UI + Business Logic + Data" as mono
}

rectangle "MICROSERVICES" {
  rectangle "Service A" as sa
  rectangle "Service B" as sb
  rectangle "Service C" as sc

  sa <--> sb
  sb <--> sc
}

note bottom of mono
  • Deploy único
  • Escala vertical
  • Uma tecnologia
  • Falha = tudo falha
end note

note bottom of sc
  • Deploy independente
  • Escala horizontal
  • Polyglot
  • Falha isolada
end note

@enduml
```

### Características de Microservices

| Característica | Descrição |
|----------------|-----------|
| **Independência** | Deploy, escala e falha independentes |
| **Single Responsibility** | Cada serviço faz uma coisa bem |
| **Comunicação via API** | REST, gRPC, mensageria |
| **Dados descentralizados** | Cada serviço tem seu banco |
| **Automação** | CI/CD é essencial |

### Padrões de Comunicação

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title PADRÕES DE COMUNICAÇÃO

rectangle "Síncrono" {
  card "REST/HTTP" as rest
  card "gRPC" as grpc
}

rectangle "Assíncrono" {
  card "Message Queue\n(RabbitMQ, Kafka)" as mq
  card "Event-Driven" as event
}

note bottom
  Síncrono: Request-Response
  Assíncrono: Fire-and-forget ou Pub/Sub
end note

@enduml
```

---

## Service Mesh

### O que é Service Mesh?

Camada de infraestrutura dedicada para comunicação service-to-service.

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title SERVICE MESH

rectangle "Pod A" {
  component "App" as app1
  component "Sidecar\nProxy" as proxy1
}

rectangle "Pod B" {
  component "App" as app2
  component "Sidecar\nProxy" as proxy2
}

rectangle "Control Plane" as cp

app1 --> proxy1 : localhost
proxy1 --> proxy2 : mTLS
proxy2 --> app2 : localhost

cp --> proxy1 : config
cp --> proxy2 : config

@enduml
```

### Funcionalidades

| Funcionalidade | Descrição |
|----------------|-----------|
| **mTLS** | Criptografia e autenticação entre serviços |
| **Traffic Management** | Routing, load balancing, canary |
| **Observability** | Métricas, traces, logs |
| **Resilience** | Retries, circuit breaker, timeout |

### Service Meshes Populares

| Service Mesh | Características |
|--------------|-----------------|
| **Istio** | Mais features, mais complexo |
| **Linkerd** | Mais simples, CNCF graduated |
| **Cilium** | Baseado em eBPF, alto desempenho |

---

## Serverless

### Conceito

Modelo onde o provedor gerencia a infraestrutura e escala automaticamente, incluindo scale-to-zero.

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title SERVERLESS

rectangle "Características" {
  card "Scale to Zero" as s1
  card "Pay per Use" as s2
  card "Event-Driven" as s3
  card "No Server Management" as s4
}

note bottom
  FaaS (Function as a Service)
  é um tipo de serverless
end note

@enduml
```

### Serverless no Kubernetes

| Projeto | Descrição |
|---------|-----------|
| **Knative** | Plataforma serverless para K8s (CNCF) |
| **OpenFaaS** | Functions as a Service |
| **Kubeless** | Funções serverless nativas |
| **KEDA** | Event-driven autoscaling |

### Knative Components

| Componente | Função |
|------------|--------|
| **Serving** | Auto-scaling, routing, scale-to-zero |
| **Eventing** | Event sources, triggers, channels |

---

## GitOps

### Princípios GitOps

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title PRINCÍPIOS GITOPS

card "1. Declarativo\nTodo estado é descrito declarativamente" as p1
card "2. Versionado\nGit como single source of truth" as p2
card "3. Automático\nMudanças aplicadas automaticamente" as p3
card "4. Reconciliação\nAgentes garantem estado desejado" as p4

p1 -[hidden]down-> p2
p2 -[hidden]down-> p3
p3 -[hidden]down-> p4

@enduml
```

### Fluxo GitOps

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title FLUXO GITOPS

actor "Developer" as dev
entity "Git Repo" as git
entity "GitOps Agent\n(ArgoCD/Flux)" as agent
entity "Kubernetes\nCluster" as k8s
dev --> git : push
git --> agent : detect changes
agent --> k8s : apply
k8s --> agent : reconcile

note bottom of agent
  Pull-based model
  Agent dentro do cluster
end note

@enduml
```

### Ferramentas GitOps

| Ferramenta | Status CNCF | Características |
|------------|-------------|-----------------|
| **ArgoCD** | Graduated | UI rica, multi-cluster |
| **Flux** | Graduated | Mais leve, helm/kustomize nativo |

---

## CI/CD

### Continuous Integration (CI)

```plaintext
CI = Build + Test automaticamente a cada commit

Objetivo:
- Detectar erros cedo
- Manter código sempre integrável
- Feedback rápido
```

### Continuous Delivery vs Deployment

| Aspecto | Continuous Delivery | Continuous Deployment |
|---------|--------------------|-----------------------|
| **Deploy para Prod** | Manual (aprovação) | Automático |
| **Risco** | Menor | Maior |
| **Velocidade** | Média | Alta |

### Pipeline Típico

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title PIPELINE CI/CD

rectangle "CI" {
  card "Build" as build
  card "Test" as test
  card "Scan" as scan
}

rectangle "CD" {
  card "Push Image" as push
  card "Deploy Staging" as staging
  card "Deploy Prod" as prod
}

build --> test
test --> scan
scan --> push
push --> staging
staging --> prod

@enduml
```

### Ferramentas CI/CD

| Categoria | Ferramentas |
|-----------|-------------|
| **CI** | Jenkins, GitHub Actions, GitLab CI, CircleCI |
| **CD** | ArgoCD, Flux, Spinnaker |
| **Cloud Native CI** | Tekton (CNCF) |

---

## Autoscaling

### Tipos de Autoscaling

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title TIPOS DE AUTOSCALING

rectangle "HPA" as hpa {
  note as n1
    Horizontal Pod Autoscaler
    Ajusta número de pods
    Baseado em CPU/mem/custom
  end note
}

rectangle "VPA" as vpa {
  note as n2
    Vertical Pod Autoscaler
    Ajusta recursos dos pods
    Requer restart
  end note
}

rectangle "Cluster Autoscaler" as ca {
  note as n3
    Ajusta número de nodes
    Pods pending → add nodes
    Nodes ociosos → remove
  end note
}

@enduml
```

### Quando Usar

| Tipo | Quando Usar |
|------|-------------|
| **HPA** | Apps stateless, carga variável |
| **VPA** | Otimizar requests, apps stateful |
| **Cluster Autoscaler** | Workloads dinâmicos em cloud |
| **KEDA** | Event-driven, scale-to-zero |

---

## Observabilidade

### Os Três Pilares

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title TRÊS PILARES DA OBSERVABILIDADE

rectangle "MÉTRICAS" as m {
  card "Números agregados\nPrometheus, Grafana" as m1
}

rectangle "LOGS" as l {
  card "Eventos textuais\nFluentd, Loki, ELK" as l1
}

rectangle "TRACES" as t {
  card "Requests distribuídos\nJaeger, Zipkin, Tempo" as t1
}

@enduml
```

### OpenTelemetry

Padrão unificado para telemetria (métricas, logs, traces).

```plaintext
OpenTelemetry = OpenTracing + OpenCensus

Componentes:
- SDKs para instrumentação
- Collector para processar dados
- Exporters para backends
```

---

## Papéis e Responsabilidades

### SRE - Site Reliability Engineering

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title SLI / SLO / SLA

rectangle "SLI" as sli {
  note as n1
    Service Level Indicator
    Métrica: latência, error rate
  end note
}

rectangle "SLO" as slo {
  note as n2
    Service Level Objective
    Meta: p99 latência < 200ms
  end note
}

rectangle "SLA" as sla {
  note as n3
    Service Level Agreement
    Contrato: 99.9% uptime
  end note
}

sli --> slo : define meta
slo --> sla : formaliza contrato

@enduml
```

### Papéis Cloud Native

| Papel | Foco |
|-------|------|
| **DevOps Engineer** | Automação, CI/CD, infraestrutura |
| **SRE** | Confiabilidade, SLOs, incident response |
| **Platform Engineer** | Plataforma interna, developer experience |
| **Cloud Architect** | Design de infraestrutura cloud |

---

## Dicas para o Exame KCNA

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title DICAS KCNA - CLOUD NATIVE

card "1. Memorize projetos CNCF\nGraduated vs Incubating" as d1
card "2. Entenda 12-Factor App\nComo mapeia para K8s" as d2
card "3. Conheça GitOps\nArgoCD, Flux, princípios" as d3
card "4. Service Mesh\nIstio, Linkerd, funcionalidades" as d4
card "5. Observabilidade\n3 pilares, OpenTelemetry" as d5
card "6. Serverless\nKnative, KEDA, scale-to-zero" as d6

@enduml
```

### Conceitos-Chave para Memorizar

| Conceito | Lembrar |
|----------|---------|
| **CNCF** | Linux Foundation, projetos graduated |
| **12-Factor** | Config no ambiente, processes stateless |
| **GitOps** | Git = source of truth, reconciliação |
| **Service Mesh** | Sidecar proxy, mTLS, traffic management |
| **Observability** | Métricas + Logs + Traces |
| **Serverless** | Scale-to-zero, event-driven |

---

## Referências

### Documentação
- [CNCF](https://www.cncf.io/)
- [12-Factor App](https://12factor.net/)
- [CNCF Landscape](https://landscape.cncf.io/)

### Arquivos Relacionados
- [KCNA](certifications/kcna.md) - Guia completo KCNA
- [Arquitetura](fundamentals/arquitetura.md) - Arquitetura Kubernetes
- [Observabilidade](observability/observabilidade.md) - Pilares da observabilidade
- [Helm](tools/helm.md) - Package manager
- [HPA](workloads/horizontal-pod-autoscaler.md) - Autoscaling
