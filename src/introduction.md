# Introducao ao Kubernetes

> **Certificacoes**: KCNA (40%), CKAD, CKA, CKS - Fundamentos essenciais para todas as certificacoes

## O que e Kubernetes?

Kubernetes, frequentemente abreviado como **K8s** (K + 8 letras + s), e uma plataforma open-source para **orquestracao de containers**. Desenvolvido originalmente pelo Google e agora mantido pela Cloud Native Computing Foundation (CNCF), o Kubernetes automatiza a implantacao, o escalonamento e a gestao de aplicacoes containerizadas.

```admonish info title="Por que K8s?"
O nome "K8s" e uma abreviacao de "Kubernetes" onde o numero 8 representa as oito letras entre o "K" e o "s" (ubernete). Esta convencao e comum em tecnologia, similar a "i18n" para "internationalization".
```

### Definicao Oficial

> Kubernetes e um sistema de orquestracao de containers open-source para automatizar a implantacao, escalonamento e gerenciamento de aplicacoes containerizadas.

### O Problema que o Kubernetes Resolve

Antes do Kubernetes, equipes enfrentavam desafios significativos ao gerenciar aplicacoes containerizadas em escala:

```admonish question title="Desafios Pre-Kubernetes"
- O que fazer quando um container apresenta problemas?
- O que fazer quando um no do cluster falha?
- Como garantir que a aplicacao continue respondendo sob alta demanda?
- Como fazer atualizacoes sem downtime?
- Como gerenciar configuracoes e secrets de forma segura?
- Como balancear carga entre multiplas instancias?
```

O Kubernetes fornece respostas automatizadas para todas essas questoes, permitindo que equipes foquem no desenvolvimento ao inves da operacao manual da infraestrutura.

## Historia e Evolucao

### Linha do Tempo

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title Historia do Kubernetes

rectangle "2003-2004" as Y1 {
  card "Google desenvolve\no Borg internamente" as B1
}

rectangle "2013" as Y2 {
  card "Docker e lancado\npopularizando containers" as B2
}

rectangle "2014" as Y3 {
  card "Google anuncia\nKubernetes open-source" as B3
}

rectangle "2015" as Y4 {
  card "Kubernetes v1.0\nCNCF e fundada" as B4
}

rectangle "2017" as Y5 {
  card "Adocao massiva\npor cloud providers" as B5
}

rectangle "2018" as Y6 {
  card "Primeiro projeto\ngraduated da CNCF" as B6
}

Y1 -right-> Y2
Y2 -right-> Y3
Y3 -down-> Y4
Y4 -left-> Y5
Y5 -left-> Y6

@enduml
```

### Marcos Importantes

| Ano | Evento |
|-----|--------|
| **2003-2004** | Google desenvolve o **Borg**, sistema interno de orquestracao |
| **2013** | Docker e lancado, popularizando containers |
| **2014** | Google anuncia o Kubernetes como projeto open-source |
| **2015** | Kubernetes v1.0 lancado; CNCF e fundada |
| **2016** | Kubernetes se torna o projeto mais ativo do GitHub |
| **2017** | Todos os principais provedores cloud adotam Kubernetes |
| **2018** | Kubernetes se torna o primeiro projeto "graduated" da CNCF |
| **2020+** | Kubernetes e o padrao de fato para orquestracao de containers |

### Do Borg ao Kubernetes

O Kubernetes herdou muitos conceitos do **Borg**, o sistema de gerenciamento de clusters do Google que executa milhoes de jobs por semana:

- **Pods**: Conceito de agrupar containers relacionados
- **Labels**: Sistema de rotulagem flexivel
- **Services**: Descoberta de servicos e balanceamento de carga
- **Replication**: Garantia de disponibilidade atraves de replicas

```admonish note title="Curiosidade"
O nome "Kubernetes" vem do grego e significa "timoneiro" ou "piloto" - aquele que guia o navio. O logo do Kubernetes e um leme de navio com sete raios, representando o codinome original do projeto: "Project Seven".
```

## Por que Usar Kubernetes?

### Beneficios Principais

#### 1. Escalabilidade Automatica

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title Horizontal Pod Autoscaler

rectangle "HPA Controller" as HPA

rectangle "Deployment" as D {
  card "Pod 1" as P1
  card "Pod 2" as P2
  card "Pod 3" as P3
  card "Pod N..." as PN #lightgray
}

cloud "Metricas" as M {
  card "CPU: 80%" as CPU
  card "Memoria: 70%" as MEM
}

M --> HPA : Monitora
HPA --> D : Scale Up/Down

note bottom of HPA
  Kubernetes ajusta automaticamente
  o numero de pods baseado em
  metricas como CPU e memoria
end note

@enduml
```

