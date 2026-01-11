# Arquitetura do Kubernetes

> **Certificacoes**: CKA (25%), KCNA (22%), CKS (10%) - Conhecimento essencial para todas as provas

## Conceitos Fundamentais

O Kubernetes e uma plataforma de orquestracao de containers de codigo aberto que automatiza a implantacao, escalonamento e gerenciamento de aplicacoes containerizadas. Sua arquitetura foi projetada para ser altamente escalavel, resiliente e extensivel.

### Por que entender a Arquitetura?

| Certificacao | Importancia |
|--------------|-------------|
| **CKA** | Essencial para troubleshooting e administracao do cluster |
| **KCNA** | Fundamento para entender conceitos cloud native |
| **CKS** | Necessario para entender superficie de ataque e hardening |
| **CKAD** | Util para entender como aplicacoes sao executadas |

---

## Visao Geral

### Arquitetura Geral do Kubernetes

O Kubernetes segue uma arquitetura master-worker (Control Plane + Worker Nodes) com comunicacao centralizada atraves do API Server.

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title ARQUITETURA DO KUBERNETES

rectangle "Control Plane (Master)" as cp #lightblue {
  component "kube-apiserver" as api
  component "etcd" as etcd
  component "kube-scheduler" as sched
  component "kube-controller-manager" as cm
  component "cloud-controller-manager" as ccm
}

rectangle "Worker Node 1" as w1 #lightyellow {
  component "kubelet" as k1
  component "kube-proxy" as kp1
  component "Container Runtime" as cr1

  rectangle "Pod" as pod1 {
    card "Container" as c1
  }
}

rectangle "Worker Node 2" as w2 #lightyellow {
  component "kubelet" as k2
  component "kube-proxy" as kp2
  component "Container Runtime" as cr2

  rectangle "Pod" as pod2 {
    card "Container" as c2
  }
}

api <--> etcd : persiste estado
api <--> sched : agenda pods
api <--> cm : gerencia controllers
api <--> ccm : integra cloud

api <--> k1 : gerencia node
api <--> k2 : gerencia node

k1 --> cr1 : gerencia containers
k2 --> cr2 : gerencia containers

@enduml
```

### Principios de Design

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title PRINCIPIOS DE DESIGN DO KUBERNETES

rectangle "Declarativo" as p1 {
  note as n1
    Voce declara O QUE quer
    Kubernetes descobre COMO fazer
  end note
}

rectangle "Estado Desejado" as p2 {
  note as n2
    Controllers monitoram continuamente
    Reconciliam atual vs desejado
  end note
}

rectangle "API-Centric" as p3 {
  note as n3
    Toda comunicacao via API Server
    RESTful, extensivel, consistente
  end note
}

rectangle "Componentizado" as p4 {
  note as n4
    Componentes independentes
    Comunicam via API
    Falha isolada
  end note
}

@enduml
```

---

## Control Plane

O Control Plane e responsavel pelas decisoes globais do cluster e pela deteccao e resposta a eventos.

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title COMPONENTES DO CONTROL PLANE

rectangle "Control Plane" {
  rectangle "kube-apiserver" as api #326CE5 {
    card "Ponto central de comunicacao" as api1
    card "RESTful API" as api2
    card "Authn/Authz/Admission" as api3
  }

  rectangle "etcd" as etcd #00BCD4 {
    card "Key-value store" as etcd1
    card "Fonte da verdade" as etcd2
    card "Consistencia forte" as etcd3
  }

  rectangle "kube-scheduler" as sched #4CAF50 {
    card "Agenda pods em nodes" as sched1
    card "Considera recursos" as sched2
    card "Considera afinidade" as sched3
  }

  rectangle "kube-controller-manager" as cm #FF9800 {
    card "Node Controller" as cm1
    card "Replication Controller" as cm2
    card "Endpoints Controller" as cm3
    card "ServiceAccount Controller" as cm4
  }

  rectangle "cloud-controller-manager" as ccm #9C27B0 {
    card "Node Controller (cloud)" as ccm1
    card "Route Controller" as ccm2
    card "Service Controller (LB)" as ccm3
  }
}

