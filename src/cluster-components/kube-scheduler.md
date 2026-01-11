# kube-scheduler

> **Certificacoes**: CKA (10%), CKS (5%)
> **Dificuldade**: Avancado

O **kube-scheduler** e o componente responsavel por decidir em qual node cada pod sera executado. Ele observa pods recem-criados que nao tem um node atribuido e seleciona o melhor node para eles.

```admonish warning title="Importante"
O scheduler apenas **decide** onde o pod vai rodar. Quem **executa** o pod e o kubelet do node selecionado.
```

## Arquitetura e Funcionamento

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title Arquitetura do kube-scheduler

package "kube-scheduler" {
    [Scheduling Queue] as queue
    [Scheduling Cycle] as cycle
    package "Framework Plugins" {
        [Filter Plugins] as filter
        [Score Plugins] as score
        [Reserve/Bind Plugins] as bind
    }
}

package "kube-apiserver" {
    [API Server] as api
}

database "etcd" as etcd

[Unscheduled\nPods] as unscheduled

unscheduled --> queue : Watch pods sem node
queue --> cycle : Pod para scheduling
cycle --> filter : Filtra nodes viaveis
filter --> score : Ranqueia nodes
score --> bind : Seleciona melhor node
bind --> api : Bind pod ao node
api --> etcd

@enduml
```

## Ciclo de Scheduling

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title Ciclo de Scheduling

start

partition "Scheduling Queue" {
    :Pod criado sem nodeName;
    :Adiciona a fila de scheduling;
    :Ordena por prioridade;
}

partition "Filtering (Predicates)" {
    :Obtem lista de todos nodes;
    :Executa filter plugins;
    note right
      - NodeSelector
      - Taints/Tolerations
      - Resources (CPU/Memory)
      - NodeAffinity
      - PodAffinity/AntiAffinity
      - Volume requirements
    end note
    if (Nodes viaveis > 0?) then (sim)
    else (nao)
        :Pod fica Pending;
        stop
    endif
}

partition "Scoring (Priorities)" {
    :Executa score plugins;
    note right
      - Resource balancing
      - Spreading
      - Node affinity weight
      - Pod affinity weight
    end note
    :Soma scores de cada node;
    :Seleciona node com maior score;
}

partition "Binding" {
    :Reserve resources no node;
    :Assume pod esta bound;
    :Envia binding ao API Server\n(assincrono);
}

stop

@enduml
```

## Filter Plugins (Predicates)

Os filter plugins eliminam nodes que nao podem executar o pod.

### Plugins de Filtering Padrao

| Plugin | Descricao |
|--------|-----------|
| `NodeResourcesFit` | Verifica se node tem recursos suficientes |
| `NodeName` | Verifica se pod especificou nodeName |
| `NodePorts` | Verifica se portas estao disponiveis |
| `NodeAffinity` | Verifica node affinity requirements |
| `TaintToleration` | Verifica se pod tolera taints do node |
| `NodeUnschedulable` | Verifica se node esta marcado unschedulable |
| `PodTopologySpread` | Verifica topology spread constraints |
| `InterPodAffinity` | Verifica pod affinity/anti-affinity |
| `VolumeBinding` | Verifica se volumes podem ser bound |
| `VolumeZone` | Verifica zone requirements de volumes |

### Exemplo de Filtering

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title Filtering - Exemplo

rectangle "Pod Requirements" as pod {
    card "CPU: 500m\nMemory: 256Mi\nTolerations: gpu=true" as req
}

rectangle "Nodes" as nodes {
    card "Node A\nCPU: 2000m\nMemory: 4Gi\nTaint: gpu=true" as a
    card "Node B\nCPU: 100m\nMemory: 128Mi\nNo Taints" as b
    card "Node C\nCPU: 2000m\nMemory: 4Gi\nNo Taints" as c
    card "Node D\nCPU: 1000m\nMemory: 1Gi\nTaint: gpu=true" as d
}

