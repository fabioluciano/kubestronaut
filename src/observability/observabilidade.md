# Observabilidade

## Conceitos Fundamentais

### Os Três Pilares da Observabilidade

A observabilidade é a capacidade de entender o estado interno de um sistema através de suas saídas externas. No contexto de Kubernetes, baseia-se em **três pilares**:

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title TRÊS PILARES DA OBSERVABILIDADE

rectangle "MÉTRICAS" as metricas {
  note as nmetricas
    Números que
    representam
    estado
    ----
    Prometheus
    Grafana
  end note
}

rectangle "LOGS" as logs {
  note as nlogs
    Eventos
    discretos
    textuais
    ----
    Loki/EFK
    Fluentd
  end note
}

rectangle "TRACES" as traces {
  note as ntraces
    Caminho de
    uma request
    distribuída
    ----
    Jaeger/Zipkin
    Tempo
  end note
}

metricas -[hidden]right-> logs
logs -[hidden]right-> traces

@enduml
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
@startuml
skinparam monochrome true
skinparam backgroundColor white

title NÍVEIS DE LOG

rectangle "Container" as container
rectangle "Pod" as pod
rectangle "Node" as node
rectangle "Cluster" as cluster

container --> pod
pod --> node
node --> cluster

note bottom of container
  1. Container Logs (stdout/stderr)
     kubectl logs <pod>
end note

note bottom of node
  2. Node Logs (/var/log/)
     - kubelet.log
     - kube-proxy.log
     - container runtime logs
end note

note bottom of cluster
  3. Control Plane Logs
     - /var/log/kube-apiserver.log
     - /var/log/kube-scheduler.log
     - /var/log/kube-controller-manager.log
end note

@enduml
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
@startuml
skinparam monochrome true
skinparam backgroundColor white

title STACK EFK

rectangle "Pods\nstdout" as pods
rectangle "Fluentd\n(DaemonSet)" as fluentd
rectangle "Elasticsearch\n(Index)" as elastic
rectangle "Kibana\n(UI)" as kibana

pods --> fluentd : Coleta
fluentd --> elastic : Processa
elastic --> kibana : Armazena

note bottom of kibana : Visualiza

@enduml
```

### Loki (Alternativa Leve)

```yaml
{{#include ../assets/observabilidade/promtail-daemonset.yaml}}
```

---

## Pilar 3: Traces (Distributed Tracing)

### Conceitos de Tracing

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title DISTRIBUTED TRACING

note as intro
  Trace: Jornada completa de uma requisição
end note

rectangle "Trace ID: abc123" as trace {
  rectangle "Span: Frontend (50ms)" as frontend {
    rectangle "Span: API Gateway (45ms)" as gateway {
      rectangle "Span: Auth Service (10ms)" as auth
      rectangle "Span: Product Service (30ms)" as product {
        rectangle "Span: Database (20ms)" as db
      }
    }
  }
}

note bottom of trace
  Cada Span contém: nome, duração, tags, logs, baggage
end note

@enduml
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
@startuml
skinparam monochrome true
skinparam backgroundColor white

title PROMETHEUS STACK

rectangle "Targets\n/metrics" as targets
rectangle "Prometheus\n(TSDB)" as prometheus
rectangle "AlertManager" as alertmgr
rectangle "Slack / Email" as notify
rectangle "Grafana\n(Dashboards)" as grafana

targets --> prometheus
prometheus --> alertmgr
alertmgr --> notify
prometheus --> grafana

@enduml
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
@startuml
skinparam monochrome true
skinparam backgroundColor white

title DICAS - OBSERVABILIDADE

rectangle "KCNA" as kcna {
  note as nkcna
    • Conhecer os 3 pilares (métricas, logs, traces)
    • Prometheus é CNCF Graduated
    • OpenTelemetry é o padrão unificado
  end note
}

rectangle "CKA" as cka {
  note as ncka
    • kubectl logs (com -f, --previous, --tail)
    • kubectl top nodes/pods
    • Instalar Metrics Server
  end note
}

rectangle "CKAD" as ckad {
  note as nckad
    • Configurar livenessProbe e readinessProbe
    • Diferença entre os três tipos de probe
    • Ajustar initialDelaySeconds e periodSeconds
  end note
}

rectangle "CKS" as cks {
  note as ncks
    • Audit logs para segurança
    • Falco para detecção de anomalias
  end note
}

kcna -[hidden]down-> cka
cka -[hidden]down-> ckad
ckad -[hidden]down-> cks

@enduml
```

---

## Referências

- [Monitoring](monitoring.md)
- [HorizontalPodAutoScaler](../workloads/horizontal-pod-autoscaler.md)
- [Troubleshooting](../maintenance/troubleshooting.md)
- [Audit](../security/audit.md)
- [Pod](../workloads/pod.md)
