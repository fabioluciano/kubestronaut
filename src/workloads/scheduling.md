# Scheduling no Kubernetes

## Conceitos Fundamentais

### Como Funciona o Scheduling

O kube-scheduler decide em qual Node cada Pod será executado, seguindo um processo de múltiplas etapas.

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title FLUXO DO SCHEDULER

|Scheduler|
start

:1. QUEUE (Fila);
note right: Pods ordenados por PriorityClass

:2. FILTER (Filtrar);
note right
  Remove nodes que não atendem requisitos
  Taints, resources, nodeSelector, affinity
end note

:3. SCORE (Pontuar);
note right
  Dá nota aos nodes restantes
  Spread, resource balance, affinity weight
end note

:4. BIND (Vincular);
note right: Associa Pod ao Node com maior score

stop

@enduml
```

### Mecanismos de Scheduling

| Mecanismo | Propósito | Escopo |
|-----------|-----------|--------|
| **nodeName** | Forçar node específico | Absoluto |
| **nodeSelector** | Selecionar por labels | Simples |
| **nodeAffinity** | Regras avançadas de node | Flexível |
| **podAffinity** | Co-localizar com pods | Inter-pod |
| **podAntiAffinity** | Separar de pods | Inter-pod |
| **taints/tolerations** | Restringir nodes | Repulsão |
| **topologySpread** | Distribuir uniformemente | Zonas/Nodes |

---

## nodeName (Scheduling Manual)

### Uso Básico

Especifica diretamente o Node - **bypassa o scheduler**.

```yaml
{{#include ../assets/scheduling/pod-manual-schedule.yaml}}
```

```admonish warning title="Limitações"
• Só funciona na criação do Pod
• Não pode ser editado depois
• Ignora taints, resources, affinity
• Se o node não existir, Pod fica Pending eternamente
```

---

## nodeSelector


### Pod com nodeSelector

```yaml
{{#include ../assets/pod/pod-with-nodeselector.yaml}}
```
### Conceito

Seleciona nodes baseado em labels. Método mais simples.

```bash
# Adicionar label ao node
kubectl label nodes worker-1 disk=ssd

# Remover label
kubectl label nodes worker-1 disk-

# Ver labels
kubectl get nodes --show-labels
```

### Usar nodeSelector

```yaml
{{#include ../assets/scheduling/pod-nodeselector.yaml}}
```

---

## Node Affinity



### Deployment com PreferredDuringScheduling

```yaml
{{#include ../assets/pod/deploy-with-nodeaffinity-preferred.yaml}}
```
### Deployment com RequiredDuringScheduling

```yaml
{{#include ../assets/pod/deploy-with-nodeaffinity-required.yaml}}
```
### Tipos de Affinity

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title NODE AFFINITY TYPES

rectangle "requiredDuringSchedulingIgnoredDuringExecution" {
  note as n1
    OBRIGATÓRIO: Pod só é scheduled se regra for satisfeita
    Se nenhum node atende, Pod fica Pending
  end note
}

rectangle "preferredDuringSchedulingIgnoredDuringExecution" {
  note as n2
    PREFERÊNCIA: Scheduler tenta, mas não é obrigatório
    Se nenhum node atende, agenda em qualquer um
    weight (1-100) define prioridade entre preferências
  end note
}

rectangle "IgnoredDuringExecution" {
  note as n3
    Se labels mudarem após scheduling,
    Pod NÃO é removido
  end note
}

@enduml
```

### Required (Obrigatório)

```yaml
{{#include ../assets/scheduling/pod-affinity-required.yaml}}
```

### Preferred (Preferência)

```yaml
{{#include ../assets/scheduling/pod-affinity-preferred.yaml}}
```

### Operadores

| Operador | Descrição |
|----------|-----------|
| `In` | Valor está na lista |
| `NotIn` | Valor não está na lista |
| `Exists` | Label existe (qualquer valor) |
| `DoesNotExist` | Label não existe |
| `Gt` | Maior que (numérico) |
| `Lt` | Menor que (numérico) |

---

## Taints e Tolerations

### Conceito

**Taints** repelem Pods de Nodes. **Tolerations** permitem que Pods ignorem Taints.

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title TAINTS E TOLERATIONS

rectangle "TAINT (no Node)" as taint
note right of taint
  Não aceito pods sem
  esta toleração
end note

rectangle "TOLERATION (no Pod)" as toleration
note right of toleration
  Eu tolero esse taint,
  pode me colocar aqui
end note

rectangle "Node\ntaint: app=blue\nNoSchedule" as node1
rectangle "Pod\ntoleration: app=blue" as pod1
node1 <-- pod1 : ✓ Aceito

rectangle "Node\ntaint: app=blue\nNoSchedule" as node2
rectangle "Pod\n(sem toleration)" as pod2
node2 <-[#red]- pod2 : ✗ Rejeitado

@enduml
```

### Efeitos de Taint

| Efeito | Comportamento |
|--------|---------------|
| `NoSchedule` | Novos pods sem toleration não são agendados |
| `PreferNoSchedule` | Scheduler tenta evitar, mas pode agendar |
| `NoExecute` | Pods existentes sem toleration são removidos |

### Comandos Taint

```bash
# Adicionar taint
kubectl taint nodes worker-1 app=blue:NoSchedule

# Remover taint (note o - no final)
kubectl taint nodes worker-1 app=blue:NoSchedule-

# Ver taints
kubectl describe node worker-1 | grep Taints

# Taint especial do control plane
kubectl describe node master | grep Taints
# node-role.kubernetes.io/control-plane:NoSchedule
```

### Toleration no Pod

```yaml
{{#include ../assets/scheduling/pod-tolerations.yaml}}
```

### tolerationSeconds (NoExecute)

```yaml
{{#include ../assets/workloads/scheduling-example-1.yaml}}
```

---

## Pod Affinity e Anti-Affinity

### Pod Affinity (Co-localizar)

```yaml
{{#include ../assets/scheduling/pod-affinity.yaml}}
```

### Pod Anti-Affinity (Separar)

```yaml
{{#include ../assets/scheduling/deployment-antiaffinity.yaml}}
```

### topologyKey

| topologyKey | Escopo |
|-------------|--------|
| `kubernetes.io/hostname` | Mesmo node |
| `topology.kubernetes.io/zone` | Mesma zona |
| `topology.kubernetes.io/region` | Mesma região |

---

## Topology Spread Constraints

### Distribuição Uniforme

```yaml
{{#include ../assets/scheduling/deployment-topology-spread.yaml}}
```

---

## Combinando Taints + Affinity

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title GARANTIR POD EM NODE ESPECÍFICO

rectangle "PROBLEMA" {
  card "Toleration permite ir para o node, mas não garante" as p1
  card "nodeAffinity garante ir para o node, mas não impede outros" as p2
}

rectangle "SOLUÇÃO: Usar AMBOS!" {
  rectangle "1. No NODE" {
    card "Taint: dedicated=database:NoSchedule" as n1
    card "Label: dedicated=database" as n2
  }
  
  rectangle "2. No POD" {
    card "Toleration: dedicated=database" as pod1
    card "nodeAffinity: dedicated=database" as pod2
  }
}

note bottom
  Resultado: Pod VAI para o node E outros pods NÃO VÃO
end note

@enduml
```

```yaml
{{#include ../assets/scheduling/pod-database-dedicated.yaml}}
```

---

## Priority e Preemption

### PriorityClass

```yaml
{{#include ../assets/scheduling/priorityclass.yaml}}
```

### Usar no Pod

```yaml
{{#include ../assets/scheduling/pod-priority.yaml}}
```

---

## Troubleshooting

### Pod Pending

```bash
# Ver eventos
kubectl describe pod <pod-name>

# Causas comuns:
# - Insufficient resources
# - No nodes match nodeSelector
# - Taints não tolerados
# - Affinity não satisfeita

# Ver recursos disponíveis
kubectl describe nodes | grep -A5 "Allocated resources"
```

### Verificar Scheduling

```bash
# Ver em qual node o pod está
kubectl get pod -o wide

# Ver eventos de scheduling
kubectl get events --field-selector reason=FailedScheduling
```

---

## Dicas para os Exames

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title DICAS - SCHEDULING

rectangle "CKA" {
  card "kubectl taint nodes <node> key=value:effect" as c1
  card "kubectl label nodes <node> key=value" as c2
  card "Combinar taints + affinity para dedicar nodes" as c3
}

rectangle "CKAD" {
  card "nodeSelector é mais simples que affinity" as k1
  card "podAntiAffinity para HA (um pod por node)" as k2
}

rectangle "IMPORTANTE" {
  card "Toleration permite ir, mas NÃO garante" as i1
  card "Affinity garante ir, mas NÃO impede outros" as i2
  card "Para dedicar: use AMBOS" as i3
  card "required = obrigatório, Pod fica Pending se não atender" as i4
  card "preferred = tenta, mas agenda em qualquer lugar se precisar" as i5
}

@enduml
```

---

## Referências

- [kube-scheduler](../cluster-components/kube-scheduler.md)
- [High Availability](fundamentals/high-availability.md)
- [DaemonSet](daemonset.md)
- [StatefulSet](statefulset.md)
- [Pod](pod.md)


---

### Pod com Tolerations

```yaml
{{#include ../assets/pod/pod-with-toleration.yaml}}
```