api --> etcd : unico que acessa etcd
sched --> api : busca pods pendentes
cm --> api : reconcilia estado
ccm --> api : integra cloud provider

@enduml
```

### kube-apiserver

O API Server e o frontend do Control Plane. Todas as operacoes passam por ele.

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title KUBE-APISERVER - FLUXO DE REQUISICAO

actor "kubectl" as client
actor "kubelet" as kubelet
actor "scheduler" as scheduler

rectangle "kube-apiserver" {
  component "1. Authentication" as auth
  component "2. Authorization\n(RBAC)" as authz
  component "3. Admission\nControl" as adm
  component "4. Validation" as valid
  component "5. etcd" as store
}

client --> auth
kubelet --> auth
scheduler --> auth

auth --> authz : Identidade verificada
authz --> adm : Permissao concedida
adm --> valid : Mutacoes/Validacoes
valid --> store : Objeto valido

note right of auth
  Metodos:
  - Client Certificates
  - Bearer Tokens
  - OIDC
  - Webhook
end note

note right of adm
  Webhooks:
  - Mutating
  - Validating
end note

@enduml
```

**Caracteristicas principais:**

| Aspecto | Descricao |
|---------|-----------|
| **Porta** | 6443 (HTTPS) |
| **Protocolo** | REST/JSON |
| **Stateless** | Pode ter multiplas replicas |
| **Autenticacao** | Certificados, tokens, OIDC |
| **Autorizacao** | RBAC, ABAC, Webhook |

**Flags importantes (CKA/CKS):**

```bash
# Ver configuracao do API Server
cat /etc/kubernetes/manifests/kube-apiserver.yaml

# Flags de seguranca importantes:
--anonymous-auth=false                    # Desabilita acesso anonimo
--enable-admission-plugins=...            # Admission controllers
--authorization-mode=RBAC,Node            # Modos de autorizacao
--tls-cert-file=/path/to/cert.pem         # Certificado TLS
--tls-private-key-file=/path/to/key.pem   # Chave privada
--client-ca-file=/path/to/ca.pem          # CA para clientes
--etcd-servers=https://127.0.0.1:2379     # Conexao com etcd
--audit-log-path=/var/log/audit.log       # Log de auditoria
```

### etcd

Banco de dados key-value que armazena todo o estado do cluster.

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title ETCD - ARMAZENAMENTO DE ESTADO

database "etcd cluster" {
  storage "etcd-0" as e0
  storage "etcd-1" as e1
  storage "etcd-2" as e2
}

rectangle "Dados Armazenados" {
  card "Pods" as pods
  card "Services" as svcs
  card "Secrets" as secrets
  card "ConfigMaps" as cms
  card "RBAC" as rbac
}

e0 <--> e1 : Raft consensus
e1 <--> e2 : Raft consensus
e0 <--> e2 : Raft consensus

note bottom of e1
  Requer maioria (quorum)
  3 nodes: tolera 1 falha
  5 nodes: tolera 2 falhas
  Recomendado: numeros impares
end note

@enduml
```

**Caracteristicas:**

| Aspecto | Descricao |
|---------|-----------|
| **Porta** | 2379 (client), 2380 (peer) |
| **Consenso** | Algoritmo Raft |
| **Consistencia** | Forte (linearizavel) |
| **Dados** | Key-value hierarquico |

**Comandos etcdctl (CKA/CKS):**

```bash
# Variaveis necessarias
export ETCDCTL_API=3
export ETCDCTL_ENDPOINTS=https://127.0.0.1:2379
export ETCDCTL_CACERT=/etc/kubernetes/pki/etcd/ca.crt
export ETCDCTL_CERT=/etc/kubernetes/pki/etcd/server.crt
export ETCDCTL_KEY=/etc/kubernetes/pki/etcd/server.key

# Verificar saude do cluster
etcdctl endpoint health
etcdctl endpoint status --write-out=table

# Listar membros
etcdctl member list

# Backup do etcd (MUITO IMPORTANTE para CKA)
etcdctl snapshot save /tmp/etcd-backup.db

