# DaemonSet

```admonish info title="Certificações"
CKA (15%), CKAD (5%), CKS (10%)
```

## Conceitos Fundamentais

### O que é DaemonSet

DaemonSet garante que todos (ou alguns) Nodes executem uma cópia de um Pod. À medida que Nodes são adicionados ao cluster, Pods são automaticamente criados neles.

```plantuml,format=png
!include ../assets/diagrams/workloads/daemonset-daemonset-controller-1.puml
```

### Casos de Uso Típicos

| Caso de Uso | Exemplo |
|-------------|---------|
| **Logging** | Fluentd, Filebeat |
| **Monitoring** | Prometheus Node Exporter, Datadog Agent |
| **Networking** | CNI plugins (Calico, Cilium, Weave) |
| **Storage** | Ceph, GlusterFS |
| **Security** | Falco, Aqua Agent |

### DaemonSet vs Deployment vs ReplicaSet

| Característica | DaemonSet | Deployment/ReplicaSet |
|----------------|-----------|----------------------|
| **Réplicas** | 1 por Node | N definido |
| **Escalonamento** | Automático (por Node) | Manual |
| **Scheduling** | Em todos os Nodes | Baseado em scheduler |
| **Propósito** | Agentes por Node | Aplicações |

---

## Comandos Essenciais

### Gerenciar DaemonSets

```bash
# Listar DaemonSets
kubectl get daemonsets
kubectl get ds          # forma curta

# Listar com detalhes
kubectl get ds -o wide

# Ver DaemonSets em todos os namespaces
kubectl get ds -A

# Descrever DaemonSet
kubectl describe ds <name>

# Ver YAML
kubectl get ds <name> -o yaml
```

### Criar DaemonSets

```bash
# Não existe comando kubectl create direto para DaemonSet
# Criar via Deployment e converter:
kubectl create deployment test --image=nginx --dry-run=client -o yaml > ds.yaml
# Depois editar: kind: DaemonSet, remover spec.replicas e spec.strategy

# Criar via arquivo
kubectl apply -f daemonset.yaml
```

### Atualizar DaemonSets

```bash
# Editar DaemonSet
kubectl edit ds <name>

# Atualizar imagem
kubectl set image ds/<name> <container>=<image>

# Rollback
kubectl rollout undo ds/<name>

# Ver histórico
kubectl rollout history ds/<name>

# Ver status do rollout
kubectl rollout status ds/<name>
```

### Deletar DaemonSets

```bash
# Deletar DaemonSet (e seus Pods)
kubectl delete ds <name>

# Deletar mantendo Pods
kubectl delete ds <name> --cascade=orphan

# Deletar por arquivo
kubectl delete -f daemonset.yaml
```

---

## Exemplos Práticos


### DaemonSet Básico

```yaml
{{#include ../assets/daemonset/daemonset-test.yaml}}
```
### DaemonSet Básico

```yaml
{{#include ../assets/daemonset/logging-agent.yaml}}
```

### DaemonSet com nodeSelector

Executar apenas em Nodes específicos:

```yaml
{{#include ../assets/daemonset/gpu-monitor.yaml}}
```

```bash
# Adicionar label ao Node
kubectl label nodes worker-1 gpu=true

# Verificar
kubectl get nodes --show-labels | grep gpu
```

### DaemonSet com Tolerations (Rodar no Control Plane)

```yaml
{{#include ../assets/daemonset/monitoring-agent.yaml}}
```

### DaemonSet com Node Affinity

```yaml
{{#include ../assets/daemonset/ssd-agent.yaml}}
```

### DaemonSet com hostNetwork

```yaml
{{#include ../assets/daemonset/network-monitor.yaml}}
```

### DaemonSet para Prometheus Node Exporter

```yaml
{{#include ../assets/daemonset/node-exporter.yaml}}
```

### DaemonSet com UpdateStrategy

```yaml
{{#include ../assets/daemonset/fluentd-update-strategy.yaml}}
```

### Update Strategies

| Strategy | Descrição |
|----------|-----------|
| `RollingUpdate` (default) | Atualiza Pods um por vez |
| `OnDelete` | Só atualiza quando Pod é deletado manualmente |

---

## DaemonSet e Taints/Tolerations

