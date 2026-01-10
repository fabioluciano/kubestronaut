# Observabilidade

## Conceitos Fundamentais

### Os Três Pilares da Observabilidade

A observabilidade é a capacidade de entender o estado interno de um sistema através de suas saídas externas. No contexto de Kubernetes, baseia-se em **três pilares**:

```plantuml,format=png
!include ../assets/diagrams/observability/observabilidade-três-pilares-da-observabilidade.puml
```

### Métricas vs Logs vs Traces

| Aspecto | Métricas | Logs | Traces |
|---------|----------|------|--------|
| **Formato** | Numérico | Texto/JSON | Spans hierárquicos |
| **Volume** | Baixo | Alto | Médio |
| **Uso** | Alertas, dashboards | Debug, auditoria | Análise de latência |
| **Retenção** | Longa (meses) | Média (semanas) | Curta (dias) |
| **Exemplo** | CPU: 80% | "Error: connection refused" | Request A → B → C |

---

## Pilar 1: Métricas

### Probes do Kubernetes

O Kubernetes fornece três tipos de probes para monitorar containers:

```yaml
{{#include ../assets/observabilidade/pod-with-probes.yaml}}
```

### Tipos de Probe

```yaml
{{#include ../assets/observabilidade/probe-types.yaml}}
```

### Configurações de Probe

| Parâmetro | Descrição | Default |
|-----------|-----------|---------|
| `initialDelaySeconds` | Tempo antes do primeiro probe | 0 |
| `periodSeconds` | Intervalo entre probes | 10 |
| `timeoutSeconds` | Timeout do probe | 1 |
| `successThreshold` | Sucessos para considerar OK | 1 |
| `failureThreshold` | Falhas para considerar NOK | 3 |

### Endpoints de Saúde do API Server

```bash
# Verificar saúde do cluster
curl -k https://$(kubectl config view -o jsonpath='{.clusters[0].cluster.server}')/healthz

# Saúde detalhada
curl -k https://<api-server>:6443/healthz?verbose

# Endpoints específicos
curl -k https://<api-server>:6443/livez   # API está viva
curl -k https://<api-server>:6443/readyz  # API pronta para tráfego
```

### Metrics Server

```bash
# Instalar Metrics Server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Verificar instalação
kubectl get deployment metrics-server -n kube-system

# Usar métricas
kubectl top nodes
kubectl top pods
kubectl top pods --containers
```

---

## Pilar 2: Logs

### Níveis de Logging

```plantuml,format=png
!include ../assets/diagrams/observability/observabilidade-níveis-de-log.puml
```

### Comandos de Log

```bash
# Logs básicos
kubectl logs <pod-name>
kubectl logs <pod-name> -c <container-name>

# Logs em tempo real
kubectl logs -f <pod-name>

# Últimas N linhas
kubectl logs --tail=100 <pod-name>

# Logs desde timestamp
kubectl logs --since=1h <pod-name>
kubectl logs --since-time="2024-01-01T00:00:00Z" <pod-name>

# Logs de pod anterior (após restart)
kubectl logs <pod-name> --previous

# Logs de todos os containers
kubectl logs <pod-name> --all-containers=true

# Logs por label
kubectl logs -l app=nginx --all-containers
```

### Stack EFK (Elasticsearch + Fluentd + Kibana)

```plantuml,format=png
!include ../assets/diagrams/observability/observabilidade-stack-efk.puml
```

### Loki (Alternativa Leve)

```yaml
{{#include ../assets/observabilidade/promtail-daemonset.yaml}}
```

---

## Pilar 3: Traces (Distributed Tracing)

### Conceitos de Tracing

```plantuml,format=png
!include ../assets/diagrams/observability/observabilidade-distributed-tracing.puml
```

### Ferramentas de Tracing

| Ferramenta | Descrição | CNCF Status |
|------------|-----------|-------------|
| **Jaeger** | Tracing distribuído | Graduated |
| **Zipkin** | Tracing distribuído (Twitter) | - |
| **Tempo** | Backend de traces (Grafana) | - |
| **OpenTelemetry** | Padrão unificado | Incubating |

### OpenTelemetry

```yaml
{{#include ../assets/observabilidade/otel-collector-configmap.yaml}}
```

---

## Prometheus e Grafana

### Arquitetura Prometheus

```plantuml,format=png
!include ../assets/diagrams/observability/observabilidade-prometheus-stack.puml
```

### ServiceMonitor (Prometheus Operator)

```yaml
{{#include ../assets/observabilidade/servicemonitor.yaml}}
```

### Queries PromQL Úteis

```promql
# CPU por pod
sum(rate(container_cpu_usage_seconds_total{namespace="default"}[5m])) by (pod)

# Memória por pod
sum(container_memory_usage_bytes{namespace="default"}) by (pod)

# Requisições por segundo
sum(rate(http_requests_total[5m])) by (service)

# Taxa de erro
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))

# Latência p99
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```

---

## Troubleshooting

### Probe Falha Constantemente

```bash
# Verificar eventos do pod
kubectl describe pod <pod-name>

# Testar endpoint manualmente
kubectl exec <pod-name> -- curl -s localhost:8080/healthz

# Verificar logs
kubectl logs <pod-name>

# Causas comuns:
# - initialDelaySeconds muito curto
# - App não implementa endpoint corretamente
# - Porta errada
```

### Sem Métricas no kubectl top

```bash
# Verificar Metrics Server
kubectl get pods -n kube-system | grep metrics

# Verificar logs
kubectl logs -n kube-system -l k8s-app=metrics-server

# Verificar API
kubectl get --raw /apis/metrics.k8s.io/v1beta1/nodes
```

---

## Dicas para os Exames

```plantuml,format=png
!include ../assets/diagrams/observability/observabilidade-dicas-observabilidade.puml
```

---

## Referências

- [Monitoring](monitoring.md)
- [HorizontalPodAutoScaler](../workloads/horizontal-pod-autoscaler.md)
- [Troubleshooting](../maintenance/troubleshooting.md)
- [Audit](../security/audit.md)
- [Pod](../workloads/pod.md)
