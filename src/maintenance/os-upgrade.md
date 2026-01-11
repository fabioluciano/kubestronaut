# Manutenção de Nodes

## Conceitos Fundamentais

### Pod Eviction Timeout

Se um node ficar **NotReady por mais de 5 minutos** (padrão), o controller-manager irá marcar os pods para eviction.

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName Monospaced

title POD EVICTION TIMEOUT

start
:Node fica NotReady;
:Aguarda pod-eviction-timeout\n(default: 5 minutos);
:Pods são marcados para eviction;
fork
  :Pods de ReplicaSet/Deployment:\nRecriados em outro node;
fork again
  :Pods standalone:\n**PERDIDOS!**;
end fork
stop

@enduml
```

### Drain vs Cordon vs Uncordon

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName Monospaced

title COMPARAÇÃO: DRAIN vs CORDON

rectangle "CORDON" as cordon
note right of cordon
  • Marca node como Unschedulable
  • Pods existentes continuam rodando
  • Novos pods NÃO são agendados no node
  
  **Usado para:** prevenir novos pods
  antes de manutenção
end note

rectangle "DRAIN" as drain
note right of drain
  • Marca node como Unschedulable (cordon)
  • MOVE pods existentes para outros nodes
  
  **Usado para:** manutenção que
  requer node vazio
end note

rectangle "UNCORDON" as uncordon
note right of uncordon
  • Marca node como Schedulable novamente
  • Permite novos pods serem agendados
  
  **Usado para:** após conclusão
  da manutenção
end note

cordon -down-> drain
drain -down-> uncordon

@enduml
```

---

## Comandos de Manutenção

### kubectl cordon

```bash
# Marcar node como unschedulable
kubectl cordon <node-name>

# Verificar status (mostra SchedulingDisabled)
kubectl get nodes
# NAME     STATUS                     ROLES    AGE   VERSION
# node-1   Ready,SchedulingDisabled   <none>   10d   v1.30.0

# Pods existentes continuam rodando
kubectl get pods -o wide
```

### kubectl drain

```bash
# Drain básico (pode falhar se houver pods problemáticos)
kubectl drain <node-name>

# Drain ignorando DaemonSets (recomendado)
kubectl drain <node-name> --ignore-daemonsets

# Drain forçando delete de pods com local storage
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data

# Drain forçando delete de pods standalone
kubectl drain <node-name> --ignore-daemonsets --force

# Drain com todas as flags (mais seguro para manutenção)
kubectl drain <node-name> \
  --ignore-daemonsets \
  --delete-emptydir-data \
  --force \
  --grace-period=30
```

### kubectl uncordon

```bash
# Retornar node ao scheduling normal
kubectl uncordon <node-name>

# Verificar status
kubectl get nodes
# NAME     STATUS   ROLES    AGE   VERSION
# node-1   Ready    <none>   10d   v1.30.0
```

---

## Flags do Drain

| Flag | Descrição |
|------|-----------|
| `--ignore-daemonsets` | Ignora pods de DaemonSets (eles não são evacuados) |
| `--delete-emptydir-data` | Deleta pods que usam emptyDir (dados locais perdidos) |
| `--force` | Força delete de pods não gerenciados por controllers |
| `--grace-period=<sec>` | Tempo para pods terminarem graciosamente |
| `--timeout=<duration>` | Tempo máximo para aguardar drain completar |
| `--dry-run` | Mostra o que seria feito sem executar |

---

## Cenários de Manutenção

### Cenário 1: Atualização do Sistema Operacional

```bash
# 1. Cordon para prevenir novos pods
kubectl cordon worker-1

# 2. Drain para mover pods existentes
kubectl drain worker-1 --ignore-daemonsets --delete-emptydir-data

# 3. SSH no node e fazer manutenção
ssh worker-1
sudo apt update && sudo apt upgrade -y
sudo reboot

# 4. Aguardar node voltar
kubectl get nodes
# Aguardar até STATUS = Ready,SchedulingDisabled

# 5. Uncordon para retomar scheduling
kubectl uncordon worker-1
```

### Cenário 2: Manutenção de Hardware

```bash
# 1. Drain com timeout maior para workloads pesados
kubectl drain worker-2 \
  --ignore-daemonsets \
  --delete-emptydir-data \
  --timeout=300s

# 2. Realizar manutenção física

# 3. Após node voltar online
kubectl uncordon worker-2
```

### Cenário 3: Substituição de Node