# Verificar backup
etcdctl snapshot status /tmp/etcd-backup.db --write-out=table

# Restore do etcd
etcdctl snapshot restore /tmp/etcd-backup.db \
  --data-dir=/var/lib/etcd-restored
```

### kube-scheduler

Responsavel por decidir em qual node cada pod vai executar.

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title KUBE-SCHEDULER - PROCESSO DE SCHEDULING

rectangle "Pod Pending" as pending
rectangle "Scheduler" as sched {
  component "1. Filtering" as filter
  component "2. Scoring" as score
  component "3. Binding" as bind
}
rectangle "Node Selecionado" as selected

pending --> filter

filter --> score : Nodes viaveis

note right of filter
  Predicates (filtros):
  - PodFitsResources
  - PodFitsHost
  - PodFitsHostPorts
  - NodeSelector
  - Taints/Tolerations
end note

score --> bind : Node com maior score

note right of score
  Priorities (pontuacao):
  - LeastRequestedPriority
  - BalancedResourceAllocation
  - NodeAffinityPriority
  - PodAffinityPriority
end note

bind --> selected

@enduml
```

**Fatores considerados no scheduling:**

| Fator | Descricao |
|-------|-----------|
| **Resources** | CPU e memoria requisitados vs disponiveis |
| **NodeSelector** | Labels obrigatorias do node |
| **NodeAffinity** | Preferencias de node |
| **PodAffinity/AntiAffinity** | Co-localizacao de pods |
| **Taints/Tolerations** | Restricoes de nodes |
| **Topology Spread** | Distribuicao entre zonas |

### kube-controller-manager

Executa os controllers que reconciliam o estado do cluster.

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title KUBE-CONTROLLER-MANAGER

rectangle "kube-controller-manager" {
  rectangle "Node Controller" as nc {
    card "Monitora nodes" as nc1
    card "Marca nodes unhealthy" as nc2
  }

  rectangle "Replication Controller" as rc {
    card "Mantem numero de replicas" as rc1
    card "Cria/deleta pods" as rc2
  }

  rectangle "Endpoints Controller" as ec {
    card "Popula Endpoints" as ec1
    card "Liga Services a Pods" as ec2
  }

  rectangle "ServiceAccount Controller" as sc {
    card "Cria SA default" as sc1
    card "Em novos namespaces" as sc2
  }

  rectangle "Deployment Controller" as dc {
    card "Gerencia ReplicaSets" as dc1
    card "Rolling updates" as dc2
  }

  rectangle "Job Controller" as jc {
    card "Gerencia Jobs" as jc1
    card "Cria pods para jobs" as jc2
  }
}

note bottom
  Cada controller roda em loop:
  1. Observa estado atual
  2. Compara com estado desejado
  3. Reconcilia diferencas
end note

@enduml
```

**Controllers principais:**

| Controller | Responsabilidade |
|------------|------------------|
| **Node Controller** | Detectar e responder quando nodes ficam down |
| **Replication Controller** | Manter numero correto de pods |
| **Endpoints Controller** | Popular objeto Endpoints |
| **ServiceAccount Controller** | Criar SA default em namespaces |
| **Deployment Controller** | Gerenciar ReplicaSets e updates |
| **StatefulSet Controller** | Gerenciar StatefulSets |
| **DaemonSet Controller** | Garantir pod em cada node |
| **Job Controller** | Gerenciar Jobs |
| **CronJob Controller** | Criar Jobs por schedule |

---

## Worker Nodes

Os Worker Nodes sao as maquinas que executam os containers das aplicacoes.

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title COMPONENTES DO WORKER NODE

rectangle "Worker Node" {
  rectangle "kubelet" as kubelet #326CE5 {
    card "Agente do node" as k1
    card "Gerencia pods" as k2
    card "Reporta status" as k3
  }

  rectangle "kube-proxy" as proxy #4CAF50 {
    card "Networking do Service" as p1
    card "iptables/IPVS rules" as p2
    card "Load balancing" as p3
  }

  rectangle "Container Runtime" as runtime #FF9800 {
    card "containerd" as r1
    card "CRI-O" as r2
    card "Docker (legado)" as r3
  }

  rectangle "Pods" as pods #9C27B0 {
    card "Pod 1" as pod1
    card "Pod 2" as pod2
    card "Pod N" as podn
  }
}

kubelet --> runtime : CRI
kubelet --> pods : gerencia lifecycle
proxy --> pods : networking

@enduml
```

