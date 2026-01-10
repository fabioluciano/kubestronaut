# Monitoring

```admonish info title="Certificações"
CKA (30%), KCNA (8%)
```

## 📖 Conceitos

### Por que Monitorar

- Identificar problemas de performance
- Planejar capacidade
- Detectar anomalias
- Troubleshooting

### Métricas Importantes

| Recurso | Métricas | Alerta Típico |
|---------|----------|---------------|
| **CPU** | Uso, throttling | >80% por 5min |
| **Memória** | Uso, OOM kills | >85% |
| **Disco** | Uso, IOPS | >90% |
| **Rede** | Throughput, erros | Erros >0 |
| **Pods** | Restarts, pending | Restarts >3 |

## 🔧 Metrics Server

### O que é

Metrics Server é o agregador de métricas de recursos do cluster. Necessário para `kubectl top` e HPA.

### Instalação

```bash
# Instalar metrics server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Para ambientes de teste (sem TLS válido)
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Editar deployment para adicionar --kubelet-insecure-tls (se necessário)
kubectl edit deployment metrics-server -n kube-system
# Adicionar em args:
# - --kubelet-insecure-tls
```

### Verificar Instalação

```bash
# Verificar se está rodando
kubectl get pods -n kube-system | grep metrics-server

# Verificar API
kubectl get apiservices | grep metrics

# Testar
kubectl top nodes
kubectl top pods
```

## 🔧 Comandos kubectl top

### Monitorar Nodes

```bash
# CPU e memória de todos nodes
kubectl top nodes

# Saída exemplo:
# NAME     CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
# node-1   250m         12%    1024Mi          25%
# node-2   500m         25%    2048Mi          50%

# Ordenar por CPU
kubectl top nodes --sort-by=cpu

# Ordenar por memória
kubectl top nodes --sort-by=memory
```

### Monitorar Pods

```bash
# Todos pods do namespace atual
kubectl top pods

# Todos pods de todos namespaces
kubectl top pods -A

# Pods de namespace específico
kubectl top pods -n kube-system

# Ordenar por CPU
kubectl top pods --sort-by=cpu

# Ordenar por memória
kubectl top pods --sort-by=memory

# Ver métricas por container
kubectl top pods --containers

# Pod específico
kubectl top pod <pod-name>
```

### Exemplos Práticos

```bash
# Top 5 pods consumindo mais CPU
kubectl top pods -A --sort-by=cpu | head -6

# Top 5 pods consumindo mais memória
kubectl top pods -A --sort-by=memory | head -6

# Pods do kube-system ordenados
kubectl top pods -n kube-system --sort-by=cpu
```

## 🔧 Prometheus (KCNA)

### Arquitetura

```plantuml,format=png
!include ../assets/diagrams/observability/monitoring-arquitetura-prometheus.puml
```

### Conceitos Básicos

- **Scraping**: Prometheus coleta métricas dos targets
- **Exporters**: Expõem métricas no formato Prometheus
- **PromQL**: Linguagem de query
- **AlertManager**: Gerencia alertas

### Métricas Comuns do Kubernetes

```promql
# CPU por pod
container_cpu_usage_seconds_total

# Memória por pod
container_memory_usage_bytes

# Pods por status
kube_pod_status_phase

# Nodes disponíveis
kube_node_status_condition
```

## 💻 Exemplos Práticos

### Exemplo 1: Verificar Recursos do Cluster

```bash
# Ver capacidade vs uso dos nodes
kubectl describe nodes | grep -A 5 "Allocated resources"

# Ver requests e limits dos pods
kubectl get pods -o custom-columns="NAME:.metadata.name,CPU_REQ:.spec.containers[*].resources.requests.cpu,CPU_LIM:.spec.containers[*].resources.limits.cpu,MEM_REQ:.spec.containers[*].resources.requests.memory,MEM_LIM:.spec.containers[*].resources.limits.memory"
```

### Exemplo 2: Identificar Pods Problemáticos

```bash
# Pods com alto uso de CPU
kubectl top pods -A --sort-by=cpu | head -10

# Pods com muitos restarts
kubectl get pods -A -o wide | awk '$5 > 0 {print}'

# Pods não Running
kubectl get pods -A | grep -v Running
```

### Exemplo 3: Monitorar em Tempo Real

```bash
# Watch nodes
watch kubectl top nodes

# Watch pods
watch kubectl top pods

# Watch com ordenação
watch "kubectl top pods --sort-by=cpu"
```

## 🐛 Troubleshooting

### Problema: kubectl top retorna "metrics not available"

**Causa**: Metrics Server não instalado ou não funcionando

```bash
# Verificar se está rodando
kubectl get pods -n kube-system | grep metrics-server

# Ver logs
kubectl logs -n kube-system deployment/metrics-server

# Verificar se API está disponível
kubectl get apiservices | grep metrics
```

### Problema: Métricas zeradas ou incorretas

**Causa**: Metrics Server não consegue acessar kubelets

```bash
# Verificar conectividade
kubectl logs -n kube-system deployment/metrics-server

# Adicionar flag para ignorar TLS (lab/dev)
# --kubelet-insecure-tls
```

### Problema: metrics-server não inicia

```bash
# Ver eventos
kubectl describe pod -n kube-system metrics-server-xxx

# Causas comuns:
# - Certificados inválidos
# - Rede bloqueada
# - Recursos insuficientes
```

## 🎓 Dicas para o Exame

### CKA

```bash
# Comandos essenciais
kubectl top nodes
kubectl top pods
kubectl top pods --sort-by=cpu
kubectl top pods --sort-by=memory
kubectl top pods -A
```

### KCNA

Conceitos teóricos importantes:
- Prometheus é o padrão de monitoramento Cloud Native
- CNCF graduated project
- Pull-based (scraping)
- Métricas em formato texto
- PromQL para queries
- Integração com Grafana para visualização

## 🔗 Referências

### Documentação
- [Metrics Server](https://github.com/kubernetes-sigs/metrics-server)
- [Resource Metrics](https://kubernetes.io/docs/tasks/debug/debug-cluster/resource-metrics-pipeline/)
- [Prometheus](https://prometheus.io/docs/)

### Arquivos Relacionados
- [Observabilidade](observabilidade.md) - Probes e health checks
- [HorizontalPodAutoScaler](../workloads/horizontal-pod-autoscaler.md) - Auto-scaling baseado em métricas
- [ResourceQuota](../configuration/resource-quota.md) - Limites de recursos
- [LimitRange](../configuration/limit-range.md) - Limites por container
