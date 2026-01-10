# HorizontalPodAutoscaler (HPA)

## Conceitos Fundamentais

### O que é HPA?

O HorizontalPodAutoscaler ajusta automaticamente o número de réplicas de um Deployment, ReplicaSet ou StatefulSet baseado em métricas observadas.

```plantuml,format=png
!include ../assets/diagrams/workloads/horizontal-pod-autoscaler-como-o-hpa-funciona-1.puml
```

### Pré-requisitos

```bash
# Metrics Server é OBRIGATÓRIO para HPA com CPU/memória
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Verificar se está funcionando
kubectl get deployment metrics-server -n kube-system
kubectl top nodes
kubectl top pods
```

---

## Criando HPA

### Via kubectl (Forma Rápida)

```bash
# HPA básico com CPU
kubectl autoscale deployment nginx --cpu-percent=50 --min=1 --max=10

# HPA com memória (requer apiVersion v2)
kubectl autoscale deployment nginx --min=1 --max=10

# Verificar HPA criado
kubectl get hpa
kubectl describe hpa nginx
```

### Via YAML (API v2)

```yaml
{{#include ../assets/hpa/hpa-basic.yaml}}
```

### HPA com Múltiplas Métricas

```yaml
{{#include ../assets/hpa/hpa-multi-metric.yaml}}
```

---

## Tipos de Métricas

### Resource Metrics (CPU/Memória)

```yaml
{{#include ../assets/hpa/metrics-resource.yaml}}
```

### Pod Metrics (Custom)

```yaml
{{#include ../assets/hpa/metrics-pods.yaml}}
```

### Object Metrics

```yaml
{{#include ../assets/hpa/metrics-object.yaml}}
```

### External Metrics

```yaml
{{#include ../assets/hpa/metrics-external.yaml}}
```

---

## Comportamento de Scaling

### Configurar Behavior (v2)

```yaml
{{#include ../assets/hpa/hpa-behavior.yaml}}
```

### Desabilitar Scale Down

```yaml
{{#include ../assets/hpa/behavior-disable-scaledown.yaml}}
```

---

## Exemplos Práticos

### Exemplo 1: Deployment + HPA Completo

```yaml
{{#include ../assets/hpa/example-complete.yaml}}
```

### Exemplo 2: Testar HPA com Carga

```bash
# Aplicar recursos
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f hpa.yaml

# Verificar status
kubectl get hpa php-apache --watch

# Em outro terminal, gerar carga
kubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://php-apache; done"

# Observar scaling
# TARGETS mostrará CPU atual / target
# REPLICAS aumentará automaticamente
```

### Exemplo 3: HPA para API com Requests

```yaml
{{#include ../assets/hpa/hpa-api-requests.yaml}}
```

---

## Comandos Úteis

```bash
# Criar HPA rapidamente
kubectl autoscale deployment <name> --cpu-percent=50 --min=1 --max=10

# Listar HPAs
kubectl get hpa
kubectl get hpa -A  # todos namespaces

# Ver detalhes
kubectl describe hpa <name>

# Monitorar em tempo real
kubectl get hpa <name> --watch

# Ver métricas raw
kubectl get --raw /apis/metrics.k8s.io/v1beta1/pods

# Ver eventos relacionados
kubectl get events --field-selector involvedObject.kind=HorizontalPodAutoscaler

# Deletar HPA
kubectl delete hpa <name>
```

---

## Troubleshooting

### HPA Mostra "unknown" ou "<unknown>"

```bash
# Problema: Metrics Server não instalado ou não funcionando
kubectl get deployment metrics-server -n kube-system

# Verificar se métricas estão disponíveis
kubectl top pods

# Se usando minikube
minikube addons enable metrics-server

# Verificar logs do Metrics Server
kubectl logs -n kube-system -l k8s-app=metrics-server
```

### HPA Não Escala

```bash
# Verificar se requests estão definidos no container
kubectl get deployment <name> -o yaml | grep -A5 resources

# Problema comum: requests não definidos
# Solução: Adicionar resources.requests ao container

# Verificar eventos do HPA
kubectl describe hpa <name>

# Verificar se target está correto
kubectl get hpa <name> -o yaml | grep scaleTargetRef -A3
```

### Scale Down Muito Lento

```yaml
{{#include ../assets/hpa/behavior-scaledown-fast.yaml}}
```

### Oscilação (Thrashing)

```yaml
{{#include ../assets/hpa/behavior-anti-thrashing.yaml}}
```

---

## HPA vs VPA vs Cluster Autoscaler

```plantuml,format=png
!include ../assets/diagrams/workloads/horizontal-pod-autoscaler-tipos-de-autoscaling-1.puml
```

---

## Dicas para os Exames

```plantuml,format=png
!include ../assets/diagrams/workloads/horizontal-pod-autoscaler-dicas-hpa-exames-1.puml
```

---

## Referências

- [Monitoring](../observability/monitoring.md)
- [Observabilidade](../observability/observabilidade.md)
- [Deployment](deployment.md)
- [ResourceQuota](../configuration/resource-quota.md)
- [LimitRange](../configuration/limit-range.md)
