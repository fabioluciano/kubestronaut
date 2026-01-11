# High Availability (HA) no Kubernetes

## Conceitos Fundamentais

### O que é Alta Disponibilidade?

Alta Disponibilidade (HA) é a capacidade de um sistema continuar operando mesmo quando componentes falham. No Kubernetes, isso envolve redundância em múltiplas camadas.

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white
skinparam defaultTextAlignment center

rectangle "CAMADAS DE HA NO KUBERNETES" {
  rectangle "1. Aplicação" as app
  rectangle "2. Worker Nodes" as workers
  rectangle "3. Control Plane" as cp
  rectangle "4. etcd" as etcd
  rectangle "5. Load Balancer" as lb
  rectangle "6. Infraestrutura" as infra
}

note right of app : Múltiplas réplicas (Deployment)
note right of workers : Múltiplos nodes, anti-affinity
note right of cp : Múltiplos masters
note right of etcd : Cluster com quorum
note right of lb : Balanceamento para API Server
note right of infra : Múltiplas zonas/regiões

app -[hidden]-> workers
workers -[hidden]-> cp
cp -[hidden]-> etcd
etcd -[hidden]-> lb
lb -[hidden]-> infra

@enduml
```

---

## Arquitetura HA do Control Plane

### Topologia Stacked (etcd junto)

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white
skinparam componentStyle rectangle

title STACKED TOPOLOGY

rectangle "LOAD BALANCER\n(HAProxy, nginx, cloud LB)" as LB

rectangle "Master 1" as M1 {
  component "API Server" as api1
  component "Scheduler" as sched1
  component "Ctrl Mgr" as cm1
  database "etcd" as etcd1
}

rectangle "Master 2" as M2 {
  component "API Server" as api2
  component "Scheduler" as sched2
  component "Ctrl Mgr" as cm2
  database "etcd" as etcd2
}

rectangle "Master 3" as M3 {
  component "API Server" as api3
  component "Scheduler" as sched3
  component "Ctrl Mgr" as cm3
  database "etcd" as etcd3
}

LB --> M1
LB --> M2
LB --> M3

etcd1 <--> etcd2
etcd2 <--> etcd3

note bottom
  Vantagens: Simples, menos máquinas
  Desvantagens: etcd compete por recursos
end note

@enduml
```

### Topologia External etcd

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white
skinparam componentStyle rectangle

title EXTERNAL ETCD TOPOLOGY

rectangle "LOAD BALANCER" as LB

rectangle "Master 1" as M1 {
  component "API Server" as api1
  component "Scheduler" as sched1
  component "Ctrl Mgr" as cm1
}

rectangle "Master 2" as M2 {
  component "API Server" as api2
  component "Scheduler" as sched2
  component "Ctrl Mgr" as cm2
}

rectangle "Master 3" as M3 {
  component "API Server" as api3
  component "Scheduler" as sched3
  component "Ctrl Mgr" as cm3
}

database "etcd 1" as etcd1
database "etcd 2" as etcd2
database "etcd 3" as etcd3

LB --> M1
LB --> M2
LB --> M3

M1 --> etcd1
M1 --> etcd2
M1 --> etcd3
M2 --> etcd1
M2 --> etcd2
M2 --> etcd3
M3 --> etcd1
M3 --> etcd2
M3 --> etcd3

etcd1 <--> etcd2
etcd2 <--> etcd3

note bottom
  Vantagens: Isolamento, melhor performance
  Desvantagens: Mais máquinas, complexidade
end note

@enduml
```

---

## etcd em Alta Disponibilidade

### Quorum e Tolerância a Falhas

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title QUORUM DO ETCD

note as N1
  **Fórmula:** Quorum = (N / 2) + 1  (maioria simples)
  
  | Nodes | Quorum | Tolerância | Recomendação |
  |-------|--------|------------|--------------|
  | 1     | 1      | 0          | Dev only     |
  | 2     | 2      | 0          | NÃO USAR     |
  | 3     | 2      | 1          | Mínimo HA    |
  | 5     | 3      | 2          | Produção     |
  | 7     | 4      | 3          | Large scale  |
  
  ⚠️ Sempre use número ÍMPAR de nodes!
  Com número par, não há benefício de tolerância
end note

@enduml
```

### Leader Election

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title RAFT CONSENSUS (etcd)

rectangle "LEADER" as leader
rectangle "Follower 1" as f1
rectangle "Follower 2" as f2
rectangle "Follower 3" as f3

note right of leader
  Recebe escritas
end note

leader --> f1 : replica
leader --> f2 : replica
leader --> f3 : replica

note as N1
  1. Um LEADER é eleito entre os members
  2. Todas as escritas vão para o leader
  3. Leader replica para followers
  4. Escrita confirmada quando MAIORIA confirma
  5. Se leader falha, nova eleição ocorre
end note

@enduml
```

### Comandos etcd

```bash
# Verificar status do cluster
ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/healthcheck-client.crt \
  --key=/etc/kubernetes/pki/etcd/healthcheck-client.key \
  endpoint status --write-out=table

# Ver membros
etcdctl member list --write-out=table

# Verificar saúde
etcdctl endpoint health --write-out=table
```

---

## Control Plane HA

### kube-apiserver

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title API Server é STATELESS - pode rodar múltiplas instâncias

rectangle "Load Balancer" as LB

rectangle "API Server\n:6443" as api1
rectangle "API Server\n:6443" as api2
rectangle "API Server\n:6443" as api3

LB --> api1
LB --> api2
LB --> api3

note bottom
  Todos ativos, load balanced
end note

@enduml
```

### kube-scheduler e controller-manager

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title Scheduler e Controller Manager são STATEFUL - requerem eleição

