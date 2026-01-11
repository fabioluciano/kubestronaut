# Deployment

> **Certificacoes**: CKAD, CKA | **Peso no Exame**: ~15-20%

## Conceitos Fundamentais

O **Deployment** e o recurso mais utilizado para deploy de aplicacoes stateless no Kubernetes. Ele fornece atualizacoes declarativas para Pods e ReplicaSets, permitindo rollouts e rollbacks controlados.

### O que e e Para que Serve

O Deployment e responsavel por:

- **Gerenciar ReplicaSets**: Cria e gerencia ReplicaSets automaticamente
- **Atualizacoes declarativas**: Define o estado desejado e o Kubernetes reconcilia
- **Rolling updates**: Atualiza Pods gradualmente sem downtime
- **Rollbacks**: Reverte para versoes anteriores em caso de problemas
- **Scaling**: Escala aplicacoes horizontal e automaticamente (com HPA)
- **Historico de revisoes**: Mantem historico de alteracoes para auditoria

### Arquitetura do Deployment

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title Arquitetura do Deployment

package "Deployment Controller" {
    [Deployment] as DEP
    [ReplicaSet v1] as RS1
    [ReplicaSet v2] as RS2

    package "Pods v1 (antiga)" {
        [Pod 1a] as P1A
    }

    package "Pods v2 (nova)" {
        [Pod 2a] as P2A
        [Pod 2b] as P2B
        [Pod 2c] as P2C
    }
}

DEP --> RS1 : gerencia\n(scale down)
DEP --> RS2 : gerencia\n(scale up)
RS1 --> P1A : controla
RS2 --> P2A : controla
RS2 --> P2B : controla
RS2 --> P2C : controla

note right of DEP
    Deployment controla:
    - Estrategia de update
    - Numero de revisoes
    - Rollback
end note

note bottom of RS1
    ReplicaSet antigo:
    replicas: 1 (scaling down)
end note

note bottom of RS2
    ReplicaSet novo:
    replicas: 3 (scaling up)
end note