### kubelet

Agente que roda em cada node e garante que os containers estejam rodando.

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title KUBELET - FUNCOES

actor "API Server" as api
rectangle "kubelet" as kubelet {
  component "Pod Lifecycle" as plc
  component "Volume Manager" as vm
  component "Probe Manager" as pm
  component "Status Manager" as sm
  component "CRI Client" as cri
}
entity "Container Runtime" as runtime
entity "Pods" as pods
api <--> kubelet : gRPC
kubelet --> runtime : CRI calls
runtime --> pods : containers

note right of plc
  - Cria/deleta pods
  - Sync com API
end note

note right of pm
  - Liveness probes
  - Readiness probes
  - Startup probes
end note

@enduml
```

**Responsabilidades do kubelet:**

| Funcao | Descricao |
|--------|-----------|
| **Pod Lifecycle** | Criar, atualizar, deletar pods |
| **Volume Management** | Montar/desmontar volumes |
| **Probes** | Executar health checks |
| **Resource Monitoring** | cAdvisor integrado |
| **Status Reporting** | Reportar status do node e pods |
| **Static Pods** | Gerenciar pods de manifests locais |

**Arquivos importantes:**

```bash
# Configuracao do kubelet
/var/lib/kubelet/config.yaml

# Diretorio de static pods
/etc/kubernetes/manifests/

# Logs do kubelet
journalctl -u kubelet -f
```

### kube-proxy

Implementa a abstraccao de Service no node.

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title KUBE-PROXY - MODOS DE OPERACAO

rectangle "iptables mode (padrao)" as ipt {
  note as n1
    - Usa regras iptables
    - Random load balancing
    - Mais simples
    - Menos overhead
  end note
}

rectangle "IPVS mode" as ipvs {
  note as n2
    - Usa IPVS do kernel
    - Mais algoritmos de LB
    - Melhor performance
    - Mais escalavel
  end note
}

rectangle "userspace mode (legado)" as user {
  note as n3
    - Proxy em user space
    - Round-robin LB
    - Mais lento
    - Evitar
  end note
}

@enduml
```

**Algoritmos de Load Balancing (IPVS):**

| Algoritmo | Descricao |
|-----------|-----------|
| rr | Round Robin |
| lc | Least Connections |
| dh | Destination Hashing |
| sh | Source Hashing |
| sed | Shortest Expected Delay |
| nq | Never Queue |

### Container Runtime

Interface para executar containers (CRI - Container Runtime Interface).

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title CONTAINER RUNTIME INTERFACE (CRI)

rectangle "kubelet" as kubelet

rectangle "CRI" as cri {
  component "RuntimeService" as rs
  component "ImageService" as is
}

rectangle "Runtimes" {
  component "containerd" as containerd #4CAF50
  component "CRI-O" as crio #326CE5
}

rectangle "OCI Runtime" {
  component "runc" as runc
  component "gVisor" as gvisor
  component "Kata" as kata
}

kubelet --> cri : gRPC
cri --> containerd
cri --> crio
containerd --> runc
crio --> runc

note bottom of containerd
  containerd e o padrao
  em kubeadm >= 1.24
end note

@enduml
```

---

## Fluxo de Criacao de Pod

### Diagrama de Sequencia

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title FLUXO DE CRIACAO DE POD

actor "kubectl" as user
participant "kube-apiserver" as api
database "etcd" as etcd
participant "kube-scheduler" as sched
participant "kubelet" as kubelet
participant "Container Runtime" as runtime

user -> api : kubectl apply -f pod.yaml
api -> api : Authentication
api -> api : Authorization
api -> api : Admission Control
api -> etcd : Persiste Pod (status: Pending)
api -> user : Pod created

sched -> api : Watch: pods sem node
api -> sched : Pod precisa de node
sched -> sched : Filtering
sched -> sched : Scoring
sched -> api : Bind: Pod -> Node X
api -> etcd : Atualiza nodeName

kubelet -> api : Watch: pods do meu node
api -> kubelet : Novo pod para voce
kubelet -> runtime : Criar containers
runtime -> runtime : Pull image
runtime -> runtime : Start containers
kubelet -> api : Status: Running
api -> etcd : Atualiza status

@enduml
```