rectangle "Scheduler\nLEADER ✓" as sched1 #lightgray
rectangle "Scheduler\nstandby" as sched2
rectangle "Scheduler\nstandby" as sched3

rectangle "Ctrl Manager\nstandby" as cm1
rectangle "Ctrl Manager\nLEADER ✓" as cm2 #lightgray
rectangle "Ctrl Manager\nstandby" as cm3

note bottom
  Apenas 1 ATIVO por vez - usa LEASE para eleição
end note

@enduml
```

### Verificar Leader

```bash
# Ver quem é o leader do scheduler
kubectl get lease -n kube-system kube-scheduler -o yaml

# Ver quem é o leader do controller-manager
kubectl get lease -n kube-system kube-controller-manager -o yaml

# Exemplo de saída
# holderIdentity: master-1_xxxxx
```

---

## Configuração kubeadm HA

### Inicializar Primeiro Master

```yaml
../assets/high-availability/kubeadm-ha-config.yaml}}
```

```bash
# Criar arquivo de configuração
# kubeadm-config.yaml com o conteúdo acima

# Inicializar
sudo kubeadm init --config=kubeadm-config.yaml --upload-certs

# Guarde os comandos de join que aparecem!
```

### Adicionar Control Plane Nodes

```bash
# Comando gerado pelo init (exemplo)
sudo kubeadm join LOAD_BALANCER_IP:6443 \
  --token <token> \
  --discovery-token-ca-cert-hash sha256:<hash> \
  --control-plane \
  --certificate-key <cert-key>
```

### Load Balancer (HAProxy)

```bash
# /etc/haproxy/haproxy.cfg
frontend kubernetes-frontend
    bind *:6443
    mode tcp
    option tcplog
    default_backend kubernetes-backend

backend kubernetes-backend
    mode tcp
    option tcp-check
    balance roundrobin
    server master-1 192.168.1.10:6443 check fall 3 rise 2
    server master-2 192.168.1.11:6443 check fall 3 rise 2
    server master-3 192.168.1.12:6443 check fall 3 rise 2
```

---

## HA de Aplicações

### Deployment com Réplicas

```yaml
../assets/high-availability/deployment-replicas.yaml}}
```

### Pod Anti-Affinity (Distribuir em Nodes)

```yaml
../assets/high-availability/deployment-anti-affinity.yaml}}
```

### Topology Spread Constraints

```yaml
../assets/high-availability/deployment-topology-spread.yaml}}
```

### PodDisruptionBudget

```yaml
../assets/high-availability/poddisruptionbudget.yaml}}
```

---

## Comportamento em Falhas

### Quando Master Falha (Single Master)

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title O QUE ACONTECE SEM MASTER (SINGLE)

rectangle "Continua funcionando" #lightgreen {
  card "✅ Pods CONTINUAM rodando nos workers" as c1
  card "✅ Services CONTINUAM funcionando" as c2
  card "✅ Tráfego CONTINUA sendo roteado" as c3
}

rectangle "Para de funcionar" #pink {
  card "❌ kubectl NÃO FUNCIONA (API Server down)" as s1
  card "❌ Novos pods NÃO serão scheduled" as s2
  card "❌ Pods que morrem NÃO serão recriados" as s3
  card "❌ Self-healing NÃO funciona" as s4
}

@enduml
```

### Quando Worker Node Falha

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title O QUE ACONTECE QUANDO WORKER FALHA

|Sequência de Eventos|
start
:kubelet para de enviar heartbeats;
:Node marcado como NotReady (5min default);
:Pod eviction timer inicia (5min default);
:Pods são rescheduled para outros nodes;
stop

note right
  Configurações:
  - node-monitor-grace-period: 40s (tempo até NotReady)
  - pod-eviction-timeout: 5m (tempo até evict pods)
end note

@enduml
```

---

## Troubleshooting HA

### Verificar Status do Cluster

```bash
# Status dos nodes
kubectl get nodes

# Status dos componentes
kubectl get componentstatuses  # deprecated mas ainda funciona
kubectl get --raw='/healthz?verbose'

# Verificar etcd
kubectl -n kube-system exec -it etcd-master-1 -- \
  etcdctl endpoint health --cluster

# Verificar leaders
kubectl get lease -n kube-system
```

### Problemas Comuns

```bash
# etcd não forma quorum
# - Verificar conectividade entre members
# - Verificar certificados
# - Ver logs: kubectl logs -n kube-system etcd-<node>

# API Server inacessível
# - Verificar Load Balancer
# - Verificar certificados
# - Verificar firewall (porta 6443)

# Scheduler/Controller não elegem leader
# - Verificar leases
# - Verificar logs
# - Reiniciar pods
```

---

## Dicas para o Exame CKA

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title DICAS CKA - HA

rectangle "1. Quorum etcd" {
  note as N1
    • 3 nodes = tolera 1 falha
    • 5 nodes = tolera 2 falhas
    • Sempre número ÍMPAR
  end note
}

rectangle "2. Componentes" {
  note as N2
    • API Server = stateless (múltiplos ativos)
    • Scheduler/Controller = leader election (1 ativo)
  end note
}

rectangle "3. kubeadm HA" {
  note as N3
    • controlPlaneEndpoint para LB
    • --upload-certs para compartilhar certificados
    • --control-plane no join de masters
  end note
}

rectangle "4. Se master morrer" {
  note as N4
    • Pods continuam rodando
    • Novos pods não são criados
  end note
}

@enduml
```

---

## Referências

- [kubeadm](tools/kubeadm.md)
- [etcd](cluster-components/etcd.md)
- [ETCDCTL](security/etcdctl.md)
- [Backup e Restore](maintenance/backup-e-restore.md)
- [Scheduling](workloads/scheduling.md)
- [Cluster Upgrade](maintenance/cluster-upgrade.md)