pod --> a : Passa (recursos OK, toleration OK)
pod --> b : Falha (recursos insuficientes)
pod --> c : Passa (recursos OK, sem taint)
pod --> d : Passa (recursos OK, toleration OK)

note bottom of nodes
  Nodes viaveis: A, C, D
end note

@enduml
```

## Score Plugins (Priorities)

Os score plugins ranqueiam os nodes viaveis.

### Plugins de Scoring Padrao

| Plugin | Descricao |
|--------|-----------|
| `NodeResourcesBalancedAllocation` | Prefere nodes com uso balanceado de recursos |
| `ImageLocality` | Prefere nodes que ja tem a imagem |
| `InterPodAffinity` | Score baseado em pod affinity |
| `NodeAffinity` | Score baseado em node affinity preferido |
| `PodTopologySpread` | Score baseado em spreading |
| `TaintToleration` | Score baseado em tolerations |
| `NodeResourcesFit` | Score baseado em recursos disponiveis |

### Exemplo de Scoring

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title Scoring - Exemplo

rectangle "Nodes Viaveis" as nodes {
    card "Node A\nResources: 70%\nImage: Yes\nAffinity Match" as a
    card "Node C\nResources: 30%\nImage: No\nNo Affinity" as c
    card "Node D\nResources: 50%\nImage: Yes\nAffinity Match" as d
}

card "Scores Finais" as scores {
    note as n
      Node A:
        - Balance: 30
        - Image: 20
        - Affinity: 50
        Total: 100

      Node C:
        - Balance: 70
        - Image: 0
        - Affinity: 0
        Total: 70

      Node D:
        - Balance: 50
        - Image: 20
        - Affinity: 50
        Total: 120 (WINNER)
    end note
}

nodes --> scores

@enduml
```

## Scheduler Profiles

A partir do Kubernetes 1.18, e possivel configurar multiplos profiles de scheduling.

### Configuracao de Profile

```yaml
{{#include ../assets/cluster-components/kubeschedulerconfiguration-noderesourcesbalancedallocation.yaml}}
```

### Usar Profile Especifico em Pod

```yaml
{{#include ../assets/pod/pod-batch-job-pod.yaml}}
```

## Scheduling Policies

### Node Affinity

```yaml
{{#include ../assets/pod/pod-with-node-affinity.yaml}}
```

### Pod Affinity e Anti-Affinity

```yaml
{{#include ../assets/pod/pod-with-pod-affinity.yaml}}
```

### Topology Spread Constraints

```yaml
{{#include ../assets/pod/pod-with-topology-spread.yaml}}
```

## Priority e Preemption

### PriorityClass

```yaml
{{#include ../assets/cluster-components/priorityclass-high-priority.yaml}}
```

### Usar PriorityClass

```yaml
{{#include ../assets/pod/pod-high-priority-pod.yaml}}
```

### Fluxo de Preemption

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title Preemption - Fluxo

start

:Pod alta prioridade nao consegue\nser scheduled (sem recursos);

:Scheduler busca pods de menor\nprioridade para preemptar;

if (Encontrou candidatos?) then (sim)
    :Seleciona pod(s) para preemptar;
    :Envia sinal de termination\n(graceful shutdown);
    :Aguarda terminacao;
    :Schedula pod de alta prioridade;
else (nao)
    :Pod permanece Pending;
endif

stop

