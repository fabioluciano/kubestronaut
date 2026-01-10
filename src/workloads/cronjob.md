# CronJobs

```admonish info title="Certificações"
CKAD (15%), CKA (10%)
```

## Conceitos Fundamentais

### O que são CronJobs

CronJobs são recursos para executar Jobs em horários agendados, seguindo a sintaxe cron do Unix. É um wrapper que cria Jobs automaticamente baseado em um schedule.

```plantuml,format=png
!include ../assets/diagrams/workloads/cronjob-cronjob-controller-1.puml
```

### Hierarquia de Objetos

```plantuml,format=png
!include ../assets/diagrams/workloads/cronjob-hierarquia-de-objetos-cronjob-1.puml
```

### Sintaxe Cron

```plantuml,format=png
!include ../assets/diagrams/workloads/cronjob-sintaxe-cron-1.puml
```

### Exemplos de Schedule

| Schedule | Descrição |
|----------|-----------|
| `* * * * *` | A cada minuto |
| `*/5 * * * *` | A cada 5 minutos |
| `0 * * * *` | A cada hora (minuto 0) |
| `0 0 * * *` | Todo dia à meia-noite |
| `0 2 * * *` | Todo dia às 2:00 |
| `0 0 * * 0` | Todo domingo à meia-noite |
| `0 0 1 * *` | Primeiro dia do mês |
| `0 0 1 1 *` | Primeiro dia do ano |
| `30 4 1,15 * *` | Dias 1 e 15 às 4:30 |
| `0 9-17 * * 1-5` | Dias úteis das 9h às 17h |


### CronJob Date

```yaml
{{#include ../assets/cronjob/cronjob-date.yaml}}
```
---

## Comandos Essenciais

### Criar CronJobs

```bash
# Criar CronJob simples
kubectl create cronjob <name> --image=<image> --schedule="* * * * *" -- <command>

# Exemplo: rodar date a cada minuto
kubectl create cronjob date-cron --image=busybox --schedule="*/1 * * * *" -- date

# Criar com dry-run
kubectl create cronjob my-cron --image=busybox --schedule="0 * * * *" \
  --dry-run=client -o yaml -- echo "hourly job" > cronjob.yaml

# Criar via arquivo
kubectl apply -f cronjob.yaml
```

### Gerenciar CronJobs

```bash
# Listar CronJobs
kubectl get cronjobs
kubectl get cj        # forma curta

# Listar com detalhes
kubectl get cj -o wide

# Descrever CronJob
kubectl describe cj <name>

# Ver YAML
kubectl get cj <name> -o yaml

# Editar CronJob
kubectl edit cj <name>
```

### Monitorar CronJobs

```bash
# Ver status do CronJob
kubectl get cj <name>

# Output:
# NAME        SCHEDULE      SUSPEND   ACTIVE   LAST SCHEDULE   AGE
# date-cron   */1 * * * *   False     0        45s             5m

# Ver Jobs criados pelo CronJob
kubectl get jobs -l job-name=<cronjob-name>

# Ver todos os recursos relacionados
kubectl get cj,jobs,pods

# Ver último job executado
kubectl get jobs --sort-by=.status.startTime | tail -1
```

### Executar Job Manualmente

```bash
# Criar Job a partir do CronJob (execução imediata)
kubectl create job <job-name> --from=cronjob/<cronjob-name>

# Exemplo
kubectl create job manual-backup --from=cronjob/db-backup
```

### Suspender/Resumir CronJob

```bash
# Suspender CronJob (para de criar novos Jobs)
kubectl patch cronjob <name> -p '{"spec":{"suspend":true}}'

# Resumir CronJob
kubectl patch cronjob <name> -p '{"spec":{"suspend":false}}'

# Verificar status
kubectl get cj <name>
```

### Deletar CronJobs

```bash
# Deletar CronJob (e Jobs/Pods associados)
kubectl delete cj <name>

# Deletar por arquivo
kubectl delete -f cronjob.yaml

# Deletar mantendo Jobs existentes
kubectl delete cj <name> --cascade=orphan
```

---

## Exemplos Práticos

### CronJob Básico

```yaml
{{#include ../assets/cronjob/hello-cron.yaml}}
```

### CronJob com TimeZone

```yaml
{{#include ../assets/cronjob/timezone-cron.yaml}}
```

### CronJob com Concurrency Policy

```yaml
{{#include ../assets/cronjob/concurrent-cron.yaml}}
```

### Políticas de Concorrência

| Policy | Comportamento |
|--------|---------------|
| `Allow` (default) | Permite múltiplos Jobs simultâneos |
| `Forbid` | Pula execução se Job anterior ainda rodando |
| `Replace` | Cancela Job atual e inicia novo |

### CronJob com Histórico

```yaml
{{#include ../assets/cronjob/history-cron.yaml}}
```

### CronJob com Starting Deadline

```yaml
{{#include ../assets/cronjob/deadline-cron.yaml}}
```

### CronJob de Backup de Banco de Dados

```yaml
{{#include ../assets/cronjob/db-backup-cron.yaml}}
```

### CronJob de Limpeza

```yaml
{{#include ../assets/cronjob/cleanup-cron.yaml}}
```

### CronJob com ServiceAccount

```yaml
{{#include ../assets/cronjob/k8s-cleanup-cron.yaml}}
```

---

## Campos Importantes