```bash
# 1. Drain completamente
kubectl drain old-worker --ignore-daemonsets --delete-emptydir-data --force

# 2. Remover node do cluster
kubectl delete node old-worker

# 3. No node (opcional): resetar kubeadm
ssh old-worker
sudo kubeadm reset

# 4. Adicionar novo node
# (no novo node)
kubeadm join <control-plane>:6443 --token <token> ...
```

---

## Tratando Erros Comuns no Drain

### Erro: Pods com Local Storage

```bash
# Erro:
# cannot delete Pods with local storage (volumes)

# Solução: Usar --delete-emptydir-data
kubectl drain <node> --ignore-daemonsets --delete-emptydir-data
```

### Erro: Pods Não Gerenciados

```bash
# Erro:
# cannot delete Pods not managed by ReplicationController, ReplicaSet, Job, DaemonSet or StatefulSet

# Solução: Usar --force (pods serão perdidos!)
kubectl drain <node> --ignore-daemonsets --force
```

### Erro: DaemonSet Pods

```bash
# Erro:
# cannot delete DaemonSet-managed Pods

# Solução: Usar --ignore-daemonsets
kubectl drain <node> --ignore-daemonsets
```

### Erro: PodDisruptionBudget

```bash
# Erro:
# Cannot evict pod as it would violate the pod's disruption budget

# Soluções:
# 1. Aguardar PDB ser satisfeito
# 2. Aumentar réplicas temporariamente
# 3. Usar --disable-eviction (cuidado!)
kubectl drain <node> --ignore-daemonsets --disable-eviction
```

---

## Pod Disruption Budget (PDB)

PDB protege aplicações durante operações de manutenção.

### Criar PDB

```yaml
{{#include ../assets/maintenance/pdb-app.yaml}}
```

### Verificar PDB

```bash
# Listar PDBs
kubectl get pdb

# Detalhes
kubectl describe pdb app-pdb
```

---

## Fluxo de Manutenção Seguro

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName Monospaced

title FLUXO DE MANUTENÇÃO SEGURO

start
:1. VERIFICAR ESTADO ATUAL\nkubectl get nodes\nkubectl get pods -o wide;
:2. VERIFICAR PDBs\nkubectl get pdb;
:3. CORDON (opcional, para planejamento)\nkubectl cordon <node>;
:4. DRAIN\nkubectl drain <node> --ignore-daemonsets;
:5. EXECUTAR MANUTENÇÃO\nssh <node>\n# ... manutenção ...;
:6. VERIFICAR NODE HEALTHY\nkubectl get nodes;
:7. UNCORDON\nkubectl uncordon <node>;
:8. VERIFICAR PODS RETORNARAM\nkubectl get pods -o wide;
stop

@enduml
```

---

## Comandos Úteis

```bash
# Ver status dos nodes
kubectl get nodes

# Ver pods em um node específico
kubectl get pods -A --field-selector spec.nodeName=<node>

# Ver eventos relacionados ao node
kubectl get events --field-selector involvedObject.name=<node>

# Verificar recursos do node
kubectl describe node <node> | grep -A 5 "Allocated resources"

# Ver taints do node
kubectl describe node <node> | grep Taints
```

---

## Dicas para o Exame CKA

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName Monospaced

rectangle "DICAS CKA - MANUTENÇÃO DE NODES" as main

rectangle "COMANDOS ESSENCIAIS" as cmds
note right of cmds
  **kubectl cordon <node>**
  → Marca unschedulable, pods existentes continuam
  
  **kubectl drain <node> --ignore-daemonsets**
  → Move pods E marca unschedulable
  
  **kubectl uncordon <node>**
  → Retorna ao normal
end note

rectangle "FLAGS IMPORTANTES DO DRAIN" as flags
note right of flags
  --ignore-daemonsets → Ignora DaemonSets
  --delete-emptydir-data → Deleta pods com emptyDir
  --force → Deleta pods não gerenciados
end note

rectangle "SEQUÊNCIA TÍPICA" as seq
note right of seq
  1. kubectl drain <node> --ignore-daemonsets
  2. Fazer manutenção
  3. kubectl uncordon <node>
end note

rectangle "LEMBRE-SE" as remember
note right of remember
  • drain = cordon + evict pods
  • DaemonSets não são drained (usam --ignore-daemonsets)
  • Pods standalone são perdidos com --force
end note

main -down-> cmds
cmds -down-> flags
flags -down-> seq
seq -down-> remember
@enduml
```

---

## Referências

- [Cluster Upgrade](cluster-upgrade.md)
- [Scheduling](../workloads/scheduling.md)
- [DaemonSet](../workloads/daemonset.md)
- [Troubleshooting](troubleshooting.md)