### Detalhamento das Etapas

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title ETAPAS DA CRIACAO DE POD

rectangle "1. SUBMISSAO" as s1 {
  card "Usuario submete YAML" as s1a
  card "API valida e persiste" as s1b
  card "Pod status: Pending" as s1c
}

rectangle "2. SCHEDULING" as s2 {
  card "Scheduler detecta pod" as s2a
  card "Filtra nodes viaveis" as s2b
  card "Pontua e seleciona" as s2c
  card "Bind pod ao node" as s2d
}

rectangle "3. EXECUCAO" as s3 {
  card "kubelet detecta pod" as s3a
  card "Pull da imagem" as s3b
  card "Cria containers" as s3c
  card "Pod status: Running" as s3d
}

s1 --> s2
s2 --> s3

@enduml
```

---

## Alta Disponibilidade

### Arquitetura HA do Control Plane

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title ALTA DISPONIBILIDADE - CONTROL PLANE

rectangle "Load Balancer" as lb #gray

rectangle "Control Plane Node 1" as cp1 {
  component "api-server" as api1
  component "scheduler" as sch1
  component "controller-manager" as cm1
  database "etcd" as etcd1
}

rectangle "Control Plane Node 2" as cp2 {
  component "api-server" as api2
  component "scheduler (standby)" as sch2 #lightgray
  component "controller-manager (standby)" as cm2 #lightgray
  database "etcd" as etcd2
}

rectangle "Control Plane Node 3" as cp3 {
  component "api-server" as api3
  component "scheduler (standby)" as sch3 #lightgray
  component "controller-manager (standby)" as cm3 #lightgray
  database "etcd" as etcd3
}

lb --> api1
lb --> api2
lb --> api3

etcd1 <--> etcd2 : Raft
etcd2 <--> etcd3 : Raft
etcd1 <--> etcd3 : Raft

note bottom of lb
  API Servers: Active-Active (stateless)
  Scheduler/CM: Active-Standby (leader election)
  etcd: Raft consensus (quorum)
end note

@enduml
```

### Topologias de etcd

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title TOPOLOGIAS DE ETCD

rectangle "Stacked etcd (mais comum)" as stacked {
  rectangle "Node 1" as n1 {
    card "API + etcd" as a1
  }
  rectangle "Node 2" as n2 {
    card "API + etcd" as a2
  }
  rectangle "Node 3" as n3 {
    card "API + etcd" as a3
  }
}

rectangle "External etcd (mais robusto)" as external {
  rectangle "API Nodes" as api {
    card "API 1" as ap1
    card "API 2" as ap2
    card "API 3" as ap3
  }
  rectangle "etcd Cluster" as etc {
    card "etcd 1" as e1
    card "etcd 2" as e2
    card "etcd 3" as e3
  }
}

note bottom of stacked
  Mais simples de gerenciar
  Menos nodes necessarios
  Se node falha, perde API + etcd
end note

note bottom of external
  etcd isolado
  Escalabilidade independente
  Mais resiliente
end note