```plantuml,format=png
!include ../assets/diagrams/workloads/daemonset-daemonset-com-taints-1.puml
```

### Taints Comuns do Sistema

```yaml
{{#include ../assets/daemonset/tolerations-sistema.yaml}}
```

---

## Troubleshooting

### Problema: Pod Não Está Sendo Criado em um Node

```bash
# Verificar status do DaemonSet
kubectl get ds <name>

# Output:
# NAME     DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   AGE
# fluentd  3         2         2       2            2           5m

# DESIRED != CURRENT indica problema

# Verificar eventos
kubectl describe ds <name>

# Verificar taints do Node
kubectl describe node <node-name> | grep -A5 Taints

# Verificar se DaemonSet tem tolerations adequadas
kubectl get ds <name> -o jsonpath='{.spec.template.spec.tolerations}'
```

### Problema: Pod em CrashLoopBackOff

```bash
# Ver pods do DaemonSet
kubectl get pods -l app=<daemonset-label> -o wide

# Ver logs
kubectl logs <pod-name>
kubectl logs <pod-name> --previous

# Verificar recursos
kubectl describe pod <pod-name>
```

### Problema: Update Não Acontece

```bash
# Verificar updateStrategy
kubectl get ds <name> -o jsonpath='{.spec.updateStrategy.type}'

# Se OnDelete, deletar pods manualmente
kubectl delete pod <pod-name>

# Verificar status do rollout
kubectl rollout status ds/<name>
```

### Verificar Cobertura do DaemonSet

```bash
# Ver em quais Nodes tem pods
kubectl get pods -l app=<label> -o wide

# Comparar com total de Nodes
kubectl get nodes

# Ver status detalhado
kubectl get ds <name> -o jsonpath='{.status}'
```

---

## Dicas para o Exame

### CKA

```admonish tip title="Dicas CKA"
1. **Criar DaemonSet a partir de Deployment**:
   ```bash
   kubectl create deployment test --image=nginx --dry-run=client -o yaml | \
     sed 's/Deployment/DaemonSet/; /replicas/d; /strategy/d' > ds.yaml
   ```

2. **Rodar em Control Plane**: Adicionar tolerations para taints do control plane

3. **nodeSelector vs tolerations**:
   - `nodeSelector`: escolhe ONDE rodar
   - `tolerations`: permite rodar em Nodes com taints

4. **UpdateStrategy**: `RollingUpdate` ou `OnDelete`
```

### CKS

```admonish tip title="Dicas CKS"
1. **DaemonSets de segurança**: Falco, security agents

2. **Cuidado com privileges**:
   - `hostNetwork: true`
   - `hostPID: true`
   - `privileged: true`

3. **Verificar DaemonSets em namespaces do sistema**:
   ```bash
   kubectl get ds -n kube-system
   ```
```

### CKAD

```admonish tip title="Dicas CKAD"
1. **Não confundir com Deployment**: DaemonSet não tem `replicas`

2. **Template é idêntico a outros controllers**: `spec.template.spec`
```

### Comandos Úteis para o Exame

```bash
# Ver todos DaemonSets
kubectl get ds -A

# Criar via conversão de Deployment (manual)
kubectl create deployment test --image=nginx --dry-run=client -o yaml > ds.yaml
# Editar: kind: DaemonSet, remover replicas e strategy

# Ver status
kubectl get ds <name>

# Atualizar imagem
kubectl set image ds/<name> <container>=<new-image>

# Rollback
kubectl rollout undo ds/<name>

# Ver pods do DaemonSet por Node
kubectl get pods -l app=<label> -o wide
```

### Template Rápido para DaemonSet

```yaml
{{#include ../assets/daemonset/template-rapido.yaml}}
```

---

## Referências

- [Kubernetes - DaemonSet](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/)
- [Kubernetes - Taints and Tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)
- [Kubernetes - Node Affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)

### Arquivos Relacionados

- [Scheduling](scheduling.md) - Agendamento de Pods
- [Taints e Tolerations](scheduling.md#taints-e-tolerations) - Controle de scheduling
- [ReplicaSet](replicaset.md) - Comparação com ReplicaSet
- [Monitoring Logging](../security/monitoring-logging.md) - Casos de uso de DaemonSets