- **Escalonamento Horizontal**: Adiciona ou remove replicas de pods automaticamente
- **Escalonamento Vertical**: Ajusta recursos (CPU/memoria) dos containers
- **Cluster Autoscaler**: Adiciona ou remove nos do cluster conforme necessidade

#### 2. Alta Disponibilidade

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title Alta Disponibilidade no Kubernetes

rectangle "Cluster Kubernetes" {
  rectangle "Node 1" as N1 {
    card "Pod A" as P1A
    card "Pod B" as P1B
  }

  rectangle "Node 2" as N2 {
    card "Pod A" as P2A
    card "Pod C" as P2C
  }

  rectangle "Node 3" as N3 {
    card "Pod B" as P3B
    card "Pod C" as P3C
  }
}

note bottom of N1
  Se um node falhar,
  os pods sao redistribuidos
  automaticamente
end note

@enduml
```

- **Self-healing**: Reinicia containers que falham
- **Redistribuicao**: Move pods quando nos ficam indisponiveis
- **Health checks**: Monitora continuamente a saude das aplicacoes

#### 3. Implantacoes Declarativas

```yaml
{{#include assets/deployment/deployment-minha-aplicacao.yaml}}
```

#### 4. Portabilidade

```admonish success title="Execute em Qualquer Lugar"
Kubernetes funciona de forma consistente em:
- **On-premises**: Data centers proprios
- **Cloud publica**: AWS (EKS), Google Cloud (GKE), Azure (AKS)
- **Cloud hibrida**: Combinacao de on-premises e cloud
- **Edge**: Dispositivos IoT e locais remotos
- **Local**: Minikube, Kind, Docker Desktop
```

### Comparacao: Sem Kubernetes vs Com Kubernetes

| Aspecto | Sem Kubernetes | Com Kubernetes |
|---------|---------------|----------------|
| **Escalonamento** | Manual, lento | Automatico, instantaneo |
| **Recuperacao de falhas** | Intervencao manual | Automatico (self-healing) |
| **Atualizacoes** | Downtime frequente | Rolling updates sem downtime |
| **Configuracao** | Scripts dispersos | Arquivos YAML versionados |
| **Descoberta de servicos** | Configuracao manual | DNS automatico |
| **Balanceamento de carga** | Load balancers externos | Integrado (Services) |
| **Secrets** | Arquivos em disco | Objetos gerenciados |

## Conceitos Fundamentais

### Arquitetura de Alto Nivel

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title Arquitetura do Kubernetes

rectangle "Control Plane" as CP {
  component "API Server" as API
  component "etcd" as ETCD
  component "Scheduler" as SCHED
  component "Controller Manager" as CM
}

rectangle "Worker Node 1" as W1 {
  component "kubelet" as K1
  component "kube-proxy" as KP1
  component "Container Runtime" as CR1

  rectangle "Pod" as POD1 {
    card "Container" as C1
  }
}

rectangle "Worker Node 2" as W2 {
  component "kubelet" as K2
  component "kube-proxy" as KP2
  component "Container Runtime" as CR2

  rectangle "Pod" as POD2 {
    card "Container" as C2
  }
}

API --> ETCD : Persiste estado
API --> SCHED : Agenda pods
API --> CM : Controla recursos
API --> K1 : Gerencia node
API --> K2 : Gerencia node

@enduml
```

### Objetos Principais

#### Pod

O **Pod** e a menor unidade deployavel no Kubernetes. Representa um ou mais containers que compartilham rede e armazenamento.

```yaml
{{#include assets/pod/pod-meu-pod.yaml}}
```

```admonish info title="Caracteristicas do Pod"
- Containers em um Pod compartilham o mesmo IP
- Containers em um Pod podem se comunicar via localhost
- Pods sao efemeros - podem ser criados e destruidos a qualquer momento
- Pods nao devem ser criados diretamente em producao (use Deployments)
```

#### Deployment

O **Deployment** gerencia ReplicaSets e Pods, fornecendo atualizacoes declarativas.

```yaml
{{#include assets/deployment/deployment-nginx-deployment-1.yaml}}
```

```admonish tip title="Quando usar Deployment"
- Para aplicacoes stateless
- Quando precisa de rolling updates
- Quando precisa de rollback facil
- Para a maioria das aplicacoes web
```

#### ReplicaSet

O **ReplicaSet** garante que um numero especificado de replicas de pods esteja rodando a qualquer momento.

```admonish warning title="Importante"
Na pratica, voce raramente cria ReplicaSets diretamente. Use Deployments, que gerenciam ReplicaSets automaticamente e fornecem recursos adicionais como rolling updates.
```

#### Service

O **Service** expoe uma aplicacao rodando em Pods como um servico de rede.

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title Service no Kubernetes

rectangle "Service (ClusterIP)" as SVC {
  card "10.96.0.1:80" as VIP
}

rectangle "Pods Backend" as PODS {
  card "Pod 1\n10.244.0.5" as P1
  card "Pod 2\n10.244.0.6" as P2
  card "Pod 3\n10.244.0.7" as P3
}

cloud "Cliente" as C

C --> SVC : my-service:80
SVC --> P1
SVC --> P2
SVC --> P3

note bottom of SVC
  O Service fornece um IP estavel
  e faz load balancing entre os Pods
end note

@enduml
```

```yaml
{{#include assets/service/service-my-service-1.yaml}}
```

**Tipos de Service:**

| Tipo | Descricao | Uso |
|------|-----------|-----|
| **ClusterIP** | IP interno do cluster | Comunicacao interna |
| **NodePort** | Expoe em porta do node (30000-32767) | Acesso externo simples |
| **LoadBalancer** | Load balancer externo (cloud) | Producao em cloud |
| **ExternalName** | Alias DNS para servico externo | Integracao externa |

#### ConfigMap e Secret

**ConfigMap** armazena dados de configuracao nao-sensiveis:

```yaml
{{#include assets/configmap/configmap-app-config.yaml}}
```

**Secret** armazena dados sensiveis (codificados em base64):

```yaml
{{#include assets/secrets/secret-app-secrets.yaml}}
```

```admonish warning title="Secrets nao sao Criptografados por Padrao"
Secrets sao apenas codificados em base64, nao criptografados. Para seguranca real:
- Habilite encryption at rest no etcd
- Use solucoes como Sealed Secrets ou Vault
- Limite acesso via RBAC
```

#### Namespace

**Namespace** fornece isolamento logico de recursos dentro do cluster.

```yaml
{{#include assets/general/namespace-producao.yaml}}
```

```bash
# Namespaces padrao do Kubernetes
kubectl get namespaces

# default        - namespace padrao para recursos sem namespace especificado
# kube-system    - componentes do sistema Kubernetes
# kube-public    - recursos publicos legiveis por todos
# kube-node-lease - leases de heartbeat dos nodes
```

### Hierarquia de Objetos

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title Hierarquia de Objetos

rectangle "Deployment" as D {
  rectangle "ReplicaSet v2 (atual)" as RS2 {
    rectangle "Pod 1" as P1 {
      card "Container" as C1
    }
    rectangle "Pod 2" as P2 {
      card "Container" as C2
    }
    rectangle "Pod 3" as P3 {
      card "Container" as C3
    }
  }

  rectangle "ReplicaSet v1 (antiga)" as RS1 #lightgray {
    note "Mantido para rollback" as N1
  }
}

note right of D
  Deployment gerencia ReplicaSets
  ReplicaSet gerencia Pods
  Pod contem Containers
end note

@enduml
```

### Relacao entre Objetos

| Objeto | Gerencia | Finalidade |
|--------|----------|------------|
| **Deployment** | ReplicaSets | Atualizacoes declarativas e rollbacks |
| **ReplicaSet** | Pods | Garante numero de replicas |
| **Pod** | Containers | Menor unidade executavel |
| **Service** | Endpoints | Expoe Pods na rede |
| **ConfigMap** | Dados | Configuracao da aplicacao |
| **Secret** | Dados sensiveis | Senhas, tokens, chaves |
| **Ingress** | Rotas HTTP | Roteamento de trafego externo |

## Casos de Uso

### 1. Microservicos

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title Arquitetura de Microservicos

rectangle "Aplicacao E-commerce" {
  rectangle "Frontend" as FE {
    card "React App" as REACT
  }

  rectangle "API Gateway" as GW {
    card "Kong/Nginx" as KONG
  }

  rectangle "Servicos" as SVCS {
    card "Catalogo" as CAT
    card "Carrinho" as CART
    card "Pagamento" as PAY
    card "Usuarios" as USER
  }

  rectangle "Dados" as DATA {
    database "PostgreSQL" as PG
    database "Redis" as REDIS
    database "MongoDB" as MONGO
  }
}

REACT --> KONG
KONG --> CAT
KONG --> CART
KONG --> PAY
KONG --> USER

CAT --> PG
CART --> REDIS
PAY --> PG
USER --> MONGO

@enduml
```

### 2. CI/CD e DevOps

```admonish example title="Pipeline GitOps"
1. Desenvolvedor faz push para Git
2. CI (Jenkins/GitLab CI) builda imagem
3. Imagem e publicada no registry
4. ArgoCD/Flux detecta mudanca
5. Kubernetes aplica nova versao
6. Rolling update sem downtime
```

### 3. Machine Learning

- Treinamento distribuido com GPU
- Serving de modelos com escalonamento
- Pipelines de dados com Kubeflow

### 4. Edge Computing

- Clusters em locais remotos
- Sincronizacao com cluster central
- Baixa latencia para IoT

### 5. Plataforma como Servico (PaaS)

- Multi-tenancy com Namespaces
- Isolamento com Network Policies
- Quotas de recursos por equipe

## Ecossistema e Comunidade

### CNCF (Cloud Native Computing Foundation)

A CNCF hospeda e promove projetos cloud native, sendo o Kubernetes o projeto mais importante.

```admonish info title="Projetos CNCF Relacionados"
**Graduated (Maduros):**
- **Kubernetes**: Orquestracao de containers
- **Prometheus**: Monitoramento e alertas
- **Envoy**: Proxy de servico
- **CoreDNS**: DNS para Kubernetes
- **containerd**: Container runtime
- **Helm**: Gerenciador de pacotes
- **etcd**: Key-value store

**Incubating:**
- **Argo**: GitOps e workflows
- **Cilium**: Networking e seguranca
- **Falco**: Runtime security
- **Linkerd**: Service mesh
```

### Distribuicoes Kubernetes

| Distribuicao | Provedor | Caracteristica |
|--------------|----------|----------------|
| **EKS** | AWS | Managed Kubernetes na AWS |
| **GKE** | Google | Managed Kubernetes no GCP |
| **AKS** | Azure | Managed Kubernetes no Azure |
| **OpenShift** | Red Hat | Enterprise Kubernetes |
| **Rancher** | SUSE | Multi-cluster management |
| **k3s** | SUSE | Lightweight Kubernetes |
| **Kind** | SIG | Kubernetes in Docker (dev) |
| **Minikube** | SIG | Local development |

### Comunidade

```admonish success title="Participacao na Comunidade"
- **Slack**: kubernetes.slack.com (200k+ membros)
- **GitHub**: github.com/kubernetes/kubernetes
- **Forum**: discuss.kubernetes.io
- **KubeCon**: Conferencia anual (10k+ participantes)
- **Meetups**: Grupos locais em todo mundo
- **SIGs**: Special Interest Groups para areas especificas
```

## Principios do Kubernetes

### 1. Configuracao Declarativa

**Imperativo** (como fazer):

```bash
kubectl run nginx --image=nginx
kubectl scale deployment nginx --replicas=3
```

**Declarativo** (o que voce quer):

```yaml
{{#include assets/deployment/deployment-nginx.yaml}}
```

```admonish tip title="Declarativo vs Imperativo"
- **Imperativo**: Descreve as acoes para alcancar o estado esperado
- **Declarativo**: Descreve o estado final desejado

Na producao, sempre prefira a abordagem declarativa, pois permite versionamento, code review e reproducibilidade.
```

### 2. Estado Desejado (Desired State)

O Kubernetes trabalha continuamente para que o **estado atual** do cluster seja igual ao **estado desejado** definido nos manifestos.

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title Control Loop do Kubernetes

rectangle "Control Loop" {
  card "Estado Desejado\n(YAML)" as DESIRED
  card "Estado Atual\n(Cluster)" as ACTUAL
  card "Controller" as CTRL
}

DESIRED --> CTRL : 1. Observa
ACTUAL --> CTRL : 2. Compara
CTRL --> ACTUAL : 3. Reconcilia

note bottom of CTRL
  O Controller continuamente:
  1. Observa o estado desejado
  2. Compara com estado atual
  3. Faz alteracoes para reconciliar
end note

@enduml
```

### 3. Imutabilidade

```admonish info title="Infraestrutura Imutavel"
- Containers nao sao modificados em execucao
- Para atualizar, cria-se um novo container com a nova versao
- Imagens antigas permanecem disponiveis para rollback
- Garante reproducibilidade e consistencia
```

### 4. Self-Healing

O Kubernetes automaticamente:

- **Reinicia** containers que falham
- **Substitui** pods em nodes que morrem
- **Mata** containers que nao respondem aos health checks
- **Esconde** pods que nao estao prontos do balanceamento de carga

## Comandos Iniciais

```bash
# Verificar versao do kubectl e cluster
kubectl version

# Informacoes do cluster
kubectl cluster-info

# Listar nodes do cluster
kubectl get nodes

# Listar todos os recursos em todos namespaces
kubectl get all --all-namespaces

# Ver pods do sistema
kubectl get pods -n kube-system

# Criar um pod simples
kubectl run nginx --image=nginx

# Ver detalhes de um pod
kubectl describe pod nginx

# Ver logs de um pod
kubectl logs nginx

# Executar comando em um pod
kubectl exec -it nginx -- /bin/bash

# Deletar um pod
kubectl delete pod nginx
```

## Referencias e Documentacao

### Documentacao Oficial

- [Documentacao Kubernetes](https://kubernetes.io/docs/home/)
- [Conceitos](https://kubernetes.io/docs/concepts/)
- [Tutoriais](https://kubernetes.io/docs/tutorials/)
- [Referencia da API](https://kubernetes.io/docs/reference/)

### Livros Recomendados

- "Kubernetes: Up and Running" - Kelsey Hightower
- "Kubernetes in Action" - Marko Luksa
- "The Kubernetes Book" - Nigel Poulton

### Cursos e Treinamentos

- [Kubernetes Basics (kubernetes.io)](https://kubernetes.io/docs/tutorials/kubernetes-basics/)
- [CNCF Training](https://www.cncf.io/certification/training/)
- [KodeKloud](https://kodekloud.com/)

## Dicas para os Exames

```admonish success title="Para o KCNA"
- Foque nos **conceitos** e **terminologia**
- Entenda a **arquitetura** de alto nivel
- Conheca o **ecossistema CNCF**
- Saiba diferenciar objetos e suas finalidades
```

```admonish success title="Para o CKAD"
- Pratique criar recursos **rapidamente**
- Domine **Pods**, **Deployments**, **Services**
- Conheca **ConfigMaps** e **Secrets**
- Pratique com **Jobs** e **CronJobs**
```

```admonish success title="Para o CKA"
- Entenda a **arquitetura** profundamente
- Domine **troubleshooting** de cluster
- Pratique **backup e restore** do etcd
- Conheca **kubeadm** para instalacao
```

```admonish success title="Para o CKS"
- Foque em **seguranca em profundidade**
- Domine **RBAC** e **Network Policies**
- Conheca **Pod Security Standards**
- Pratique **auditoria** e **hardening**
```

## Proximos Passos

Apos entender os conceitos basicos, recomenda-se estudar:

1. [Arquitetura do Kubernetes](./Arquitetura.md) - Componentes e funcionamento
2. [Pods](./workload/pod.md) - Unidade basica do Kubernetes
3. [Deployments](./workload/deployment.md) - Gerenciamento de aplicacoes
4. [Services](./network/service.md) - Exposicao de aplicacoes
5. [kubectl](./Kubectl.md) - Ferramenta de linha de comando

---

```admonish quote title="Citacao"
"Kubernetes is becoming the Linux of the cloud." - Jim Zemlin, The Linux Foundation
```