@enduml
```

## Custom Scheduler

Voce pode criar e executar seu proprio scheduler.

### Deploy de Custom Scheduler

```yaml
{{#include ../assets/serviceaccount/serviceaccount-my-scheduler.yaml}}
```

### Usar Custom Scheduler

```yaml
{{#include ../assets/pod/pod-pod-with-custom-scheduler.yaml}}
```

## Configuracao do kube-scheduler

### Manifest Completo

```yaml
{{#include ../assets/pod/pod-kube-scheduler.yaml}}
```

### Arquivo de Configuracao

```yaml
{{#include ../assets/cluster-components/kubeschedulerconfiguration-noderesourcesfit.yaml}}
```

## Troubleshooting

### Verificar Status

```bash
# Verificar se scheduler esta rodando
crictl ps | grep scheduler

# Ver logs
kubectl logs -n kube-system kube-scheduler-<node>

# Health check
curl -k https://127.0.0.1:10259/healthz

# Ver leader
kubectl get lease -n kube-system kube-scheduler -o yaml
```

### Pod Pendente

```bash
# Ver eventos do pod
kubectl describe pod <pod-name>

# Motivos comuns:
# - 0/3 nodes are available: insufficient cpu
# - 0/3 nodes are available: insufficient memory
# - 0/3 nodes are available: 3 node(s) had taint {key: NoSchedule}
# - 0/3 nodes are available: 3 node(s) didn't match Pod's node affinity

# Ver recursos dos nodes
kubectl describe nodes | grep -A 5 "Allocated resources"

# Ver taints dos nodes
kubectl describe nodes | grep Taints

# Verificar node selectors/affinity do pod
kubectl get pod <pod-name> -o yaml | grep -A 10 nodeSelector
kubectl get pod <pod-name> -o yaml | grep -A 20 affinity
```

### Verificar Scheduling Events

```bash
# Ver eventos de scheduling
kubectl get events --field-selector reason=FailedScheduling

# Ver eventos recentes
kubectl get events --sort-by='.lastTimestamp' | grep -i schedul

# Ver metricas do scheduler
curl -k https://127.0.0.1:10259/metrics | grep scheduler
```

### Simulacoes com dry-run

```bash
# Ver onde pod seria scheduled (alpha feature)
kubectl alpha debug -it pod/<pod> --image=busybox --dry-run=server
```

## Dicas para o Exame

```admonish tip title="CKA/CKS"
1. **Caminho do manifest**: `/etc/kubernetes/manifests/kube-scheduler.yaml`
2. **Saiba a diferenca entre**:
   - `nodeSelector` - simples, labels
   - `nodeAffinity` - avancado, operadores
   - `podAffinity/AntiAffinity` - relacao entre pods
3. **Taints e Tolerations** - scheduler respeita, mas nao garante placement
4. **PriorityClass** - controla ordem de scheduling e preemption
5. **spec.schedulerName** - para usar scheduler customizado
6. **Porta de health**: 10259 (HTTPS)
7. **kubectl describe pod** - mostra motivo de Pending
```

## Comandos Rapidos de Referencia

```bash
# === VERIFICACAO ===
crictl ps | grep scheduler
kubectl get pods -n kube-system | grep scheduler
kubectl logs -n kube-system kube-scheduler-<node>

# === LEADER ELECTION ===
kubectl get lease -n kube-system kube-scheduler -o yaml

# === DEBUG POD PENDING ===
kubectl describe pod <pod>
kubectl get events --field-selector reason=FailedScheduling

# === NODES ===
kubectl describe nodes | grep -A 5 "Allocated"
kubectl describe nodes | grep Taints
kubectl get nodes -o custom-columns=NAME:.metadata.name,TAINTS:.spec.taints

# === PRIORITY ===
kubectl get priorityclasses
kubectl describe priorityclass <name>

# === CONFIGURACAO ===
cat /etc/kubernetes/manifests/kube-scheduler.yaml
kubectl get cm -n kube-system | grep scheduler
```

## Referencias

- [kube-scheduler Reference](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-scheduler/)
- [Scheduler Configuration](https://kubernetes.io/docs/reference/scheduling/config/)
- [Scheduling Framework](https://kubernetes.io/docs/concepts/scheduling-eviction/scheduling-framework/)
- [Assigning Pods to Nodes](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)
- [Pod Priority and Preemption](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/)
- [Topology Spread Constraints](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/)