@enduml
```

## Estrutura Basica

### Campos Principais

```yaml
{{#include ../assets/deployment/deployment-campos-importantes.yaml}}
```

### Exemplo Basico de Deployment

```yaml
{{#include ../assets/deployment/nginx-deployment.yaml}}
```

```admonish info title="Regra de Ouro"
As labels em `spec.selector.matchLabels` **DEVEM** corresponder a `spec.template.metadata.labels`. Caso contrario, o Deployment nao conseguira gerenciar os Pods.
```

## Estrategias de Update

O Kubernetes suporta duas estrategias de atualizacao: **RollingUpdate** (padrao) e **Recreate**.

### Diagrama Comparativo

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title Comparacao: Recreate vs RollingUpdate

rectangle "Recreate Strategy" {
    rectangle "Estado Inicial" as R1 {
        [Pod v1] as RP1
        [Pod v1] as RP2
        [Pod v1] as RP3
    }

    rectangle "Durante Update" as R2 {
        note "Todos Pods\nterminados\n(DOWNTIME)" as RN
    }

    rectangle "Estado Final" as R3 {
        [Pod v2] as RP4
        [Pod v2] as RP5
        [Pod v2] as RP6
    }

    R1 --> R2 : Termina todos
    R2 --> R3 : Cria novos
}

rectangle "RollingUpdate Strategy" {
    rectangle "Fase 1" as RU1 {
        [Pod v1] as RUP1
        [Pod v1] as RUP2
        [Pod v2] as RUP3
    }

    rectangle "Fase 2" as RU2 {
        [Pod v1] as RUP4
        [Pod v2] as RUP5
        [Pod v2] as RUP6
    }

    rectangle "Fase 3" as RU3 {
        [Pod v2] as RUP7
        [Pod v2] as RUP8
        [Pod v2] as RUP9
    }

    RU1 --> RU2 : Gradual
    RU2 --> RU3 : Sem downtime
}

@enduml
```

### Estrategia Recreate

Todos os Pods existentes sao terminados **antes** de criar os novos. Causa **downtime**, mas e util quando:

- A aplicacao nao suporta multiplas versoes simultaneas
- Ha restricoes de recursos que impedem ter pods extras
- E necessario garantir que todos os pods estejam na mesma versao

```yaml
{{#include ../assets/deployment/recreate-deployment.yaml}}
```

### Estrategia RollingUpdate (Padrao)

Atualiza Pods gradualmente, mantendo a aplicacao disponivel durante o processo.

```yaml
{{#include ../assets/deployment/rolling-deployment.yaml}}
```

#### Parametros do RollingUpdate

| Parametro | Descricao | Valor Padrao |
|-----------|-----------|--------------|
| `maxSurge` | Maximo de Pods extras durante update | 25% |
| `maxUnavailable` | Maximo de Pods indisponiveis | 25% |

**Exemplo pratico com 4 replicas:**
- `maxSurge: 25%` = maximo de 1 Pod extra (5 total)
- `maxUnavailable: 25%` = maximo de 1 Pod indisponivel (minimo 3 disponiveis)

```admonish tip title="Dica para o Exame"
Para updates mais rapidos, aumente `maxSurge`. Para updates mais seguros (menos risco), diminua `maxUnavailable`.
```

## Rollout e Rollback

### Ciclo de Vida de um Rollout

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title Ciclo de Vida do Rollout

[*] --> Progressing : kubectl apply

state Progressing {
    [*] --> CreatingRS : Cria novo ReplicaSet
    CreatingRS --> ScalingUp : Scale up novos Pods
    ScalingUp --> ScalingDown : Scale down antigos
    ScalingDown --> [*] : Concluido
}

Progressing --> Complete : Sucesso
Progressing --> Failed : Timeout/Erro
Progressing --> Paused : kubectl rollout pause

Paused --> Progressing : kubectl rollout resume

Failed --> Progressing : kubectl rollout undo
Complete --> Progressing : Nova alteracao

Complete --> [*]

@enduml
```

### Comandos de Rollout

```bash
# Ver status do rollout
kubectl rollout status deployment/my-app

# Ver historico de revisoes
kubectl rollout history deployment/my-app

# Ver detalhes de uma revisao especifica
kubectl rollout history deployment/my-app --revision=2

# Fazer rollback para revisao anterior
kubectl rollout undo deployment/my-app

# Fazer rollback para revisao especifica
kubectl rollout undo deployment/my-app --to-revision=2

# Pausar rollout (util para fazer multiplas alteracoes)
kubectl rollout pause deployment/my-app

# Retomar rollout pausado
kubectl rollout resume deployment/my-app

# Reiniciar todos os Pods (trigger rolling restart)
kubectl rollout restart deployment/my-app
```

### Annotations para Historico

Para manter registro do motivo das alteracoes:

```bash
# Aplicar com annotation de causa
kubectl apply -f deployment.yaml
kubectl annotate deployment/my-app kubernetes.io/change-cause="Updated to v2.0"

# Ou usando set image com record (deprecated, mas ainda funciona)
kubectl set image deployment/my-app app=myapp:v2 --record
```

```admonish warning title="Atencao"
A flag `--record` esta deprecated. Use annotations manualmente com `kubernetes.io/change-cause`.
```

### Configurando Historico de Revisoes

```yaml
{{#include ../assets/workloads/deployment-example-1.yaml}}
```

## Scaling

### Scaling Manual

```bash
# Via kubectl scale
kubectl scale deployment/my-app --replicas=5

# Via kubectl edit
kubectl edit deployment/my-app

# Via kubectl patch
kubectl patch deployment/my-app -p '{"spec":{"replicas":5}}'

# Via arquivo YAML
kubectl apply -f deployment-updated.yaml
```

### Scaling Automatico (HPA)

O HorizontalPodAutoscaler pode escalar Deployments automaticamente baseado em metricas:

```yaml
{{#include ../assets/workloads/horizontalpodautoscaler-my-app-hpa.yaml}}
```

```bash
# Criar HPA via comando
kubectl autoscale deployment/my-app --min=2 --max=10 --cpu-percent=70

# Ver HPAs
kubectl get hpa
```

Para mais detalhes, consulte [HorizontalPodAutoscaler](./horizontal-pod-autoscaler.md).

## Pausing e Resuming

Util quando voce precisa fazer multiplas alteracoes e nao quer trigger de multiplos rollouts:

```bash
# 1. Pausar o Deployment
kubectl rollout pause deployment/my-app

# 2. Fazer varias alteracoes
kubectl set image deployment/my-app app=myapp:v2
kubectl set resources deployment/my-app -c app --limits=cpu=200m,memory=512Mi
kubectl set env deployment/my-app -c app ENV=production

# 3. Retomar - aplica todas as alteracoes em um unico rollout
kubectl rollout resume deployment/my-app
```

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title Fluxo de Pause/Resume

start

:Deployment rodando normalmente;

:kubectl rollout pause;
note right: Alteracoes nao\ntrigger rollout

partition "Multiplas Alteracoes" {
    :set image;
    :set resources;
    :set env;
}

:kubectl rollout resume;
note right: Um unico rollout\ncom todas alteracoes

:Rollout executado;

stop

@enduml
```

## Patterns de Deployment Avancados

### Blue/Green Deployment

O padrao Blue/Green mantem duas versoes completas da aplicacao. O switch e instantaneo, alterando para qual versao o Service aponta.

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title Blue/Green Deployment

rectangle "Blue (v1 - Atual)" as BLUE {
    [Pod v1] as BP1
    [Pod v1] as BP2
    [Pod v1] as BP3
}

rectangle "Green (v2 - Nova)" as GREEN {
    [Pod v2] as GP1
    [Pod v2] as GP2
    [Pod v2] as GP3
}

entity "Service" as SVC
actor Usuario

Usuario --> SVC
SVC --> BLUE : selector: version=blue

note bottom of GREEN
    Pronto para receber trafego.
    Basta mudar o selector do
    Service para version=green
end note

@enduml
```

#### Implementacao via Service

```yaml
{{#include ../assets/deployment/blue-green-deployment.yaml}}
```

#### Implementacao via Service (Exemplo Completo)

```yaml
{{#include ../assets/deployment/bluegreen-service-based.yaml}}
```

#### Switch Blue para Green

```bash
# Verificar versao atual
kubectl get svc myapp-service -o jsonpath='{.spec.selector.version}'

# Fazer switch para Green
kubectl patch svc myapp-service -p '{"spec":{"selector":{"version":"green"}}}'

# Ou editar diretamente
kubectl edit svc myapp-service
# Alterar selector.version de "blue" para "green"
```

#### Implementacao via Ingress

```yaml
{{#include ../assets/deployment/bluegreen-ingress-based.yaml}}
```

### Canary Deployment

O padrao Canary envia uma pequena porcentagem do trafego para a nova versao para validacao antes do rollout completo.

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace

title Canary Deployment

rectangle "Stable (v1)" as STABLE {
    [Pod v1] as SP1
    [Pod v1] as SP2
    [Pod v1] as SP3
    [Pod v1] as SP4
    [Pod v1] as SP5
    [Pod v1] as SP6
    [Pod v1] as SP7
    [Pod v1] as SP8
    [Pod v1] as SP9
}

rectangle "Canary (v2)" as CANARY {
    [Pod v2] as CP1
}

entity "Service" as SVC
actor Usuario

Usuario --> SVC
SVC --> STABLE : 90% trafego
SVC --> CANARY : 10% trafego

note bottom of CANARY
    Mesma label "app: myapp"
    Service balanceia entre
    todos os pods (9:1)
end note

@enduml
```

#### Implementacao via Service (Proporcao de Replicas)

```yaml
{{#include ../assets/deployment/canary-deployment.yaml}}
```

#### Implementacao via Service (Exemplo Completo)

```yaml
{{#include ../assets/deployment/canary-service-based.yaml}}
```

#### Implementacao via Ingress com Nginx

```yaml
{{#include ../assets/deployment/canary-ingress-based.yaml}}
```

```admonish info title="Canary com Ingress"
A implementacao via Ingress permite controle preciso da porcentagem de trafego usando annotations do Nginx Ingress Controller, independente do numero de replicas.
```

### Comparativo dos Patterns

| Caracteristica | Blue/Green | Canary |
|----------------|------------|--------|
| Rollback | Instantaneo | Gradual |
| Recursos | 2x (duas versoes completas) | 1x + pequena fracao |
| Risco | Tudo ou nada | Exposicao gradual |
| Validacao | Ambiente isolado | Producao real |
| Complexidade | Media | Alta |

## Comandos kubectl Essenciais

### Criacao e Gerenciamento

```bash
# Criar Deployment
kubectl create deployment nginx --image=nginx:1.25 --replicas=3

# Criar com dry-run (gerar YAML)
kubectl create deployment nginx --image=nginx --dry-run=client -o yaml > deploy.yaml

# Aplicar arquivo
kubectl apply -f deployment.yaml

# Criar com porta exposta
kubectl create deployment nginx --image=nginx --port=80
```

### Atualizacao

```bash
# Atualizar imagem
kubectl set image deployment/my-app app=myapp:v2

# Atualizar recursos
kubectl set resources deployment/my-app -c app \
  --requests=cpu=100m,memory=128Mi \
  --limits=cpu=200m,memory=256Mi

# Atualizar variaveis de ambiente
kubectl set env deployment/my-app ENV=production DEBUG=false

# Atualizar service account
kubectl set serviceaccount deployment/my-app my-sa
```

### Consulta e Monitoramento

```bash
# Listar Deployments
kubectl get deployments
kubectl get deploy  # forma curta

# Detalhes completos
kubectl describe deployment/my-app

# Ver Pods do Deployment
kubectl get pods -l app=my-app

# Ver ReplicaSets do Deployment
kubectl get rs -l app=my-app

# Ver eventos
kubectl get events --field-selector involvedObject.name=my-app

# Acompanhar rollout em tempo real
kubectl rollout status deployment/my-app -w
```

### Rollout e Rollback

```bash
# Ver historico
kubectl rollout history deployment/my-app

# Ver revisao especifica
kubectl rollout history deployment/my-app --revision=3

# Rollback para anterior
kubectl rollout undo deployment/my-app

# Rollback para revisao especifica
kubectl rollout undo deployment/my-app --to-revision=2

# Pausar/Retomar
kubectl rollout pause deployment/my-app
kubectl rollout resume deployment/my-app

# Reiniciar todos os Pods
kubectl rollout restart deployment/my-app
```

### Scaling

```bash
# Escalar manualmente
kubectl scale deployment/my-app --replicas=5

# Autoscaling
kubectl autoscale deployment/my-app --min=2 --max=10 --cpu-percent=80
```

### Delecao

```bash
# Deletar Deployment (e todos Pods/ReplicaSets)
kubectl delete deployment/my-app

# Deletar mantendo Pods (orphan)
kubectl delete deployment/my-app --cascade=orphan
```

## Troubleshooting

### Deployment nao progride

```bash
# Verificar status do rollout
kubectl rollout status deployment/my-app

# Ver eventos do Deployment
kubectl describe deployment/my-app | grep -A 20 Events

# Verificar progressDeadlineSeconds
kubectl get deployment/my-app -o jsonpath='{.spec.progressDeadlineSeconds}'
```

### Pods nao iniciam

```bash
# Ver status dos Pods
kubectl get pods -l app=my-app

# Descrever Pod com problema
kubectl describe pod <pod-name>

# Ver logs do container
kubectl logs <pod-name> -c <container-name>

# Ver logs do container anterior (se crashou)
kubectl logs <pod-name> -c <container-name> --previous
```

### Rollout travado

```bash
# Verificar condicoes do Deployment
kubectl get deployment/my-app -o jsonpath='{.status.conditions[*].message}'

# Verificar se esta pausado
kubectl get deployment/my-app -o jsonpath='{.spec.paused}'

# Se pausado, retomar
kubectl rollout resume deployment/my-app

# Se travado por muito tempo, verificar recursos
kubectl describe nodes | grep -A 10 "Allocated resources"
```

### ReplicaSet antigo nao scala down

```bash
# Verificar se ha Pods em estados problematicos
kubectl get pods -l app=my-app -o wide

# Verificar PodDisruptionBudget
kubectl get pdb

# Forcar delecao de Pods stuck
kubectl delete pod <pod-name> --force --grace-period=0
```

### Imagem nao atualiza

```bash
# Verificar se a imagem foi realmente alterada
kubectl get deployment/my-app -o jsonpath='{.spec.template.spec.containers[0].image}'

# Se usar tag :latest, forcar pull
kubectl rollout restart deployment/my-app

# Ou usar imagePullPolicy: Always no spec
```

## Dicas para o Exame

```admonish tip title="Dicas CKAD/CKA"
1. **Comando de criacao rapida**:
   ```bash
   kubectl create deployment nginx --image=nginx --replicas=3 --dry-run=client -o yaml > deploy.yaml
   ```

2. **Memorize os comandos de rollout**:
   - `kubectl rollout status` - ver status
   - `kubectl rollout history` - ver historico
   - `kubectl rollout undo` - rollback
   - `kubectl rollout restart` - reiniciar pods

3. **Atualizacao rapida de imagem**:
   ```bash
   kubectl set image deployment/name container=image:tag
   ```

4. **Scaling rapido**:
   ```bash
   kubectl scale deployment/name --replicas=5
   ```

5. **Para Blue/Green no exame**:
   - Crie dois Deployments com labels diferentes
   - Use `kubectl patch svc` para switch

6. **Para Canary no exame**:
   - Use mesma label base em ambos Deployments
   - Controle proporcao pelo numero de replicas

7. **Verificar rapidamente replicas**:
   ```bash
   kubectl get deploy
   # READY mostra replicas disponiveis
   ```

8. **Debug rapido**:
   ```bash
   kubectl describe deploy/name | tail -20
   ```
```

## Best Practices

1. **Use sempre resource requests e limits** para evitar problemas de scheduling e garantir QoS

2. **Configure probes** (readiness e liveness) para garantir zero-downtime durante updates

3. **Defina `revisionHistoryLimit`** apropriado para balancear auditoria vs uso de recursos

4. **Use labels consistentes** e descritivas para facilitar selecao e organizacao

5. **Mantenha registro das alteracoes** usando annotation `kubernetes.io/change-cause`

6. **Configure `progressDeadlineSeconds`** adequadamente para detectar rollouts travados

7. **Use `minReadySeconds`** para garantir que Pods estejam estaveis antes de prosseguir

8. **Para producao, prefira RollingUpdate** com `maxUnavailable: 0` para zero-downtime

9. **Teste rollbacks** regularmente para garantir que o processo funciona

10. **Monitore metricas durante rollouts** para detectar problemas rapidamente

## Referencias

- [Documentacao Oficial - Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Documentacao Oficial - Rolling Update](https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/)
- [Documentacao Oficial - Blue/Green e Canary](https://kubernetes.io/blog/2018/04/30/zero-downtime-deployment-kubernetes-jenkins/)
- [Estrategias de Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#strategy)


---

### Recreate Strategy

```yaml
{{#include ../assets/deployment/deployment-strategy-recreate.yaml}}
```


---

### RollingUpdate Strategy

```yaml
{{#include ../assets/deployment/deployment-strategy-rollingupdate.yaml}}
```