@enduml
```

### Recomendacoes de HA

| Componente | Minimo | Recomendado | Notas |
|------------|--------|-------------|-------|
| **Control Plane Nodes** | 3 | 3 ou 5 | Numeros impares para quorum |
| **etcd** | 3 | 3 ou 5 | Tolera (n-1)/2 falhas |
| **Worker Nodes** | 1 | 3+ | Depende da carga |
| **Load Balancer** | 1 | 2 (HA) | Para API Server |

---

## Comunicacao entre Componentes

### Diagrama de Comunicacao

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title COMUNICACAO ENTRE COMPONENTES

rectangle "Control Plane" {
  component "API Server\n(6443)" as api
  database "etcd\n(2379/2380)" as etcd
  component "Scheduler\n(10259)" as sched
  component "Controller Manager\n(10257)" as cm
}

rectangle "Worker Node" {
  component "kubelet\n(10250)" as kubelet
  component "kube-proxy\n(10256)" as proxy
}

api <--> etcd : gRPC/TLS
api <--> sched : HTTPS
api <--> cm : HTTPS
api <--> kubelet : HTTPS
api <--> proxy : HTTPS

note right of api
  Todas conexoes sao
  TLS mutuamente autenticadas
  (exceto metrics/healthz)
end note

@enduml
```

### Portas Importantes (para firewall)

| Componente | Porta | Protocolo | Uso |
|------------|-------|-----------|-----|
| **API Server** | 6443 | TCP | API HTTPS |
| **etcd** | 2379 | TCP | Client requests |
| **etcd** | 2380 | TCP | Peer communication |
| **kubelet** | 10250 | TCP | API |
| **kube-scheduler** | 10259 | TCP | Secure port |
| **controller-manager** | 10257 | TCP | Secure port |
| **kube-proxy** | 10256 | TCP | Health check |
| **NodePort Services** | 30000-32767 | TCP | Servicos externos |

---

## Dicas para o Exame

### CKA - Pontos Importantes

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title DICAS CKA - ARQUITETURA

rectangle "OBRIGATORIO SABER" {
  card "1. Localizar manifests:\n/etc/kubernetes/manifests/" as d1
  card "2. Logs dos componentes:\njournalctl -u kubelet\nkubectl logs -n kube-system" as d2
  card "3. Backup etcd:\netcdctl snapshot save" as d3
  card "4. Portas e comunicacao\nentre componentes" as d4
}

rectangle "TROUBLESHOOTING" {
  card "kubelet nao inicia:\nverificar certificados" as t1
  card "API Server down:\nverificar /etc/kubernetes/manifests/" as t2
  card "etcd problems:\nverificar quorum" as t3
}

@enduml
```

### KCNA - Conceitos Chave

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title KCNA - CONCEITOS ARQUITETURA

card "Control Plane:\nCerebro do cluster\nAPI Server, etcd, Scheduler, CM" as c1
card "Worker Node:\nOnde pods executam\nkubelet, kube-proxy, runtime" as c2
card "etcd:\nBanco de dados\nArmazena todo estado" as c3
card "API Server:\nPonto central\nToda comunicacao passa por ele" as c4
card "Scheduler:\nDecide onde pod roda\nFiltering + Scoring" as c5
card "Controllers:\nReconciliam estado\nAtual vs Desejado" as c6

@enduml
```

### Comandos Uteis para Troubleshooting

```bash
# Ver componentes do control plane
kubectl get pods -n kube-system

# Ver status dos nodes
kubectl get nodes -o wide
kubectl describe node <node-name>

# Ver logs dos componentes (kubeadm)
kubectl logs -n kube-system kube-apiserver-<node>
kubectl logs -n kube-system kube-scheduler-<node>
kubectl logs -n kube-system kube-controller-manager-<node>
kubectl logs -n kube-system etcd-<node>

# Logs do kubelet
journalctl -u kubelet -f

# Verificar certificados
kubeadm certs check-expiration
openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text -noout

# Verificar conectividade
kubectl get --raw='/healthz'
kubectl get --raw='/readyz'
curl -k https://localhost:6443/healthz

# Ver eventos do cluster
kubectl get events --sort-by='.lastTimestamp'
kubectl get events -A --sort-by='.lastTimestamp'
```

---

## Referencias

### Links Internos

- [Componentes dos Nos](cluster-components/node-components.md) - Detalhes de cada componente
- [kube-apiserver](cluster-components/kube-apiserver.md)
- [etcd](cluster-components/etcd.md)
- [kube-scheduler](cluster-components/kube-scheduler.md)
- [kube-controller-manager](cluster-components/kube-controller-manager.md)
- [kubelet](cluster-components/kubelet.md)
- [kube-proxy](cluster-components/kube-proxy.md)
- [Alta Disponibilidade](fundamentals/high-availability.md)
- [Backup e Restore](maintenance/backup-e-restore.md)