```plaintext
┌─────────────────────────────────────────────────────────────────┐
│                    CAMPOS DO CRONJOB                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  spec.schedule: "*/5 * * * *"                                  │
│  └── Expressão cron (obrigatório)                              │
│                                                                 │
│  spec.timeZone: "America/Sao_Paulo"                            │
│  └── Timezone para schedule (default: timezone do controller)  │
│                                                                 │
│  spec.concurrencyPolicy: Allow | Forbid | Replace              │
│  └── Como lidar com execuções simultâneas                      │
│                                                                 │
│  spec.suspend: true | false                                     │
│  └── Pausar CronJob                                             │
│                                                                 │
│  spec.successfulJobsHistoryLimit: 3                            │
│  └── Jobs bem-sucedidos a manter (default: 3)                  │
│                                                                 │
│  spec.failedJobsHistoryLimit: 1                                │
│  └── Jobs falhos a manter (default: 1)                         │
│                                                                 │
│  spec.startingDeadlineSeconds: 200                             │
│  └── Segundos de atraso tolerados                              │
│                                                                 │
│  spec.jobTemplate: {...}                                        │
│  └── Template do Job (spec do Job dentro)                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Troubleshooting

### Problema: CronJob Não Está Criando Jobs

```bash
# Verificar status do CronJob
kubectl get cj <name>

# Verificar se está suspenso
kubectl get cj <name> -o jsonpath='{.spec.suspend}'

# Verificar schedule
kubectl get cj <name> -o jsonpath='{.spec.schedule}'

# Verificar eventos
kubectl describe cj <name>

# Verificar controller
kubectl get pods -n kube-system | grep cronjob
```

### Problema: Jobs Estão Falhando

```bash
# Ver Jobs do CronJob
kubectl get jobs -l cronjob-name=<name>

# Ver logs do último Job
kubectl logs job/<job-name>

# Ver pods do Job
kubectl get pods -l job-name=<job-name>

# Verificar eventos
kubectl describe job <job-name>
```

### Problema: Jobs Executando Simultaneamente

```bash
# Verificar concurrencyPolicy
kubectl get cj <name> -o jsonpath='{.spec.concurrencyPolicy}'

# Se precisar evitar concorrência:
kubectl patch cj <name> -p '{"spec":{"concurrencyPolicy":"Forbid"}}'
```

### Problema: Jobs Não Estão Sendo Limpos

```bash
# Verificar limites de histórico
kubectl get cj <name> -o jsonpath='{.spec.successfulJobsHistoryLimit}'
kubectl get cj <name> -o jsonpath='{.spec.failedJobsHistoryLimit}'

# Limpar manualmente Jobs antigos
kubectl delete jobs -l cronjob-name=<name>
```

### Problema: Timezone Incorreto

```bash
# Verificar timezone configurado
kubectl get cj <name> -o jsonpath='{.spec.timeZone}'

# Se não configurado, usa timezone do kube-controller-manager
# Verificar timezone do controller
kubectl exec -n kube-system <controller-pod> -- date
```

---

## Dicas para o Exame

### CKAD

```admonish tip title="Dicas CKAD"
1. **Criar CronJob rápido**:
   ```bash
   kubectl create cronjob test --image=busybox --schedule="*/1 * * * *" -- date
   ```

2. **Executar Job imediato**:
   ```bash
   kubectl create job manual --from=cronjob/<name>
   ```

3. **Memorizar sintaxe cron**:
   - `* * * * *` = minuto hora dia mês dia-semana
   - `*/5` = a cada 5 unidades

4. **concurrencyPolicy**:
   - `Forbid` = não executa se anterior ainda rodando
   - `Replace` = cancela anterior e inicia novo
```

### CKA

```admonish tip title="Dicas CKA"
1. **Suspender CronJob**:
   ```bash
   kubectl patch cj <name> -p '{"spec":{"suspend":true}}'
   ```

2. **Histórico de Jobs**: Ajustar `successfulJobsHistoryLimit` e `failedJobsHistoryLimit`

3. **Debugging**: Verificar Jobs criados e seus logs
```

### Comandos Úteis para o Exame

```bash
# Criar CronJob
kubectl create cronjob my-cron --image=busybox --schedule="*/1 * * * *" -- echo "hello"

# Ver CronJobs e Jobs
kubectl get cj,jobs

# Executar Job manualmente do CronJob
kubectl create job manual --from=cronjob/<name>

# Suspender CronJob
kubectl patch cj <name> -p '{"spec":{"suspend":true}}'

# Ver logs do último Job
kubectl logs job/$(kubectl get jobs -l cronjob-name=<name> --sort-by=.status.startTime -o jsonpath='{.items[-1].metadata.name}')

# Deletar CronJob
kubectl delete cj <name>
```

### Template Rápido para CronJob

```yaml
{{#include ../assets/cronjob/cronjob-template.yaml}}
```

---

## Referências

- [Kubernetes - CronJob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/)
- [Kubernetes - Running Automated Tasks](https://kubernetes.io/docs/tasks/job/automated-tasks-with-cron-jobs/)
- [Crontab Guru](https://crontab.guru/) - Validador de expressões cron

### Arquivos Relacionados

- [Job](job.md) - Jobs únicos
- [Scheduling](scheduling.md) - Agendamento de Pods
- [ConfigMap](../configuration/configmap.md) - Configuração para CronJobs
- [Secrets](../configuration/secrets.md) - Dados sensíveis para CronJobs