### Documentacao Oficial

- [Kubernetes Components](https://kubernetes.io/docs/concepts/overview/components/)
- [Cluster Architecture](https://kubernetes.io/docs/concepts/architecture/)
- [Communication between Nodes](https://kubernetes.io/docs/concepts/architecture/control-plane-node-communication/)
- [etcd](https://etcd.io/docs/)
- [High Availability](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/)

---

## Best Practices

### Arquitetura de Producao

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title BEST PRACTICES - ARQUITETURA

rectangle "CONTROL PLANE" {
  card "3+ masters (impar)" as bp1
  card "etcd em SSD" as bp2
  card "Load balancer na frente" as bp3
  card "Backups regulares do etcd" as bp4
}

rectangle "WORKER NODES" {
  card "Separar por workload type" as bp5
  card "Node pools/groups" as bp6
  card "Recursos adequados" as bp7
  card "Monitoramento ativo" as bp8
}

rectangle "SEGURANCA" {
  card "TLS em todas conexoes" as bp9
  card "RBAC bem configurado" as bp10
  card "Network policies" as bp11
  card "Audit logging" as bp12
}

@enduml
```

### Recomendacoes por Componente

| Componente | Best Practice |
|------------|---------------|
| **API Server** | Multiplas replicas, rate limiting, audit logs |
| **etcd** | 3 ou 5 nodes, SSD, backups frequentes |
| **Scheduler** | Configurar priorities corretamente |
| **Controller Manager** | Monitorar logs para erros de reconciliacao |
| **kubelet** | Reservar recursos para sistema |
| **kube-proxy** | Considerar IPVS para clusters grandes |

### Dimensionamento

| Tamanho do Cluster | Control Plane | Workers | etcd |
|-------------------|---------------|---------|------|
| **Pequeno** (<50 pods) | 1 | 1-3 | 1 |
| **Medio** (50-500 pods) | 3 | 3-10 | 3 |
| **Grande** (500-5000 pods) | 3-5 | 10-100 | 5 |
| **Muito Grande** (5000+ pods) | 5+ | 100+ | 5-7 |

---

## Troubleshooting Arquitetural

### Problemas Comuns

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title TROUBLESHOOTING - PROBLEMAS COMUNS

rectangle "API Server" {
  card "Connection refused\n→ Verificar porta 6443" as p1
  card "Certificate expired\n→ kubeadm certs renew" as p2
  card "etcd connection failed\n→ Verificar etcd health" as p3
}

rectangle "Scheduler" {
  card "Pods nao schedulam\n→ Verificar recursos/taints" as p4
  card "Leader election failing\n→ Verificar lease" as p5
}

rectangle "kubelet" {
  card "Node NotReady\n→ journalctl -u kubelet" as p6
  card "Container runtime error\n→ crictl info" as p7
}

@enduml
```

### Comandos de Diagnostico

```bash
# API Server
kubectl get --raw='/healthz?verbose'
curl -k https://localhost:6443/healthz

# etcd
etcdctl endpoint health --cluster
etcdctl endpoint status --write-out=table

# Scheduler e Controller Manager
kubectl get lease -n kube-system
kubectl logs -n kube-system kube-scheduler-<node>

# kubelet
systemctl status kubelet
journalctl -u kubelet -f --since "10 minutes ago"

# Rede
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl run test --image=busybox --rm -it -- wget -qO- kubernetes
```

---

> **Resumo**: O Kubernetes tem arquitetura Control Plane + Worker Nodes. O Control Plane (API Server, etcd, Scheduler, Controller Manager) toma decisoes globais. Os Worker Nodes (kubelet, kube-proxy, container runtime) executam containers. Toda comunicacao passa pelo API Server. O etcd armazena todo estado (fazer backup!). Para HA, use 3+ control plane nodes com etcd em quorum.
